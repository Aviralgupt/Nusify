# 🎵 Nusify - AI-Powered Lyrics to Song Generator

Transform your lyrics into complete songs with AI-generated background music and voice cloning capabilities - completely free!

## ✨ Features

- **🎤 Lyrics to Song**: Convert any lyrics into a complete musical composition
- **🎼 AI Background Music**: Automatically generates music based on song mood (happy, sad, energetic, etc.)
- **🎭 Voice Cloning**: Clone voices of famous artists (with ethical considerations)
- **🆓 Zero Cost**: Built entirely with open-source AI models and free APIs
- **🎨 Mood Detection**: AI automatically detects and matches music style to lyrics content
- **📱 Web Interface**: Beautiful, responsive web application

## 🚀 Tech Stack

- **Frontend**: React.js with modern UI components
- **Backend**: Python Flask API
- **AI Models**: 
  - Text-to-Speech: Coqui TTS (open source)
  - Music Generation: Magenta (Google's open source music AI)
  - Voice Cloning: YourTTS (open source)
  - Mood Analysis: Transformers (Hugging Face)
- **Audio Processing**: Librosa, PyDub
- **Styling**: Tailwind CSS

## 🛠️ Installation

### Prerequisites
- Python 3.8+
- Node.js 16+
- FFmpeg (for audio processing)

### Quick Start (Local Development)
```bash
# Clone the repository
git clone <your-repo-url>
cd Nusify

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install

# Start the backend
cd ..
python app.py

# Start the frontend (in new terminal)
cd frontend
npm start
```

### 🚀 Quick Deploy to GitHub

**Windows:**
```cmd
deploy.bat
```

**Linux/Mac:**
```bash
# Make the deployment script executable
chmod +x deploy.sh

# Run the deployment script
./deploy.sh
```

The script will:
- Initialize git repository (if needed)
- Build the frontend
- Commit and push to GitHub
- Guide you through hosting platform setup

## 🎯 How It Works

1. **Lyrics Input**: User enters lyrics through the web interface
2. **Mood Analysis**: AI analyzes lyrics to determine emotional tone
3. **Music Generation**: AI generates appropriate background music
4. **Voice Synthesis**: Converts lyrics to speech with selected voice
5. **Audio Mixing**: Combines voice and background music
6. **Download**: User gets the complete song as an audio file

## 🔧 Configuration

- Voice models can be customized in `config/voices.json`
- Music generation parameters in `config/music_config.py`
- API endpoints in `app.py`

## 📁 Project Structure

```
Nusify/
├── app.py                 # Main Flask backend
├── requirements.txt       # Python dependencies
├── config/               # Configuration files
├── models/               # AI model files
├── utils/                # Utility functions
├── frontend/             # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
├── .github/              # GitHub Actions workflows
├── deploy.sh             # Deployment automation script
├── Procfile              # Heroku deployment config
└── README.md
```

## 🎨 Voice Cloning Artists

The system includes pre-trained models for various artists (ethical use only):
- Pop artists
- Rock vocalists
- Country singers
- And more...

## ⚠️ Ethical Considerations

- Voice cloning is for educational and creative purposes only
- Respect artist rights and copyright
- Use responsibly and ethically

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines.

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues, please open an issue on GitHub.

## 🚀 Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Supported Platforms
- **Render** (Recommended for free tier)
- **Heroku**
- **Vercel** (Frontend)
- **Railway**
- **GitHub Pages** (Frontend only)

---

**Made with ❤️ and AI for the music community**
