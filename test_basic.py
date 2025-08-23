#!/usr/bin/env python3
"""
Basic tests for Nusify project
"""

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import app
        print("✅ Flask app imports successfully")
    except ImportError as e:
        print(f"❌ Flask app import failed: {e}")
        return False
    
    try:
        from utils.mood_analyzer import MoodAnalyzer
        print("✅ MoodAnalyzer imports successfully")
    except ImportError as e:
        print(f"❌ MoodAnalyzer import failed: {e}")
        return False
    
    try:
        from utils.music_generator import MusicGenerator
        print("✅ MusicGenerator imports successfully")
    except ImportError as e:
        print(f"❌ MusicGenerator import failed: {e}")
        return False
    
    try:
        from utils.voice_cloner import VoiceCloner
        print("✅ VoiceCloner imports successfully")
    except ImportError as e:
        print(f"❌ VoiceCloner import failed: {e}")
        return False
    
    try:
        from utils.audio_mixer import AudioMixer
        print("✅ AudioMixer imports successfully")
    except ImportError as e:
        print(f"❌ AudioMixer import failed: {e}")
        return False
    
    try:
        from utils.lyrics_processor import LyricsProcessor
        print("✅ LyricsProcessor imports successfully")
    except ImportError as e:
        print(f"❌ LyricsProcessor import failed: {e}")
        return False
    
    return True

def test_config():
    """Test that configuration files exist"""
    import os
    
    required_files = [
        'requirements.txt',
        'app.py',
        'config/voices.json',
        'frontend/package.json'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    return True

def test_flask_app():
    """Test that Flask app can be created"""
    try:
        from app import app
        print("✅ Flask app instance created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Running basic tests for Nusify...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config,
        test_flask_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Project is ready for deployment.")
        exit(0)
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        exit(1)
