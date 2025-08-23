# ✅ Deployment Checklist for Nusify

Use this checklist to ensure a smooth deployment process.

## 🐙 GitHub Setup

- [ ] **Create GitHub Repository**
  - [ ] Go to [GitHub](https://github.com) and sign in
  - [ ] Click "New repository"
  - [ ] Name: `nusify` (or your preferred name)
  - [ ] Description: "AI-powered lyrics to song generator"
  - [ ] Make it Public or Private
  - [ ] Don't initialize with README (we already have one)
  - [ ] Click "Create repository"

- [ ] **Initialize Local Git Repository**
  ```bash
  git init
  git add .
  git commit -m "Initial commit: AI-powered lyrics to song generator"
  ```

- [ ] **Connect to GitHub**
  ```bash
  git remote add origin https://github.com/YOUR_USERNAME/nusify.git
  git branch -M main
  git push -u origin main
  ```

## 🔧 Pre-Deployment Checks

- [ ] **Test Local Application**
  - [ ] Backend runs without errors: `python app.py`
  - [ ] Frontend builds successfully: `cd frontend && npm run build`
  - [ ] All dependencies are in `requirements.txt` and `package.json`

- [ ] **Check File Structure**
  - [ ] `.gitignore` exists and excludes unnecessary files
  - [ ] `Procfile` exists for Heroku deployment
  - [ ] `requirements.txt` includes `gunicorn`
  - [ ] Frontend has proper build scripts

## 🚀 Automated Deployment

- [ ] **Run Deployment Script**
  ```bash
  chmod +x deploy.sh
  ./deploy.sh
  ```

- [ ] **Verify GitHub Push**
  - [ ] Check GitHub repository for latest commit
  - [ ] Verify GitHub Actions are running

## 🌐 Choose Hosting Platform

### Option 1: Render (Recommended - Free Tier)

- [ ] **Backend Deployment**
  - [ ] Sign up at [Render](https://render.com)
  - [ ] Click "New +" → "Web Service"
  - [ ] Connect GitHub repository
  - [ ] Configure:
    - Name: `nusify-backend`
    - Environment: `Python 3`
    - Build Command: `pip install -r requirements.txt`
    - Start Command: `gunicorn app:app`
    - Plan: Free

- [ ] **Frontend Deployment**
  - [ ] Click "New +" → "Static Site"
  - [ ] Connect GitHub repository
  - [ ] Configure:
    - Name: `nusify-frontend`
    - Build Command: `cd frontend && npm install && npm run build`
    - Publish Directory: `frontend/build`
    - Plan: Free

### Option 2: Heroku

- [ ] **Install Heroku CLI**
  - [ ] Download from [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
  - [ ] Run `heroku login`

- [ ] **Deploy Backend**
  ```bash
  heroku create nusify-backend
  git push heroku main
  ```

- [ ] **Deploy Frontend**
  ```bash
  heroku create nusify-frontend --buildpack mars/create-react-app-buildpack
  git push heroku main
  ```

### Option 3: Vercel (Frontend Only)

- [ ] **Sign up at [Vercel](https://vercel.com)**
- [ ] **Import GitHub repository**
- [ ] **Configure:**
  - Framework Preset: Create React App
  - Root Directory: `frontend`
  - Build Command: `npm run build`
  - Output Directory: `build`

### Option 4: GitHub Pages

- [ ] **Enable GitHub Pages**
  - [ ] Go to repository Settings
  - [ ] Scroll to "Pages" section
  - [ ] Source: "GitHub Actions"
  - [ ] Verify workflow runs successfully

## 🔧 Post-Deployment Configuration

- [ ] **Update Frontend API URL**
  - [ ] Create `frontend/src/config.js`
  - [ ] Update production API URL to your backend URL

- [ ] **Test Deployed Application**
  - [ ] Frontend loads without errors
  - [ ] Backend API endpoints respond
  - [ ] Audio generation works
  - [ ] Voice cloning functions

- [ ] **Set Environment Variables**
  - [ ] Add production environment variables in hosting platform
  - [ ] Ensure `FLASK_ENV=production`

## 📊 Monitoring & Maintenance

- [ ] **Set up Health Checks**
  - [ ] Backend: `GET /api/health`
  - [ ] Frontend: Build status in hosting platform

- [ ] **Monitor Logs**
  - [ ] Check hosting platform logs regularly
  - [ ] Monitor GitHub Actions for build status

- [ ] **Update Application**
  ```bash
  git pull origin main
  ./deploy.sh
  ```

## 🆘 Troubleshooting

- [ ] **Common Issues Checked**
  - [ ] CORS errors resolved
  - [ ] Build failures fixed
  - [ ] Dependencies properly installed
  - [ ] Environment variables set

- [ ] **Support Resources**
  - [ ] Check hosting platform documentation
  - [ ] Review GitHub Actions logs
  - [ ] Open issues on GitHub repository

---

## 🎉 Deployment Complete!

Once all items are checked, your Nusify application should be live and accessible online!

**Next Steps:**
1. Share your deployed application URL
2. Monitor performance and usage
3. Consider adding custom domain
4. Set up analytics and monitoring

**Need Help?**
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions
- Open issues on GitHub for support
- Review hosting platform documentation
