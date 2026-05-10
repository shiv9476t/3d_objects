# 3D Object Generator — Prototype

A working prototype for an AI-powered 3D object generation tool. The tool allows a user to enter a natural language prompt and generate an interactive 3D model rendered in the browser via Three.js.

**Live prototype:** https://3d-objects.up.railway.app

## Stack

- **Frontend:** HTML/CSS/JavaScript, Three.js (GLTFLoader, OrbitControls)
- **Backend:** Python, Flask
- **3D Generation API:** Tripo3D AI
- **Deployment:** Railway

## How it works

1. User enters a natural language prompt
2. Flask backend sends the prompt to the Tripo3D API
3. Backend polls for status and downloads the generated GLB file
4. Three.js renders the model in the browser with orbit controls

## Running locally

```bash
pip install -r requirements.txt
```

Add a `.env` file with:

```
API_KEY=your_tripo3d_api_key
```

Then:

```bash
python app.py
```