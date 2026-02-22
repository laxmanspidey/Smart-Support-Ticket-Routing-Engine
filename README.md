# 🚀 Smart-Support Ticket Routing Engine

An intelligent, high-throughput, and self-healing asynchronous ticket
routing engine built for the System Design & NLP Hackathon Track.

This system ingests thousands of support tickets, categorizes them using
Deep Learning, calculates urgency, and routes them to the optimal agent
while remaining resilient to system failures and ticket storms.

------------------------------------------------------------------------

## 🏗️ Architecture Overview

Client → FastAPI → Redis Queue → Celery Workers → ML Models\
↓\
Skill-Based Routing Engine\
↓\
Webhook / Agent System

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   API Framework: FastAPI\
-   Message Broker: Redis\
-   Task Queue: Celery\
-   Machine Learning: PyTorch\
-   NLP Models: Hugging Face Transformers\
-   Embeddings: sentence-transformers\
-   Concurrency: Redis Atomic Locks (Mutex)\
-   Webhooks: Slack / Discord (Mock)

------------------------------------------------------------------------

# 🏆 Hackathon Milestones Achieved

## ✅ Milestone 1: The Minimum Viable Router (MVR)

-   REST API accepts JSON payloads and stores tickets in a priority
    queue (heapq).
-   Keyword-based routing into Billing, Technical, or Legal categories.
-   Regex-based urgency detection ("broken", "ASAP", "urgent").

------------------------------------------------------------------------

## ✅ Milestone 2: The Intelligent Queue

-   Migrated to Redis + Celery asynchronous architecture.
-   API returns 202 Accepted immediately.
-   Transformer-based zero-shot classification.
-   Sentiment regression model generating continuous urgency score S ∈
    \[0,1\].
-   Redis atomic locks prevent duplicate processing.
-   Webhook triggered for S \> 0.8.

------------------------------------------------------------------------

## ✅ Milestone 3: The Autonomous Orchestrator

### Semantic Deduplication

Cosine similarity formula:

similarity = (A · B) / (\|\|A\|\| \|\|B\|\|)

If similarity \> 0.9 for more than 10 tickets in 5 minutes: - Suppress
individual alerts - Create a Master Incident - Prevent ticket storms

### Circuit Breakers

-   Monitor transformer latency
-   If latency \> 500ms → fallback to lightweight baseline model

### Skill-Based Routing

-   Maintains agent skill vectors
-   Routes based on capacity + skill match optimization

------------------------------------------------------------------------

# ⚙️ Installation & Setup

## 1. Create Virtual Environment

python -m venv venv\
.`\venv`{=tex}`\Scripts`{=tex}`\activate  `{=tex}

## 2. Install Dependencies

pip install fastapi uvicorn celery redis transformers torch
sentence-transformers requests

## 3. Start Redis (Docker)

docker run -p 6379:6379 -d redis

------------------------------------------------------------------------

# 🏃‍♂️ How to Run

## Terminal 1 -- Start Worker

python -m celery -A worker.celery_app worker --loglevel=info --pool=solo

## Terminal 2 -- Start FastAPI

python -m uvicorn main:app --reload

Swagger UI available at: http://127.0.0.1:8000/docs

------------------------------------------------------------------------

# 🧪 Run Test Suite

Ensure worker and API are running, then:

python test_suite.py

------------------------------------------------------------------------

# 📈 Key Highlights

-   Non-blocking API responses\
-   Transformer-based NLP\
-   Race-condition safe\
-   Self-healing circuit breaker\
-   Storm-resistant design\
-   Optimization-based routing

------------------------------------------------------------------------

Built for System Design & NLP Hackathon 🚀
