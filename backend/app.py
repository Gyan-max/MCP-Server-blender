from flask import Flask, request, jsonify
from api.claude_api import ask_claude
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agent import run_blender_code

app = Flask(__name__, static_folder="../frontend", static_url_path="")

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/prompt", methods=["POST"])
def generate_blender_object():
    user_prompt = request.json["prompt"]
    bpy_code = ask_claude(user_prompt)  # Claude API

    # Only run if bpy_code is a string (valid code)
    if isinstance(bpy_code, str):
        run_blender_code(bpy_code)          # agent.py
        return {"status": "success", "message": "Object created in Blender"}
    else:
        # Return the error from Claude
        return {"status": "error", "message": bpy_code.get("error", "Unknown error from Claude")}

@app.route("/api/blender", methods=["POST"])
def run_blender():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400
    result = run_blender_code(code)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True) 