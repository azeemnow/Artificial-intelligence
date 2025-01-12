# schemawiseAI/integrations/ollama_handler.py
import requests
import json
from ..core.registry import SchemaRegistry
from ..core.processor import MiddlewareProcessor

class OllamaHandler:
    def __init__(self, model="llama3.2:1b", base_url="http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        
    def get_template_for_request(self, request: str) -> str:
        templates = {
            "bandwidth": 'sourcetype="proxy" | stats sum(bytes) as total_bytes, count as request_count by srcip | eval bytes_per_sec=total_bytes/86400 | sort -total_bytes | head {limit}',
            
            "method_status": 'sourcetype="proxy" | where mtd="{method}" AND status{operator}{code} | stats count as request_count by url, srcip | sort -request_count',
            
            "domains_time": 'sourcetype="proxy" {timerange}| stats count as request_count by dhost | sort -request_count | head 10',
            
            "failed_requests": 'sourcetype="proxy" | where status>=400 | stats count as error_count by status, dhost | sort -error_count',
            
            "protocol_bandwidth": 'sourcetype="proxy" | stats count as request_count, sum(bytes) as total_bytes by proto | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes',
            
            "exe_files": 'sourcetype="proxy" | where url LIKE "%.exe" OR url ENDS WITH ".exe" | stats count as download_count by srcip, url | sort -download_count',
            
            "failed_domains": 'sourcetype="proxy" | where status>=400 | stats count as error_count by dhost | sort -error_count | head 10',
            
            "status_domains_time": 'sourcetype="proxy" {timerange}| where status{operator}{code} | stats count as error_count by dhost | sort -error_count | head 10',
            
            "domain_suffix": 'sourcetype="proxy" | where dhost LIKE "*.{suffix}" | stats count as request_count, sum(bytes) as total_bytes by dhost | sort -request_count | head 100',
            
            "domain_traffic": 'sourcetype="proxy" | where dhost LIKE "*.{domain}" OR dhost="{domain}" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes',
            
            "domain_errors": 'sourcetype="proxy" | where (dhost LIKE "*.{domain}" OR dhost="{domain}") AND status>=400 | stats count as error_count by status, dhost | sort -error_count',
            
            "domain_methods": 'sourcetype="proxy" | where dhost LIKE "*.{domain}" OR dhost="{domain}" | stats count as request_count by mtd, dhost | sort -request_count',
            
            "domain_users": 'sourcetype="proxy" | where dhost LIKE "*.{domain}" OR dhost="{domain}" | stats dc(srcip) as unique_users, count as request_count by dhost | sort -request_count'
        }

        def get_timerange(request):
            if "hour" in request.lower():
                return 'earliest=-1h latest=now '
            elif "day" in request.lower():
                return 'earliest=-24h@h latest=@h '
            elif "week" in request.lower():
                return 'earliest=-7d@d latest=@d '
            return ''

        def extract_domain_info(request: str) -> tuple:
            """Extract domain and determine if it's a suffix search."""
            domain_extensions = ['.com', '.org', '.net', '.edu', '.gov']
            words = request.lower().split()

            # Check for suffix-specific search
            if "ending with" in request.lower() or "ends with" in request.lower():
                for ext in domain_extensions:
                    if ext in request.lower():
                        return None, ext.lstrip('.')

            # Regular domain search
            for word in words:
                if any(ext in word for ext in domain_extensions):
                    return word.strip('*.'), None
                    
            return None, None

        # Extract domain info
        domain, suffix = extract_domain_info(request)
        
        # Handle suffix searches
        if suffix:
            return templates["domain_suffix"].format(suffix=suffix)
            
        # Handle specific domain searches
        if domain:
            if "traffic" in request.lower():
                return templates["domain_traffic"].format(domain=domain)
            elif "error" in request.lower():
                return templates["domain_errors"].format(domain=domain)
            elif "method" in request.lower() or "request type" in request.lower():
                return templates["domain_methods"].format(domain=domain)
            elif "user" in request.lower():
                return templates["domain_users"].format(domain=domain)
            else:
                return templates["domain_traffic"].format(domain=domain)

        # Standard template matching
        if "exe" in request.lower():
            return templates["exe_files"]
            
        if "protocol" in request.lower() and ("bandwidth" in request.lower() or "bytes" in request.lower()):
            return templates["protocol_bandwidth"]
            
        if "domain" in request.lower() and "404" in request:
            timerange = get_timerange(request)
            return templates["status_domains_time"].format(
                timerange=timerange,
                operator="=",
                code="404"
            )
            
        if "POST" in request.upper() and "500" in request:
            return templates["method_status"].format(
                method="POST",
                operator="=",
                code="500"
            )
            
        if "failed" in request.lower() and "domain" in request.lower():
            return templates["failed_domains"]
            
        if "bandwidth" in request.lower() or "bytes" in request.lower():
            limit = "5" if "5" in request else "10"
            return templates["bandwidth"].format(limit=limit)
            
        elif any(method in request.upper() for method in ["GET", "POST"]):
            method = "POST" if "POST" in request.upper() else "GET"
            operator = "=" if any(code in request for code in ["404", "500"]) else ">="
            code = next((c for c in ["404", "500"] if c in request), "400")
            return templates["method_status"].format(
                method=method,
                operator=operator,
                code=code
            )
            
        elif "domain" in request.lower():
            timerange = get_timerange(request)
            return templates["domains_time"].format(timerange=timerange)
            
        elif "status" in request.lower() or "failed" in request.lower():
            return templates["failed_requests"]
            
        return ""

    def generate_query(self, prompt: str) -> str:
        template_query = self.get_template_for_request(prompt)
        if template_query:
            print(f"Using template query: {template_query}")
            return template_query

        formatted_prompt = """
        Generate a Splunk query for proxy logs using these fields:
        srcip: Source IP
        dstip: Destination IP
        bytes: Bytes transferred
        status: HTTP status code
        dhost: Destination hostname
        proto: Protocol
        mtd: HTTP method
        url: URL

        Important syntax rules:
        1. Always start with sourcetype="proxy"
        2. Use "| where" for filtering conditions
        3. Use meaningful names for calculated fields (e.g., as total_bytes)
        4. Join multiple conditions with AND
        5. Put time ranges before where clauses

        Request: {prompt}
        Only return the query, no explanations or backticks.""".format(prompt=prompt)

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": formatted_prompt,
                    "system": "You are a Splunk query generator. Return only the exact query.",
                    "stream": False
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                query = data.get('response', '').strip()
                query = query.replace('`', '').strip()
                query = query.split('\n')[0].strip()
                
                if not query.startswith('sourcetype="proxy"'):
                    query = 'sourcetype="proxy" ' + query
                
                return query
                
        except Exception as e:
            print(f"Error: {str(e)}")
            return ""

class QueryGenerator:
    def __init__(self, schema_registry: SchemaRegistry, ollama_model="llama3.2:1b"):
        self.ollama = OllamaHandler(model=ollama_model)
        self.processor = MiddlewareProcessor(schema_registry)
    
    def process_request(self, user_request: str) -> str:
        print(f"\nProcessing request: {user_request}")
        raw_query = self.ollama.generate_query(user_request)
        if not raw_query:
            return "Failed to generate query"
        processed_query = self.processor.process_query(raw_query)
        print(f"Processed query: {processed_query}")
        return processed_query