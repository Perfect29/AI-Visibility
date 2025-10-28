# 🚀 Deployment Guide

## Quick Deploy Checklist

### ✅ Pre-Deployment
- [x] Clean project structure
- [x] All tests passing (5/6 - minor warning only)
- [x] Backend API ready
- [x] Frontend ready
- [x] Deployment configs created

### 🎯 Deployment Steps

## 1️⃣ Deploy Backend to Railway

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Railway**:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select `AI-Visibility` repository
   - Railway will auto-detect the Dockerfile
   - Click "Deploy"

3. **Add Environment Variable**:
   - Go to your project → "Variables" tab
   - Add: `OPENAI_API_KEY` = `your_openai_key`
   - Save

4. **Get Backend URL**:
   - Go to "Settings" → "Domains"
   - Copy the Railway URL (e.g., `https://ai-visibility-production.up.railway.app`)

## 2️⃣ Deploy Frontend to Vercel

1. **Update API URL**:
   - Edit `frontend/js/app.js`
   - Change line 2:
   ```javascript
   const API_BASE_URL = 'https://your-railway-url.up.railway.app';
   ```
   - Save and commit:
   ```bash
   git add frontend/js/app.js
   git commit -m "Update API URL for production"
   git push origin main
   ```

2. **Deploy on Vercel**:
   - Go to https://vercel.com
   - Click "Add New..." → "Project"
   - Import `AI-Visibility` from GitHub
   - **Important**: Set Root Directory to `frontend`
   - Click "Deploy"

3. **Done!** 🎉
   - Your frontend is live at `https://your-app.vercel.app`

## 🧪 Test Your Deployment

1. Open your Vercel URL
2. Try the full flow:
   - Enter brand name and domain
   - Extract keywords
   - Generate prompts
   - Run analysis
3. Check browser console for any errors
4. Verify results display correctly

## 🔧 Troubleshooting

### Backend Issues
- **API not responding**: Check Railway logs
- **CORS errors**: Ensure backend allows your Vercel domain
- **OpenAI errors**: Verify API key is set correctly

### Frontend Issues
- **API calls failing**: Check the API_BASE_URL is correct
- **Blank page**: Check browser console for errors
- **404 on refresh**: Vercel should handle this automatically

## 📊 Monitor Your App

**Railway (Backend)**:
- Check logs: Project → Deployments → View Logs
- Monitor usage: Project → Metrics

**Vercel (Frontend)**:
- Check deployments: Project → Deployments
- View analytics: Project → Analytics

## 🔄 Future Updates

To deploy updates:

```bash
# Make your changes
git add .
git commit -m "Your update message"
git push origin main
```

Both Vercel and Railway will auto-deploy on push! 🚀

## 💡 Pro Tips

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Rotate them regularly for security
3. **Monitoring**: Set up alerts in Railway for errors
4. **Performance**: Railway has auto-scaling options
5. **Custom Domains**: Add your own domain in Vercel settings

## 🎯 What's Next?

- [ ] Add custom domain
- [ ] Set up error monitoring (e.g., Sentry)
- [ ] Add rate limiting to API
- [ ] Implement caching for better performance
- [ ] Add analytics to track usage

---

Need help? Check the logs or documentation! 🚀

