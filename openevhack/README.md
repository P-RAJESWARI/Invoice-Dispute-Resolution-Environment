---
title: Invoice Dispute Resolution
emoji: 💼
colorFrom: blue
colorTo: purple
sdk: docker
app_file: server/app.py
python_version: "3.10"
pinned: false
---

# Invoice Dispute Resolution Environment

An AI-powered system for resolving billing disputes using reinforcement learning. The environment supports 3 difficulty levels and evaluates agent performance on correctness, efficiency, and policy compliance.

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

## 🚀 Quick Start

### Local Development

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r server/requirements.txt

# Start FastAPI server
python -m uvicorn server.app:app --reload --port 7860
```

The API will be available at `http://localhost:7860`

### Interactive API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:7860/docs
- **ReDoc**: http://localhost:7860/redoc

## 🔑 Environment Variables (OpenAI-Compatible)

The baseline agent uses the **OpenAI Python client library**, which works with ANY provider:

### For Judges/Evaluation
Judges will inject these during evaluation:
```bash
API_KEY=<provided-by-judges>           # API key for LLM provider
API_BASE_URL=<provided-by-judges>      # Base URL for LLM provider
MODEL_NAME=<provided-by-judges>        # Model name to use
```

### For Local Development (Free Options)

**Option 1: HuggingFace (Free)**
```bash
export API_KEY="hf_..."  # Your HuggingFace token (free)
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
```

**Option 2: OpenAI (Paid)**
```bash
export API_KEY="sk-..."  # Your OpenAI API key
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-3.5-turbo"
```

**Option 3: Legacy Support**
```bash
export OPENAI_API_KEY="sk-..."  # For backward compatibility
```

Then run baseline:
```bash
python inference.py
```

## 📚 API Endpoints

### 1. Health Check
```bash
GET /health
```
**Response:**
```json
{
  "status": "ok",
  "env": "invoice-dispute-env"
}
```

### 2. Reset Episode
```bash
POST /reset
Content-Type: application/json

{
  "difficulty": "easy"  // or "medium", "hard"
}
```

**Response:** `DisputeObservation` object

### 3. Submit Decision
```bash
POST /step
Content-Type: application/json

{
  "decision": "approve_full",
  "response_text": "Your refund has been approved.",
  "refund_amount": null
}
```

**Decision options:**
- `full_refund` - Approve 100% refund
- `partial_refund` - Approve partial refund (requires `refund_amount`)
- `reject` - Deny dispute
- `escalate` - Escalate to human
- `request_info` - Request more information

### 4. Get Current State
```bash
GET /state
```

**Response:** `DisputeState` object with:
- Invoice details
- Customer information
- Dispute details
- Company policy
- Customer history

## 🎯 Difficulty Levels

| Level | Description | Features |
|-------|-------------|----------|
| **Easy** | Clear-cut disputes | Obvious correct answer, 80%+ baseline reward |
| **Medium** | Ambiguous cases | Requires careful analysis, 50%+ baseline reward |
| **Hard** | Complex scenarios | Multiple perspectives, 30%+ baseline reward |

## 🏗️ Project Structure

```
.
├── server/
│   ├── app.py              # FastAPI application
│   ├── environment.py      # Dispute environment logic
│   ├── models.py           # Pydantic models
│   ├── __init__.py
│   └── requirements.txt    # Python dependencies
├── inference.py            # Baseline evaluation script
├── models.py               # Shared models
├── openenv.yaml            # OpenEnv configuration
├── Dockerfile              # Docker configuration
├── README.md               # This file
└── pyproject.toml
```

## 🐳 Docker Deployment

### Build locally
```bash
docker build -t invoice-dispute:latest .
```

### Run locally
```bash
docker run -p 7860:7860 invoice-dispute:latest
```

### Deploy to Hugging Face Spaces
1. Push to GitHub
2. Create Space: https://huggingface.co/new-space
3. Select **Docker** runtime
4. Connect your GitHub repository
5. Add secrets:
   - `HF_TOKEN` (optional)
   - `OPENAI_API_KEY` (if using GPT)
6. Deploy!

## 📊 Running Baseline Evaluation

```bash
python inference.py
```

This evaluates the environment baseline on all 3 difficulty levels:
- Easy: Expected ~0.80 reward
- Medium: Expected ~0.50 reward
- Hard: Expected ~0.30 reward

## 🔧 Testing Endpoints

### Using curl

```bash
# Check health
curl http://localhost:7860/health

# Start episode (easy)
curl -X POST http://localhost:7860/reset \
  -H "Content-Type: application/json" \
  -d '{"difficulty": "easy"}'

# Get current state
curl http://localhost:7860/state

# Submit decision (full refund)
curl -X POST http://localhost:7860/step \
  -H "Content-Type: application/json" \
  -d '{
    "decision": "full_refund",
    "response_text": "Your refund has been approved.",
    "refund_amount": null
  }'
```

### Using Python

```python
import requests

API_URL = "http://localhost:7860"

# Reset
response = requests.post(f"{API_URL}/reset", json={"difficulty": "medium"})
print(response.json())

# Get state
response = requests.get(f"{API_URL}/state")
print(response.json())

# Step
response = requests.post(f"{API_URL}/step", json={
    "decision": "partial_refund",
    "response_text": "Partial refund approved due to service delay.",
    "refund_amount": 150.00
})
print(response.json())
```

## 🔐 Environment Variables

Optional configuration via `.env`:

```bash
HF_TOKEN=your_huggingface_token
OPENAI_API_KEY=your_openai_api_key
MODEL_NAME=meta-llama/Llama-2-7b-chat-hf
```

## 📈 Data Types

### DisputeObservation
Response from `/step` endpoint:
```python
{
    "reward": float,           # Reward for this decision (-1 to 1)
    "feedback": str,           # Explanation of reward
    "step_result": str,        # What happened
    "customer_reaction": str,  # How customer reacted
    "done": bool               # Is episode finished?
}
```

### DisputeState
Response from `/state` endpoint:
```python
{
    "invoice_id": str,
    "invoice_date": str,
    "invoice_amount": float,
    "dispute_type": str,
    "customer_message": str,
    "customer_tier": str,      # standard, premium, enterprise
    "line_items": list,
    "customer_history": dict,
    "policy": dict
}
```

### DisputeAction
Request to `/step` endpoint:
```python
{
    "decision": str,           # one of the 5 decision types
    "response_text": str,      # Your message to customer
    "refund_amount": float | null
}
```

## 🛠️ Development

### Creating virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r server/requirements.txt
```

### Running tests

```bash
python -m pytest
```

### Code structure

- `server/app.py` - FastAPI app with all endpoints
- `server/environment.py` - Core environment logic
- `server/models.py` - Pydantic data models
- `inference.py` - Example agent/baseline
- `models.py` - Shared type definitions

## 🎓 Example Agent

See `inference.py` for a baseline agent that:
1. Resets the environment
2. Gets the current state
3. Makes decisions based on simple rules
4. Tracks rewards

You can modify this to test your own strategies!

## 📝 API Response Examples

### Successful Reset
```json
{
  "invoice_id": "INV-2024-001",
  "invoice_amount": 1500.00,
  "customer_message": "I was charged twice for the same service...",
  "dispute_type": "billing_error",
  "reward": 0,
  "feedback": "Episode started",
  "step_result": "",
  "customer_reaction": null,
  "done": false
}
```

### Successful Step
```json
{
  "reward": 0.85,
  "feedback": "Great decision! Customer was clearly overcharged and you recognized it quickly.",
  "step_result": "Full refund of $1500.00 approved and processed.",
  "customer_reaction": "Very satisfied! Thank you for resolving this quickly.",
  "done": true
}
```

## 🚨 Error Handling

All endpoints return proper HTTP status codes:
- `200` - Success
- `400` - Bad request (invalid difficulty, missing fields, etc.)
- `500` - Server error

Error responses include a detail message:
```json
{
  "detail": "Difficulty must be: easy, medium, or hard"
}
```

## 📊 Performance

- **Average response time**: 100-500ms per request
- **Concurrent users**: Tested with 1 user (stateful)
- **Memory footprint**: ~500MB (Python + models)
- **Startup time**: ~5 seconds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

MIT

## 👥 Authors

OpenEV Hackathon Team

## 🔗 Links

- [Hugging Face Spaces](https://huggingface.co/spaces)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## 💬 Support

For issues and questions, please create an issue on GitHub or reach out to the team.

---

**Built with ❤️ for the OpenEV Hackathon**
