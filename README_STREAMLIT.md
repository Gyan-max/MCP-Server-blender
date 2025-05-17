# Blender Text-to-3D Generator

This Streamlit application connects to Blender using the MCP (Machine Control Protocol) client to generate 3D content from text prompts.

## Prerequisites

1. Blender installed on your system
2. Blender MCP addon installed and enabled in Blender
3. Python 3.8+ installed on your system

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Blender is running with the MCP addon enabled
   - Open Blender
   - Go to Edit > Preferences > Add-ons
   - Enable the "Blender MCP" addon
   - In the 3D Viewport, open the sidebar (N key) and click on the "BlenderMCP" tab
   - Click "Connect to Claude" to start the MCP server

3. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

## Usage

1. Enter a text prompt in the "Create" tab to generate new 3D models
   - Example prompts: "Create a chair", "Generate a tree", "Make a table"

2. Use the "Modify" tab to change existing objects in Blender
   - First, select an object in Blender
   - Then use prompts like "Make it red", "Scale it bigger", or "Rotate it"

3. Check the connection status in the sidebar

## How It Works

The application:
1. Connects to Blender using the MCP client
2. Takes your text prompt
3. Translates it into Blender Python code
4. Executes the code in Blender to create or modify 3D objects
5. Shows the result in Blender's viewport

## Troubleshooting

- If you have connection issues, make sure the MCP server is running in Blender
- Check that the port in the configuration (blender_mcp.json) matches the port used by the Blender MCP addon (default is 9876)
- Look for error messages in the Streamlit interface or terminal output

## Extending the App

You can extend this application by:
- Adding more specific 3D generation templates
- Implementing material and texture control
- Adding animation capabilities
- Integrating with more advanced 3D generation models 