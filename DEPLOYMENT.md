# Deploying Job Application Co-Pilot to Render

## Prerequisites
- A [Render account](https://render.com) (free)
- Your Groq API key (get it from [console.groq.com](https://console.groq.com))
- Git installed and project pushed to GitHub/GitLab/Bitbucket

## Step 1: Push Your Code to Git

If you haven't already:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## Step 2: Deploy on Render

### Option A: Using render.yaml (Recommended)

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub/GitLab/Bitbucket repository
4. Render will detect the `render.yaml` file automatically
5. Click **"Apply"**
6. Set your environment variables:
   - **DATABASE_URL**: Leave as default `sqlite:///./job_copilot.db` or use PostgreSQL (see below)
   - **GROQ_API_KEY**: Your Groq API key from console.groq.com
   - **SECRET_KEY**: Will be auto-generated (or set your own)

### Option B: Manual Setup

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Web Service"**
3. Connect your repository
4. Configure:
   - **Name**: `job-copilot` (or any name you prefer)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: `Free`

5. Add environment variables (click "Advanced"):
   - `DATABASE_URL` = `sqlite:///./job_copilot.db`
   - `SECRET_KEY` = (generate a random string)
   - `GROQ_API_KEY` = (your API key)
   - `GROQ_MODEL` = `llama-3.1-8b-instant`
   - `GROQ_MAX_TOKENS` = `800`
   - `GROQ_MAX_RETRIES` = `2`

6. Click **"Create Web Service"**

## Step 3: Wait for Deployment

Render will:
- Install dependencies from `requirements.txt`
- Start your FastAPI app
- Give you a URL like `https://job-copilot-xxxx.onrender.com`

⏱️ First deployment takes 5-10 minutes.

## Step 4: Test Your App

Once deployed, visit:
- **Frontend UI**: `https://your-app.onrender.com/`
- **API Docs**: `https://your-app.onrender.com/docs`

## Important Notes

### Database Considerations

**SQLite (Default - Ephemeral Storage)**
- ⚠️ Render's free tier uses ephemeral storage
- Your database will be **wiped** when the service restarts
- Good for testing, **not for production**

**PostgreSQL (Recommended for Production)**

1. Create a free PostgreSQL database on Render:
   - Click **"New +"** → **"PostgreSQL"**
   - Name it and create
   - Copy the **Internal Database URL**

2. Update your web service environment variable:
   - Set `DATABASE_URL` to the PostgreSQL URL

### Free Tier Limitations

- Service sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds to wake up
- 750 hours/month free (enough for one service)

### Monitoring

Check logs in Render dashboard:
- Go to your service → **"Logs"** tab
- View real-time application logs

## Troubleshooting

### Build Fails
- Check that `requirements.txt` is in the repository
- Verify Python version compatibility

### App Won't Start
- Check environment variables are set correctly
- View logs for error messages

### Database Issues
- If using SQLite, data resets on restart (expected behavior)
- Upgrade to PostgreSQL for persistent data

### API Rate Limits
- Monitor Groq API usage at console.groq.com
- Adjust `GROQ_MAX_RETRIES` if needed

## Upgrading from Free Tier

When ready for production:
- Upgrade to a paid plan for:
  - Persistent disk storage (if using SQLite)
  - No sleep timeout
  - More resources
- Or use PostgreSQL database (recommended)

## Custom Domain (Optional)

1. Go to your service → **"Settings"** → **"Custom Domain"**
2. Add your domain
3. Update DNS records as instructed

---

**Need Help?**
- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/render/)
