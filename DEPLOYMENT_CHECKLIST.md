# 🚀 Render Deployment Quick Fix Guide

## Issue: "alembic: command not found"

This error occurs because the command is not in the PATH or running from wrong directory.

## ✅ Solution Applied

Updated `render.yaml` with:
- **Build Command:** `cd backend && pip install -r requirements.txt`
- **Start Command:** `cd backend && python -m alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT`

Using `python -m` ensures the module is found in the Python path.

---

## 🔧 Manual Deployment Steps for Render

### Option 1: Use Blueprint (render.yaml) - Recommended

1. **Push Updated Code:**
   ```bash
   git add render.yaml
   git commit -m "Fix deployment commands"
   git push origin main
   ```

2. **Deploy on Render:**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repo
   - Select `render.yaml`
   - Click "Apply"

### Option 2: Manual Web Service Setup

If Blueprint doesn't work, create manually:

1. **Go to Render Dashboard** → "New +" → "Web Service"

2. **Configure:**
   - **Name:** `devops-copilot-api`
   - **Environment:** Python 3
   - **Build Command:**
     ```bash
     cd backend && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     cd backend && python -m alembic upgrade head && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

3. **Add Environment Variables:**
   ```
   DATABASE_URL = <your-database-url>
   REDIS_URL = <your-redis-url>
   AI_PROVIDER = groq
   GROQ_API_KEY = <your-groq-key>
   SECRET_KEY = <auto-generate>
   WEBHOOK_SECRET = <auto-generate>
   KESTRA_URL = http://localhost:8080
   KESTRA_API_KEY = dummy
   ALLOWED_ORIGINS = https://your-app.vercel.app
   ```

---

## 🗄️ Database Setup

### Create PostgreSQL on Render

1. **Dashboard** → "New +" → "PostgreSQL"
2. **Configure:**
   - Name: `devops-copilot-db`
   - Database: `devops_copilot`
   - User: `devops_user`
   - Plan: Free (or Starter $7/month)
3. **Copy Internal Database URL** → Use for `DATABASE_URL`

### Alternative: Supabase (Free Forever)

1. Go to [Supabase](https://supabase.com)
2. Create new project
3. Get connection string from Settings → Database
4. Format: `postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres`

---

## 🔴 Redis Setup

### Redis Cloud (Free 30MB)

1. Go to [Redis Cloud](https://redis.com/try-free)
2. Create free database
3. Copy connection URL
4. Format: `redis://default:[PASSWORD]@[HOST]:[PORT]`

### Alternative: Upstash

1. Go to [Upstash](https://upstash.com)
2. Create Redis database
3. Copy connection URL

---

## 🔑 Get Groq API Key

1. Go to [Groq Console](https://console.groq.com)
2. Sign up for free account
3. Create API key
4. Free tier: 30 requests/minute

---

## ✅ Deployment Checklist

- [ ] Database created (Render PostgreSQL or Supabase)
- [ ] Redis created (Redis Cloud or Upstash)
- [ ] Groq API key obtained
- [ ] Updated `render.yaml` pushed to GitHub
- [ ] Environment variables configured in Render
- [ ] Backend deployed successfully
- [ ] Health check passing: `https://your-backend.onrender.com/health`
- [ ] Frontend environment variables updated in Vercel
- [ ] Frontend redeployed

---

## 🐛 Troubleshooting

### Build Fails

**Check Render Logs:**
- Dashboard → Your Service → Logs

**Common Issues:**
1. **Missing dependencies:** Check `requirements.txt`
2. **Python version:** Ensure Python 3.11+
3. **Path issues:** Ensure `cd backend` in commands

### Alembic Migration Fails

**Error:** `alembic.util.exc.CommandError: Can't locate revision identified by...`

**Solution:**
```bash
# Option 1: Skip migrations initially
# Change start command to:
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT

# Then run migrations manually via Render Shell
cd backend
python -m alembic upgrade head
```

**Error:** `sqlalchemy.exc.OperationalError: could not connect to server`

**Solution:**
- Verify `DATABASE_URL` is correct
- Check database is running
- Ensure database allows connections from Render

### CORS Errors

**Symptom:** Frontend can't connect to backend

**Solution:**
1. Add your Vercel URL to `ALLOWED_ORIGINS`
2. Format: `https://your-app.vercel.app,https://your-app-preview.vercel.app`
3. Redeploy backend

### Redis Connection Fails

**Error:** `redis.exceptions.ConnectionError`

**Solution:**
- Verify `REDIS_URL` format
- Check Redis instance is running
- Test connection: `redis-cli -u <REDIS_URL> ping`

---

## 🎯 Alternative: Deploy Without Database Migrations

If migrations keep failing, you can:

1. **Update Start Command:**
   ```bash
   cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Run Migrations Locally:**
   ```bash
   # Set production database URL
   export DATABASE_URL="<your-render-database-url>"
   
   # Run migrations
   cd backend
   python -m alembic upgrade head
   ```

3. **Or Use Render Shell:**
   - Dashboard → Your Service → Shell tab
   - Run:
     ```bash
     cd backend
     python -m alembic upgrade head
     ```

---

## 📊 Verify Deployment

### Test Backend

```bash
# Health check
curl https://your-backend.onrender.com/health

# API root
curl https://your-backend.onrender.com/

# Expected response:
# {"message": "DevOps Co-Pilot API", "version": "v1", "status": "operational"}
```

### Test Frontend Connection

1. Open Vercel frontend URL
2. Open browser DevTools → Console
3. Check for API connection errors
4. Try creating a test incident

---

## 💰 Free Tier Limitations

| Service | Free Tier | Limitation |
|---------|-----------|------------|
| Render Web Service | ✅ Free | Sleeps after 15min inactivity |
| Render PostgreSQL | ✅ 90 days free | Then $7/month |
| Redis Cloud | ✅ Free | 30MB storage |
| Groq API | ✅ Free | 30 req/min |

**Upgrade to Render Starter ($7/month) for:**
- No sleep (always on)
- Faster performance
- Better for production

---

## 🚀 Next Steps After Deployment

1. **Test the API** - Verify all endpoints work
2. **Configure Webhooks** - Set up monitoring tool webhooks
3. **Set Up Monitoring** - Enable Render alerts
4. **Add Logging** - Consider Papertrail or Logtail
5. **Database Backups** - Set up automated backups
6. **SSL Certificate** - Render provides free SSL

---

## 📞 Support

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Groq Docs:** https://console.groq.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com

---

**Last Updated:** November 30, 2025
