# Escalation Context Packet Generator

## Run from GitHub

Clone the repository and enter the project folder:

```powershell
git clone https://github.com/navyavishwakarma/escalation-packet.git
cd escalation-packet
```

## Setup (5 minutes)

### 1. Get a free Gemini API key
- Go to https://aistudio.google.com
- Sign in with Google → click "Get API key" → "Create API key"
- Copy it (starts with `AIza...`)

### 2. Add your key
- Go into the `backend` folder
- Copy `.env.example` to `.env`
- Open `.env` and replace `paste-your-key-here` with your real key

### 3. Install and run the backend
Open a terminal in the `backend` folder and run:

```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn main:app --reload
```

(On Mac/Linux, use `source venv/bin/activate` instead of `venv\Scripts\activate.bat`.)

Leave this terminal running. You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### 4. Open the frontend

Keep the backend terminal running. In a second terminal from the project root, run:

```powershell
python -m http.server 5500 --directory frontend
```

Open http://127.0.0.1:5500 in your browser and select a ticket. The dashboard calls the backend at `http://127.0.0.1:8000`.

Opening `frontend/index.html` directly also works in most browsers, but the local frontend server avoids browser file restrictions.

## Deploy a shareable live website

The repository includes `render.yaml` so Render can deploy the backend and frontend as one web service.

1. Create an account at https://render.com and choose **New +** -> **Blueprint**.
2. Connect the GitHub repository `navyavishwakarma/escalation-packet`.
3. Confirm the service created from `render.yaml`.
4. In the service's **Environment** settings, add `GEMINI_API_KEY` with your real key.
5. Deploy the service.

Render will provide a URL like `https://escalation-packet.onrender.com`. Share that URL; it serves the dashboard and API together. The free service may take a few seconds to wake up after inactivity.

Your `.env` file will NOT be uploaded (it's in `.gitignore`) — this is intentional, it protects your API key.

## If something breaks
- "ModuleNotFoundError" → you forgot to activate venv, or forgot `pip install -r requirements.txt`
- Frontend shows "Could not reach backend" → make sure the uvicorn terminal is still running
- Empty/garbled AI response → check your API key is correct in `.env`
