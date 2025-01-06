# tests/test_integration.py
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
        "Show me top 5 source IPs by bandwidth usage per day",
        "List all HTTP GET requests with status 404 from the last hour",
        "Find the most accessed domains in the last week",
        "Show me all failed requests with status >= 400",
        "Count requests and bandwidth by protocol",
        "Show me POST requests with status code 500",
        "What domains have the most failed requests?",
        "Show me source IPs downloading exe files",
        "Show me the protocols with highest bandwidth consumption rate",
        "Find domains with most 404 errors in the last day"
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