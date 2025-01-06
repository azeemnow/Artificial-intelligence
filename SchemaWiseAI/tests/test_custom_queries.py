# tests/test_custom_queries.py
from schemawiseAI.integrations.ollama_handler import QueryGenerator
from schemawiseAI.core.registry import SchemaRegistry

def test_custom_queries():
    registry = SchemaRegistry()
    registry._extract_rules({
        "proxy_logs": {
            "fields": {
                "srcip": {"map_to": "src"},
                "dstip": {"map_to": "dst"},
                "bytes": {"map_to": "bytes_total"}
            }
        }
    })

    generator = QueryGenerator(registry)

    # Queries that won't match templates
    custom_cases = [
        "Show me traffic patterns during weekends",
        "Find requests where response time is more than 5 seconds",
        "Identify unusual user-agent strings",
        "Show me connections with encrypted traffic",
        "Find requests with SQL injection attempts"
    ]

    print("\nTesting Non-Template Queries")
    print("=" * 50)
    
    for request in custom_cases:
        print(f"\nUser Request: {request}")
        result = generator.process_request(request)
        print(f"Final Query: {result}")
        print("-" * 50)

if __name__ == "__main__":
    test_custom_queries()