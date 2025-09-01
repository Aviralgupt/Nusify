from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import json
import tempfile
from werkzeug.utils import secure_filename
import logging

# Import our custom modules
from utils.mood_analyzer import MoodAnalyzer
from utils.music_generator import MusicGenerator
from utils.voice_cloner import VoiceCloner
from utils.audio_mixer import AudioMixer
from utils.lyrics_processor import LyricsProcessor

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize AI components
mood_analyzer = MoodAnalyzer()
music_generator = MusicGenerator()
voice_cloner = VoiceCloner()
audio_mixer = AudioMixer()
lyrics_processor = LyricsProcessor()

@app.route('/', methods=['GET'])
def home():
    """Home page with instructions"""
    return """
    <html>
    <head>
        <title>Nusify AI Music Generator</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
            .container { max-width: 800px; margin: 0 auto; background: rgba(255,255,255,0.1); padding: 30px; border-radius: 15px; }
            h1 { text-align: center; margin-bottom: 30px; }
            .api-list { background: rgba(255,255,255,0.2); padding: 20px; border-radius: 10px; margin: 20px 0; }
            .endpoint { margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; }
            .method { color: #4CAF50; font-weight: bold; }
            .url { color: #FFD700; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎵 Nusify AI Music Generator</h1>
            <p>Welcome to Nusify! Your AI-powered lyrics to song generator is running successfully.</p>
            
            <div class="api-list">
                <h2>📡 Available API Endpoints:</h2>
                <div class="endpoint">
                    <span class="method">GET</span> <span class="url">/api/health</span> - Health check
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/analyze-mood</span> - Analyze lyrics mood
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/generate-music</span> - Generate background music
                </div>
                <div class="endpoint">
                    <span class="method">POST</span> <span class="url">/api/clone-voice</span> - Clone voice for lyrics
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
            
            <h2>🚀 Next Steps:</h2>
            <ol>
                <li><strong>Start the Frontend:</strong> Open a new terminal and run:
                    <br><code>cd frontend && npm install && npm start</code></li>
                <li><strong>Access the Web Interface:</strong> The frontend will be available at <code>http://localhost:3000</code></li>
                <li><strong>Test the API:</strong> Use the endpoints above to create songs from lyrics</li>
            </ol>
            
            <p><strong>Status:</strong> ✅ Backend server is running successfully on port 5000</p>
        </div>
    </body>
    </html>
    """

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Nusify AI Music Generator',
        'version': '1.0.0'
    })

@app.route('/api/analyze-mood', methods=['POST'])
def analyze_mood():
    """Analyze the mood of lyrics"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Analyze mood using AI
        mood_result = mood_analyzer.analyze(lyrics)
        
        return jsonify({
            'mood': mood_result['mood'],
            'confidence': mood_result['confidence'],
            'emotions': mood_result['emotions'],
            'suggested_genre': mood_result['suggested_genre']
        })
    
    except Exception as e:
        logger.error(f"Error analyzing mood: {str(e)}")
        return jsonify({'error': 'Failed to analyze mood'}), 500

@app.route('/api/generate-music', methods=['POST'])
def generate_music():
    """Generate background music based on mood and genre"""
    try:
        data = request.get_json()
        mood = data.get('mood', 'neutral')
        genre = data.get('genre', 'pop')
        duration = data.get('duration', 30)  # seconds
        
        # Generate music using AI
        music_path = music_generator.generate(mood, genre, duration)
        
        return jsonify({
            'music_path': music_path,
            'duration': duration,
            'mood': mood,
            'genre': genre
        })
    
    except Exception as e:
        logger.error(f"Error generating music: {str(e)}")
        return jsonify({'error': 'Failed to generate music'}), 500

@app.route('/api/clone-voice', methods=['POST'])
def clone_voice():
    """Clone voice for lyrics"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        artist_voice = data.get('artist_voice', 'default')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Clone voice using AI
        voice_path = voice_cloner.clone_voice(lyrics, artist_voice)
        
        return jsonify({
            'voice_path': voice_path,
            'artist_voice': artist_voice,
            'duration': len(lyrics.split()) * 0.5  # Rough estimate
        })
    
    except Exception as e:
        logger.error(f"Error cloning voice: {str(e)}")
        return jsonify({'error': 'Failed to clone voice'}), 500

@app.route('/api/create-song', methods=['POST'])
def create_song():
    """Create complete song from lyrics"""
    try:
        data = request.get_json()
        lyrics = data.get('lyrics', '')
        artist_voice = data.get('artist_voice', 'default')
        genre = data.get('genre', 'auto')
        
        if not lyrics:
            return jsonify({'error': 'Lyrics are required'}), 400
        
        # Step 1: Analyze mood
        mood_result = mood_analyzer.analyze(lyrics)
        
        # Step 2: Generate background music
        if genre == 'auto':
            genre = mood_result['suggested_genre']
        
        music_path = music_generator.generate(
            mood_result['mood'], 
            genre, 
            len(lyrics.split()) * 2  # Duration based on lyrics length
        )
        
        # Step 3: Clone voice
        voice_path = voice_cloner.clone_voice(lyrics, artist_voice)
        
        # Step 4: Mix audio
        song_path = audio_mixer.mix_audio(voice_path, music_path)
        
        # Step 5: Clean up temporary files
        os.remove(music_path)
        os.remove(voice_path)
        
        return jsonify({
            'song_path': song_path,
            'mood': mood_result['mood'],
            'genre': genre,
            'duration': len(lyrics.split()) * 2,
            'download_url': f'/api/download-song/{os.path.basename(song_path)}'
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

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('generated_songs', exist_ok=True)
    os.makedirs('temp_audio', exist_ok=True)
    
    logger.info("Starting Nusify AI Music Generator...")
    app.run(debug=True, host='0.0.0.0', port=5000)
