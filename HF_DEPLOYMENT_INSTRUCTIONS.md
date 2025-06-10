# 🚀 HuggingFace Spaces Deployment Instructions

## ✅ **FILES READY FOR DEPLOYMENT**

Your Chandigarh Policy Assistant has been optimized for HuggingFace Spaces deployment with:
- ❌ **Gradio removed** - Pure Flask/Docker deployment
- ✅ **HuggingFace Spaces compatible** - Port 7860, Docker SDK
- ✅ **All functionality intact** - Sub-5s responses, professional UI

## 🔑 **Step 1: Get HuggingFace Access Token**

1. Go to [HuggingFace Settings > Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give it a name like "botbot-deployment"
4. Select **Write** permissions
5. Copy the token (starts with `hf_...`)

## 📤 **Step 2: Push to HuggingFace Spaces**

Run these commands in your terminal:

```bash
# Configure git with your HF username and token
git config user.name "mohikAgnext"
git config user.email "your-email@example.com"

# Set up authentication (replace YOUR_TOKEN with your actual token)
git remote set-url origin https://mohikAgnext:YOUR_TOKEN@huggingface.co/spaces/mohikAgnext/botbot

# Push the changes
git push
```

**Alternative method using git credentials:**
```bash
# When prompted for password, use your HuggingFace access token (not your password)
git push
```

## ⚙️ **Step 3: Configure Environment Variables**

After pushing, you need to set up environment variables in HuggingFace Spaces:

1. Go to your Space: https://huggingface.co/spaces/mohikAgnext/botbot
2. Click on **Settings** tab
3. Scroll down to **Repository secrets**
4. Add these secrets:

| Variable Name | Value | Description |
|---------------|-------|-------------|
| `PINECONE_API_KEY` | Your Pinecone API key | Required for vector database |
| `GROQ_API_KEY` | Your Groq API key | Required for LLM responses |
| `PINECONE_INDEX` | Your Pinecone index name | Your vector database index |
| `PINECONE_HOST` | Your Pinecone host URL | Pinecone connection endpoint |

## 🏗️ **Step 4: Wait for Build**

HuggingFace Spaces will automatically:
1. Detect the Docker configuration from `README.md` metadata
2. Build the Docker container with your Flask app
3. Deploy on port 7860
4. Show build logs in real-time

## ✅ **Step 5: Verify Deployment**

Once deployed, your app will be available at:
- **Main Interface**: https://mohikagnext-botbot.hf.space
- **Health Check**: https://mohikagnext-botbot.hf.space/api/health
- **Performance Stats**: https://mohikagnext-botbot.hf.space/api/stats

## 🔧 **Configuration Details**

Your `README.md` already includes the correct HuggingFace metadata:

```yaml
---
title: Chandigarh Policy Assistant
emoji: 🏛️
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860  # HuggingFace Spaces requirement
pinned: false
license: mit
---
```

## 🐳 **Docker Configuration**

Your `Dockerfile` is configured for HuggingFace Spaces with:
- User ID 1000 (HF requirement)
- Port 7860 (HF requirement)
- All dependencies included
- Production environment

## 🚀 **Expected Performance**

Once deployed on HuggingFace Spaces:
- **Startup Time**: 30-60 seconds (Docker build + model loading)
- **Response Time**: 2-5 seconds per query
- **Interface**: Professional Flask web app with HTML/CSS/JS
- **API Endpoints**: Full REST API available

## 🛠️ **Troubleshooting**

**If build fails:**
1. Check build logs in HuggingFace Spaces
2. Verify environment variables are set
3. Ensure API keys are valid

**If app doesn't respond:**
1. Check the health endpoint: `/api/health`
2. Verify environment variables in Spaces settings
3. Check application logs

## 📋 **Quick Commands Summary**

```bash
# Set up authentication
git remote set-url origin https://mohikAgnext:YOUR_TOKEN@huggingface.co/spaces/mohikAgnext/botbot

# Push to deploy
git push

# Check status
curl https://mohikagnext-botbot.hf.space/api/health
```

## 🎉 **You're All Set!**

Your Docker-optimized Chandigarh Policy Assistant is ready for HuggingFace Spaces deployment. Just follow the authentication steps above and push to deploy! 