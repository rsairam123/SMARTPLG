# SmartPLG Accelerator - Deployment Guide

## 🚀 Deployment Architecture

This application uses a **split deployment** approach:
- **Frontend**: Vercel (Static HTML/React)
- **Backend**: Railway/Render/PythonAnywhere (Flask API)

---

## 📦 Option 1: Deploy Frontend to Vercel + Backend to Railway (Recommended)

### Step 1: Deploy Backend to Railway

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Connect your repository

3. **Configure Backend**
   - Railway will auto-detect Python
   - Add environment variables (if needed)
   - Railway will use `requirements.txt` automatically

4. **Get Backend URL**
   - After deployment, Railway provides a URL like: `https://your-app.railway.app`
   - Copy this URL

5. **Update Frontend API URL**
   - Open `index.html`
   - Find line: `const API_BASE_URL = 'http://localhost:5001/api';`
   - Replace with: `const API_BASE_URL = 'https://your-app.railway.app/api';`

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (Optional)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via Vercel Dashboard**
   - Go to https://vercel.com
   - Click "Add New Project"
   - Import your Git repository
   - Vercel will auto-detect the `vercel.json` configuration
   - Click "Deploy"

3. **Or Deploy via CLI**
   ```bash
   cd "/Users/rangampetasairam/Downloads/SmartCSV UI"
   vercel
   ```

4. **Your App is Live!**
   - Vercel provides a URL like: `https://your-app.vercel.app`

---

## 📦 Option 2: Deploy Backend to Render

### Step 1: Deploy Backend to Render

1. **Create Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select the repository

3. **Configure Service**
   ```
   Name: smartplg-backend
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: python app.py
   ```

4. **Add Environment Variables** (if needed)
   - Click "Environment"
   - Add any required variables

5. **Deploy**
   - Click "Create Web Service"
   - Render provides a URL like: `https://smartplg-backend.onrender.com`

6. **Update Frontend**
   - Update `API_BASE_URL` in `index.html` with Render URL

### Step 2: Deploy Frontend to Vercel
   - Follow same steps as Option 1, Step 2

---

## 📦 Option 3: Deploy Backend to PythonAnywhere

### Step 1: Deploy Backend to PythonAnywhere

1. **Create PythonAnywhere Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Go to "Files" tab
   - Upload all Python files:
     - `app.py`
     - `smartcsv_ui.py`
     - `csv_to_gentran_ddf.py`
     - `requirements.txt`

3. **Install Dependencies**
   - Go to "Consoles" tab
   - Open Bash console
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Flask"
   - Set source code path
   - Set WSGI configuration file

5. **Get Backend URL**
   - PythonAnywhere provides: `https://yourusername.pythonanywhere.com`

6. **Update Frontend**
   - Update `API_BASE_URL` in `index.html`

### Step 2: Deploy Frontend to Vercel
   - Follow same steps as Option 1, Step 2

---

## 🔧 Configuration Files

### vercel.json (Already Created)
```json
{
  "version": 2,
  "builds": [
    {
      "src": "index.html",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

### requirements.txt (Already Exists)
```
Flask==3.0.0
Flask-CORS==4.0.0
PyPDF2==3.0.1
openpyxl==3.1.2
```

---

## 🌐 CORS Configuration

The backend (`app.py`) already has CORS enabled:
```python
from flask_cors import CORS
CORS(app)  # Allows all origins
```

For production, you may want to restrict origins:
```python
CORS(app, origins=["https://your-app.vercel.app"])
```

---

## 📝 Environment Variables

### Backend (Railway/Render)
```
PORT=5001
FLASK_ENV=production
```

### Frontend (Vercel)
No environment variables needed - API URL is hardcoded in `index.html`

---

## 🧪 Testing Deployment

1. **Test Backend**
   ```bash
   curl https://your-backend-url.com/api/health
   ```
   Should return: `{"status": "healthy", "message": "SmartPLG Accelerator API is running"}`

2. **Test Frontend**
   - Open `https://your-app.vercel.app`
   - Upload a PDF file
   - Check browser console for API calls
   - Verify file downloads work

---

## 🔒 Security Considerations

1. **HTTPS**: Both Vercel and Railway provide HTTPS by default
2. **File Size Limits**: 
   - Vercel: 4.5 MB per file
   - Railway: No strict limit
   - Render: 100 MB
3. **Rate Limiting**: Consider adding rate limiting to backend
4. **API Keys**: If needed, use environment variables

---

## 📊 Monitoring

### Railway
- Built-in metrics dashboard
- View logs in real-time
- Monitor CPU/Memory usage

### Render
- Logs available in dashboard
- Email alerts for downtime
- Metrics dashboard

### Vercel
- Analytics dashboard
- Performance insights
- Error tracking

---

## 🚨 Troubleshooting

### Issue: CORS Error
**Solution**: Ensure `Flask-CORS` is installed and configured in `app.py`

### Issue: 404 on API Calls
**Solution**: Check `API_BASE_URL` in `index.html` matches your backend URL

### Issue: File Upload Fails
**Solution**: Check file size limits and backend logs

### Issue: Backend Timeout
**Solution**: Increase timeout settings in hosting platform

---

## 📱 Quick Deploy Commands

### Deploy Frontend to Vercel
```bash
cd "/Users/rangampetasairam/Downloads/SmartCSV UI"
vercel --prod
```

### Test Backend Locally
```bash
python app.py
# Visit http://localhost:5001/api/health
```

---

## 🎯 Production Checklist

- [ ] Backend deployed and accessible
- [ ] Frontend `API_BASE_URL` updated
- [ ] CORS configured correctly
- [ ] HTTPS enabled on both frontend and backend
- [ ] File upload tested
- [ ] PDF processing tested
- [ ] DDF generation tested
- [ ] Error handling verified
- [ ] Monitoring set up

---

## 📞 Support

For deployment issues:
- Railway: https://railway.app/help
- Render: https://render.com/docs
- Vercel: https://vercel.com/docs
- PythonAnywhere: https://help.pythonanywhere.com

---

**Made with ❤️ for EDI professionals**