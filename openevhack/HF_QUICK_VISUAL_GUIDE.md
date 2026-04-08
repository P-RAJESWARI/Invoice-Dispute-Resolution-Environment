# 📖 HuggingFace Spaces Deployment - Visual Quick Guide

## 🎯 6 Simple Steps to Deploy

---

## STEP 1️⃣: Push Code to GitHub

### What to do:
```bash
cd /Users/raj-23437/Downloads/invoice-dispute-main/openevhack
git init
git add .
git commit -m "Ready for HF Spaces"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/invoice-dispute-env.git
git push -u origin main
```

### What you'll see:
✅ Code uploaded to GitHub
✅ Your repo at: `github.com/YOUR_USERNAME/invoice-dispute-env`

### Time: ⏱️ 5 minutes

---

## STEP 2️⃣: Create HuggingFace Space

### What to do:
1. Go to: https://huggingface.co/spaces
2. Click **"Create new Space"** (blue button)
3. Fill form:
   - **Space name**: `invoice-dispute-env`
   - **License**: MIT
   - **Visibility**: Public
   - **Space SDK**: **DOCKER** ← IMPORTANT!
4. Click **"Create Space"**

### What you'll see:
✅ New Space created
✅ Empty Docker environment
✅ Settings page opens

### Time: ⏱️ 2 minutes

---

## STEP 3️⃣: Link GitHub Repository

### What to do:
1. In Space → Click **"Settings"** (gear icon)
2. Scroll to **"Repository"** section
3. Enter GitHub URL:
   ```
   https://github.com/YOUR_USERNAME/invoice-dispute-env
   ```
4. Click **"Save"**

### What you'll see:
✅ "Building Docker image..."
✅ In **"Logs"** tab: build progress
✅ Takes 2-3 minutes

### Time: ⏱️ 1 minute

---

## STEP 4️⃣: Add Environment Secrets

### What to do:
In Space Settings → **"Repository secrets"** section

Add 3 secrets by clicking **"Add a secret"** for each:

**Secret 1:**
```
Name:  API_KEY
Value: hf_your_huggingface_token
```
Get token from: https://huggingface.co/settings/tokens

**Secret 2:**
```
Name:  API_BASE_URL
Value: https://router.huggingface.co/v1
```

**Secret 3:**
```
Name:  MODEL_NAME
Value: Qwen/Qwen2.5-72B-Instruct
```

Click **"Save"** after each secret.

### What you'll see:
✅ 3 secrets added and hidden (for security)
✅ Listed in Repository secrets section

### Time: ⏱️ 2 minutes

---

## STEP 5️⃣: Wait for Build

### What to do:
1. Go to your Space page (click Space name)
2. Click **"Logs"** tab at top
3. Watch the Docker build process

### What you'll see:
```
Building Docker image...
Step 1/15 : FROM python:3.10
Step 2/15 : WORKDIR /app
...
Successfully built Docker image
Launching app...
App is running on port 7860
```

### What to expect:
- Build log shows progress
- Typically takes **2-3 minutes**
- When done, see "App is running on port 7860" ✅

### Time: ⏱️ 3-5 minutes

---

## STEP 6️⃣: Verify Deployment

### What to do:
1. **Visit your Space:**
   ```
   https://YOUR_USERNAME-invoice-dispute-env.hf.space
   ```

2. **Test Health Endpoint:**
   ```bash
   curl https://YOUR_USERNAME-invoice-dispute-env.hf.space/health
   ```
   
   You should see:
   ```json
   {"status":"ok","env":"invoice-dispute-env"}
   ```

3. **Visit Swagger UI:**
   ```
   https://YOUR_USERNAME-invoice-dispute-env.hf.space/docs
   ```
   
   You should see interactive API documentation

### What you'll see:
✅ Home page with welcome message
✅ Health check returns 200 OK
✅ Swagger UI shows all endpoints
✅ App is fully functional!

### Time: ⏱️ 2 minutes

---

## 🎉 Deployment Complete!

Your app is now **LIVE** on HuggingFace Spaces! 🚀

**Your Space URL:**
```
https://YOUR_USERNAME-invoice-dispute-env.hf.space
```

---

## 📋 Complete Checklist

- [x] **Step 1** - Code on GitHub ✅
- [x] **Step 2** - HF Space created ✅
- [x] **Step 3** - GitHub linked ✅
- [x] **Step 4** - Secrets added ✅
- [x] **Step 5** - Build complete ✅
- [x] **Step 6** - Verified working ✅

**Status: DEPLOYED AND LIVE!** ✅

---

## 🎯 What's Now Available

After deployment, these URLs work:

| Resource | URL |
|----------|-----|
| **Home Page** | `https://YOUR_SPACE/` |
| **Swagger UI** | `https://YOUR_SPACE/docs` |
| **Health Check** | `https://YOUR_SPACE/health` |
| **Reset Endpoint** | `https://YOUR_SPACE/reset` |
| **Step Endpoint** | `https://YOUR_SPACE/step` |
| **State Endpoint** | `https://YOUR_SPACE/state` |

---

## 📲 Share Your Space

Your Space is now **public**! Share the URL:

```
https://YOUR_USERNAME-invoice-dispute-env.hf.space
```

With:
- 👨‍⚖️ Judges
- 👥 Team members
- 🌍 Anyone interested
- 📋 OpenEnv Hub (for community access)

---

## 🔄 Update Your App

If you make changes locally:

```bash
git add .
git commit -m "Updated feature"
git push origin main
```

HuggingFace automatically:
- Detects the push
- Rebuilds Docker image
- Redeploys your Space
- No manual steps needed!

---

## ⚠️ If Something Goes Wrong

### Build Failed?
- Click **"Logs"** tab
- Read the error message
- Common fixes:
  - Add missing dependencies to `requirements.txt`
  - Fix Python syntax errors
  - Check Docker format

### App Not Running?
- Wait another minute (sometimes slow)
- Restart Space: Settings → **"Restart"**
- Check logs for errors

### Environment Variables Not Working?
- Verify secrets were added correctly
- Restart Space after adding secrets
- Check that your code reads `os.getenv("API_KEY")` etc.

---

## 🎓 Example: Testing Your Deployed App

### Test 1: Simple Request
```bash
curl https://YOUR_SPACE/health
```

### Test 2: Reset Episode
```bash
curl -X POST https://YOUR_SPACE/reset \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"easy"}'
```

### Test 3: Use Swagger UI
```
https://YOUR_SPACE/docs
```

Click any endpoint → "Try it out" → Click "Execute"

---

## 📊 Your Deployment Summary

```
Name:           invoice-dispute-env
Type:           Docker
Runtime:        HuggingFace Spaces
URL:            https://YOUR_USERNAME-invoice-dispute-env.hf.space
Status:         Active ✅
Visibility:     Public
Uptime:         24/7
Cost:           FREE! 💰
```

---

## ✨ Next Steps

1. **Share your Space URL** with judges
2. **Monitor logs** occasionally (Settings → Logs)
3. **Make updates** as needed (push to GitHub)
4. **Test baseline** if desired:
   ```bash
   python inference.py --api-url https://YOUR_SPACE
   ```
5. **Submit to OpenEnv Hub** (optional):
   - Visit: https://hub.openenvhub.org
   - Submit your Space URL
   - Community can use your environment!

---

## 🏆 You're Done!

Your Invoice Dispute Resolution Environment is:
- ✅ Deployed on HuggingFace Spaces
- ✅ Live and accessible 24/7
- ✅ Running your baseline agent
- ✅ Ready for judges to evaluate
- ✅ Perfect for the hackathon!

**Congratulations!** 🎉

---

## 📚 Need More Help?

- **Complete detailed guide**: `HF_DEPLOYMENT_STEPS.md`
- **Troubleshooting**: See "If Something Goes Wrong" section above
- **General questions**: `README.md`
- **Environment setup**: `ENVIRONMENT_VARIABLES.md`

---

## 🚀 You're Ready to Go!

Your app is live. Share the URL. Good luck with the hackathon! 🏆
