import requests
import json

print("Testing minimal Blender API call...")

# Create very simple code to add a cube - no collections or advanced features
simple_code = '''
import bpy

# Clear the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a simple cube
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
cube = bpy.context.active_object
cube.name = "SimpleCube"

print("Simple cube created successfully!")
'''

# Build the request based on how the addon.py expects it
payload = {
    "type": "execute_code",  # Must match handler name in addon.py
    "params": {
        "code": simple_code
    }
}

try:
    print("Sending request to Blender...")
    response = requests.post(
        'http://localhost:9876/execute',
        json=payload
    )
    
    print(f"Response status code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("\nResponse from Blender:")
        print(json.dumps(result, indent=2))
    else:
        print("\nRequest failed!")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:200]}")
except Exception as e:
    print(f"\nError: {e}")
    
print("\nTest complete.") 