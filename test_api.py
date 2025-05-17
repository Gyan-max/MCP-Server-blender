import requests

def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/version")
        response.raise_for_status()
        print("Ollama is running!")
        print("Version:", response.json())
        return True
    except requests.exceptions.ConnectionError:
        print("Could not connect to Ollama. Is it running?")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False

def test_ollama_api():
    # First check if Ollama is running
    if not test_ollama_connection():
        return

    # Ollama API configuration
    API_URL = "http://localhost:11434/api/generate"
    
    try:
        # Make a simple test call
        payload = {
            "model": "mistral",  # You can also use "llama2", "codellama", etc.
            "prompt": "Say hello!",
            "stream": False
        }
        
        print("\nSending request to Ollama...")
        response = requests.post(API_URL, json=payload)
        
        # Check for HTTP errors
        response.raise_for_status()
        
        # Parse and print the response
        result = response.json()
        print("\nAPI Test Successful!")
        print("Response:", result["response"])
        
    except requests.exceptions.ConnectionError:
        print("\nConnection Error: Could not connect to Ollama")
        print("Please make sure Ollama is running on your system")
        print("You can check if Ollama is running with: curl http://localhost:11434/api/version")
        
    except requests.exceptions.HTTPError as e:
        print("\nAPI Test Failed!")
        print(f"HTTP Error: {str(e)}")
        
    except Exception as e:
        print("\nAPI Test Failed!")
        print(f"Error: {str(e)}")
        print("\nPlease check:")
        print("1. Ollama is installed and running")
        print("2. You have the correct model pulled")
        print("3. Your system meets the requirements")

if __name__ == "__main__":
    test_ollama_api() 