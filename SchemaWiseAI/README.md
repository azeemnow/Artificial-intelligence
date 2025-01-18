
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
cd Artificial-intelligence #ignore the "AI-Policy-Development-Guide" directory
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

This error typically occurs because your system's Python environment is being managed by the operating system, preventing you from installing packages globally. To resolve this, we recommend using a virtual environment to install Python packages locally without affecting your system setup. 

Refer to the **Troubleshoot** section at the end for instructions on setting up a virtual environment.

## Why Use Ollama for SchemaWiseAI?

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

# Usage 
## Schema Mapping
The project currently includes a basic proxy schema structure. You can find detailed information about the schema and field mappings in the `test_integration.py` file (located inside the `tests` directory .

```python
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
```
The `test_integration.py` file also contains a list of test cases used for training and evaluating the proof of concept. You can add to this list and test to see how the program performs.
```python
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
```
## Run Program
```python
python tests/test_integration.py
```
### Successful Output

If the program runs successfully, the output should resemble the following:
```plaintext
User Request: List all HTTP GET requests with status 404 from the last hour

Processing request: List all HTTP GET requests with status 404 from the last hour
Using template query: sourcetype="proxy" | where mtd="GET" AND status=404 | stats count as request_count by url, srcip | sort -request_count
Processed query: sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count
Final Query: sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count
```
###  Output Explanation 

| **Step**               | **Description**                                                                                       | **Query**                                                                                                          | **Changes Made**                                                                                       |
|-------------------------|-------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **User Request**        | The natural language question from the user about what they want to know from their proxy logs.       | *(Not applicable)*                                                                                                | No query yet, just a plain user request in natural language.                                           |
| **Processing Request**  | SchemaWiseAI acknowledges receipt and begins processing the input.                                   | *(Not applicable)*                                                                                                | No query yet; SchemaWiseAI is processing the input.                                                    |
| **Using Template Query**| The initial query generated using predefined templates, using standard field names. | `sourcetype="proxy" | where mtd="GET" AND status=404 | stats count as request_count by url, srcip | sort -request_count` | Used placeholder field names: `mtd`, `status`, `url`, and `srcip`.                                    |
| **Processed Query**     | The query after field name mapping is applied.    | `sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count` | Changed field names: `mtd` → `method`, `status` → `http_status`, `url` → `uri`, `srcip` → `src`.      |
| **Final Query**         | The completed query ready for execution in Splunk, with all field names matching the organization's schema. | `sourcetype="proxy" | where method="GET" AND http_status=404 | stats count as request_count by uri, src | sort -request_count` | No further changes made; same as the processed query.                                                 |

#### Summery

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

### Use of Templates

The template system serves two main purposes:

- **Predictable Output**  
  For common queries, templates ensure consistent, well-formed Splunk syntax.

- **Reduced LLM Dependency**  
  Templates are faster and more reliable than LLM-generated queries.

#### When a Request Doesn’t Match Any Template
SchemaWiseAI follows a fallback process to handle unmatched user requests.

---
## Evaluation
Below is an example of transformations successfully performed by SchemaWiseAI, where a natural language user request for a specific Splunk query was generated by the LLM, while simultaneously mapping generic field names to organization-specific ones (e.g., `status → http_status`).


```plaintext
============================================================
User Request: Show me all failed requests with status >= 400

Processing request: Show me all failed requests with status >= 400
Using template query: sourcetype="proxy" | where status>=400 | stats count as error_count by status, dhost | sort -error_count
Processed query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
Final Query: sourcetype="proxy" | where http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
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

User Request: Find domains with most 404 errors in the last day

Processing request: Find domains with most 404 errors in the last day
Using template query: sourcetype="proxy" earliest=-24h@h latest=@h | where status=404 | stats count as error_count by dhost | sort -error_count | head 10
Processed query: sourcetype="proxy" earliest=-24h@h latest=@h | where http_status=404 | stats count as error_count by dest_host | sort -error_count | head 10
Final Query: sourcetype="proxy" earliest=-24h@h latest=@h | where http_status=404 | stats count as error_count by dest_host | sort -error_count | head 10
------------------------------------------------------------

User Request: Find the most accessed domains in the last week

Processing request: Find the most accessed domains in the last week
Using template query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dhost | sort -request_count | head 10
Processed query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dest_host | sort -request_count | head 10
Final Query: sourcetype="proxy" earliest=-7d@d latest=@d | stats count as request_count by dest_host | sort -request_count | head 10
------------------------------------------------------------

User Request: Show me source IPs downloading exe files

Processing request: Show me source IPs downloading exe files
Using template query: sourcetype="proxy" | where url LIKE "%.exe" OR url ENDS WITH ".exe" | stats count as download_count by srcip, url | sort -download_count
Processed query: sourcetype="proxy" | where uri LIKE "%.exe" OR uri ENDS WITH ".exe" | stats count as download_count by src, uri | sort -download_count
Final Query: sourcetype="proxy" | where uri LIKE "%.exe" OR uri ENDS WITH ".exe" | stats count as download_count by src, uri | sort -download_count
------------------------------------------------------------

User Request: Find outbound traffic to google.com

Processing request: Find outbound traffic to google.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.google.com" OR dhost="google.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.google.com" OR dest_host="google.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.google.com" OR dest_host="google.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: Show me errors from microsoft.com

Processing request: Show me errors from microsoft.com
Using template query: sourcetype="proxy" | where (dhost LIKE "*.microsoft.com" OR dhost="microsoft.com") AND status>=400 | stats count as error_count by status, dhost | sort -error_count
Processed query: sourcetype="proxy" | where (dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com") AND http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
Final Query: sourcetype="proxy" | where (dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com") AND http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
------------------------------------------------------------

User Request: What request methods are used for facebook.com

Processing request: What request methods are used for facebook.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.facebook.com" OR dhost="facebook.com" | stats count as request_count by mtd, dhost | sort -request_count
Processed query: sourcetype="proxy" | where dest_host LIKE "*.facebook.com" OR dest_host="facebook.com" | stats count as request_count by method, dest_host | sort -request_count
Final Query: sourcetype="proxy" | where dest_host LIKE "*.facebook.com" OR dest_host="facebook.com" | stats count as request_count by method, dest_host | sort -request_count
------------------------------------------------------------

User Request: How many unique users access amazon.com

Processing request: How many unique users access amazon.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.amazon.com" OR dhost="amazon.com" | stats dc(srcip) as unique_users, count as request_count by dhost | sort -request_count
Processed query: sourcetype="proxy" | where dest_host LIKE "*.amazon.com" OR dest_host="amazon.com" | stats dc(src) as unique_users, count as request_count by dest_host | sort -request_count
Final Query: sourcetype="proxy" | where dest_host LIKE "*.amazon.com" OR dest_host="amazon.com" | stats dc(src) as unique_users, count as request_count by dest_host | sort -request_count
------------------------------------------------------------

User Request: Show traffic patterns for github.com

Processing request: Show traffic patterns for github.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.github.com" OR dhost="github.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: List all domains ending with .edu

Processing request: List all domains ending with .edu
Using template query: sourcetype="proxy" | where dhost LIKE "*.edu" | stats count as request_count, sum(bytes) as total_bytes by dhost | sort -request_count | head 100
Processed query: sourcetype="proxy" | where dest_host LIKE "*.edu" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host | sort -request_count | head 100
Final Query: sourcetype="proxy" | where dest_host LIKE "*.edu" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host | sort -request_count | head 100
------------------------------------------------------------

User Request: Show domains ending with .gov

Processing request: Show domains ending with .gov
Using template query: sourcetype="proxy" | where dhost LIKE "*.gov" | stats count as request_count, sum(bytes) as total_bytes by dhost | sort -request_count | head 100
Processed query: sourcetype="proxy" | where dest_host LIKE "*.gov" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host | sort -request_count | head 100
Final Query: sourcetype="proxy" | where dest_host LIKE "*.gov" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host | sort -request_count | head 100
------------------------------------------------------------

User Request: Show traffic to *.google.com

Processing request: Show traffic to *.google.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.google.com" OR dhost="google.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.google.com" OR dest_host="google.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.google.com" OR dest_host="google.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: Find errors from any microsoft.com subdomain

Processing request: Find errors from any microsoft.com subdomain
Using template query: sourcetype="proxy" | where (dhost LIKE "*.microsoft.com" OR dhost="microsoft.com") AND status>=400 | stats count as error_count by status, dhost | sort -error_count
Processed query: sourcetype="proxy" | where (dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com") AND http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
Final Query: sourcetype="proxy" | where (dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com") AND http_status>=400 | stats count as error_count by http_status, dest_host | sort -error_count
------------------------------------------------------------

User Request: Show me access patterns for github.com and its subdomains

Processing request: Show me access patterns for github.com and its subdomains
Using template query: sourcetype="proxy" | where dhost LIKE "*.github.com" OR dhost="github.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: Count unique users accessing *.amazon.com

Processing request: Count unique users accessing *.amazon.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.amazon.com" OR dhost="amazon.com" | stats dc(srcip) as unique_users, count as request_count by dhost | sort -request_count
Processed query: sourcetype="proxy" | where dest_host LIKE "*.amazon.com" OR dest_host="amazon.com" | stats dc(src) as unique_users, count as request_count by dest_host | sort -request_count
Final Query: sourcetype="proxy" | where dest_host LIKE "*.amazon.com" OR dest_host="amazon.com" | stats dc(src) as unique_users, count as request_count by dest_host | sort -request_count
------------------------------------------------------------

User Request: Show .edu traffic in the last hour

Processing request: Show .edu traffic in the last hour
Using template query: sourcetype="proxy" | where dhost LIKE "*.edu" OR dhost="edu" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.edu" OR dest_host="edu" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.edu" OR dest_host="edu" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: Find failed requests to microsoft.com today

Processing request: Find failed requests to microsoft.com today
Using template query: sourcetype="proxy" | where dhost LIKE "*.microsoft.com" OR dhost="microsoft.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.microsoft.com" OR dest_host="microsoft.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
------------------------------------------------------------

User Request: What HTTP methods are used on *.github.com

Processing request: What HTTP methods are used on *.github.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.github.com" OR dhost="github.com" | stats count as request_count by mtd, dhost | sort -request_count
Processed query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count by method, dest_host | sort -request_count
Final Query: sourcetype="proxy" | where dest_host LIKE "*.github.com" OR dest_host="github.com" | stats count as request_count by method, dest_host | sort -request_count
------------------------------------------------------------

User Request: Show POST requests to api.example.com

Processing request: Show POST requests to api.example.com
Using template query: sourcetype="proxy" | where dhost LIKE "*.api.example.com" OR dhost="api.example.com" | stats count as request_count, sum(bytes) as total_bytes by dhost, srcip | sort -total_bytes
Processed query: sourcetype="proxy" | where dest_host LIKE "*.api.example.com" OR dest_host="api.example.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes
Final Query: sourcetype="proxy" | where dest_host LIKE "*.api.example.com" OR dest_host="api.example.com" | stats count as request_count, sum(bytes_total) as total_bytes by dest_host, src | sort -total_bytes

------------------------------------------------------------
```
## Current Limitations

#### Maintenance Issues:
 -   Growing template list becomes harder to manage
 -   Templates require constant updates
 -   Risk of template conflicts
 -   Hard to maintain consistency
#### Flexibility Problems:
 -   Can't handle unexpected query patterns
 -   Limited to predefined scenarios
 -   Requires manual template creation
 -   Rigid structure
#### Scaling Challenges:
 -   Doesn't scale well with new use cases
 -   Not easily adaptable to different log types
 -   Hard to extend to other query languages
 -   High maintenance overhead
 
## Potential Solutions & Future Work
 - Integration for other LLMs (OpenAI, etc).
 - Include additional schemas (splunk: palo alto, dns, windows, etc. MDRs)
 - The manage scalability limitations, take machine learning, pattern-based learning approach, or a hybrid approach.
 - Benefits of a hybrid approach:
 --Use templates for common, well-defined patterns
--Use ML for unexpected queries
--Learn from user feedback
--Gradually improve accuracy
--Scale better with usage
 


### Disclosure
This project includes contributions from AI-generated code (e.g., ChatGPT, Claude, etc.) 

#
# Troubleshoot
If you encounter the following error while trying to install the required Python packages:
```error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

```

This error occurs because your system’s Python environment is controlled by the operating system, blocking global package installs. To fix this, use a virtual environment to install packages locally without affecting your system.

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

4. Deactivate the virtual environment when you're done.
---------------



