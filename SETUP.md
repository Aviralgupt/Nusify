# 🚀 Nusify Setup Guide

Welcome to Nusify! This guide will help you get the AI-powered music generator up and running on your system.

## 📋 Prerequisites

Before you begin, make sure you have the following installed:

- **Python 3.8+** - [Download here](https://www.python.org/downloads/)
- **Node.js 16+** - [Download here](https://nodejs.org/)
- **FFmpeg** - Required for audio processing
  - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
  - **macOS**: `brew install ffmpeg`
  - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo yum install ffmpeg` (CentOS/RHEL)

## 🛠️ Installation Steps

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Nusify
```

### 2. Set Up Python Backend

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Set Up React Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Return to root directory
cd ..
```

## 🚀 Running the Application

### Option 1: Using the Startup Scripts

#### Windows
```bash
# Double-click start.bat or run in Command Prompt
start.bat
```

#### macOS/Linux
```bash
# Make script executable
chmod +x start.py

# Run the startup script
python start.py
```

### Option 2: Manual Startup

#### Start Backend (Terminal 1)
```bash
# Activate virtual environment if using one
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start Flask backend
python app.py
```

#### Start Frontend (Terminal 2)
```bash
cd frontend
npm start
```

## 🌐 Accessing the Application

- **Backend API**: http://localhost:5000
- **Frontend**: http://localhost:3000
- **API Health Check**: http://localhost:5000/api/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory for custom configurations:

```env
# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True

# Audio Processing
SAMPLE_RATE=44100
BIT_DEPTH=16

# Model Paths
TTS_MODEL_PATH=models/tts
MUSIC_MODEL_PATH=models/music
```

### Voice and Genre Customization

- **Voice Profiles**: Edit `config/voices.json` to add custom voices
- **Music Genres**: Modify `utils/music_generator.py` to add new genres
- **Mood Analysis**: Customize `utils/mood_analyzer.py` for different analysis methods

## 📁 Project Structure

```
Nusify/
├── app.py                 # Main Flask application
├── start.py              # Startup script
├── requirements.txt       # Python dependencies
├── config/               # Configuration files
│   ├── voices.json       # Voice profiles
│   └── __init__.py
├── utils/                # Core AI modules
│   ├── mood_analyzer.py  # Lyrics mood analysis
│   ├── music_generator.py # AI music generation
│   ├── voice_cloner.py   # Voice cloning
│   ├── audio_mixer.py    # Audio mixing
│   ├── lyrics_processor.py # Lyrics processing
│   └── __init__.py
├── frontend/             # React frontend
│   ├── src/              # Source code
│   ├── public/           # Public assets
│   ├── package.json      # Node.js dependencies
│   └── tailwind.config.js # Tailwind CSS config
├── generated_songs/       # Output directory
├── temp_audio/           # Temporary audio files
└── models/               # AI model files
```

## 🎯 First Use

1. **Start the application** using one of the methods above
2. **Open your browser** and go to http://localhost:3000
3. **Navigate to the Generator page**
4. **Enter some lyrics** in the text area
5. **Click "Analyze Mood"** to see AI mood detection
6. **Select a voice and genre** (or let AI choose automatically)
7. **Click "Generate Song"** to create your AI-powered music
8. **Download your song** when generation is complete

## 🐛 Troubleshooting

### Common Issues

#### Python Dependencies
```bash
# If you get import errors, try reinstalling dependencies
pip uninstall -r requirements.txt
pip install -r requirements.txt
```

#### Audio Processing Issues
```bash
# Make sure FFmpeg is installed and in PATH
ffmpeg -version

# On Windows, add FFmpeg to PATH or place ffmpeg.exe in project root
```

#### Frontend Issues
```bash
# Clear npm cache and reinstall
cd frontend
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

#### Port Conflicts
```bash
# If ports 3000 or 5000 are in use, you can change them:

# Backend (edit app.py)
app.run(host='0.0.0.0', port=5001)

# Frontend (edit package.json)
"scripts": {
  "start": "PORT=3001 react-scripts start"
}
```

### Performance Issues

- **Large Models**: First run may take longer as models download
- **Memory Usage**: AI models can be memory-intensive; close other applications if needed
- **GPU Acceleration**: Install CUDA for faster processing (optional)

## 🔒 Security & Ethics

### Voice Cloning Guidelines

- **Educational Use**: Voice cloning is for educational and creative purposes
- **Respect Rights**: Always respect artist rights and copyright
- **No Deception**: Do not use voice cloning for impersonation or fraud
- **Attribution**: Credit original artists when using their voice styles

### Privacy

- **Local Processing**: Audio processing happens locally on your machine
- **No Data Collection**: We don't collect or store your lyrics or generated music
- **Secure**: All processing is done offline for maximum privacy

## 📚 API Documentation

### Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze-mood` - Analyze lyrics mood
- `POST /api/generate-music` - Generate background music
- `POST /api/clone-voice` - Clone voice for lyrics
- `POST /api/create-song` - Create complete song
- `GET /api/download-song/<filename>` - Download generated song
- `GET /api/available-voices` - Get available voice options
- `GET /api/available-genres` - Get available music genres

### Example Usage

```bash
# Analyze mood
curl -X POST http://localhost:5000/api/analyze-mood \
  -H "Content-Type: application/json" \
  -d '{"lyrics": "I am happy today"}'

# Generate song
curl -X POST http://localhost:5000/api/create-song \
  -H "Content-Type: application/json" \
  -d '{"lyrics": "Your lyrics here", "artist_voice": "pop_female", "genre": "auto"}'
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest

# Format code
black .
isort .

# Lint code
flake8 .
```

## 📞 Support

If you encounter issues:

1. **Check this guide** for common solutions
2. **Search existing issues** on GitHub
3. **Create a new issue** with detailed information
4. **Join our community** discussions

## 📄 License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Happy music making with Nusify! 🎵✨**
