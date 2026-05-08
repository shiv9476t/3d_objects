import requests
import time
import os

API_KEY = "loriBblFa7T1CGywDmfhWZiOUoQcLMDLvGnJ"
BASE_URL = "https://api.3daistudio.com"


def send_prompt(prompt):
    response = requests.post(
        f"{BASE_URL}/v1/3d-models/tripo/text-to-3d/",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={"prompt": prompt}
    )
    
    data = response.json()
    if "task_id" not in data:
        raise Exception(f"API error: {data}")
    
    task_id = data["task_id"]
    print(f"Task ID: {task_id}")
    return task_id

def check_status(task_id):
    status_response = requests.get(
        f"{BASE_URL}/v1/generation-request/{task_id}/status/",
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    
    data = status_response.json()
    status = data["status"]
    print(f"Status: {status}")
    
    if status == "FINISHED":
        print("Full response:", data)
        download_url = data["results"][0]["asset"]
        print(f"Download URL: {download_url}")
        download_model(download_url, task_id)
        return status, task_id
    elif status == "PENDING" or status == "IN_PROGRESS":
        return status, None
    elif status == "FAILED":
        print(f"Failed: {data['failure_reason']}")
        return status, None
            
def download_model(download_url, task_id):
    glb_response = requests.get(download_url)
    filepath = f"{task_id}.glb"
    with open(filepath, "wb") as f:
        f.write(glb_response.content)
    return filepath

   
    
    



