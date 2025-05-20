import asyncio
from mcp_use import MCPClient
import requests
import json
import sys
import time

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        print("Checking Ollama connection...")
        response = requests.get("http://localhost:11434/api/version")
        response.raise_for_status()
        version = response.json()
        print(f"Ollama is running! Version: {version}")
        
        # Check if Mistral model is available
        print("Checking if Mistral model is available...")
        try:
            # Try to use the model directly to verify it's available
            test_payload = {
                "model": "mistral",
                "prompt": "test",
                "stream": False
            }
            test_response = requests.post("http://localhost:11434/api/generate", json=test_payload)
            test_response.raise_for_status()
            print("Mistral model is available and working!")
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                print("Mistral model not found. Please run: ollama pull mistral")
            else:
                print(f"Error testing Mistral model: {str(e)}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Is it running?")
        print("Note: If you see 'address already in use', Ollama is already running!")
        return False
    except Exception as e:
        print(f"Error checking Ollama: {e}")
        return False

def check_blender_mcp_connection():
    """Check if Blender MCP server is running and accessible"""
    try:
        # Try to read the config file
        with open("/home/gyan-max/Desktop/mcp-use-main/blender_mcp.json", 'r') as f:
            config = json.load(f)
            print("Config file loaded successfully:", config)
    except Exception as e:
        print(f"Error reading config file: {e}")
        return False
    return True

def clean_generated_code(code: str) -> str:
    """Clean up the generated code by removing comments and ensuring it's valid Python."""
    # Split the code into lines
    lines = code.split('\n')
    cleaned_lines = []
    
    for line in lines:
        # Skip lines that are just comments or empty
        if line.strip().startswith('#') or not line.strip():
            continue
        # Skip lines that look like markdown or documentation
        if line.strip().startswith('```') or line.strip().startswith('This code'):
            continue
        # Skip lines that are just descriptions
        if line.strip().startswith('This will') or line.strip().startswith('The code'):
            continue
        cleaned_lines.append(line)
    
    # Join the lines back together
    cleaned_code = '\n'.join(cleaned_lines)
    
    # Ensure the code starts with import bpy
    if not cleaned_code.strip().startswith('import bpy'):
        cleaned_code = 'import bpy\n' + cleaned_code
        
    return cleaned_code

def generate_blender_code_with_ollama(description: str) -> str:
    """Generate Blender Python code using Ollama based on a text description."""
    API_URL = "http://localhost:11434/api/generate"
    
    # First check if Ollama is running
    if not check_ollama_connection():
        return "Error: Ollama is not running. Please start Ollama with 'ollama serve'"
    
    prompt = f"""Generate ONLY Python code for Blender (bpy) to create a 3D model based on this description: {description}

    Requirements:
    1. Use only Blender's Python API (bpy)
    2. Create a complete, working code block
    3. Include necessary imports
    4. Use appropriate Blender operations to create the described model
    5. Add materials and colors if relevant
    6. Position the model appropriately in the scene
    7. Use proper naming for objects
    8. DO NOT include any comments or explanations
    9. Return ONLY the Python code

    Example format:
    import bpy
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    cube = bpy.context.active_object
    cube.name = "MyCube"
    """
    
    try:
        print("\nPreparing to send request to Ollama...")
        payload = {
            "model": "mistral",
            "prompt": prompt,
            "stream": False,
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 2000
        }
        
        print("Sending request to Ollama...")
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        result = response.json()
        
        generated_code = result["response"].strip()
        
        # Clean up the generated code
        cleaned_code = clean_generated_code(generated_code)
        print("\nCleaned generated code:", cleaned_code)
        
        return cleaned_code
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print("Error: Mistral model not found. Please run: ollama pull mistral")
        else:
            print(f"Error in Ollama API call: {str(e)}")
        return f"Error generating code: {str(e)}"
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama. Is it running?")
        return "Error: Ollama connection failed. Please ensure Ollama is running with 'ollama serve'"
    except Exception as e:
        print(f"Error in Ollama API call: {str(e)}")
        return f"Error generating code: {str(e)}"

async def run_blender_code_async(code: str):
    try:
        config_path = "/home/gyan-max/Desktop/mcp-use-main/blender_mcp.json"
        print("\nChecking Blender MCP connection...")
        if not check_blender_mcp_connection():
            return {"error": "Blender MCP configuration check failed"}
            
        print("Connecting to MCP server...")
        client = MCPClient.from_config_file(config_path)
        
        print("Connected. Creating session...")
        session = await client.create_session("blender")
        
        print("Session created. Sending code...")
        print("Code to be executed:", code)
        
        response = await session.call_tool("execute_blender_code", {"code": code})
        print("Code sent. Response:", response)
        
        print("Closing session...")
        await client.close_session("blender")
        print("Session closed.")
        
        return response
    except Exception as e:
        print(f"Error in run_blender_code_async: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print("Full traceback:", traceback.format_exc())
        return {"error": str(e)}

def run_blender_code(code: str):
    try:
        return asyncio.run(run_blender_code_async(code))
    except Exception as e:
        print(f"Error in run_blender_code: {str(e)}")
        return {"error": str(e)}

def create_3d_model_from_description(description: str):
    """Create a 3D model in Blender based on a text description using Ollama."""
    print(f"\nGenerating 3D model for description: {description}")
    
    # Generate Blender code using Ollama
    generated_code = generate_blender_code_with_ollama(description)
    
    if generated_code.startswith("Error"):
        return {"error": generated_code}
    
    print("\nGenerated code:", generated_code)
    
    # Execute the generated code in Blender
    result = run_blender_code(generated_code)
    print("\nExecution result:", result)
    return result

if __name__ == "__main__":
    print("Welcome to the 3D Model Generator!")
    print("Checking system configuration...")
    
    # Check if Ollama is running
    if not check_ollama_connection():
        print("Error: Ollama is not running. Please start Ollama with 'ollama serve'")
        sys.exit(1)
    
    # Check if Blender MCP is running
    if not check_blender_mcp_connection():
        print("Error: Blender MCP configuration check failed. Please ensure Blender MCP is running on port 9876")
        sys.exit(1)
    
    print("System check passed. Ready to generate 3D models!")
    print("Enter your description of the 3D model you want to create.")
    print("Type 'quit' to exit.")
    
    while True:
        description = input("\nEnter your model description: ").strip()
        
        if description.lower() == 'quit':
            break
            
        if not description:
            print("Please enter a valid description.")
            continue
            
        print("\nGenerating 3D model...")
        result = create_3d_model_from_description(description)
        print("\nFinal result:", result)

    # Example usage: create a cube
    code = "import bpy; bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))"
    print(run_blender_code(code))

    # Example usage: create a UV sphere
    code = "import bpy; bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(2, 2, 0))"
    print(run_blender_code(code))

    # Example usage: create a cone
    code = "import bpy; bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(-2, 0, 0))"
    print(run_blender_code(code))

    # Example usage: create a cone
    code = "import bpy; bpy.ops.mesh.primitive_cone_add(radius1=1, depth=2, location=(-2, 0, 0))"
    print("Claude output:", code)
    print(run_blender_code(code))