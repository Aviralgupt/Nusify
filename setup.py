#!/usr/bin/env python3
"""
Nusify AI Music Generator - Setup Script
This script sets up the Nusify application with all required dependencies.
"""

import os
import sys
import subprocess
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        logger.error("❌ Python 3.8 or higher is required")
        return False
    logger.info(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_python_dependencies():
    """Install Python dependencies"""
    try:
        logger.info("📦 Installing Python dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        logger.info("✅ Python dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install Python dependencies: {e}")
        return False

def check_ffmpeg():
    """Check if FFmpeg is available"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        logger.info("✅ FFmpeg is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        logger.warning("⚠️  FFmpeg not found - audio processing may not work properly")
        logger.info("📋 Please install FFmpeg:")
        logger.info("   - Windows: choco install ffmpeg")
        logger.info("   - Conda: conda install -c conda-forge ffmpeg")
        logger.info("   - See setup_ffmpeg.md for detailed instructions")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ['generated_songs', 'temp_audio', 'models']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"📁 Directory ready: {directory}")

def setup_frontend():
    """Setup frontend dependencies"""
    try:
        logger.info("📦 Installing frontend dependencies...")
        os.chdir("frontend")
        subprocess.check_call(["npm", "install"])
        os.chdir("..")
        logger.info("✅ Frontend dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install frontend dependencies: {e}")
        return False
    except FileNotFoundError:
        logger.error("❌ npm not found - please install Node.js")
        return False

def test_imports():
    """Test if all modules can be imported"""
    try:
        logger.info("🧪 Testing module imports...")
        
        # Test core modules
        from utils.mood_analyzer import MoodAnalyzer
        from utils.music_generator import MusicGenerator
        from utils.voice_cloner import VoiceCloner
        from utils.audio_mixer import AudioMixer
        from utils.lyrics_processor import LyricsProcessor
        from app import app
        
        logger.info("✅ All modules imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("🚀 Setting up Nusify AI Music Generator...")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install Python dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    # Check FFmpeg
    check_ffmpeg()
    
    # Create directories
    create_directories()
    
    # Setup frontend
    if not setup_frontend():
        logger.warning("⚠️  Frontend setup failed - you can run it manually later")
    
    # Test imports
    if not test_imports():
        logger.error("❌ Setup incomplete - some modules failed to import")
        sys.exit(1)
    
    logger.info("🎉 Setup completed successfully!")
    logger.info("🎵 You can now start Nusify with: python start.py")
    logger.info("🌐 Frontend can be started with: cd frontend && npm start")

if __name__ == '__main__':
    main()
