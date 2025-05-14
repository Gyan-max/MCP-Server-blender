import asyncio
from mcp_use import MCPClient

async def main():
    try:
        # Explicitly load config file
        config_path = "/home/gyan-max/Desktop/mcp-use-main/blender_mcp.json"
        client = MCPClient.from_config_file(config_path)
        print("Client initialized successfully")
        
        # Create session for 'blender'
        session = await client.create_session("blender")
        print("Session created:", session)

        # Discover available tools
        tools = await session.discover_tools()
        print("Discovered tools:", [tool.name for tool in tools])
        
        # Send command to add a cube using the 'execute_code' tool
        code = "import bpy; bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))"
        # Add a circle at the origin
        # code = "import bpy; bpy.ops.mesh.primitive_circle_add(vertices=32, radius=1.0, fill_type='NGON', location=(0, 0, 10))"
        response = await session.call_tool("execute_blender_code", {"code": code})
        print("Response from server:", response)
        # primitive_cube_add = response.get("primitive_cube_add")
        # print("Primitive cube add:", primitive_cube_add)
        # Clean up
        await client.close_session("blender")
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    asyncio.run(main())