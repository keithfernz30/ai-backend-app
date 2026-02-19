from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI, AsyncOpenAI
import os
import json
import time
from dotenv import load_dotenv
from typing import Literal
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# -----------------------------
# Setup
# -----------------------------
load_dotenv()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_frontend():
    return FileResponse("static/index.html")

USE_MOCK = True  # 🔥 Set to False when you want real OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
async_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# Input Schema
# -----------------------------
class UserInput(BaseModel):
    text: str
    task: Literal["summarize", "sentiment", "keywords"] = "summarize"

# -----------------------------
# Smarter NLP Logic (Mock Mode)
# -----------------------------

def extract_keywords(text: str):
    words = text.split()
    stopwords = {"is", "the", "a", "an", "and", "or", "to", "of"}
    keywords = []
    i = 0

    while i < len(words):
        word = words[i]

        # Proper noun detection
        if word.istitle():
            keywords.append(word)

        # Phrase detection like "very happy"
        elif word.lower() == "very" and i + 1 < len(words):
            phrase = f"{word} {words[i+1]}"
            keywords.append(phrase)
            i += 1

        # Meaningful word
        elif word.lower() not in stopwords and len(word) > 3:
            keywords.append(word)

        i += 1

    return list(set(keywords))


def analyze_sentiment(text: str):
    positive_words = {"good", "happy", "great", "excellent", "love", "amazing"}
    negative_words = {"bad", "sad", "terrible", "hate", "angry", "awful"}

    words = text.lower().split()

    positive_score = sum(word in positive_words for word in words)
    negative_score = sum(word in negative_words for word in words)

    if positive_score > negative_score:
        sentiment = "positive"
        confidence = round(0.6 + positive_score * 0.1, 2)
    elif negative_score > positive_score:
        sentiment = "negative"
        confidence = round(0.6 + negative_score * 0.1, 2)
    else:
        sentiment = "neutral"
        confidence = 0.5

    return sentiment, min(confidence, 0.95)


def mock_llm_response(text: str, task: str):
    words = text.split()

    if task == "summarize":
        return {
            "summary": f"(MOCK) Summary of: {text}",
            "word_count": len(words)
        }

    elif task == "sentiment":
        sentiment, confidence = analyze_sentiment(text)
        return {
            "sentiment": sentiment,
            "confidence": confidence
        }

    elif task == "keywords":
        keywords = extract_keywords(text)
        return {
            "keywords": keywords,
            "count": len(keywords)
        }

# -----------------------------
# Main Route
# -----------------------------

@app.post("/analyze")
async def analyze(input: UserInput):
    start_time = time.time()

    # -----------------------------
    # MOCK MODE
    # -----------------------------
    if USE_MOCK:
        result = mock_llm_response(input.text, input.task)

        latency_ms = round((time.time() - start_time) * 1000, 2)

        prompt_tokens = len(input.text.split())
        completion_tokens = 20
        total_tokens = prompt_tokens + completion_tokens

        return {
            "mode": "mock",
            "task": input.task,
            "result": result,
            "latency_ms": latency_ms,
            "tokens": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens
            }
        }

    # -----------------------------
    # REAL OPENAI MODE
    # -----------------------------

    system_prompts = {
        "summarize": "Summarize the text and return JSON with summary and word_count.",
        "sentiment": "Analyze sentiment and return JSON with sentiment and confidence.",
        "keywords": "Extract meaningful keywords and phrases and return JSON with keywords list and count."
    }

    response = await async_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompts[input.task]},
            {"role": "user", "content": input.text}
        ],
        response_format={"type": "json_object"}
    )

    content = response.choices[0].message.content
    parsed = json.loads(content)

    latency_ms = round((time.time() - start_time) * 1000, 2)
    usage = response.usage

    return {
        "mode": "real",
        "task": input.task,
        "result": parsed,
        "latency_ms": latency_ms,
        "tokens": {
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens
        }
    }
