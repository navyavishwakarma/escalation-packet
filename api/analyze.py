from fastapi import FastAPI

from backend.main import Conversation, analyze

app = FastAPI()


@app.post("/")
def analyze_conversation(convo: Conversation):
    return analyze(convo)