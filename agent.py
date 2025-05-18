import asyncio
from mcp_use import MCPClient

async def run_blender_code_async(code: str):
    try:
        config_path = "/home/gyan-max/Desktop/mcp-use-main/blender_mcp.json"
        print("Connecting to MCP server...")
        client = MCPClient.from_config_file(config_path)
        print("Connected. Creating session...")
        session = await client.create_session("blender")
        print("Session created. Sending code...")
        response = await session.call_tool("execute_blender_code", {"code": code})
        print("Code sent. Response:", response)
        await client.close_session("blender")
        print("Session closed.")
        return response
    except Exception as e:
        return {"error": str(e)}

# Synchronous wrapper for Flask

def run_blender_code(code: str):
    return asyncio.run(run_blender_code_async(code))

if __name__ == "__main__":
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