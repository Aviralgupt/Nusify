import os
import logging
import google.generativeai as genai
from typing import Dict, List, Any
import json
import numpy as np
import soundfile as sf
import tempfile

logger = logging.getLogger(__name__)

class GeminiMusicGenerator:
    """AI-powered music generator using Google Gemini API for creative direction"""
    
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.api_available = True
        else:
            self.api_available = False
            logger.error("Gemini API not configured")
        
        self.sample_rate = 44100
        self.available_genres = [
            'pop', 'rock', 'electronic', 'jazz', 'classical', 'country',
            'r&b', 'hip-hop', 'ambient', 'orchestral', 'indie', 'ballad',
            'dance', 'atmospheric', 'folk', 'blues', 'reggae', 'punk'
        ]
        
        # Enhanced genre-specific parameters
        self.genre_params = {
            'pop': {
                'tempo': 120, 'key': 'C', 'chord_progression': ['C', 'G', 'Am', 'F'],
                'instruments': ['piano', 'drums', 'bass', 'synth'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'rock': {
                'tempo': 140, 'key': 'E', 'chord_progression': ['E', 'A', 'B', 'C#m'],
                'instruments': ['electric_guitar', 'drums', 'bass'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'electronic': {
                'tempo': 128, 'key': 'Am', 'chord_progression': ['Am', 'F', 'C', 'G'],
                'instruments': ['synth', 'drums', 'bass', 'effects'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'jazz': {
                'tempo': 90, 'key': 'F', 'chord_progression': ['F', 'Bbm7', 'Eb7', 'Abmaj7'],
                'instruments': ['piano', 'saxophone', 'bass', 'drums'],
                'rhythm_pattern': [1, 0, 0, 1, 0, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'classical': {
                'tempo': 80, 'key': 'D', 'chord_progression': ['D', 'A', 'Bm', 'G'],
                'instruments': ['strings', 'piano', 'woodwinds'],
                'rhythm_pattern': [1, 0, 0, 0, 1, 0, 0, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'ambient': {
                'tempo': 60, 'key': 'Dm', 'chord_progression': ['Dm', 'Am', 'C', 'G'],
                'instruments': ['pad', 'atmosphere', 'texture'],
                'rhythm_pattern': [1, 0, 0, 0, 0, 0, 0, 0],
                'bass_pattern': [1, 0, 0, 0, 0, 0, 0, 0]
            }
        }
        
        # Musical note frequencies
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }
    
    def generate(self, mood: str, genre: str, duration: int) -> str:
        """
        Generate background music based on mood and genre using Gemini for creative direction
        
        Args:
            mood (str): The mood of the music
            genre (str): The music genre
            duration (int): Duration in seconds
            
        Returns:
            str: Path to generated music file
        """
        try:
            logger.info(f"Generating {genre} music with {mood} mood for {duration} seconds")
            
            # Get creative direction from Gemini
            creative_direction = self._get_creative_direction(mood, genre, duration)
            
            # Get base genre parameters
            if genre not in self.genre_params:
                genre = 'pop'
            
            base_params = self.genre_params[genre].copy()
            
            # Apply Gemini's creative suggestions
            modified_params = self._apply_creative_direction(base_params, creative_direction, mood)
            
            # Generate the music
            music_data = self._generate_music_data(modified_params, duration)
            
            # Save to file
            output_path = self._save_music(music_data, genre, mood)
            
            logger.info(f"Music generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating music: {e}")
            return self._generate_fallback_music(duration)
    
    def _get_creative_direction(self, mood: str, genre: str, duration: int) -> Dict[str, Any]:
        """Get creative direction from Gemini API"""
        try:
            if not self.api_available:
                return self._get_fallback_direction(mood, genre)
            
            prompt = f"""
Create a detailed musical composition plan for a {genre} song with {mood} mood, {duration} seconds long.

Return a JSON object with:
{{
    "tempo_modifier": 0.8-1.2,
    "key_modifier": "major" or "minor",
    "energy_level": 0.0-1.0,
    "instrumentation_focus": ["primary", "secondary", "tertiary"],
    "rhythm_complexity": 0.0-1.0,
    "melodic_style": "simple", "complex", "experimental",
    "harmonic_richness": 0.0-1.0,
    "dynamic_range": 0.0-1.0,
    "creative_notes": "brief description of the musical approach"
}}

Consider the mood and genre characteristics. Be creative but practical for AI music generation.
Return only the JSON object.
"""
            
            response = self.model.generate_content(prompt)
            return self._parse_creative_response(response.text)
            
        except Exception as e:
            logger.error(f"Error getting creative direction: {e}")
            return self._get_fallback_direction(mood, genre)
    
    def _parse_creative_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's creative direction response"""
        try:
            response_text = response_text.strip()
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error parsing creative response: {e}")
            return self._get_fallback_direction("neutral", "pop")
    
    def _get_fallback_direction(self, mood: str, genre: str) -> Dict[str, Any]:
        """Fallback creative direction when Gemini is not available"""
        mood_modifiers = {
            'happy': {'tempo_modifier': 1.2, 'energy_level': 0.8, 'key_modifier': 'major'},
            'sad': {'tempo_modifier': 0.8, 'energy_level': 0.3, 'key_modifier': 'minor'},
            'energetic': {'tempo_modifier': 1.3, 'energy_level': 0.9, 'key_modifier': 'major'},
            'calm': {'tempo_modifier': 0.7, 'energy_level': 0.2, 'key_modifier': 'minor'},
            'romantic': {'tempo_modifier': 0.9, 'energy_level': 0.6, 'key_modifier': 'major'},
            'mysterious': {'tempo_modifier': 0.8, 'energy_level': 0.4, 'key_modifier': 'minor'}
        }
        
        return mood_modifiers.get(mood, {
            'tempo_modifier': 1.0,
            'energy_level': 0.5,
            'key_modifier': 'major',
            'instrumentation_focus': ['melody', 'rhythm', 'harmony'],
            'rhythm_complexity': 0.5,
            'melodic_style': 'simple',
            'harmonic_richness': 0.5,
            'dynamic_range': 0.5,
            'creative_notes': 'Standard composition approach'
        })
    
    def _apply_creative_direction(self, base_params: Dict, creative_direction: Dict, mood: str) -> Dict[str, Any]:
        """Apply Gemini's creative direction to base parameters"""
        modified = base_params.copy()
        
        # Apply tempo modification
        if 'tempo_modifier' in creative_direction:
            modified['tempo'] = int(base_params['tempo'] * creative_direction['tempo_modifier'])
        
        # Apply energy level
        modified['energy_level'] = creative_direction.get('energy_level', 0.5)
        
        # Apply key modification
        if 'key_modifier' in creative_direction:
            modified['key_type'] = creative_direction['key_modifier']
        
        # Apply other creative elements
        modified['rhythm_complexity'] = creative_direction.get('rhythm_complexity', 0.5)
        modified['melodic_style'] = creative_direction.get('melodic_style', 'simple')
        modified['harmonic_richness'] = creative_direction.get('harmonic_richness', 0.5)
        modified['dynamic_range'] = creative_direction.get('dynamic_range', 0.5)
        
        return modified
    
    def _generate_music_data(self, params: Dict, duration: int) -> np.ndarray:
        """Generate musical audio data"""
        # Calculate timing
        beats_per_second = params['tempo'] / 60
        beats_total = int(duration * beats_per_second)
        
        # Generate different layers
        melody = self._generate_melody(params, beats_total, beats_per_second)
        harmony = self._generate_harmony(params, beats_total, beats_per_second)
        rhythm = self._generate_rhythm(params, beats_total, beats_per_second)
        bass = self._generate_bass(params, beats_total, beats_per_second)
        
        # Mix layers with energy level
        energy = params.get('energy_level', 0.5)
        mixed = self._mix_layers([melody, harmony, rhythm, bass], [0.3, 0.4, 0.2, 0.3])
        
        # Apply energy boost
        mixed *= (0.5 + energy)
        
        # Apply effects
        mixed = self._apply_effects(mixed, params)
        
        return mixed
    
    def _generate_melody(self, params: Dict, beats_total: int, beats_per_second: float) -> np.ndarray:
        """Generate melodic line"""
        melody = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            chord_index = i % len(params['chord_progression'])
            note = chord_notes[chord_index][i % len(chord_notes[chord_index])]
            
            note_duration = beat_end - beat_start
            t = np.linspace(0, note_duration / self.sample_rate, note_duration)
            frequency = note * (2 ** (np.random.randint(-1, 2)))
            
            melody[beat_start:beat_end] = np.sin(2 * np.pi * frequency * t) * 0.3
        
        return melody
    
    def _generate_harmony(self, params: Dict, beats_total: int, beats_per_second: float) -> np.ndarray:
        """Generate harmonic accompaniment"""
        harmony = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            chord_index = i % len(params['chord_progression'])
            chord = chord_notes[chord_index]
            
            for note in chord:
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                harmony[beat_start:beat_end] += np.sin(2 * np.pi * note * t) * 0.2
        
        return harmony
    
    def _generate_rhythm(self, params: Dict, beats_total: int, beats_per_second: float) -> np.ndarray:
        """Generate rhythmic pattern"""
        rhythm = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        pattern = params.get('rhythm_pattern', [1, 0, 1, 0, 1, 0, 1, 0])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            if pattern[i % len(pattern)]:
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                
                kick = np.sin(2 * np.pi * 60 * t) * np.exp(-5 * t)
                snare = np.random.random(note_duration) * np.exp(-3 * t)
                
                rhythm[beat_start:beat_end] = kick + snare * 0.5
        
        return rhythm
    
    def _generate_bass(self, params: Dict, beats_total: int, beats_per_second: float) -> np.ndarray:
        """Generate bass line"""
        bass = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        pattern = params.get('bass_pattern', [1, 0, 0, 0, 1, 0, 0, 0])
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            if pattern[i % len(pattern)]:
                chord_index = i % len(params['chord_progression'])
                root_note = chord_notes[chord_index][0] / 2
                
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                
                bass[beat_start:beat_end] = np.sin(2 * np.pi * root_note * t) * 0.4
        
        return bass
    
    def _get_chord_notes(self, chord_progression: List[str], key: str) -> List[List[float]]:
        """Get actual frequencies for chord progression"""
        chords = []
        for chord in chord_progression:
            if chord.endswith('m'):
                root_note = chord[:-1]
                chord_notes = [
                    self.note_frequencies.get(root_note, 261.63),
                    self.note_frequencies.get(self._shift_note(root_note, 3), 329.63),
                    self.note_frequencies.get(self._shift_note(root_note, 7), 392.00)
                ]
            elif chord.endswith('7'):
                root_note = chord[:-1]
                chord_notes = [
                    self.note_frequencies.get(root_note, 261.63),
                    self.note_frequencies.get(self._shift_note(root_note, 4), 349.23),
                    self.note_frequencies.get(self._shift_note(root_note, 7), 392.00),
                    self.note_frequencies.get(self._shift_note(root_note, 10), 466.16)
                ]
            else:
                chord_notes = [
                    self.note_frequencies.get(chord, 261.63),
                    self.note_frequencies.get(self._shift_note(chord, 4), 349.23),
                    self.note_frequencies.get(self._shift_note(chord, 7), 392.00)
                ]
            chords.append(chord_notes)
        
        return chords
    
    def _shift_note(self, note: str, semitones: int) -> str:
        """Shift note by semitones"""
        notes = list(self.note_frequencies.keys())
        try:
            current_index = notes.index(note)
            new_index = (current_index + semitones) % 12
            return notes[new_index]
        except ValueError:
            return note
    
    def _mix_layers(self, layers: List[np.ndarray], volumes: List[float]) -> np.ndarray:
        """Mix multiple audio layers"""
        mixed = np.zeros_like(layers[0])
        for layer, volume in zip(layers, volumes):
            mixed += layer * volume
        
        # Normalize
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.8
        
        return mixed
    
    def _apply_effects(self, audio: np.ndarray, params: Dict) -> np.ndarray:
        """Apply audio effects"""
        # Apply dynamic range
        dynamic_range = params.get('dynamic_range', 0.5)
        if dynamic_range < 1.0:
            audio = audio * (0.5 + dynamic_range * 0.5)
        
        # Final normalization
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.9
        
        return audio
    
    def _save_music(self, music_data: np.ndarray, genre: str, mood: str) -> str:
        """Save generated music to file"""
        try:
            os.makedirs('temp_audio', exist_ok=True)
            filename = f"temp_audio/music_{genre}_{mood}_{hash(str(music_data)) % 10000}.wav"
            sf.write(filename, music_data, self.sample_rate)
            return filename
        except Exception as e:
            logger.error(f"Error saving music: {e}")
            filename = f"temp_audio/music_{genre}_{mood}_fallback.wav"
            sf.write(filename, music_data, self.sample_rate)
            return filename
    
    def _generate_fallback_music(self, duration: int) -> str:
        """Generate simple fallback music when main method fails"""
        try:
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            audio = (np.sin(2 * np.pi * 261.63 * t) +
                    np.sin(2 * np.pi * 329.63 * t) +
                    np.sin(2 * np.pi * 392.00 * t))
            
            filename = f"temp_audio/music_fallback_{hash(str(audio)) % 10000}.wav"
            os.makedirs('temp_audio', exist_ok=True)
            sf.write(filename, audio, self.sample_rate)
            return filename
        except Exception as e:
            logger.error(f"Error generating fallback music: {e}")
            return None
    
    def get_available_genres(self) -> List[str]:
        """Get list of available music genres"""
        return self.available_genres
    
    def get_genre_info(self, genre: str) -> Dict[str, Any]:
        """Get detailed information about a specific genre"""
        if genre in self.genre_params:
            return self.genre_params[genre]
        else:
            return None
