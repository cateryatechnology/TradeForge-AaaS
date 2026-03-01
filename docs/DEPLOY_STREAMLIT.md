# Deploy TradeForge to Streamlit Cloud

**Author:** Ary HH | **Email:** <cateryatechnology@proton.me>

---

## 🚀 Deployment Steps

### 1. Prerequisites

- GitHub account
- Streamlit Cloud account (free at <https://streamlit.io/cloud>)
- Your TradeForge repository on GitHub

### 2. Prepare Your Repository

#### A. Create `requirements.txt` for Frontend

Already included at `frontend/requirements.txt`

#### B. Create `.streamlit/config.toml` (Optional)

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

#### C. Update `frontend/app.py`

Make sure it can run standalone:

```python
import streamlit as st
import os

# Backend URL for Streamlit Cloud
API_BASE_URL = os.getenv("API_BASE_URL", "https://your-backend.onrender.com")
```

### 3. Deploy to Streamlit Cloud

#### Step 1: Go to Streamlit Cloud

Visit: <https://streamlit.io/cloud>

#### Step 2: Connect GitHub

1. Click "New app"
2. Connect your GitHub account
3. Select repository: `TradeForge-AaaS`
4. Select branch: `main`
5. Main file path: `frontend/app.py`

#### Step 3: Configure Secrets

Go to "Advanced settings" → "Secrets"

Add your environment variables:

```toml
# API Configuration
API_BASE_URL = "https://your-backend-url.com"

# Optional: If you want to enable features
ENABLE_TRADING = false
ENABLE_DEFI = false
```

#### Step 4: Deploy

Click "Deploy!" and wait 2-3 minutes

### 4. Connect to Backend

#### Option A: Deploy Backend Separately

Use Render, Railway, or DigitalOcean for backend:

```bash
# Set in Streamlit secrets
API_BASE_URL = "https://your-backend.onrender.com"
```

#### Option B: Mock Backend (Development)

For demo purposes only:

```python
# In frontend/app.py
DEMO_MODE = st.sidebar.checkbox("Demo Mode (No Backend)")

if DEMO_MODE:
    # Use mock data
else:
    # Call real API
```

### 5. Custom Domain (Optional)

#### Free Subdomain

Streamlit provides: `your-app.streamlit.app`

#### Custom Domain (Paid Plan)

1. Upgrade to Pro plan
2. Go to Settings → Custom domain
3. Add CNAME record in your DNS:

   ```
   CNAME app yourdomain.streamlit.app
   ```

---

## 🔐 Security Considerations

### Never Store Secrets in Code

❌ **DON'T:**

```python
API_KEY = "sk-1234567890abcdef"  # NEVER DO THIS!
```

✅ **DO:**

```python
API_KEY = st.secrets.get("API_KEY", "")
```

### Use Streamlit Secrets

All sensitive data should go in Streamlit Cloud secrets:

- API keys
- Database URLs
- Passwords
- Tokens

### Read-Only Mode Recommended

For public deployment, consider:

```python
# Disable trading in public deployment
if os.getenv("ENVIRONMENT") == "production":
    TRADING_ENABLED = False
    DEFI_ENABLED = False
```

---

## 🎨 Customization

### 1. App Appearance

```python
st.set_page_config(
    page_title="TradeForge AaaS",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

### 2. Caching for Performance

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_market_data():
    # Your API call here
    pass
```

### 3. Session State

```python
if "user_data" not in st.session_state:
    st.session_state.user_data = {}
```

---

## 📊 Monitoring

### View Logs

Streamlit Cloud Dashboard → Your App → Logs

### Analytics

Streamlit Cloud Dashboard → Your App → Analytics

### Resource Usage

Free tier limits:

- 1 GB RAM
- 1 vCPU
- Sleep after 7 days of inactivity

---

## 🐛 Troubleshooting

### App Won't Start

1. Check logs in Streamlit Cloud dashboard
2. Verify `requirements.txt` is correct
3. Ensure `frontend/app.py` exists
4. Check for missing dependencies

### Import Errors

```bash
# Add to requirements.txt
package-name==version
```

### Backend Connection Issues

```python
try:
    response = requests.get(f"{API_BASE_URL}/health", timeout=5)
except Exception as e:
    st.error("Backend unavailable. Running in demo mode.")
```

### Session State Issues

```python
# Initialize properly
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    # Set default values
```

---

## 🔄 Updates & Redeployment

### Automatic Redeployment

Streamlit Cloud automatically redeploys on git push to main branch

### Manual Reboot

Dashboard → Your App → Reboot

### Rollback

Dashboard → Your App → Manage app → Previous versions

---

## 💡 Best Practices

1. **Use Demo Mode** for public deployments
2. **Cache aggressively** to reduce API calls
3. **Handle errors gracefully** with try-except
4. **Add loading indicators** for better UX
5. **Test locally first** before deploying
6. **Monitor resource usage** to avoid throttling
7. **Use secrets** for all sensitive data
8. **Document limitations** of free tier

---

## 🌐 Alternative: Deploy Only Frontend

If you want Streamlit-only (no backend):

### Option 1: Static Data

```python
# Use CSV or JSON files
df = pd.read_csv("data/sample_data.csv")
```

### Option 2: Direct API Calls

```python
# Call exchanges directly (client-side)
import ccxt
exchange = ccxt.binance()
```

### Option 3: Supabase/Firebase

```python
# Use serverless backend
from supabase import create_client
supabase = create_client(url, key)
```

---

## 📚 Resources

- [Streamlit Docs](https://docs.streamlit.io/)
- [Streamlit Cloud](https://streamlit.io/cloud)
- [Community Forum](https://discuss.streamlit.io/)
- [GitHub Examples](https://github.com/streamlit/streamlit/tree/main/examples)

---

## ⚠️ Limitations

### Free Tier

- Public apps only (anyone can view)
- 1 GB RAM limit
- Apps sleep after 7 days inactivity
- Limited concurrent viewers

### Paid Tier ($20/month per app)

- Private apps
- Custom domains
- More resources
- No sleep
- Priority support

---

**For production trading platform, consider:**

- Deploy backend separately (Render, Railway, AWS)
- Use Streamlit Pro for private access
- Implement proper authentication
- Use HTTPS only
- Regular security audits

---

**Author:** Ary HH  
**Email:** <cateryatechnology@proton.me>  
**GitHub:** [@cateryatechnology](https://github.com/cateryatechnology)
