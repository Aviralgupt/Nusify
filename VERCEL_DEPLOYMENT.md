# 🚀 Nusify Vercel Deployment Guide

## Overview
This guide will help you deploy Nusify AI Music Generator to Vercel using Google Gemini API for enhanced AI capabilities.

## ✨ What's New in Vercel Edition
- **Google Gemini AI Integration**: Advanced mood analysis and creative direction
- **Serverless Architecture**: Optimized for Vercel's serverless functions
- **Reduced Dependencies**: Lighter weight for faster cold starts
- **Enhanced Performance**: Better suited for cloud deployment

## 🔧 Prerequisites

### 1. Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Create a new project or select existing one
3. Generate an API key
4. Copy the API key for later use

### 2. Vercel Account
1. Sign up at [vercel.com](https://vercel.com)
2. Connect your GitHub account

## 📦 Installation & Setup

### 1. Clone and Prepare
```bash
git clone https://github.com/Aviralgupt/Nusify.git
cd Nusify
```

### 2. Install Vercel CLI
```bash
npm i -g vercel
```

### 3. Install Dependencies
```bash
pip install -r requirements-vercel.txt
```

## 🚀 Deployment Steps

### Method 1: Vercel CLI (Recommended)

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy from your project directory**
   ```bash
   vercel
   ```

3. **Set Environment Variables**
   ```bash
   vercel env add GEMINI_API_KEY
   # Paste your Gemini API key when prompted
   ```

4. **Redeploy with environment variables**
   ```bash
   vercel --prod
   ```

### Method 2: GitHub Integration

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Vercel deployment configuration"
   git push origin main
   ```

2. **Connect to Vercel**
   - Go to [vercel.com/dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Set the following:
     - **Framework Preset**: Other
     - **Root Directory**: ./
     - **Build Command**: `pip install -r requirements-vercel.txt`
     - **Output Directory**: ./

3. **Add Environment Variables**
   - Go to Project Settings → Environment Variables
   - Add `GEMINI_API_KEY` with your API key
   - Redeploy the project

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key (required)

### Vercel Settings
- **Function Timeout**: 30 seconds (max for hobby plan)
- **Memory**: 1024 MB (recommended)
- **Region**: Choose closest to your users

## 📁 Project Structure for Vercel

```
Nusify/
├── vercel_app.py          # Main Flask app for Vercel
├── vercel.json            # Vercel configuration
├── requirements-vercel.txt # Python dependencies
├── api/
│   └── index.py           # Vercel serverless entry point
├── utils/
│   ├── gemini_mood_analyzer.py
│   ├── gemini_music_generator.py
│   ├── gemini_voice_cloner.py
│   ├── audio_mixer.py
│   └── lyrics_processor.py
└── frontend/              # React frontend (optional)
```

## 🧪 Testing Your Deployment

### 1. Health Check
```bash
curl https://your-app.vercel.app/api/health
```

### 2. Test Mood Analysis
```bash
curl -X POST https://your-app.vercel.app/api/analyze-mood \
  -H "Content-Type: application/json" \
  -d '{"lyrics": "I am so happy today, the sun is shining bright!"}'
```

### 3. Test Music Generation
```bash
curl -X POST https://your-app.vercel.app/api/generate-music \
  -H "Content-Type: application/json" \
  -d '{"mood": "happy", "genre": "pop", "duration": 10}'
```

## 🎯 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with API documentation |
| `/api/health` | GET | Health check |
| `/api/analyze-mood` | POST | Analyze lyrics mood with Gemini AI |
| `/api/generate-music` | POST | Generate background music |
| `/api/clone-voice` | POST | Clone voice for lyrics |
| `/api/create-song` | POST | Create complete song |
| `/api/available-voices` | GET | Get available voices |
| `/api/available-genres` | GET | Get available genres |

## 🔍 Troubleshooting

### Common Issues

1. **Function Timeout**
   - Reduce music generation duration
   - Optimize API calls
   - Consider upgrading Vercel plan

2. **Memory Issues**
   - Reduce audio file sizes
   - Optimize numpy operations
   - Check Vercel function memory limits

3. **API Key Issues**
   - Verify GEMINI_API_KEY is set correctly
   - Check API key permissions
   - Ensure API key is not expired

4. **Import Errors**
   - Check all dependencies in requirements-vercel.txt
   - Verify file paths are correct
   - Test locally before deploying

### Debugging

1. **Check Vercel Logs**
   ```bash
   vercel logs
   ```

2. **Test Locally**
   ```bash
   python vercel_app.py
   ```

3. **Check Environment Variables**
   ```bash
   vercel env ls
   ```

## 📊 Performance Optimization

### For Vercel Deployment
- Use shorter audio durations (10-30 seconds)
- Implement caching for repeated requests
- Optimize AI model calls
- Use streaming for large responses

### Cost Optimization
- Monitor API usage
- Implement rate limiting
- Use efficient audio formats
- Cache common responses

## 🎉 Success!

Once deployed, your Nusify AI Music Generator will be available at:
`https://your-app-name.vercel.app`

### Next Steps
1. Test all endpoints
2. Set up custom domain (optional)
3. Configure monitoring
4. Deploy frontend separately (if needed)

## 📞 Support

If you encounter issues:
1. Check Vercel documentation
2. Review Google Gemini API docs
3. Check project logs
4. Open an issue on GitHub

---

**Happy Deploying! 🚀🎵**
