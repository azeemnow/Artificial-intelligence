# tests/test_integration.py

import sys
import os
# Add the parent directory to the Python path so that 'schemawiseAI' can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from schemawiseAI.integrations.ollama_handler import QueryGenerator
from schemawiseAI.core.registry import SchemaRegistry

def test_ollama_integration():
    # Initialize registry with field mappings
    registry = SchemaRegistry()
    registry._extract_rules({
        "proxy_logs": {
            "fields": {
                "srcip": {"map_to": "src", "type": "string"},
                "dstip": {"map_to": "dst", "type": "string"},
                "bytes": {"map_to": "bytes_total", "type": "string"},
                "status": {"map_to": "http_status", "type": "string"},
                "dhost": {"map_to": "dest_host", "type": "string"},
                "proto": {"map_to": "protocol", "type": "string"},
                "mtd": {"map_to": "method", "type": "string"},
                "url": {"map_to": "uri", "type": "string"}
            }
        }
    })

    generator = QueryGenerator(registry, ollama_model="llama3.2:1b")

    test_cases = [
        # Bandwidth and Traffic Analysis
        "Show me top 5 source IPs by bandwidth usage per day",
        "Show me the protocols with highest bandwidth consumption rate",
        "Count requests and bandwidth by protocol",
        
        # Status Code and Error Analysis
        "List all HTTP GET requests with status 404 from the last hour",
        "Show me all failed requests with status >= 400",
        "Show me POST requests with status code 500",
        "What domains have the most failed requests?",
        "Find domains with most 404 errors in the last day",
        
        # Domain Analysis - General
        "Find the most accessed domains in the last week",
        
        # EXE File Analysis
        "Show me source IPs downloading exe files",
        
        # Specific Domain Traffic
        "Find outbound traffic to google.com",
        "Show me errors from microsoft.com",
        "What request methods are used for facebook.com",
        "How many unique users access amazon.com",
        "Show traffic patterns for github.com",
        
        # Domain Pattern Analysis
        "List all domains ending with .edu",
        "Show domains ending with .gov",
        "Show traffic to *.google.com",
        "Find errors from any microsoft.com subdomain",
        "Show me access patterns for github.com and its subdomains",
        "Count unique users accessing *.amazon.com",
        
        # Time-Based Domain Analysis
        "Show .edu traffic in the last hour",
        "Find failed requests to microsoft.com today",
        
        # Method-Specific Domain Analysis
        "What HTTP methods are used on *.github.com",
        "Show POST requests to api.example.com"
    ]

    print("\nTesting Final Template Generation")
    print("=" * 60)
    
    for request in test_cases:
        print(f"\nUser Request: {request}")
        result = generator.process_request(request)
        print(f"Final Query: {result}")
        print("-" * 60)

if __name__ == "__main__":
    test_ollama_integration()