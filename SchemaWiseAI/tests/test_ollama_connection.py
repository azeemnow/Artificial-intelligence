# tests/test_ollama_connection.py
import requests
import json

def test_ollama_connection():
    base_url = "http://localhost:11434"
    
    # Test version endpoint
    try:
        version_response = requests.get(f"{base_url}/api/version")
        print(f"Version endpoint response: {version_response.status_code}")
        print(version_response.json())
    except Exception as e:
        print(f"Version endpoint error: {e}")

    # Test generate endpoint
    try:
        generate_response = requests.post(
            f"{base_url}/api/generate",
            json={
                "model": "llama3.2:1b",
                "prompt": "Generate a simple Splunk query",
                "stream": False
            }
        )
        print(f"\nGenerate endpoint response: {generate_response.status_code}")
        print(f"Response headers: {generate_response.headers}")
        print(f"Response content: {generate_response.text}")
    except Exception as e:
        print(f"Generate endpoint error: {e}")

if __name__ == "__main__":
    test_ollama_connection()