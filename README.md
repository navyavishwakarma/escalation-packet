# Escalation Context Packet Generator

## Setup (5 minutes)

### 1. Get a free Gemini API key
- Go to https://aistudio.google.com
- Sign in with Google → click "Get API key" → "Create API key"
- Copy it (starts with `AIza...`)

### 2. Add your key
- Go into the `backend` folder
- Rename `.env.example` to `.env`
- Open `.env` and replace `paste-your-key-here` with your real key

### 3. Install and run the backend
Open a terminal in the `backend` folder and run:

```
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
uvicorn main:app --reload
```

(On Mac/Linux, use `source venv/bin/activate` instead of `venv\Scripts\activate.bat`)

Leave this terminal running. You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### 4. Open the frontend
Just double-click `frontend/index.html` to open it in your browser.
Click any ticket button — it should call your backend and show the generated packet.

## Push to GitHub

```
cd escalation-packet
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/escalation-packet.git
git push -u origin main
```

Your `.env` file will NOT be uploaded (it's in `.gitignore`) — this is intentional, it protects your API key.

## If something breaks
- "ModuleNotFoundError" → you forgot to activate venv, or forgot `pip install -r requirements.txt`
- Frontend shows "Could not reach backend" → make sure the uvicorn terminal is still running
- Empty/garbled AI response → check your API key is correct in `.env`
