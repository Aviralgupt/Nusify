from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import tempfile
from werkzeug.utils import secure_filename
import logging

# Import our Gemini-powered modules
from utils.gemini_mood_analyzer import GeminiMoodAnalyzer
from utils.gemini_music_generator import GeminiMusicGenerator
from utils.gemini_voice_cloner import GeminiVoiceCloner
from utils.audio_mixer import AudioMixer
from utils.lyrics_processor import LyricsProcessor

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI components
mood_analyzer = GeminiMoodAnalyzer()
music_generator = GeminiMusicGenerator()
voice_cloner = GeminiVoiceCloner()
audio_mixer = AudioMixer()
lyrics_processor = LyricsProcessor()

@app.route('/', methods=['GET'])
def home():
    """Home page with instructions"""
    return """
    <html>
    <head>
        <title>Nusify AI Music Generator - Powered by Gemini</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            h1 { text-align: center; margin-bottom: 30px; }
            .api-list { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin: 20px 0; }
            .endpoint { margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; }
            .method { color: #4CAF50; font-weight: bold; }
            .url { color: #FFD700; }
            .gemini-badge { background: #4285F4; padding: 5px 10px; border-radius: 15px; font-size: 12px; margin-left: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 Nusify AI Music Generator <span class="gemini-badge">Powered by Gemini</span></h1>
            <p>Welcome to Nusify! Your AI-powered lyrics to song generator is running successfully on Vercel.</p>
            
            <div class="api-list">
                <h2>📡 Available API Endpoints:</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/health</span> - Health check
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/analyze-mood</span> - Analyze lyrics mood with Gemini AI
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/generate-music</span> - Generate background music with Gemini AI
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/clone-voice</span> - Clone voice for lyrics with Gemini AI
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/create-song</span> - Create complete song
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/available-voices</span> - Get available voices
                </div>
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/available-genres</span> - Get available genres
                </div>
            </div>
            
            <h2>🚀 Features:</h2>
            <ul>
                <li><strong>Google Gemini AI Integration:</strong> Advanced mood analysis and creative direction</li>
                <li><strong>Serverless Deployment:</strong> Optimized for Vercel hosting</li>
                <li><strong>Real-time Music Generation:</strong> Create songs from lyrics instantly</li>
                <li><strong>Multiple Voice Styles:</strong> 10 different artist voice profiles</li>
                <li><strong>18 Music Genres:</strong> From pop to classical to electronic</li>
            </ul>
            
            <p><strong>Status:</strong> ✅ Backend server is running successfully on Vercel</p>
            <p><strong>Environment:</strong> Production-ready serverless deployment</p>
        </div>
    </body>
    </html>
    """

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Nusify AI Music Generator - Gemini Edition',
        'version': '2.0.0',
        'platform': 'Vercel',
        'ai_provider': 'Google Gemini'
    })

@app.route('/api/analyze-mood', methods=['POST'])
def analyze_mood():
    """Analyze the mood of lyrics using Gemini AI"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Analyze mood using Gemini AI
        mood_result = mood_analyzer.analyze(lyrics)
        
        return jsonify({
            'mood': mood_result['mood'],
            'confidence': mood_result['confidence'],
            'emotions': mood_result['emotions'],
            'suggested_genre': mood_result['suggested_genre'],
            'themes': mood_result.get('themes', []),
            'analysis_notes': mood_result.get('analysis_notes', ''),
            'ai_provider': 'Google Gemini'
        })
    
    except Exception as e:
        logger.error(f"Error analyzing mood: {str(e)}")
        return jsonify({'error': 'Failed to analyze mood'}), 500

@app.route('/api/generate-music', methods=['POST'])
def generate_music():
    """Generate background music using Gemini AI creative direction"""
    try:
        data = request.get_json()
        mood = data.get('mood', 'neutral')
        genre = data.get('genre', 'pop')
        duration = data.get('duration', 30)
        
        # Generate music using Gemini AI
        music_path = music_generator.generate(mood, genre, duration)
        
        return jsonify({
            'music_path': music_path,
            'duration': duration,
            'mood': mood,
            'genre': genre,
            'ai_provider': 'Google Gemini'
        })
    
    except Exception as e:
        logger.error(f"Error generating music: {str(e)}")
        return jsonify({'error': 'Failed to generate music'}), 500

@app.route('/api/clone-voice', methods=['POST'])
def clone_voice():
    """Clone voice for lyrics using Gemini AI voice characteristics"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        artist_voice = data.get('artist_voice', 'default')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Clone voice using Gemini AI
        voice_path = voice_cloner.clone_voice(lyrics, artist_voice)
        
        return jsonify({
            'voice_path': voice_path,
            'artist_voice': artist_voice,
            'duration': len(lyrics.split()) * 0.5,
            'ai_provider': 'Google Gemini'
        })
    
    except Exception as e:
        logger.error(f"Error cloning voice: {str(e)}")
        return jsonify({'error': 'Failed to clone voice'}), 500

@app.route('/api/create-song', methods=['POST'])
def create_song():
    """Create complete song from lyrics using Gemini AI"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        artist_voice = data.get('artist_voice', 'default')
        genre = data.get('genre', 'auto')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Step 1: Analyze mood with Gemini AI
        mood_result = mood_analyzer.analyze(lyrics)
        
        # Step 2: Generate background music with Gemini AI
        if genre == 'auto':
            genre = mood_result['suggested_genre']
        
        music_path = music_generator.generate(
            mood_result['mood'], 
            genre, 
            len(lyrics.split()) * 2
        )
        
        # Step 3: Clone voice with Gemini AI
        voice_path = voice_cloner.clone_voice(lyrics, artist_voice)
        
        # Step 4: Mix audio
        song_path = audio_mixer.mix_audio(voice_path, music_path, genre)
        
        # Step 5: Clean up temporary files
        try:
            if os.path.exists(music_path):
                os.remove(music_path)
            if os.path.exists(voice_path):
                os.remove(voice_path)
        except:
            pass  # Ignore cleanup errors in serverless environment
        
        return jsonify({
            'song_path': song_path,
            'mood': mood_result['mood'],
            'genre': genre,
            'duration': len(lyrics.split()) * 2,
            'download_url': f'/api/download-song/{os.path.basename(song_path)}',
            'ai_provider': 'Google Gemini',
            'confidence': mood_result['confidence']
        })
    
    except Exception as e:
        logger.error(f"Error creating song: {str(e)}")
        return jsonify({'error': 'Failed to create song'}), 500

@app.route('/api/download-song/<filename>', methods=['GET'])
def download_song(filename):
    """Download generated song"""
    try:
        song_dir = os.path.join(os.getcwd(), 'generated_songs')
        song_path = os.path.join(song_dir, filename)
        
        if not os.path.exists(song_path):
            return jsonify({'error': 'Song not found'}), 404
        
        return send_file(song_path, as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error downloading song: {str(e)}")
        return jsonify({'error': 'Failed to download song'}), 500

@app.route('/api/available-voices', methods=['GET'])
def get_available_voices():
    """Get list of available artist voices"""
    try:
        voices = voice_cloner.get_available_voices()
        return jsonify({'voices': voices})
    
    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        return jsonify({'error': 'Failed to get voices'}), 500

@app.route('/api/available-genres', methods=['GET'])
def get_available_genres():
    """Get list of available music genres"""
    try:
        genres = music_generator.get_available_genres()
        return jsonify({'genres': genres})
    
    except Exception as e:
        logger.error(f"Error getting genres: {str(e)}")
        return jsonify({'error': 'Failed to get genres'}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Vercel serverless function handler
def handler(request):
    return app(request.environ, lambda *args: None)

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('generated_songs', exist_ok=True)
    os.makedirs('temp_audio', exist_ok=True)
    
    logger.info("Starting Nusify AI Music Generator - Gemini Edition...")
    app.run(debug=True, host='0.0.0.0', port=5000)
