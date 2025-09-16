#!/usr/bin/env python3
"""
Test script for Gemini-powered Nusify components
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_gemini_mood_analyzer():
    """Test Gemini mood analyzer"""
    try:
        logger.info("Testing Gemini Mood Analyzer...")
        
        from utils.gemini_mood_analyzer import GeminiMoodAnalyzer
        analyzer = GeminiMoodAnalyzer()
        
        # Test with sample lyrics
        test_lyrics = "I'm so happy today, the sun is shining bright and I feel amazing!"
        result = analyzer.analyze(test_lyrics)
        
        logger.info(f"✅ Mood analysis result: {result['mood']} (confidence: {result['confidence']:.2f})")
        logger.info(f"   Emotions: {[e.get('emotion', 'unknown') for e in result.get('emotions', [])]}")
        logger.info(f"   Suggested genre: {result['suggested_genre']}")
        
        return True
    except Exception as e:
        logger.error(f"❌ Gemini mood analyzer test failed: {e}")
        return False

def test_gemini_music_generator():
    """Test Gemini music generator"""
    try:
        logger.info("Testing Gemini Music Generator...")
        
        from utils.gemini_music_generator import GeminiMusicGenerator
        generator = GeminiMusicGenerator()
        
        # Test genre list
        genres = generator.get_available_genres()
        logger.info(f"✅ Available genres: {len(genres)} genres")
        
        # Test music generation (short duration for testing)
        logger.info("Generating test music (5 seconds)...")
        music_path = generator.generate('happy', 'pop', 5)
        
        if music_path and os.path.exists(music_path):
            logger.info(f"✅ Music generated successfully: {music_path}")
            # Clean up test file
            os.remove(music_path)
            return True
        else:
            logger.error("❌ Music generation failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Gemini music generator test failed: {e}")
        return False

def test_gemini_voice_cloner():
    """Test Gemini voice cloner"""
    try:
        logger.info("Testing Gemini Voice Cloner...")
        
        from utils.gemini_voice_cloner import GeminiVoiceCloner
        cloner = GeminiVoiceCloner()
        
        # Test voice list
        voices = cloner.get_available_voices()
        logger.info(f"✅ Available voices: {len(voices)} voices")
        
        # Test voice generation (short text for testing)
        logger.info("Generating test voice...")
        voice_path = cloner.clone_voice("Hello world, this is a test.", 'default')
        
        if voice_path and os.path.exists(voice_path):
            logger.info(f"✅ Voice generated successfully: {voice_path}")
            # Clean up test file
            os.remove(voice_path)
            return True
        else:
            logger.error("❌ Voice generation failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Gemini voice cloner test failed: {e}")
        return False

def test_vercel_app():
    """Test Vercel app imports"""
    try:
        logger.info("Testing Vercel App...")
        
        from vercel_app import app
        logger.info("✅ Vercel app imported successfully")
        
        # Test a simple endpoint
        with app.test_client() as client:
            response = client.get('/api/health')
            if response.status_code == 200:
                logger.info("✅ Health endpoint working")
                return True
            else:
                logger.error(f"❌ Health endpoint failed: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"❌ Vercel app test failed: {e}")
        return False

def check_environment():
    """Check environment setup"""
    logger.info("Checking environment setup...")
    
    # Check for Gemini API key
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        logger.info("✅ GEMINI_API_KEY found in environment")
    else:
        logger.warning("⚠️  GEMINI_API_KEY not found - some features may not work")
    
    # Check Python version
    python_version = sys.version_info
    logger.info(f"✅ Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    return True

def main():
    """Run all tests"""
    logger.info("🧪 Starting Gemini-powered Nusify tests...")
    
    tests = [
        ("Environment Check", check_environment),
        ("Gemini Mood Analyzer", test_gemini_mood_analyzer),
        ("Gemini Music Generator", test_gemini_music_generator),
        ("Gemini Voice Cloner", test_gemini_voice_cloner),
        ("Vercel App", test_vercel_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
        else:
            logger.error(f"❌ {test_name} test failed")
    
    logger.info(f"\n🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Nusify Gemini edition is ready for Vercel deployment.")
        return True
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
