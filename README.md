# 🚀 AI Backend API

An async FastAPI-based AI backend with task routing, mock mode support, latency tracking, and deployment-ready configuration.

---

## 📌 Overview

This project demonstrates a production-style AI backend architecture featuring:

* ⚡ Async FastAPI backend
* 🧠 Task-based request routing
* 🧪 Mock mode (no API cost during development)
* 🤖 Real OpenAI integration
* 📦 JSON response enforcement
* ⏱️ Latency measurement
* 📊 Token usage tracking
* 🌐 Simple frontend interface
* ☁️ Cloud deployment ready

---

## 🏗️ Architecture

```
Frontend (HTML + JavaScript)
        ↓
FastAPI Backend (Async)
        ↓
Mock NLP Logic   OR   OpenAI API
```

The backend supports two operating modes:

* 🧪 **Mock Mode** – Local testing without API usage
* 🤖 **Real Mode** – Calls OpenAI API for actual responses

---

## 🔌 API Endpoint

### POST `/analyze`

Request body:

```json
{
  "text": "Keith is very happy",
  "task": "keywords"
}
```

Supported tasks:

* 📝 summarize
* 😊 sentiment
* 🔑 keywords

---

## 📤 Example Response

```json
{
  "mode": "mock",
  "task": "keywords",
  "result": {
    "keywords": ["Keith", "very happy"],
    "count": 2
  },
  "latency_ms": 9.31,
  "tokens": {
    "prompt_tokens": 4,
    "completion_tokens": 20,
    "total_tokens": 24
  }
}
```

---

## ✨ Features

### 🧭 Task Routing

A single endpoint dynamically routes logic based on task type.

### 🧠 Mock NLP Engine

Includes:

* Proper noun detection
* Phrase extraction (e.g., "very happy")
* Stopword filtering
* Rule-based sentiment scoring

### ⏱️ Latency Tracking

Each request returns processing time in milliseconds.

### 📊 Token Usage Tracking

* Simulated token counts in mock mode
* Real usage data in OpenAI mode

---

## 🛠️ Tech Stack

* 🐍 Python 3.9+
* ⚡ FastAPI
* 🚀 Uvicorn
* 🤖 OpenAI SDK (Async)
* 🌐 HTML + Vanilla JavaScript
* ☁️ Render (Deployment)

---

## 🧑‍💻 Local Setup

Clone the repository:

```bash
git clone https://github.com/keithfernz30/ai-backend-app.git
cd ai-backend-app
```

Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

Run the server:

```bash
python -m uvicorn main:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## 🔄 Switching Between Mock & Real Mode

Inside `main.py`:

```python
USE_MOCK = True
```

Set:

* 🧪 `True` → Mock mode
* 🤖 `False` → Real OpenAI mode

---

## ☁️ Deployment (Render)

Build Command:

```
pip install -r requirements.txt
```

Start Command:

```
uvicorn main:app --host 0.0.0.0 --port 10000
```

Add environment variable in Render dashboard:

```
OPENAI_API_KEY=your_key
```

---

## 📂 Project Structure

```
ai-backend-app/
│
├── main.py
├── requirements.txt
├── .gitignore
├── README.md
└── static/
    └── index.html
```

---

## 🎯 What This Project Demonstrates

* ⚡ Async backend design
* 🧠 Feature flag architecture (mock vs real)
* 📦 Structured JSON enforcement
* 🤖 AI API integration
* 📊 Latency & token monitoring
* 🚀 Deployment workflow

---

## 👨‍💻 Author

Keith Fernandes

---
