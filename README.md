# Escalation Context Packet Generator

> A support-agent dashboard that turns an escalated conversation into a structured context packet.

**Live demo:** https://escalation-packet.vercel.app/

## Free deployment with Hugging Face Spaces

Hugging Face Spaces can run this app publicly on a free CPU Docker Space. No Render payment setup is required.

1. Create an account at https://huggingface.co and open **New Space**.
2. Choose a Space name, select **Docker** as the SDK, choose **CPU basic**, and set visibility to **Public**.
3. In the new Space, open **Files** -> **Add file** -> **Upload files** and upload the contents of this repository, including `Dockerfile`.
4. Open **Settings** -> **Variables and secrets** -> **New secret** and add:

	```text
	GEMINI_API_KEY=your_new_key
	```

5. Wait for the build to finish, then open the Space's **App** tab. The public link will look like:
	`https://huggingface.co/spaces/YOUR-USERNAME/YOUR-SPACE-NAME`

The Space runs the frontend and backend together. The local `.env` file is not uploaded or needed.

## Deploy with Vercel

Vercel can host this project using its Python serverless runtime.

1. Open https://vercel.com and sign in with GitHub.
2. Choose **Add New** -> **Project** and import `navyavishwakarma/escalation-packet`.
3. Leave the framework preset as **Other**. Vercel will use `vercel.json`.
4. Add an environment variable named `GEMINI_API_KEY` with your Gemini key.
5. Click **Deploy**.

Vercel will provide a public URL such as `https://escalation-packet.vercel.app`. Vercel loads the FastAPI app from `backend.main:app`, which serves both the dashboard and the `/conversations` and `/analyze` endpoints.

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
