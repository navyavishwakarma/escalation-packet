from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import os
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---- Sample conversations for the demo (edit freely) ----
SAMPLES = {
    "billing": [
        "Customer: I was charged twice for my subscription this month",
        "Agent: I'm sorry to hear that, let me check your account",
        "Customer: This is the third time this has happened, it's really frustrating",
    ],
    "delivery": [
        "Customer: My order still hasn't arrived",
        "Agent: It shows as in transit, should arrive in 2 days",
        "Customer: It's already been 5 days, I need it today for an event",
    ],
    "bug": [
        "Customer: The app crashes every time I try to upload a photo",
        "Agent: Can you tell me what device and app version you're using?",
        "Customer: iPhone 13, latest version, happens every single time",
    ],
    "messy": [
        "Customer: This is honestly useless",
        "Agent: I'm sorry you're having trouble, let's take a look",
        "Customer: fine, whatever, thanks for checking",
        "Customer: wait, it just broke again!!",
    ],
    "refund": [
        "Customer: I returned the headphones two weeks ago but I still don't see my refund",
        "Agent: I can see the return was scanned by the carrier",
        "Customer: The tracking says delivered on Monday and nobody can tell me where the money is",
    ],
    "login": [
        "Customer: I am locked out of my account after changing my phone number",
        "Agent: I sent a password reset link to the email on file",
        "Customer: I don't have access to that email anymore and the reset link is useless",
    ],
    "cancellation": [
        "Customer: Please cancel my annual plan before it renews tomorrow",
        "Agent: I can help with that, but the cancellation screen is currently unavailable",
        "Customer: I have tried three times and I cannot afford another charge",
    ],
    "outage": [
        "Customer: Our whole team cannot access the dashboard this morning",
        "Agent: We are checking whether this is related to the maintenance window",
        "Customer: This is blocking payroll for 40 people and we need an update now",
    ],
    "invoice": [
        "Customer: The invoice total does not match the usage report for August",
        "Agent: I compared the line items and found a duplicate seat charge",
        "Customer: Please correct it before our finance team pays the invoice",
    ],
    "verification": [
        "Customer: My identity verification has been pending since yesterday",
        "Agent: Please upload a clearer photo of your ID in good lighting",
        "Customer: I already did that twice and the status has not changed",
    ],
}


class Conversation(BaseModel):
    messages: list[str]


def fallback_packet(messages: list[str]) -> str:
    customer_messages = [
        message.split(":", 1)[1].strip()
        for message in messages
        if message.lower().startswith("customer:") and ":" in message
    ]
    agent_messages = [
        message.split(":", 1)[1].strip()
        for message in messages
        if message.lower().startswith("agent:") and ":" in message
    ]
    customer_messages = customer_messages or messages
    transcript = " ".join(customer_messages).lower()

    negative_words = ("broken", "crash", "charged", "frustrat", "useless", "late", "failed", "can't", "cannot")
    positive_words = ("thanks", "thank", "great", "fixed", "working")
    sentiment = sum(word in transcript for word in positive_words) * 0.25
    sentiment -= sum(word in transcript for word in negative_words) * 0.25
    sentiment = max(-1.0, min(1.0, sentiment))
    sentiment_trend = [round(sentiment * (index + 1) / len(customer_messages), 2) for index in range(len(customer_messages))]

    urgent_words = ("today", "urgent", "asap", "event", "third time", "every time")
    urgency = "high" if any(word in transcript for word in urgent_words) else "medium"
    tone = "frustrated" if sentiment < 0 else "neutral"

    return json.dumps({
        "issue_summary": customer_messages[0],
        "attempted_fixes": agent_messages or ["No resolution recorded before escalation."],
        "key_facts": customer_messages,
        "tone": tone,
        "urgency": urgency,
        "sentiment_trend": sentiment_trend,
    })


@app.get("/conversations")
def get_conversations():
    return SAMPLES


@app.post("/analyze")
def analyze(convo: Conversation):
    transcript = "\n".join(convo.messages)
    prompt = f"""You are analyzing a customer support conversation.
Return ONLY valid JSON (no markdown, no code fences) with exactly these keys:
issue_summary, attempted_fixes, key_facts, tone, urgency (must be one of: low, medium, high), sentiment_trend

sentiment_trend must be an array of numbers, one per customer message only (skip agent messages), each between -1 (very negative) and 1 (very positive), in order.

Conversation:
{transcript}
"""

    if not API_KEY:
        return {"result": fallback_packet(convo.messages)}

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"
    payload = {
    "contents": [{"parts": [{"text": prompt}]}],
    "generationConfig": {
        "maxOutputTokens": 2048,
        "thinkingConfig": {"thinkingBudget": 0}
    }
}

    import time

    for attempt in range(4):
        response = None
        try:
            response = requests.post(url, json=payload, timeout=45)
            response.raise_for_status()
            data = response.json()

            print("GEMINI STATUS:", response.status_code)
            print("GEMINI RAW RESPONSE:", data)

            text = data["candidates"][0]["content"]["parts"][0]["text"]
            break

        except requests.RequestException as e:
            status = response.status_code if response is not None else "network error"
            print("GEMINI ERROR:", status, type(e).__name__)

            if response is not None and 400 <= response.status_code < 500:
                return {"result": fallback_packet(convo.messages)}

            if attempt == 3:
                return {"result": fallback_packet(convo.messages)}
            time.sleep(5)
        except (KeyError, IndexError, TypeError, ValueError) as e:
            print("GEMINI RESPONSE ERROR:", type(e).__name__)

            if attempt == 3:
                return {"result": fallback_packet(convo.messages)}
            time.sleep(5)

    # Clean up common formatting issues (markdown code fences)
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:].strip()

    return {"result": cleaned}


frontend_path = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
