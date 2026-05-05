# 🚂 Railway Backend Deployment Guide

## Why Railway?

**Vercel cannot host Python Flask backends.** Vercel is designed for:
- ✅ Static frontends (HTML, CSS, JavaScript)
- ✅ Node.js serverless functions
- ❌ Python Flask applications

**Railway is perfect for Python backends:**
- ✅ Free tier available ($5 credit/month)
- ✅ Automatic Python detection
- ✅ Easy GitHub integration
- ✅ Automatic HTTPS
- ✅ Environment variables support

---

## 🎯 Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  Frontend (Vercel)                                      │
│  https://smartplg-accelerator.vercel.app               │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  index.html (React App)                          │  │
│  │  - Upload PDFs                                   │  │
│  │  - Upload CSVs                                   │  │
│  │  - Display results                               │  │
│  └──────────────────────────────────────────────────┘  │
│                          │                              │
│                          │ API Calls                    │
│                          ▼                              │
└─────────────────────────────────────────────────────────┘
                           │
                           │
┌──────────────────────────▼──────────────────────────────┐
│                                                         │
│  Backend (Railway)                                      │
│  https://smartplg-backend.railway.app                  │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  app.py (Flask API)                              │  │
│  │  - Process PDFs                                  │  │
│  │  - Generate Excel/CSV                            │  │
│  │  - Generate DDF files                            │  │
│  │  - File downloads                                │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

1. **GitHub Account** (free)
2. **Railway Account** (free - sign up with GitHub)
3. **Git installed** on your computer

---

## 🚀 Step-by-Step Deployment

### Step 1: Create GitHub Repository

1. **Go to GitHub:**
   ```
   https://github.com/new
   ```

2. **Create new repository:**
   - Repository name: `smartplg-accelerator`
   - Description: `SmartPLG Accelerator - EDI Field Extractor & DDF Generator`
   - Visibility: Public or Private (your choice)
   - ✅ Click "Create repository"

3. **Push your code to GitHub:**
   ```bash
   cd "/Users/rangampetasairam/Downloads/SmartCSV UI"
   
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit - SmartPLG Accelerator"
   
   # Add remote (replace YOUR_USERNAME with your GitHub username)
   git remote add origin https://github.com/YOUR_USERNAME/smartplg-accelerator.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

---

### Step 2: Deploy Backend to Railway

1. **Go to Railway:**
   ```
   https://railway.app
   ```

2. **Sign up with GitHub** (if not already signed up)

3. **Create New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your `smartplg-accelerator` repository

4. **Railway will automatically:**
   - ✅ Detect Python
   - ✅ Install dependencies from `requirements.txt`
   - ✅ Run `python app.py` (from Procfile)
   - ✅ Assign a public URL

5. **Wait for deployment** (2-3 minutes)
   - You'll see build logs
   - Status will change to "Active" when ready

6. **Get your backend URL:**
   - Click on your deployment
   - Go to "Settings" tab
   - Find "Domains" section
   - Copy the URL (e.g., `https://smartplg-backend.railway.app`)

---

### Step 3: Update Frontend with Backend URL

1. **Open `index.html`** in your editor

2. **Find line ~226** (search for `API_BASE_URL`):
   ```javascript
   const API_BASE_URL = 'http://localhost:5001/api';
   ```

3. **Replace with your Railway URL:**
   ```javascript
   const API_BASE_URL = 'https://YOUR-APP-NAME.railway.app/api';
   ```
   
   Example:
   ```javascript
   const API_BASE_URL = 'https://smartplg-backend.railway.app/api';
   ```

4. **Save the file**

---

### Step 4: Redeploy Frontend to Vercel

1. **Deploy updated frontend:**
   ```bash
   cd "/Users/rangampetasairam/Downloads/SmartCSV UI"
   vercel --prod
   ```

2. **Wait for deployment** (30 seconds)

3. **Your app is now LIVE!** 🎉

---

## ✅ Verify Deployment

### Test Backend (Railway)

1. **Health Check:**
   ```bash
   curl https://YOUR-APP-NAME.railway.app/api/health
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
   curl https://YOUR-APP-NAME.railway.app/api/supported-formats
   ```

### Test Frontend (Vercel)

1. **Open your app:**
   ```
   https://smartplg-accelerator.vercel.app
   ```

2. **Test PDF Upload:**
   - Go to "Extract Fields from PDF" tab
   - Upload an EDI PDF (850, 810, or 856)
   - Should process and show results
   - Download Excel/CSV files

3. **Test DDF Generation:**
   - Go to "Generate DDF from CSV" tab
   - Upload a CSV file
   - Enter transaction name
   - Generate and download DDF file

---

## 🔧 Configuration Files

### Files Created for Railway:

1. **`railway.json`** - Railway configuration
   ```json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python app.py"
     }
   }
   ```

2. **`Procfile`** - Process file
   ```
   web: python app.py
   ```

3. **`requirements.txt`** - Python dependencies (already exists)

4. **`app.py`** - Updated to use PORT environment variable
   ```python
   port = int(os.environ.get('PORT', 5001))
   app.run(debug=True, host='0.0.0.0', port=port)
   ```

---

## 💰 Railway Pricing

### Free Tier:
- ✅ $5 credit per month
- ✅ Enough for small to medium usage
- ✅ No credit card required initially
- ✅ Automatic HTTPS
- ✅ Custom domains

### Usage Estimates:
- **Light usage** (testing): ~$1-2/month
- **Medium usage** (100 requests/day): ~$3-4/month
- **Heavy usage**: May need paid plan ($5+/month)

---

## 🐛 Troubleshooting

### Backend Issues:

1. **Build Failed:**
   - Check Railway logs
   - Verify `requirements.txt` is correct
   - Ensure all dependencies are listed

2. **App Crashed:**
   - Check Railway logs for errors
   - Verify `app.py` runs locally
   - Check PORT environment variable

3. **CORS Errors:**
   - Verify `flask-cors` is installed
   - Check CORS configuration in `app.py`

### Frontend Issues:

1. **API Calls Failing:**
   - Verify `API_BASE_URL` is correct
   - Check Railway backend is running
   - Open browser console for errors

2. **File Upload Not Working:**
   - Check file size (max 16MB)
   - Verify file type (PDF or CSV)
   - Check backend logs

---

## 🔄 Updating Your App

### Update Backend:

1. **Make changes to code**
2. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Update backend"
   git push
   ```
3. **Railway auto-deploys** from GitHub

### Update Frontend:

1. **Make changes to `index.html`**
2. **Redeploy to Vercel:**
   ```bash
   vercel --prod
   ```

---

## 📊 Monitoring

### Railway Dashboard:
- View deployment logs
- Monitor resource usage
- Check request metrics
- View error logs

### Vercel Dashboard:
- View deployment history
- Monitor bandwidth usage
- Check build logs
- View analytics

---

## 🎉 Success Checklist

- [ ] GitHub repository created
- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Backend deployed to Railway
- [ ] Backend URL obtained
- [ ] Frontend updated with backend URL
- [ ] Frontend redeployed to Vercel
- [ ] Health check passes
- [ ] PDF upload works
- [ ] DDF generation works
- [ ] File downloads work

---

## 🆘 Need Help?

### Railway Support:
- Documentation: https://docs.railway.app
- Discord: https://discord.gg/railway
- GitHub: https://github.com/railwayapp/railway

### Vercel Support:
- Documentation: https://vercel.com/docs
- Discord: https://vercel.com/discord
- GitHub: https://github.com/vercel/vercel

---

## 🎓 What You've Learned

1. ✅ Vercel is for frontends, not Python backends
2. ✅ Railway is perfect for Python Flask apps
3. ✅ Split deployment: Frontend + Backend
4. ✅ Environment variables for configuration
5. ✅ CORS for cross-origin requests
6. ✅ Automatic deployments from GitHub

---

## 🚀 Your Live URLs

After deployment, you'll have:

**Frontend (Vercel):**
```
https://smartplg-accelerator.vercel.app
```

**Backend (Railway):**
```
https://YOUR-APP-NAME.railway.app
```

**Share your app with anyone!** 🎉

---

Made with ❤️ by SmartPLG Accelerator Team