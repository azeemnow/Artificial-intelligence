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


### Installation
```bash
git clone https://github.com/azeemnow/Artificial-intelligence.git
cd SchemaWiseAI
pip install -e .
```

#### Python Package Error
If you encounter the following error while trying to install the required Python packages:
```error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
```

This error typically occurs because your system's Python environment is being managed by the operating system, preventing you from installing packages globally. To resolve this, we recommend using a virtual environment to install Python packages locally without affecting your system setup. Follow the steps below for virtual environment.

### Steps to Create, Activate, and Deactivate a Virtual Environment
1. Install Python Virtual Environment Support (if needed)
If you don't have python3-venv installed, you can install it by running:

```sudo apt install python3-venv ```

2. Create a Virtual Environment

```python3 -m venv venv```

This will create a new directory named venv in your project folder, containing the virtual environment.

3. Activate the Virtual Environment

To activate the virtual environment, use the following command:
For Linux/macOS:

```source venv/bin/activate```

After activating the virtual environment, your prompt should change to indicate the environment is active. It will look something like this:

```(venv) user@ubuntu24:~/Documents/YourProject$```

4. Install the Required Python Packages

With the virtual environment activated, you can now run the installation command:

```pip install -e .```

This will install the Python packages locally within the virtual environment, avoiding the "externally-managed-environment" error.

5. Deactivate the Virtual Environment

Once you're done with the virtual environment, you can deactivate it by running:

```deactivate```

Your terminal prompt should return to normal, and you will be back to the system's Python environment.


### Reactivate an Existing Virtual Environment

You do not need to recreate the virtual environment every time you want to use it. Once you’ve created the virtual environment, you can simply reactivate it when needed. The virtual environment persists in its directory, and you can return to it anytime.


Here's how to reactivate an existing virtual environment:

1. Navigate to your project directory (where the venv folder is located).

```cd path/to/your/project```


2. Activate the previously created virtual environment:

For Linux/macOS:

```source venv/bin/activate```

After activating, you should see (venv) at the beginning of your terminal prompt, indicating the virtual environment is active.

3. Install additional packages (if needed) or continue working with your project.

4.Deactivate the virtual environment when you're done.


### Why Use Ollama for SchemaWiseAI?

Ollama (https://ollama.com/) is the perfect platform for building SchemaWiseAI, a middleware tool that adapts LLM-generated queries to match custom data schemas. Here's why:

- **Privacy First**: Run models locally, ensuring sensitive data schemas stay secure.
- **Customizable Models**: Easily tailor AI to your organization’s unique database structures.
- **Full Control**: Adjust and fine-tune the LLM for precise, accurate query adaptations.
- **Fast and Efficient**: Avoid latency issues with local processing for real-time performance.
- **Cost-Effective**: Save on cloud processing costs by keeping everything in-house.

Ollama simplifies building a tool like SchemaWiseAI, making it easy to align AI outputs with your specific data needs.


### Install Ollama

I have a quick blog detailing the steps for installing and configuring Ollama. You can check it out here: [How to Install and Configure Ollama on Kali Linux](https://azeemnow.com/2024/11/02/how-to-install-and-configure-ollama-on-kali-linux/)

### Running Ollama

First, verify that Ollama is running by using the following command:
```bash
ollama list
```


If it's not running, start Ollama with:
```
ollama serve
```


Make sure you have a model pulled. You can do so with:
```
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
### Current Test Results

#### Process Flow

1. **User Request**  
   The natural language question from the user about what they want to know from their proxy logs.

2. **Processing Request**  
   SchemaWiseAI acknowledges receipt and begins processing the input.

3. **Using Template Query**  
   The initial query generated using predefined templates, using standard field names (e.g., `status`, `dhost`).

4. **Processed Query**  
   The query after field name mapping is applied (e.g., `status → http_status`, `dhost → dest_host`).

5. **Final Query**  
   The completed query ready for execution in Splunk, with all field names matching the organization's schema.

---

#### Purpose of Using Templates

The template system serves two main purposes:

- **Predictable Output**  
  For common queries, templates ensure consistent, well-formed Splunk syntax.

- **Reduced LLM Dependency**  
  Templates are faster and more reliable than LLM-generated queries.

#### When a Request Doesn’t Match Any Template

SchemaWiseAI follows a fallback process to handle unmatched user requests.

---
### Example Transformation  
SchemaWiseAI transformed a natural language request into a Splunk query while mapping generic field names to organization-specific ones (e.g., `status → http_status`).


```plaintext
============================================================
User Request: Show me top 5 source IPs by bandwidth usage per day

Processing request: Show me top 5 source IPs by bandwidth usage per day
Using template query: sourcetype="proxy" | stats sum(bytes) as total_bytes, count as request_count by srcip | eval bytes_per_sec=total_bytes/86400 | sort -total_bytes | head 5
Processed query: sourcetype="proxy" | stats sum(bytes_total) as total_bytes, count as request_count by src | eval bytes_per_sec=total_bytes/86400 | sort -total_bytes | head 5
Final Query: sourcetype="proxy" | stats sum(bytes_total) as total_bytes, count as request_count by src | eval bytes_per_sec=total_bytes/86400 | sort -total_bytes | head 5
------------------------------------------------------------

User Request: List all HTTP GET requests with status 404 from the last hour

Processing request: List all HTTP GET requests with status 404 from the last hour
Using template query: sourcetype="proxy" | where mtd="GET" AND status=404 | stats count as request_count by url, srcip | sort -request_count
Processed query: sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count
Final Query: sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count
------------------------------------------------------------

User Request: Find the most accessed domains in the last week

Processing request: Find the most accessed domains in the last week
Using template query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dhost | sort -request_count | head 10
Processed query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dest_host | sort -request_count | head 10
Final Query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dest_host | sort -request_count | head 10
------------------------------------------------------------

User Request: Show me all failed requests with status >= 400

Processing request: Show me all failed requests with status >= 400
Using template query: sourcetype="proxy" | where status>=400 | stats count as error_count by status, dhost | sort -error_count
Processed query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
Final Query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
------------------------------------------------------------

User Request: Count requests and bandwidth by protocol

Processing request: Count requests and bandwidth by protocol
Using template query: sourcetype="proxy" | stats count as request_count, sum(bytes) as total_bytes by proto | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
Processed query: sourcetype="proxy" | stats count as request_count, sum(bytes_total) as total_bytes by protocol | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
Final Query: sourcetype="proxy" | stats count as request_count, sum(bytes_total) as total_bytes by protocol | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
------------------------------------------------------------

User Request: Show me POST requests with status code 500

Processing request: Show me POST requests with status code 500
Using template query: sourcetype="proxy" | where mtd="POST" AND status=500 | stats count as request_count by url, srcip | sort -request_count
Processed query: sourcetype="proxy" | where method="POST" AND http_status=500 | stats count as request_count by uri, src | sort -request_count
Final Query: sourcetype="proxy" | where method="POST" AND http_status=500 | stats count as request_count by uri, src | sort -request_count
------------------------------------------------------------

User Request: What domains have the most failed requests?

Processing request: What domains have the most failed requests?
Using template query: sourcetype="proxy" | where status>=400 | stats count as error_count by dhost | sort -error_count | head 10
Processed query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by dest_host | sort -error_count | head 10
Final Query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by dest_host | sort -error_count | head 10
------------------------------------------------------------

User Request: Show me source IPs downloading exe files

Processing request: Show me source IPs downloading exe files
Using template query: sourcetype="proxy" | where url LIKE "%.exe" OR url ENDS WITH ".exe" | stats count as download_count by srcip, url | sort -download_count
Processed query: sourcetype="proxy" | where uri LIKE "%.exe" OR uri ENDS WITH ".exe" | stats count as download_count by src, uri | sort -download_count
Final Query: sourcetype="proxy" | where uri LIKE "%.exe" OR uri ENDS WITH ".exe" | stats count as download_count by src, uri | sort -download_count
------------------------------------------------------------

User Request: Show me the protocols with highest bandwidth consumption rate

Processing request: Show me the protocols with highest bandwidth consumption rate
Using template query: sourcetype="proxy" | stats count as request_count, sum(bytes) as total_bytes by proto | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
Processed query: sourcetype="proxy" | stats count as request_count, sum(bytes_total) as total_bytes by protocol | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
Final Query: sourcetype="proxy" | stats count as request_count, sum(bytes_total) as total_bytes by protocol | eval MB_per_sec=round(total_bytes/1024/1024/86400,2) | sort -total_bytes
------------------------------------------------------------

User Request: Find domains with most 404 errors in the last day

Processing request: Find domains with most 404 errors in the last day
Using template query: sourcetype="proxy" earliest=-24h@h latest=@h | where status=404 | stats count as error_count by dhost | sort -error_count | head 10
Processed query: sourcetype="proxy" earliest=-24h@h latest=@h | where http_status=404 | stats count as error_count by dest_host | sort -error_count | head 10
Final Query: sourcetype="proxy" earliest=-24h@h latest=@h | where http_status=404 | stats count as error_count by dest_host | sort -error_count | head 10
------------------------------------------------------------
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

### Disclosure
Please note that some of the code were generated with the help of AI and Large Language Models (LLMs).The generated code has been carefully reviewed and adapted to ensure accuracy and relevance.
