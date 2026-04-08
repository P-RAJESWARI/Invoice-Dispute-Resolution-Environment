"""
Invoice Dispute Resolution Environment — FastAPI Server
Exposes the environment via HTTP endpoints compatible with OpenEnv.
"""
from typing import Optional
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from models import DisputeAction, DisputeObservation, DisputeState
from server.environment import InvoiceDisputeEnv

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Invoice Dispute Resolution Environment",
    description=(
        "An OpenEnv-compatible RL environment where an AI agent learns to resolve "
        "billing disputes correctly, efficiently, and in compliance with company policy. "
        "Supports 3 difficulty levels: easy, medium, hard."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global environment instance (starts with medium difficulty)
env = InvoiceDisputeEnv(difficulty="medium")


class ResetRequest(BaseModel):
    """Request body for reset endpoint with optional difficulty."""
    difficulty: str = "medium"


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Invoice Dispute Resolution Environment</title>
            <style>
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto;
                    max-width: 800px;
                    margin: 50px auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    padding: 40px;
                    border-radius: 12px;
                    backdrop-filter: blur(10px);
                }
                h1 { margin-top: 0; }
                a { color: #fff; text-decoration: none; font-weight: bold; }
                a:hover { text-decoration: underline; }
                .button {
                    display: inline-block;
                    padding: 10px 20px;
                    background: white;
                    color: #667eea;
                    border-radius: 6px;
                    margin: 10px 10px 10px 0;
                    font-weight: bold;
                    cursor: pointer;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Invoice Dispute Resolution Environment</h1>
                <p>An AI-powered system for resolving billing disputes using reinforcement learning.</p>
                
                <h2>📚 API Documentation</h2>
                <a href="/docs" class="button">📖 Swagger UI</a>
                <a href="/redoc" class="button">📋 ReDoc</a>
                
                <h2>🏥 Status</h2>
                <p>✅ Backend is running on port 7860</p>
                
                <h2>🎯 Quick Start</h2>
                <ul>
                    <li>Visit <a href="/docs">/docs</a> to test APIs interactively</li>
                    <li>Or use: <code>curl http://localhost:7860/health</code></li>
                </ul>
            </div>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok", "env": "invoice-dispute-env"}


@app.post("/reset", response_model=DisputeObservation)
def reset(request: Optional[ResetRequest] = None):
    """
    Start a new dispute episode.
    Defaults to 'easy' if no difficulty provided.
    """

    difficulty = "easy"  # default

    if request and request.difficulty:
        if request.difficulty not in ["easy", "medium", "hard"]:
            raise HTTPException(
                status_code=400,
                detail="Difficulty must be: easy, medium, or hard"
            )
        difficulty = request.difficulty

    global env
    env = InvoiceDisputeEnv(difficulty=difficulty)
    obs = env.reset()

    return obs


@app.post("/step", response_model=DisputeObservation)
def step(action: DisputeAction):
    """
    Submit the agent's resolution decision.
    Returns reward, feedback, done flag, and customer reaction.
    """
    try:
        obs = env.step(action)
        return obs
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/state", response_model=DisputeState)
def get_state():
    """
    Return the full current state of the environment.
    Includes invoice, dispute details, customer history, and company policy.
    """
    try:
        return env.state
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))


# ── Entry point ────────────────────────────────────────────────────────────────
def create_app() -> FastAPI:
    return app

import uvicorn

def main():
    uvicorn.run("server.app:app",host="0.0.0.0",port=7860)
    
if __name__ == "__main__":
    main()
