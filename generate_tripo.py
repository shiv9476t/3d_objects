import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
BASE_URL = "https://api.tripo3d.ai/v2/openapi"

def send_prompt(prompt):
    response = requests.post(
        f"{BASE_URL}/task",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "type": "text_to_model",
            "prompt": prompt
        }
    )
    data = response.json()
    if "data" not in data or "task_id" not in data["data"]:
        raise Exception(f"API error: {data}")
    
    task_id = data["data"]["task_id"]
    print(f"Task ID: {task_id}")
    return task_id

def check_status(task_id):
    response = requests.get(
        f"{BASE_URL}/task/{task_id}",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    data = response.json()
    status = data["data"]["status"]
    print(f"Status: {status}")
    
    if status == "success":
        output = data["data"]["output"]
        download_url = output.get("pbr_model") or output.get("model") or output.get("rendered_image")
        if not download_url:
            print("Full output:", output)
            return "FAILED", None
        download_model(download_url, task_id)
        return "FINISHED", task_id
    elif status in ["queued", "running"]:
        return "IN_PROGRESS", None
    elif status == "failed":
        print(f"Failed: {data['data'].get('message', 'unknown error')}")
        return "FAILED", None

def download_model(download_url, task_id):
    glb_response = requests.get(download_url)
    filepath = f"/tmp/{task_id}.glb"
    with open(filepath, "wb") as f:
        f.write(glb_response.content)
    print("Saved to", filepath)
    return filepath
    