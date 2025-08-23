# 🚀 Deployment Guide for Nusify

This guide will help you deploy Nusify to various platforms after pushing to GitHub.

## 📋 Prerequisites

- GitHub repository set up
- Python 3.8+ installed
- Node.js 16+ installed
- FFmpeg installed

## 🐙 GitHub Setup

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: AI-powered lyrics to song generator"
```

### 2. Create GitHub Repository
1. Go to [GitHub](https://github.com) and sign in
2. Click "New repository"
3. Name it `nusify` or your preferred name
4. Make it public or private as desired
5. Don't initialize with README (we already have one)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/nusify.git
git branch -M main
git push -u origin main
```

## 🌐 Deployment Options

### Option 1: Render (Recommended for Free Tier)

#### Backend Deployment
1. Go to [Render](https://render.com) and sign up
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `nusify-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Free

#### Frontend Deployment
1. Click "New +" → "Static Site"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `nusify-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/build`
   - **Plan**: Free

### Option 2: Heroku

#### Backend Deployment
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create `Procfile` in root:
   ```
   web: gunicorn app:app
   ```
3. Deploy:
   ```bash
   heroku create nusify-backend
   git push heroku main
   ```

#### Frontend Deployment
1. Use [Heroku Buildpacks](https://github.com/mars/create-react-app-buildpack)
2. Deploy:
   ```bash
   heroku create nusify-frontend --buildpack mars/create-react-app-buildpack
   git push heroku main
   ```

### Option 3: Vercel (Frontend Only)

1. Go to [Vercel](https://vercel.com) and sign up
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### Option 4: Railway

1. Go to [Railway](https://railway.app) and sign up
2. Connect your GitHub repository
3. Deploy both services automatically

## 🔧 Environment Variables

Create `.env` file for production:

```env
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here
```

## 📱 Frontend Configuration

Update `frontend/src/config.js` (create if doesn't exist):

```javascript
const config = {
  development: {
    apiUrl: 'http://localhost:5000'
  },
  production: {
    apiUrl: 'https://your-backend-url.com'
  }
};

export default config[process.env.NODE_ENV || 'development'];
```

## 🚀 Quick Deploy Script

Create `deploy.sh`:

```bash
#!/bin/bash
echo "🚀 Deploying Nusify..."

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm run build
cd ..

# Commit and push
echo "📝 Committing changes..."
git add .
git commit -m "Deploy: $(date)"
git push origin main

echo "✅ Deployment initiated! Check your hosting platform."
```

Make it executable:
```bash
chmod +x deploy.sh
```

## 🔍 Monitoring & Maintenance

### Health Checks
- Backend: `GET /health`
- Frontend: Build status in hosting platform

### Logs
- Render: Dashboard → Logs
- Heroku: `heroku logs --tail`
- Vercel: Dashboard → Functions → Logs

### Updates
```bash
git pull origin main
./deploy.sh
```

## 🆘 Troubleshooting

### Common Issues
1. **Build Failures**: Check dependency versions in `requirements.txt` and `package.json`
2. **CORS Errors**: Ensure backend allows frontend domain
3. **Audio Processing**: Verify FFmpeg is available in production environment

### Support
- Check hosting platform documentation
- Review GitHub Actions logs
- Open issues on GitHub repository

---

**Happy Deploying! 🎵✨**
