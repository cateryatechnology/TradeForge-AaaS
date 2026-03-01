# Deploy TradeForge to Render

**Author:** Ary HH | **Email:** <cateryatechnology@proton.me>

---

## 🚀 Full Stack Deployment on Render

Render offers free tier for both backend and database, perfect for MVP deployment.

---

## 📋 Prerequisites

- GitHub account
- Render account (free at <https://render.com>)
- Your TradeForge repository on GitHub

---

## 🗄️ Step 1: Deploy PostgreSQL Database

### 1. Create Database

1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - **Name:** `tradeforge-db`
   - **Database:** `tradeforge_db`
   - **User:** `tradeforge`
   - **Region:** Choose closest to you
   - **Plan:** Free

4. Click "Create Database"
5. **SAVE** the Internal Database URL (you'll need it)

### 2. Note Database Details

```
Internal Database URL: postgresql://user:pass@hostname/dbname
External Database URL: (for local development)
```

---

## 🔴 Step 2: Deploy Redis (Optional)

### Option A: Redis Labs (Free)

1. Go to <https://redis.com/try-free/>
2. Create free account
3. Create new database
4. Get connection URL: `redis://default:password@hostname:port`

### Option B: Upstash (Free)

1. Go to <https://upstash.com/>
2. Create Redis database
3. Get REST URL

### Option C: Skip Redis

Set in environment: `REDIS_URL=`

---

## 🔙 Step 3: Deploy Backend

### 1. Create Web Service

1. Render Dashboard → "New +" → "Web Service"
2. Connect GitHub repository
3. Fill in:
   - **Name:** `tradeforge-backend`
   - **Region:** Same as database
   - **Branch:** `main`
   - **Root Directory:** `backend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### 2. Set Environment Variables

Add these in Environment section:

```bash
# Python
PYTHON_VERSION=3.11

# Database (from Step 1)
DATABASE_URL=postgresql://user:pass@hostname/dbname

# Redis (from Step 2, or leave empty)
REDIS_URL=redis://hostname:port

# Security (generate new ones!)
SECRET_KEY=your-generated-secret-key-here
ENCRYPTION_KEY=your-generated-encryption-key-here
ALGORITHM=HS256

# App Config
ENVIRONMENT=production
DEBUG=false
APP_NAME=TradeForge AaaS

# CORS (add your frontend URL after deployment)
BACKEND_CORS_ORIGINS=https://tradeforge-frontend.onrender.com

# Blockchain (get from Alchemy/Infura)
ETH_RPC_URL=your-alchemy-url
POLYGON_RPC_URL=your-alchemy-url

# Optional: Exchange APIs (keep empty if not using)
BINANCE_API_KEY=
BINANCE_API_SECRET=
```

### 3. Deploy

Click "Create Web Service"

Wait 5-10 minutes for build and deployment.

Your backend will be available at: `https://tradeforge-backend.onrender.com`

---

## 🎨 Step 4: Deploy Frontend

### 1. Create Web Service for Frontend

1. Render Dashboard → "New +" → "Web Service"
2. Connect same GitHub repository
3. Fill in:
   - **Name:** `tradeforge-frontend`
   - **Region:** Same as backend
   - **Branch:** `main`
   - **Root Directory:** `frontend`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### 2. Set Environment Variables

```bash
# Python
PYTHON_VERSION=3.11

# Backend URL (from Step 3)
API_BASE_URL=https://tradeforge-backend.onrender.com

# Streamlit Config
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_SERVER_PORT=8501
DEFAULT_LANGUAGE=en
```

### 3. Deploy

Click "Create Web Service"

Your frontend will be available at: `https://tradeforge-frontend.onrender.com`

---

## 🔗 Step 5: Connect Everything

### 1. Update Backend CORS

Go back to backend environment variables and update:

```bash
BACKEND_CORS_ORIGINS=https://tradeforge-frontend.onrender.com,http://localhost:8501
```

### 2. Test Connection

Visit your frontend URL and check if it can connect to backend.

---

## 🗄️ Step 6: Run Database Migrations

### Option A: Using Render Shell

1. Go to backend service → Shell tab
2. Run:

```bash
alembic upgrade head
```

### Option B: Manual SQL

1. Go to PostgreSQL database → Query tab
2. Run initialization SQL if needed

---

## 🔐 Security Hardening

### 1. Generate Strong Secrets

```bash
# SECRET_KEY
openssl rand -hex 32

# ENCRYPTION_KEY
python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 2. Environment Variables

Never commit `.env` file. Always use Render's Environment Variables.

### 3. HTTPS Only

Render provides free SSL. Ensure:

```python
# In config.py
if ENVIRONMENT == "production":
    # Force HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)
```

---

## 📊 Monitoring

### 1. Logs

Render Dashboard → Service → Logs tab

### 2. Metrics

Render Dashboard → Service → Metrics tab

### 3. Health Checks

Render automatically monitors your app's health endpoint:

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## 💰 Cost Breakdown

### Free Tier (Suitable for MVP)

- **PostgreSQL:** Free (1 GB, expires after 90 days)
- **Backend:** Free (512 MB RAM, spins down after 15 min inactivity)
- **Frontend:** Free (512 MB RAM, spins down after 15 min inactivity)
- **Total:** $0/month

### Paid Tier (Production)

- **PostgreSQL:** $7/month (256 MB RAM, persistent)
- **Backend:** $7/month (512 MB RAM, always on)
- **Frontend:** $7/month (512 MB RAM, always on)
- **Total:** $21/month

---

## ⚡ Performance Optimization

### 1. Keep Services Warm

Free tier spins down after 15 minutes inactivity.

**Solution:** Use cron job to ping every 14 minutes:

```bash
# Use cron-job.org or similar
curl https://tradeforge-backend.onrender.com/health
```

### 2. Database Connection Pooling

```python
# In database.py
engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True
)
```

### 3. Caching

```python
# Use Redis for caching
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Check:**

1. Build logs for dependency issues
2. Environment variables are set correctly
3. PORT variable is used in start command

**Fix:**

```bash
# Start command must use $PORT
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Database Connection Failed

**Check:**

1. DATABASE_URL is correct
2. Database is in same region
3. Internal Database URL is used (not external)

**Fix:**

```bash
# Use Internal Database URL
DATABASE_URL=postgresql://internal-host/db
```

### Frontend Can't Reach Backend

**Check:**

1. API_BASE_URL points to backend HTTPS URL
2. CORS is configured correctly
3. Backend is running (not spun down)

**Fix:**

```bash
# Frontend env
API_BASE_URL=https://tradeforge-backend.onrender.com

# Backend env
BACKEND_CORS_ORIGINS=https://tradeforge-frontend.onrender.com
```

### App Spins Down (Free Tier)

**Workaround:**

- Use <https://cron-job.org/> to ping every 14 minutes
- Upgrade to paid tier ($7/month per service)

---

## 🔄 CI/CD Setup

Render auto-deploys on git push to main branch.

### Custom Deploy Hook

```bash
# Manual deploy via webhook
curl -X POST https://api.render.com/deploy/srv-xxxxx?key=yyyy
```

### GitHub Actions

```yaml
# .github/workflows/deploy.yml
name: Deploy to Render
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Render Deploy
        run: curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

---

## 📱 Custom Domain (Optional)

### 1. Upgrade to Paid Tier

Custom domains require paid plan ($7/month minimum)

### 2. Add Domain

1. Service Settings → Custom Domains
2. Add your domain: `app.yourdomain.com`
3. Add CNAME record in your DNS:

   ```
   CNAME app your-app.onrender.com
   ```

### 3. SSL Certificate

Render automatically provisions Let's Encrypt SSL.

---

## 🌐 Alternative Architecture

### Option 1: Backend on Render + Frontend on Streamlit Cloud

- Backend: Render (always available)
- Frontend: Streamlit Cloud (free, public)
- DB: Render PostgreSQL

### Option 2: Everything on Render

- Backend: Render
- Frontend: Render (Streamlit)
- DB: Render PostgreSQL
- Redis: Upstash

### Option 3: Hybrid (Cost-Effective)

- Backend: Render Free ($0)
- Frontend: Streamlit Cloud ($0)
- DB: Supabase Free ($0)
- Redis: Upstash Free ($0)

---

## 📚 Resources

- [Render Docs](https://render.com/docs)
- [FastAPI on Render](https://render.com/docs/deploy-fastapi)
- [Streamlit on Render](https://render.com/docs/deploy-streamlit)
- [PostgreSQL on Render](https://render.com/docs/databases)

---

## ⚠️ Production Checklist

- [ ] Use strong SECRET_KEY
- [ ] Use strong ENCRYPTION_KEY
- [ ] Set DEBUG=false
- [ ] Configure proper CORS
- [ ] Use HTTPS only
- [ ] Set up monitoring
- [ ] Configure logging
- [ ] Set up backups (paid tier)
- [ ] Use environment secrets
- [ ] Enable health checks
- [ ] Set up error tracking (Sentry)
- [ ] Configure rate limiting

---

**Author:** Ary HH  
**Email:** <cateryatechnology@proton.me>  
**GitHub:** [@cateryatechnology](https://github.com/cateryatechnology)
