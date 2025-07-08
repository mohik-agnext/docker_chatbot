# 🚀 Render Deployment Guide for Chandigarh Policy Assistant

## Quick Deploy Steps

### 1. Prerequisites
- [Render account](https://render.com) (free tier available)
- API keys for: Pinecone, Jina AI, and Groq
- GitHub repository with the project

### 2. Deploy on Render

1. **Connect Repository**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `https://github.com/mohik-agnext/docker_chatbot`

2. **Configure Service**
   ```
   Name: chandigarh-policy-assistant
   Environment: Docker
   Dockerfile Path: ./Dockerfile (default)
   Instance Type: Starter (free) or Professional
   ```

3. **Set Environment Variables**
   In Render dashboard → Environment tab, add:
   ```
   PINECONE_API_KEY=your_pinecone_key
   JINA_API_KEY=your_jina_key  
   GROQ_API_KEY=your_groq_key
   PINECONE_INDEX=cursor2
   PORT=10000
   FLASK_ENV=production
   USE_JINA_API=true
   JINA_MODEL=jina-embeddings-v3
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build and deployment (5-10 minutes)

### 3. Health Check
Once deployed, visit:
- Main app: `https://your-app-name.onrender.com`
- Health check: `https://your-app-name.onrender.com/ready`
- API: `https://your-app-name.onrender.com/api/search`

## 🔧 Configuration Details

### Port Configuration
- **Render**: Uses port `10000` (configured in Dockerfile)
- **Health Check Path**: `/ready`
- **Auto-Deploy**: Enabled for main branch

### API Keys Required
| Service | Purpose | Get Key From |
|---------|---------|--------------|
| Pinecone | Vector database | [pinecone.io](https://pinecone.io) |
| Jina AI | Embeddings API | [jina.ai](https://jina.ai) |
| Groq | LLM inference | [groq.com](https://groq.com) |

### Performance Settings
- **Workers**: 2 (optimized for Render free tier)
- **Timeout**: 120s
- **Memory**: ~1GB usage
- **Startup Time**: 2-3 minutes

## 🐛 Troubleshooting

### Common Issues

1. **Build Fails**
   ```bash
   # Check Dockerfile syntax
   docker build -t test .
   ```

2. **Environment Variables Missing**
   ```bash
   # Use env checker
   python render_env_check.py
   ```

3. **API Connection Issues**
   - Verify API keys in Render dashboard
   - Check service logs in Render dashboard
   - Test individual APIs outside the app

4. **Memory Issues**
   - Upgrade to Professional plan ($7/month)
   - Reduce worker count to 1

### Logs Access
- Render Dashboard → Your Service → Logs
- Real-time deployment and runtime logs

## 🚀 Performance Optimization

### For Free Tier
- Uses 1GB RAM limit efficiently
- Sub-5 second response times
- Handles ~20 concurrent users

### For Professional Tier  
- Can handle 100+ concurrent users
- Sub-2 second response times
- Better reliability

## 📞 Support

### Testing Deployment
1. Visit the deployed URL
2. Try asking: "What are the EV incentives in Chandigarh?"
3. Check response time and accuracy

### API Testing
```bash
curl -X POST https://your-app.onrender.com/api/search \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the license fee for microbrewery?"}'
```

### Environment Check
```bash
# SSH into Render shell (if available) or check logs
python render_env_check.py
```

---

**🎯 Expected Result**: Your Chandigarh Policy Assistant should be live and responding to policy questions within 5-10 minutes of deployment!

**📚 Documentation**: For more details, see `PROJECT_DOCUMENTATION.md` 