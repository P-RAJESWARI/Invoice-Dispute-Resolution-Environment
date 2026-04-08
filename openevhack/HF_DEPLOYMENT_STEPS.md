# 🚀 HuggingFace Spaces Deployment - Complete Step-by-Step Guide

## ⏱️ Time Required: ~15 minutes total

---

## 📋 Pre-Deployment Checklist

Before starting, verify you have:

- [x] GitHub account (create at https://github.com if needed)
- [x] HuggingFace account (create at https://huggingface.co if needed)
- [x] Your code ready (already done ✅)
- [x] Git installed locally (check: `git --version`)
- [x] Internet connection

---

## 🎯 Complete Deployment Steps

### STEP 1: Prepare Your GitHub Repository (5 minutes)

#### 1.1 Initialize Git Repository
```bash
cd /Users/raj-23437/Downloads/invoice-dispute-main/openevhack

# Initialize git (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Invoice Dispute Resolution Environment - Ready for HF Spaces"

# Verify files are staged
git status
```

Expected output:
```
On branch master
nothing to commit, working tree clean
```

#### 1.2 Create GitHub Repository

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `invoice-dispute-env`
   - **Description**: "OpenEnv Invoice Dispute Resolution Environment"
   - **Visibility**: Public
   - **Add .gitignore**: No (already have one)
   - **Add license**: MIT (optional)
3. Click **"Create repository"**

#### 1.3 Connect to GitHub and Push

Copy the commands from GitHub (they'll look like this):

```bash
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/invoice-dispute-env.git
git push -u origin main
```

**Replace YOUR_USERNAME with your GitHub username**

Then run:
```bash
git push -u origin main
```

You should see:
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR_USERNAME/invoice-dispute-env.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

✅ **Step 1 Complete: Code is on GitHub**

---

### STEP 2: Create HuggingFace Space (2 minutes)

#### 2.1 Go to HuggingFace Spaces

1. Visit https://huggingface.co/spaces
2. Click **"Create new Space"** button (top right)

#### 2.2 Fill in Space Details

You'll see a form. Fill it in:

| Field | Value |
|-------|-------|
| **Space name** | `invoice-dispute-env` |
| **License** | MIT (or your choice) |
| **Visibility** | Public |
| **Space SDK** | **Docker** ← IMPORTANT! |

**Important**: Make sure you select **Docker** (not Gradio or Streamlit)

#### 2.3 Create the Space

Click **"Create Space"**

HF will create an empty Docker space and show you the page.

✅ **Step 2 Complete: HF Space is created**

---

### STEP 3: Connect GitHub Repository (1 minute)

After creating the Space, you'll be on the Space page.

#### 3.1 Click Settings

In the top menu, click **"Settings"** (gear icon)

#### 3.2 Configure Space

Scroll down to **"Repository"** section:

1. Select: **"Link to Git repository"** (if not already selected)
2. Enter your GitHub repo URL:
   ```
   https://github.com/YOUR_USERNAME/invoice-dispute-env
   ```
3. Click **"Save"**

HF will:
- Connect to your GitHub repo
- Auto-detect the Dockerfile
- Start building the Docker image

Monitor the "Logs" tab to watch the build progress.

✅ **Step 3 Complete: GitHub linked to HF Space**

---

### STEP 4: Add Environment Secrets (2 minutes)

Your app needs environment variables for the LLM API.

#### 4.1 Go to Secrets

In Space settings, scroll to **"Repository secrets"**

#### 4.2 Add Three Secrets

Click **"Add a secret"** for each:

**Secret 1: API_KEY**
- Name: `API_KEY`
- Value: `hf_your_huggingface_token_here`
  
  (Get your free HuggingFace token from https://huggingface.co/settings/tokens)

**Secret 2: API_BASE_URL**
- Name: `API_BASE_URL`
- Value: `https://router.huggingface.co/v1`

**Secret 3: MODEL_NAME**
- Name: `MODEL_NAME`
- Value: `Qwen/Qwen2.5-72B-Instruct`

After each, click **"Save"**

#### 4.3 Verify Secrets

You should see:
```
✓ API_KEY (hidden)
✓ API_BASE_URL (hidden)
✓ MODEL_NAME (hidden)
```

✅ **Step 4 Complete: Secrets configured**

---

### STEP 5: Wait for Deployment (3-5 minutes)

#### 5.1 Monitor Build Progress

1. Go back to your Space page (click the Space name)
2. Click **"Logs"** tab to watch the build

You'll see:
```
Building Docker image...
Step 1/XX : FROM python:3.10
Step 2/XX : WORKDIR /app
...
Successfully built Docker image
Launching app...
```

#### 5.2 Deployment Complete

When you see:
```
App is running on port 7860
```

Your app is LIVE! 🎉

The build typically takes **2-3 minutes**.

✅ **Step 5 Complete: App deployed!**

---

### STEP 6: Verify Deployment (2 minutes)

#### 6.1 Get Your Space URL

On the Space page, you'll see the public URL at the top:
```
https://YOUR_USERNAME-invoice-dispute-env.hf.space
```

#### 6.2 Test Home Page

Visit your Space URL in browser:
```
https://YOUR_USERNAME-invoice-dispute-env.hf.space/
```

You should see:
- ✅ Welcome message
- ✅ Links to documentation
- ✅ Status showing "Backend is running"

#### 6.3 Test Health Check

```bash
curl https://YOUR_USERNAME-invoice-dispute-env.hf.space/health
```

Expected response:
```json
{"status":"ok","env":"invoice-dispute-env"}
```

#### 6.4 Test API Documentation

Visit:
```
https://YOUR_USERNAME-invoice-dispute-env.hf.space/docs
```

You should see Swagger UI with all endpoints.

✅ **Step 6 Complete: Deployment verified!**

---

## 🎉 Deployment Complete!

Your app is now live and accessible to everyone!

---

## 📊 What's Deployed

| Component | Location |
|-----------|----------|
| **Home Page** | `https://YOUR_SPACE/` |
| **API Docs** | `https://YOUR_SPACE/docs` |
| **Health Check** | `https://YOUR_SPACE/health` |
| **Reset Endpoint** | `https://YOUR_SPACE/reset` |
| **Step Endpoint** | `https://YOUR_SPACE/step` |
| **State Endpoint** | `https://YOUR_SPACE/state` |

---

## 🧪 Test Your Deployed App

### Test 1: Health Check
```bash
curl https://YOUR_SPACE/health
```

### Test 2: Reset Episode
```bash
curl -X POST https://YOUR_SPACE/reset \
  -H "Content-Type: application/json" \
  -d '{"difficulty":"easy"}'
```

### Test 3: Visit Swagger UI
```
https://YOUR_SPACE/docs
```

Click "Try it out" on any endpoint to test interactively.

---

## 🔄 Making Updates

If you need to update your code:

### Update Locally
```bash
cd /Users/raj-23437/Downloads/invoice-dispute-main/openevhack

# Make your changes

git add .
git commit -m "Update description"
git push origin main
```

### HF Auto-Redeploys
HF will automatically detect the push and rebuild your Space!

Monitor progress in the Logs tab.

---

## ⚠️ Troubleshooting

### Issue: Build Fails
**Solution**: Check the Logs tab for errors. Common issues:
- Missing dependencies - add to `requirements.txt`
- Syntax errors in code - fix and repush
- Large file size - remove unnecessary files

### Issue: App Times Out
**Solution**: The build might be slow. Wait 5 minutes before refreshing.

### Issue: 404 Not Found
**Solution**: Wait a few more minutes for deployment to complete.

### Issue: Environment Variables Not Working
**Solution**: 
- Verify secrets were added correctly
- Restart the Space (Settings → Restart space)
- Check logs for errors

---

## 📞 Quick Reference URLs

| Purpose | URL |
|---------|-----|
| Your Space | `https://YOUR_USERNAME-invoice-dispute-env.hf.space` |
| GitHub Repo | `https://github.com/YOUR_USERNAME/invoice-dispute-env` |
| HF Account | `https://huggingface.co/YOUR_USERNAME` |
| API Docs | `https://YOUR_USERNAME-invoice-dispute-env.hf.space/docs` |

---

## 🎯 Next Steps After Deployment

1. **Share Your Space**
   - Copy the URL
   - Share with friends, judges, or team
   - It's public and accessible!

2. **Run Baseline Evaluation**
   ```bash
   # Locally (if you have API key set)
   python inference.py --api-url https://YOUR_SPACE
   ```

3. **Submit to OpenEnv Hub (Optional)**
   - Visit https://hub.openenvhub.org
   - Submit your HF Space URL
   - Community can use your environment!

4. **Monitor & Update**
   - Check Space Logs occasionally
   - Update code as needed
   - HF redeploys automatically

---

## ✅ Final Checklist

- [x] Code pushed to GitHub
- [x] HF Space created
- [x] GitHub linked to Space
- [x] Environment secrets added
- [x] Build complete
- [x] App is running
- [x] Endpoints tested
- [x] API docs accessible
- [x] Space shared with URL
- [x] Ready for submission!

---

## 🎉 Congratulations!

Your Invoice Dispute Resolution Environment is now **live on HuggingFace Spaces**!

**Your Space URL:**
```
https://YOUR_USERNAME-invoice-dispute-env.hf.space
```

Share this link with:
- Judges
- Team members
- OpenEnv Hub
- Anyone interested!

---

## 📚 Need Help?

Refer to these guides:
- **Setup Issues?** → `ENVIRONMENT_VARIABLES.md`
- **API Questions?** → `README.md`
- **More Details?** → `HF_SPACES_COMPATIBILITY.md`
- **Structure Questions?** → `HF_STRUCTURE_VERIFIED.md`

---

## 🚀 You're All Set!

Your environment is deployed, tested, and ready for the OpenEV Hackathon!

Good luck! 🏆
