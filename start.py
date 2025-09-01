#!/usr/bin/env python3
"""
Nusify AI Music Generator - Startup Script
This script starts the Flask backend server for the Nusify application.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if required dependencies are available"""
    try:
        import flask
        import numpy
        import librosa
        import pydub
        import transformers
        import torch
        # TTS import removed - not used in current implementation
        logger.info("✅ All required dependencies are available")
        return True
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        logger.error("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_directories():
    """Create necessary directories if they don't exist"""
    directories = ['generated_songs', 'temp_audio', 'models']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"📁 Directory ready: {directory}")

def main():
    """Main startup function"""
    logger.info("🚀 Starting Nusify AI Music Generator...")
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check and create directories
    check_directories()
    
    try:
        # Import and start the Flask app
        from app import app
        
        logger.info("🎵 Nusify is ready!")
        logger.info("🌐 Web interface will be available at: http://localhost:5000")
        logger.info("📱 Frontend should be started separately with: cd frontend && npm start")
        logger.info("⏹️  Press Ctrl+C to stop the server")
        
        # Start the Flask app
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to avoid duplicate processes
        )
        
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"💥 Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
