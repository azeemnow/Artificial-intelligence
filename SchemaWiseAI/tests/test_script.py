# tests/test_script.py

import sys
import os
# Add the parent directory to the Python path so that 'schemawiseAI' can be found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemawiseAI.core.registry import SchemaRegistry
from schemawiseAI.core.processor import MiddlewareProcessor

def run_test_cases():
    # Initialize components
    registry = SchemaRegistry()
    registry._extract_rules({
        "proxy_logs": {
            "fields": {
                "srcip": {"map_to": "src", "type": "string"},
                "dstip": {"map_to": "dst", "type": "string"},
                "bytes": {"map_to": "bytes_total", "type": "string"},
                "status": {"map_to": "http_status", "type": "string"},
                "dhost": {"map_to": "dest_host", "type": "string"},
                "src_port": {"map_to": "source_port", "type": "string"},
                "proto": {"map_to": "protocol", "type": "string"},
                "mtd": {"map_to": "method", "type": "string"},
                "urlp": {"map_to": "url_port", "type": "string"},
                "url": {"map_to": "uri", "type": "string"}
            }
        }
    })

    processor = MiddlewareProcessor(registry)

    # Test cases covering different Splunk commands and scenarios
    test_queries = [
        # Basic statistics
        'sourcetype="proxy" srcip="10.181.0.0" | stats sum(bytes) by dhost',
        # Complex filtering
        'sourcetype="proxy" | where status="407*" | table srcip, dstip, proto, mtd',
        # Port analysis
        'sourcetype="proxy" src_port>1024 | stats count by dhost',
        # Multiple aggregations
        'sourcetype="proxy" | stats count, sum(bytes) by srcip, dhost',
        # URL analysis
        'sourcetype="proxy" | where url="*.exe" | stats count by srcip, url',
        # Protocol distribution
        'sourcetype="proxy" | stats count by proto | sort -count',
        # Error analysis
        'sourcetype="proxy" status>=400 | stats count by status, dhost'
    ]

    print("\nRunning test cases...")
    print("=" * 50)
    for query in test_queries:
        print("\nOriginal:", query)
        modified = processor.process_query(query)
        print("Modified:", modified)
        print("-" * 50)

if __name__ == "__main__":
    run_test_cases()