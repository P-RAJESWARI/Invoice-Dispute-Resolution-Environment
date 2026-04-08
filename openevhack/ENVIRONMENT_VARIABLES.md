# OpenAI-Compatible Baseline Agent Setup

## ✅ Key Feature: Works with ANY LLM Provider

Your baseline agent uses the **OpenAI Python client library**, which is **provider-agnostic**. This means:

- ✅ Works with OpenAI's GPT models
- ✅ Works with HuggingFace models (FREE during evaluation)
- ✅ Works with ANY OpenAI-compatible provider
- ✅ Judges can inject their own API credentials at evaluation time
- ✅ You don't need to pay for API access

## 🔑 Environment Variable Configuration

### During Evaluation (Judges Inject These)

Judges will provide:
```bash
API_KEY=<their-api-key>                    # Provider's API key
API_BASE_URL=<provider-base-url>           # Provider's API base URL
MODEL_NAME=<model-name>                    # Model to evaluate
```

Your code automatically uses these values.

### For Local Development (FREE Options)

#### Option 1: HuggingFace (Recommended - FREE)

1. Get a free token from https://huggingface.co/settings/tokens
2. Set environment variables:

```bash
export API_KEY="hf_your_token_here"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
```

3. Run baseline:
```bash
python inference.py
```

#### Option 2: OpenAI (PAID - Only if you have credits)

```bash
export API_KEY="sk_your_openai_key_here"
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-3.5-turbo"
python inference.py
```

#### Option 3: Legacy Compatibility

If you have old `OPENAI_API_KEY`:
```bash
export OPENAI_API_KEY="sk_..."
python inference.py
```

## 💡 How It Works

The `inference.py` script:

```python
from openai import OpenAI

# Reads from environment variables
api_key = os.getenv("API_KEY") or os.getenv("OPENAI_API_KEY")
api_base_url = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
model_name = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

# Creates OpenAI-compatible client
# Works with ANY provider that implements the API
client = OpenAI(
    api_key=api_key,
    base_url=api_base_url
)

# Uses provided model
response = client.chat.completions.create(
    model=model_name,
    messages=[...],
)
```

## 🧪 Testing Different Providers

### Test with HuggingFace
```bash
export API_KEY="hf_..."
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
python inference.py --episodes 1
```

### Test with OpenAI
```bash
export API_KEY="sk_..."
export API_BASE_URL="https://api.openai.com/v1"
export MODEL_NAME="gpt-3.5-turbo"
python inference.py --episodes 1
```

### Test with Custom Provider
```bash
export API_KEY="your_api_key"
export API_BASE_URL="https://your-provider.com/v1"
export MODEL_NAME="your-model-name"
python inference.py --episodes 1
```

## 📝 Available Models

### HuggingFace (FREE - via router.huggingface.co)
```
Qwen/Qwen2.5-72B-Instruct
meta-llama/Llama-2-7b-chat-hf
mistralai/Mistral-7B-Instruct-v0.2
NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO
```

### OpenAI (PAID)
```
gpt-3.5-turbo
gpt-4
gpt-4-turbo
```

## 🚀 Deployment to HuggingFace Spaces

The environment automatically uses environment variables injected by HF Spaces:

1. Create `.env` file in Space settings with:
   ```
   API_KEY=hf_your_token
   API_BASE_URL=https://router.huggingface.co/v1
   MODEL_NAME=Qwen/Qwen2.5-72B-Instruct
   ```

2. Or use HF Space secrets (recommended):
   ```
   API_KEY = hf_...
   API_BASE_URL = https://router.huggingface.co/v1
   MODEL_NAME = Qwen/Qwen2.5-72B-Instruct
   ```

3. Space auto-uses these when running inference

## ✨ Why This Approach Works

**For You (Hackathon Developer)**:
- ✅ No need to buy API credits
- ✅ Use free HuggingFace models locally
- ✅ Code works with any provider
- ✅ Easy to test different models
- ✅ Portable across environments

**For Judges (Evaluation)**:
- ✅ Can inject their own API credentials
- ✅ Can use their preferred LLM provider
- ✅ Can evaluate with models they trust
- ✅ No vendor lock-in
- ✅ Reproducible evaluation

## 🔄 Fallback Behavior

If environment variables are not set:
```bash
python inference.py
```

Output:
```
⚠️  API_KEY or OPENAI_API_KEY environment variable not set

For local development, use free options:
  1. HuggingFace: export API_KEY='hf_...'
     export API_BASE_URL='https://router.huggingface.co/v1'
     export MODEL_NAME='Qwen/Qwen2.5-72B-Instruct'

  2. OpenAI: export API_KEY='sk-...'
     export API_BASE_URL='https://api.openai.com/v1'

During evaluation, judges will inject API_KEY and API_BASE_URL
Continuing with available configuration...
```

## 📚 Documentation

- **`.env.example`**: All available environment variables
- **`inference.py`**: Baseline agent implementation
- **`README.md`**: Quick start guide
- **`server/app.py`**: Environment implementation

## 🎯 Quick Checklist

Before submission:
- [ ] `inference.py` reads from environment variables ✅
- [ ] Works with OpenAI-compatible APIs ✅
- [ ] Can be configured via `.env` file ✅
- [ ] Gracefully handles missing credentials ✅
- [ ] Documented in README and .env.example ✅
- [ ] No hardcoded API keys ✅
- [ ] Works with judges' injected credentials ✅

## ✅ Status

Your environment is configured to:
- ✅ Work with ANY OpenAI-compatible LLM provider
- ✅ Allow judges to inject their own credentials
- ✅ Use free models during development
- ✅ Be flexible and portable
- ✅ Pass evaluation with any provider judges choose

**Ready for hackathon submission!** 🚀
