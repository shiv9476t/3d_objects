from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from generate_tripo import send_prompt, check_status
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return send_file("index.html")

@app.route("/models", methods=["POST"])
def generate_model():
    data = request.json
    if not data or "prompt" not in data:
        return jsonify({"error": "prompt is required"}), 400
    try:
        task_id = send_prompt(data["prompt"])
        return jsonify({"task_id": task_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/models/<task_id>", methods=["GET"])
def get_model(task_id):
    status, result = check_status(task_id)
    if status == "PENDING" or status == "IN_PROGRESS":
        return jsonify({"status": status, "file_url": None}), 200
    elif status == "FINISHED":
        return jsonify({"status": status, "file_url": f"/models/{task_id}/file"}), 200
    elif status == "FAILED":
        return jsonify({"status": status, "file_url": None}), 400

@app.route("/models/<task_id>/file", methods=["GET"])
def get_model_file(task_id):
    filepath = f"/tmp/{task_id}.glb"
    if not os.path.exists(filepath):
        return jsonify({"error": "file not found"}), 404
    return send_file(filepath, mimetype="model/gltf-binary")

@app.route("/test-model", methods=["GET"])
def test_model():
    import glob
    glb_files = glob.glob("*.glb")
    if not glb_files:
        return jsonify({"error": "no glb files found"}), 404
    return send_file(glb_files[0], mimetype="model/gltf-binary")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)