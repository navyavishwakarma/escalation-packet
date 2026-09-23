from fastapi import FastAPI

from backend.main import SAMPLES

app = FastAPI()


@app.get("/")
def get_conversations():
    return SAMPLES