# SchemaWiseAI

SchemaWiseAI is a middleware solution that adapts LLM-generated queries to match your specific data schema. It bridges the gap between generic LLM outputs and organization-specific data structures.

When cybersecurity analysts, data engineers, or other professionals use Large Language Models (LLMs) to generate database queries or scripts, these outputs often don’t match the specific data schemas in their systems. This mismatch requires manual updates to align with field names, table structures, and data types, wasting time and effort.

SchemaWiseAI solves this by ingesting the user’s custom data schemas and automatically modifying LLM-generated queries to fit the exact structure of their environment. This ensures that the outputs are accurate, usable, and aligned with their system, saving time and reducing errors.

## Problem Solved
- LLMs generate generic field names and data structures
- Analysts waste time manually adapting queries
- Schema mismatches cause query errors
- Inconsistent naming conventions

## Features
- Field name mapping
- Query transformation
- Template-based query generation
- Time-range handling
- Rate calculations
- Splunk query optimization

## Project Structure
```
schemawiseAI/
├── core/
│   ├── registry.py       # Schema mapping registry
│   ├── processor.py      # Query transformation engine
├── integrations/
│   ├── ollama_handler.py # Ollama LLM integration
└── tests/
    ├── test_script.py    # Basic tests
    ├── test_integration.py # Integration tests
```

## Getting Started

### Prerequisites
- Python 3.8+
- Ollama
- PyYAML

### Why Use Ollama for SchemaWiseAI?

Ollama (https://ollama.com/) is the perfect platform for building SchemaWiseAI, a middleware tool that adapts LLM-generated queries to match custom data schemas. Here's why:

- **Privacy First**: Run models locally, ensuring sensitive data schemas stay secure.
- **Customizable Models**: Easily tailor AI to your organization’s unique database structures.
- **Full Control**: Adjust and fine-tune the LLM for precise, accurate query adaptations.
- **Fast and Efficient**: Avoid latency issues with local processing for real-time performance.
- **Cost-Effective**: Save on cloud processing costs by keeping everything in-house.

Ollama simplifies building a tool like SchemaWiseAI, making it easy to align AI outputs with your specific data needs.

### Installation
```bash
git clone https://github.com/yourusername/SchemaWiseAI.git
cd SchemaWiseAI
pip install -e .
```

### Running Ollama
```bash
ollama serve
ollama pull llama3.2:1b
```

### Usage Example
```python
from schemawiseAI.integrations.ollama_handler import QueryGenerator
from schemawiseAI.core.registry import SchemaRegistry

# Initialize registry with your schema
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

# Create generator
generator = QueryGenerator(registry)

# Generate and transform query
request = "Show me top 5 source IPs by bandwidth usage"
result = generator.process_request(request)
print(result)
```

### Example Output
```sql
sourcetype="proxy" | stats sum(bytes_total) as total_bytes by src | sort -total_bytes | head 5
```

## Current Limitations
- Supports Splunk queries only
- Limited to proxy log schema
- Requires Ollama setup

## Future Roadmap
- Integration for other LLMs (OpenAI, etc).
- Include additional schemas (splunk: palo alto, dns, windows, etc. MDRs)
- UX/UI

  
## Contributing
Pull requests welcome. For major changes, open an issue first.
