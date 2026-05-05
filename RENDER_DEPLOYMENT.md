# 🚀 Render Deployment Guide - SmartPLG Accelerator

## ✅ Prerequisites Complete

- ✅ Code pushed to GitHub: https://github.com/rsairam123/SMARTPLG.git
- ✅ `gunicorn` added to requirements.txt
- ✅ `render.yaml` configuration created
- ✅ Frontend deployed to Vercel

---

## 🎯 Deploy Backend to Render (5 Minutes)

### Step 1: Sign Up for Render

1. **Go to Render:**
   ```
   https://render.com
   ```

2. **Sign up with GitHub** (1 click)
   - Click "Get Started for Free"
   - Click "GitHub" button
   - Authorize Render to access your repositories

---

### Step 2: Create New Web Service

1. **Click "New +"** in top right
2. **Select "Web Service"**
3. **Connect Repository:**
   - Find and select: `rsairam123/SMARTPLG`
   - Click "Connect"

---

### Step 3: Configure Service

Fill in the following settings:

**Basic Settings:**
- **Name:** `smartplg-backend`
- **Region:** Choose closest to you (e.g., Oregon, Frankfurt)
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`

**Build & Deploy:**
- **Build Command:**
  ```
  pip install -r requirements.txt
  ```

- **Start Command:**
  ```
  gunicorn app:app --bind 0.0.0.0:$PORT
  ```

**Instance Type:**
- Select **"Free"** (0.1 CPU, 512 MB RAM)

**Advanced Settings (Optional):**
- **Auto-Deploy:** Yes (recommended)
- **Health Check Path:** `/api/health`

---

### Step 4: Deploy

1. **Click "Create Web Service"**
2. **Wait for deployment** (2-3 minutes)
   - You'll see build logs
   - Status will change to "Live" when ready

3. **Your backend URL will be:**
   ```
   https://smartplg-backend.onrender.com
   ```

---

### Step 5: Test Backend

1. **Health Check:**
   ```bash
   curl https://smartplg-backend.onrender.com/api/health
   ```
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "message": "SmartCSV API is running"
   }
   ```

2. **Supported Formats:**
   ```bash
   curl https://smartplg-backend.onrender.com/api/supported-formats
   ```

---

### Step 6: Update Frontend

1. **Edit `index.html`** (line 226):
   ```javascript
   // Change from:
   const API_BASE_URL = 'http://localhost:5001/api';
   
   // To:
   const API_BASE_URL = 'https://smartplg-backend.onrender.com/api';
   ```

2. **Save the file**

---

### Step 7: Redeploy Frontend

1. **Commit changes:**
   ```bash
   cd "/Users/rangampetasairam/Downloads/SmartCSV UI"
   git add index.html
   git commit -m "Update API URL to Render backend"
   git push
   ```

2. **Redeploy to Vercel:**
   ```bash
   vercel --prod
   ```

3. **Wait 30 seconds** for deployment

---

## 🎉 Your App is Now LIVE!

### URLs:

**Frontend (Vercel):**
```
https://smartplg-accelerator.vercel.app
```

**Backend (Render):**
```
https://smartplg-backend.onrender.com
```

**GitHub Repository:**
```
https://github.com/rsairam123/SMARTPLG.git
```

---

## ✅ Test Your App

1. **Open frontend:**
   ```
   https://smartplg-accelerator.vercel.app
   ```

2. **Upload a PDF file** (EDI 850, 810, or 856)

3. **Extract fields** → Download Excel/CSV

4. **Upload CSV** → Generate DDF

5. **Download DDF file**

**Everything should work!** 🎉

---

## 📊 Render Free Tier Details

### What You Get:
- ✅ 750 hours/month (enough for 24/7 operation)
- ✅ 512 MB RAM
- ✅ 0.1 CPU
- ✅ Automatic HTTPS
- ✅ Custom domains
- ✅ Auto-deploy from GitHub
- ✅ Build minutes included

### Limitations:
- ⚠️ **Spins down after 15 minutes of inactivity**
- ⚠️ **First request after spin-down takes 30-60 seconds**
- ⚠️ Limited to 100 GB bandwidth/month

### Solutions:
- Use a service like UptimeRobot to ping every 14 minutes
- Upgrade to paid plan ($7/month) for always-on service

---

## 🔧 Configuration Files

### Files Created:

1. **`render.yaml`** - Render configuration
   ```yaml
   services:
     - type: web
       name: smartplg-backend
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

2. **`requirements.txt`** - Updated with gunicorn
   ```
   PyPDF2>=3.0.0
   openpyxl>=3.0.0
   Flask>=3.0.0
   Flask-CORS>=4.0.0
   gunicorn>=21.0.0
   ```

---

## 🐛 Troubleshooting

### Backend Not Starting:

1. **Check Render logs:**
   - Go to Render dashboard
   - Click on your service
   - View "Logs" tab

2. **Common issues:**
   - Missing dependencies → Check requirements.txt
   - Port binding error → Verify start command
   - Import errors → Check file paths

### Frontend Can't Connect:

1. **Check API URL:**
   - Verify `API_BASE_URL` in index.html
   - Ensure it ends with `/api`
   - No trailing slash

2. **CORS errors:**
   - Verify `flask-cors` is installed
   - Check CORS configuration in app.py

### Slow First Request:

- **Normal behavior** on free tier
- Service spins down after 15 minutes
- First request wakes it up (30-60 seconds)
- Subsequent requests are fast

---

## 🔄 Updating Your App

### Update Backend:

1. **Make changes to code**
2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update backend"
   git push
   ```
3. **Render auto-deploys** (if enabled)

### Update Frontend:

1. **Make changes to index.html**
2. **Redeploy:**
   ```bash
   vercel --prod
   ```

---

## 📱 Monitoring

### Render Dashboard:
- View deployment logs
- Monitor resource usage
- Check request metrics
- View error logs
- Configure environment variables

### Vercel Dashboard:
- View deployment history
- Monitor bandwidth usage
- Check build logs
- View analytics

---

## 💡 Pro Tips

### Keep Service Awake:

1. **Use UptimeRobot** (free):
   - Sign up at https://uptimerobot.com
   - Add monitor for your Render URL
   - Set interval to 14 minutes
   - Service stays awake 24/7

2. **Or upgrade to paid plan** ($7/month):
   - Always-on service
   - No spin-down
   - Faster performance
   - More resources

### Custom Domain:

1. Go to Render dashboard
2. Click on your service
3. Settings → Custom Domains
4. Add your domain
5. Update DNS records

---

## 🎓 What You've Accomplished

1. ✅ Deployed frontend to Vercel
2. ✅ Deployed backend to Render
3. ✅ Connected frontend to backend
4. ✅ Configured automatic deployments
5. ✅ Set up free hosting for both
6. ✅ Created production-ready app

---

## 🆘 Need Help?

### Render Support:
- Documentation: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

### Vercel Support:
- Documentation: https://vercel.com/docs
- Discord: https://vercel.com/discord

---

## ✨ Summary

**Your SmartPLG Accelerator is now fully deployed!**

- ✅ Frontend: Vercel (fast, global CDN)
- ✅ Backend: Render (free, Python support)
- ✅ GitHub: Version control
- ✅ Auto-deploy: Push to deploy
- ✅ HTTPS: Automatic SSL
- ✅ Custom domains: Supported

**Share your app with anyone!** 🚀

---

Made with ❤️ by SmartPLG Accelerator Team