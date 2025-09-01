#!/usr/bin/env python3
"""
Nusify AI Music Generator - Test Script
This script tests the core functionality of Nusify.
"""

import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_imports():
    """Test if all modules can be imported"""
    try:
        logger.info("Testing module imports...")
        
        from utils.mood_analyzer import MoodAnalyzer
        from utils.music_generator import MusicGenerator
        from utils.voice_cloner import VoiceCloner
        from utils.audio_mixer import AudioMixer
        from utils.lyrics_processor import LyricsProcessor
        
        logger.info("✅ All modules imported successfully")
        return True
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        return False

def test_mood_analyzer():
    """Test mood analyzer functionality"""
    try:
        logger.info("Testing mood analyzer...")
        
        from utils.mood_analyzer import MoodAnalyzer
        analyzer = MoodAnalyzer()
        
        # Test with sample lyrics
        test_lyrics = "I'm so happy today, the sun is shining bright!"
        result = analyzer.analyze(test_lyrics)
        
        logger.info(f"✅ Mood analysis result: {result['mood']} (confidence: {result['confidence']:.2f})")
        return True
    except Exception as e:
        logger.error(f"❌ Mood analyzer test failed: {e}")
        return False

def test_lyrics_processor():
    """Test lyrics processor functionality"""
    try:
        logger.info("Testing lyrics processor...")
        
        from utils.lyrics_processor import LyricsProcessor
        processor = LyricsProcessor()
        
        # Test with sample lyrics
        test_lyrics = """Verse 1:
I'm walking down the street
Feeling the rhythm in my feet

Chorus:
This is my song
I'll sing it all day long"""
        
        result = processor.process_lyrics(test_lyrics)
        
        logger.info(f"✅ Lyrics processing result: {result['processing_info']['total_lines']} lines, {result['processing_info']['total_words']} words")
        return True
    except Exception as e:
        logger.error(f"❌ Lyrics processor test failed: {e}")
        return False

def test_music_generator():
    """Test music generator functionality"""
    try:
        logger.info("Testing music generator...")
        
        from utils.music_generator import MusicGenerator
        generator = MusicGenerator()
        
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
        logger.error(f"❌ Music generator test failed: {e}")
        return False

def test_voice_cloner():
    """Test voice cloner functionality"""
    try:
        logger.info("Testing voice cloner...")
        
        from utils.voice_cloner import VoiceCloner
        cloner = VoiceCloner()
        
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
        logger.error(f"❌ Voice cloner test failed: {e}")
        return False

def test_audio_mixer():
    """Test audio mixer functionality"""
    try:
        logger.info("Testing audio mixer...")
        
        from utils.audio_mixer import AudioMixer
        from utils.music_generator import MusicGenerator
        from utils.voice_cloner import VoiceCloner
        
        mixer = AudioMixer()
        music_gen = MusicGenerator()
        voice_clone = VoiceCloner()
        
        # Generate test files
        logger.info("Creating test audio files...")
        music_path = music_gen.generate('happy', 'pop', 3)
        voice_path = voice_clone.clone_voice("Test lyrics for mixing", 'default')
        
        if music_path and voice_path and os.path.exists(music_path) and os.path.exists(voice_path):
            # Test mixing
            logger.info("Testing audio mixing...")
            mixed_path = mixer.mix_audio(voice_path, music_path, 'pop')
            
            if mixed_path and os.path.exists(mixed_path):
                logger.info(f"✅ Audio mixing successful: {mixed_path}")
                
                # Clean up test files
                os.remove(music_path)
                os.remove(voice_path)
                os.remove(mixed_path)
                return True
            else:
                logger.error("❌ Audio mixing failed")
                return False
        else:
            logger.error("❌ Could not create test audio files")
            return False
            
    except Exception as e:
        logger.error(f"❌ Audio mixer test failed: {e}")
        return False

def main():
    """Run all tests"""
    logger.info("🧪 Starting Nusify functionality tests...")
    
    tests = [
        ("Module Imports", test_imports),
        ("Mood Analyzer", test_mood_analyzer),
        ("Lyrics Processor", test_lyrics_processor),
        ("Music Generator", test_music_generator),
        ("Voice Cloner", test_voice_cloner),
        ("Audio Mixer", test_audio_mixer)
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
        logger.info("🎉 All tests passed! Nusify is working correctly.")
        return True
    else:
        logger.error(f"❌ {total - passed} tests failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
