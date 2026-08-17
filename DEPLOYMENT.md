# 🚀 GitHub & Deployment Guide for AgriAI

## Step 1: Initialize Git Locally

Open PowerShell in your project folder and run:

```powershell
cd "c:\IMP_DOCS\projects from gethub\helimet track"

# Initialize git repository
git init

# Configure git with your GitHub info
git config user.name "Your Name"
git config user.email "your-email@example.com"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: AgriAI - Crop Yield Prediction System"
```

## Step 2: Create Repository on GitHub

1. Go to **https://github.com/new**
2. Fill in:
   - **Repository name**: `AI-Crop-Yield-Prediction`
   - **Description**: AI-Powered Crop Yield Prediction & Smart Agricultural Optimization System
   - **Public** or **Private** (your choice)
   - ✅ Check "Add a README file" (optional)
   - ✅ Check ".gitignore" → Select "Python"

3. Click **Create Repository**

## Step 3: Connect Local Repo to GitHub

Copy and run these commands:

```powershell
# Add remote repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/AI-Crop-Yield-Prediction.git

# Rename branch to main (if needed)
git branch -M main

# Push code to GitHub
git push -u origin main
```

**IMPORTANT**: Replace `YOUR_USERNAME` with your actual GitHub username!

## Step 4: Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/AI-Crop-Yield-Prediction`
2. You should see all your files uploaded! ✅

## Updating Code (Future Pushes)

After making changes, run:

```powershell
git add .
git commit -m "Your commit message"
git push
```

---

# 📦 Deployment Options

## Option 1: Deploy on Render (Recommended - Free Tier Available)

### Step 1: Prepare for Deployment

Create `Procfile` (no extension):
```
web: cd backend && gunicorn app:app
```

Create `runtime.txt`:
```
python-3.10.12
```

Add to `requirements.txt`:
```
gunicorn==20.1.0
```

### Step 2: Deploy on Render

1. Go to **https://render.com**
2. Click **Sign up** (use GitHub account)
3. Click **New** → **Web Service**
4. Select your GitHub repo
5. Fill in:
   - **Name**: agriAI
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app`
6. Click **Create Web Service**

Your app will be live in 2-3 minutes! 🎉

**Access**: `https://agriAI-xxx.onrender.com`

---

## Option 2: Deploy on Heroku (Free tier limited)

### Step 1: Install Heroku CLI
Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Deploy

```powershell
# Login to Heroku
heroku login

# Create app
heroku create agriAI-app

# Add Procfile and runtime.txt (as shown above)
git add .
git commit -m "Add deployment files"

# Deploy
git push heroku main
```

---

## Option 3: Deploy on Google Cloud Run

### Step 1: Create Dockerfile

Create `Dockerfile` in root:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:8080", "backend.app:app"]
```

### Step 2: Deploy using Cloud Console

1. Go to **https://console.cloud.google.com**
2. Create a new project
3. Go to **Cloud Run** → **Create Service**
4. Select **Deploy from source code**
5. Select your GitHub repo
6. Choose Python runtime
7. Set entry point: `backend.app:app`
8. Deploy! 🚀

---

## Option 4: Deploy on PythonAnywhere

### Step 1: Create Account
Go to **https://www.pythonanywhere.com** and sign up

### Step 2: Upload Code

1. Upload zip file of your project
2. Set up a new web app
3. Choose Python 3.10
4. Configure WSGI file to point to `backend/app.py`
5. Reload web app

---

# 🔧 Environment Variables (if needed)

Create `.env` file in root:

```
FLASK_ENV=production
FLASK_DEBUG=0
```

Add to `backend/app.py`:

```python
import os
from dotenv import load_dotenv

load_dotenv()
DEBUG = os.getenv('FLASK_DEBUG', False)
```

---

# ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.gitignore` updated with `*.pkl`, `*.csv`, `__pycache__`
- [ ] `requirements.txt` updated with all dependencies
- [ ] `Procfile` created for deployment
- [ ] `runtime.txt` created
- [ ] Deployment platform configured
- [ ] App is live! 🚀

---

# 📊 Sharing Your App

Once deployed, share the link:

- **Render**: `https://agriAI-xxx.onrender.com`
- **Heroku**: `https://agriAI-app.herokuapp.com`
- **Google Cloud**: `https://agriAI-xxx.run.app`

Share on:
- GitHub repository link
- LinkedIn
- Portfolio website
- Social media

---

# 🐛 Troubleshooting Deployments

### App not loading?
- Check logs on deployment platform
- Ensure `requirements.txt` is complete
- Make sure `app.py` is in `backend/` folder

### Port issues?
- Deployment platforms use port 8080 by default
- Update app.py if needed:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
```

### Dataset CSV not found?
- Upload dataset to `/dataset/crop_yield_data.csv`
- Or download on app startup

### Models not found?
- Train models locally and commit `.pkl` files
- Or add model training on startup

---

**Questions? Check the respective platform's documentation!** 📚
