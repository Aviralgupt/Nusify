import os
import logging
import tempfile
import numpy as np
from scipy.io import wavfile
import librosa
import soundfile as sf

logger = logging.getLogger(__name__)

class MusicGenerator:
    """AI-powered music generator for background music"""

    def __init__(self):
        self.sample_rate = 44100
        self.available_genres = [
            'pop', 'rock', 'electronic', 'jazz', 'classical', 'country',
            'r&b', 'hip-hop', 'ambient', 'orchestral', 'indie', 'ballad',
            'dance', 'atmospheric', 'folk', 'blues', 'reggae', 'punk'
        ]

        # Enhanced genre-specific parameters
        self.genre_params = {
            'pop': {
                'tempo': 120,
                'key': 'C',
                'chord_progression': ['C', 'G', 'Am', 'F'],
                'instruments': ['piano', 'drums', 'bass', 'synth'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],  # 4/4 beat
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'rock': {
                'tempo': 140,
                'key': 'E',
                'chord_progression': ['E', 'A', 'B', 'C#m'],
                'instruments': ['electric_guitar', 'drums', 'bass'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'electronic': {
                'tempo': 128,
                'key': 'Am',
                'chord_progression': ['Am', 'F', 'C', 'G'],
                'instruments': ['synth', 'drums', 'bass', 'effects'],
                'rhythm_pattern': [1, 0, 1, 0, 1, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'jazz': {
                'tempo': 90,
                'key': 'F',
                'chord_progression': ['F', 'Bbm7', 'Eb7', 'Abmaj7'],
                'instruments': ['piano', 'saxophone', 'bass', 'drums'],
                'rhythm_pattern': [1, 0, 0, 1, 0, 0, 1, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'classical': {
                'tempo': 80,
                'key': 'D',
                'chord_progression': ['D', 'A', 'Bm', 'G'],
                'instruments': ['strings', 'piano', 'woodwinds'],
                'rhythm_pattern': [1, 0, 0, 0, 1, 0, 0, 0],
                'bass_pattern': [1, 0, 0, 0, 1, 0, 0, 0]
            },
            'ambient': {
                'tempo': 60,
                'key': 'Dm',
                'chord_progression': ['Dm', 'Am', 'C', 'G'],
                'instruments': ['pad', 'atmosphere', 'texture'],
                'rhythm_pattern': [1, 0, 0, 0, 0, 0, 0, 0],
                'bass_pattern': [1, 0, 0, 0, 0, 0, 0, 0]
            }
        }

        # Enhanced mood modifications
        self.mood_modifications = {
            'happy': {
                'tempo_multiplier': 1.2,
                'key_shift': 2,  # Major key
                'brightness': 1.3,
                'reverb': 0.3,
                'chord_type': 'major',
                'energy_boost': 1.4
            },
            'sad': {
                'tempo_multiplier': 0.8,
                'key_shift': -3,  # Minor key
                'brightness': 0.7,
                'reverb': 0.8,
                'chord_type': 'minor',
                'energy_boost': 0.6
            },
            'energetic': {
                'tempo_multiplier': 1.5,
                'key_shift': 0,
                'brightness': 1.5,
                'reverb': 0.2,
                'chord_type': 'power',
                'energy_boost': 1.8
            },
            'calm': {
                'tempo_multiplier': 0.6,
                'key_shift': -2,
                'brightness': 0.8,
                'reverb': 1.0,
                'chord_type': 'suspended',
                'energy_boost': 0.5
            },
            'romantic': {
                'tempo_multiplier': 0.9,
                'key_shift': 1,
                'brightness': 1.1,
                'reverb': 0.6,
                'chord_type': 'major7',
                'energy_boost': 1.2
            },
            'mysterious': {
                'tempo_multiplier': 0.7,
                'key_shift': -1,
                'brightness': 0.5,
                'reverb': 1.2,
                'chord_type': 'diminished',
                'energy_boost': 0.8
            }
        }

        # Musical note frequencies
        self.note_frequencies = {
            'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
            'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
            'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
        }

    def generate(self, mood, genre, duration):
        """
        Generate background music based on mood and genre

        Args:
            mood (str): The mood of the music
            genre (str): The music genre
            duration (int): Duration in seconds

        Returns:
            str: Path to generated music file
        """
        try:
            logger.info(f"Generating {genre} music with {mood} mood for {duration} seconds")

            # Get genre parameters
            if genre not in self.genre_params:
                genre = 'pop'  # Default fallback

            base_params = self.genre_params[genre].copy()

            # Apply mood modifications
            mood_mods = self.mood_modifications.get(mood, {})
            modified_params = self._apply_mood_modifications(base_params, mood_mods)

            # Generate the music
            music_data = self._generate_music_data(modified_params, duration)

            # Save to file
            output_path = self._save_music(music_data, genre, mood)

            logger.info(f"Music generated successfully: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error generating music: {e}")
            # Return a simple fallback music
            return self._generate_fallback_music(duration)

    def _apply_mood_modifications(self, base_params, mood_mods):
        """Apply mood-based modifications to music parameters"""
        modified = base_params.copy()
        
        # Apply tempo modification
        if 'tempo_multiplier' in mood_mods:
            modified['tempo'] = int(base_params['tempo'] * mood_mods['tempo_multiplier'])
        
        # Apply key shift
        if 'key_shift' in mood_mods:
            current_key = base_params['key']
            modified['key'] = self._shift_key(current_key, mood_mods['key_shift'])
        
        # Apply chord type modification
        if 'chord_type' in mood_mods:
            modified['chord_type'] = mood_mods['chord_type']
        
        # Apply energy boost
        if 'energy_boost' in mood_mods:
            modified['energy_boost'] = mood_mods['energy_boost']
        
        return modified

    def _shift_key(self, key, semitones):
        """Shift musical key by semitones"""
        notes = list(self.note_frequencies.keys())
        try:
            current_index = notes.index(key)
            new_index = (current_index + semitones) % 12
            return notes[new_index]
        except ValueError:
            return key

    def _generate_music_data(self, params, duration):
        """Generate musical audio data"""
        # Calculate timing
        beats_per_second = params['tempo'] / 60
        beats_total = int(duration * beats_per_second)
        
        # Generate different layers
        melody = self._generate_melody(params, beats_total, beats_per_second)
        harmony = self._generate_harmony(params, beats_total, beats_per_second)
        rhythm = self._generate_rhythm(params, beats_total, beats_per_second)
        bass = self._generate_bass(params, beats_total, beats_per_second)
        
        # Mix layers
        mixed = self._mix_layers([melody, harmony, rhythm, bass], [0.3, 0.4, 0.2, 0.3])
        
        # Apply effects
        mixed = self._apply_effects(mixed, params)
        
        return mixed

    def _generate_melody(self, params, beats_total, beats_per_second):
        """Generate melodic line"""
        melody = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        # Create melodic pattern based on chord progression
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            # Choose note from current chord
            chord_index = i % len(params['chord_progression'])
            note = chord_notes[chord_index][i % len(chord_notes[chord_index])]
            
            # Generate note
            note_duration = beat_end - beat_start
            t = np.linspace(0, note_duration / self.sample_rate, note_duration)
            frequency = note * (2 ** (np.random.randint(-1, 2)))  # Add octave variation
            
            melody[beat_start:beat_end] = np.sin(2 * np.pi * frequency * t) * 0.3
        
        return melody

    def _generate_harmony(self, params, beats_total, beats_per_second):
        """Generate harmonic accompaniment"""
        harmony = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            chord_index = i % len(params['chord_progression'])
            chord = chord_notes[chord_index]
            
            # Play full chord
            for note in chord:
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                harmony[beat_start:beat_end] += np.sin(2 * np.pi * note * t) * 0.2
        
        return harmony

    def _generate_rhythm(self, params, beats_total, beats_per_second):
        """Generate rhythmic pattern"""
        rhythm = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        pattern = params.get('rhythm_pattern', [1, 0, 1, 0, 1, 0, 1, 0])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            if pattern[i % len(pattern)]:
                # Generate drum hit
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                
                # Kick drum (low frequency)
                kick = np.sin(2 * np.pi * 60 * t) * np.exp(-5 * t)
                # Snare (noise-like)
                snare = np.random.random(note_duration) * np.exp(-3 * t)
                
                rhythm[beat_start:beat_end] = kick + snare * 0.5
        
        return rhythm

    def _generate_bass(self, params, beats_total, beats_per_second):
        """Generate bass line"""
        bass = np.zeros(int(beats_total / beats_per_second * self.sample_rate))
        
        pattern = params.get('bass_pattern', [1, 0, 0, 0, 1, 0, 0, 0])
        chord_notes = self._get_chord_notes(params['chord_progression'], params['key'])
        
        for i in range(beats_total):
            beat_start = int(i / beats_per_second * self.sample_rate)
            beat_end = int((i + 1) / beats_per_second * self.sample_rate)
            
            if pattern[i % len(pattern)]:
                chord_index = i % len(params['chord_progression'])
                root_note = chord_notes[chord_index][0] / 2  # Lower octave
                
                note_duration = beat_end - beat_start
                t = np.linspace(0, note_duration / self.sample_rate, note_duration)
                
                bass[beat_start:beat_end] = np.sin(2 * np.pi * root_note * t) * 0.4
        
        return bass

    def _get_chord_notes(self, chord_progression, key):
        """Get actual frequencies for chord progression"""
        chords = []
        for chord in chord_progression:
            if chord.endswith('m'):  # Minor chord
                root_note = chord[:-1]
                chord_notes = [
                    self.note_frequencies.get(root_note, 261.63),
                    self.note_frequencies.get(self._shift_note(root_note, 3), 329.63),
                    self.note_frequencies.get(self._shift_note(root_note, 7), 392.00)
                ]
            elif chord.endswith('7'):  # Seventh chord
                root_note = chord[:-1]
                chord_notes = [
                    self.note_frequencies.get(root_note, 261.63),
                    self.note_frequencies.get(self._shift_note(root_note, 4), 349.23),
                    self.note_frequencies.get(self._shift_note(root_note, 7), 392.00),
                    self.note_frequencies.get(self._shift_note(root_note, 10), 466.16)
                ]
            else:  # Major chord
                chord_notes = [
                    self.note_frequencies.get(chord, 261.63),
                    self.note_frequencies.get(self._shift_note(chord, 4), 349.23),
                    self.note_frequencies.get(self._shift_note(chord, 7), 392.00)
                ]
            chords.append(chord_notes)
        
        return chords

    def _shift_note(self, note, semitones):
        """Shift note by semitones"""
        notes = list(self.note_frequencies.keys())
        try:
            current_index = notes.index(note)
            new_index = (current_index + semitones) % 12
            return notes[new_index]
        except ValueError:
            return note

    def _mix_layers(self, layers, volumes):
        """Mix multiple audio layers"""
        mixed = np.zeros_like(layers[0])
        for layer, volume in zip(layers, volumes):
            mixed += layer * volume
        
        # Normalize
        max_val = np.max(np.abs(mixed))
        if max_val > 0:
            mixed = mixed / max_val * 0.8
        
        return mixed

    def _apply_effects(self, audio, params):
        """Apply audio effects"""
        # Reverb effect
        if 'reverb' in params:
            reverb_amount = params.get('reverb', 0.2)
            reverb_delay = int(0.1 * self.sample_rate)  # 100ms delay
            reverb_signal = np.zeros_like(audio)
            reverb_signal[reverb_delay:] = audio[:-reverb_delay] * reverb_amount
            audio = audio + reverb_signal
        
        # Energy boost
        if 'energy_boost' in params:
            audio = audio * params['energy_boost']
        
        # Final normalization
        max_val = np.max(np.abs(audio))
        if max_val > 0:
            audio = audio / max_val * 0.9
        
        return audio

    def _save_music(self, music_data, genre, mood):
        """Save generated music to file"""
        try:
            # Create temp directory if it doesn't exist
            os.makedirs('temp_audio', exist_ok=True)
            
            # Generate filename
            filename = f"temp_audio/music_{genre}_{mood}_{hash(str(music_data)) % 10000}.wav"
            
            # Save audio
            sf.write(filename, music_data, self.sample_rate)
            
            return filename
            
        except Exception as e:
            logger.error(f"Error saving music: {e}")
            # Fallback to simple filename
            filename = f"temp_audio/music_{genre}_{mood}_fallback.wav"
            sf.write(filename, music_data, self.sample_rate)
            return filename

    def _generate_fallback_music(self, duration):
        """Generate simple fallback music when main method fails"""
        try:
            # Simple chord progression
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            
            # C major chord
            audio = (np.sin(2 * np.pi * 261.63 * t) +  # C
                    np.sin(2 * np.pi * 329.63 * t) +  # E
                    np.sin(2 * np.pi * 392.00 * t))   # G
            
            # Add some rhythm
            rhythm = np.zeros_like(t)
            for i in range(int(duration * 2)):  # 2 beats per second
                start = int(i * self.sample_rate / 2)
                end = start + int(self.sample_rate * 0.1)
                if end < len(rhythm):
                    rhythm[start:end] = 0.3
            
            audio = audio * 0.3 + rhythm
            
            filename = f"temp_audio/music_fallback_{hash(str(audio)) % 10000}.wav"
            os.makedirs('temp_audio', exist_ok=True)
            sf.write(filename, audio, self.sample_rate)
            
            return filename
            
        except Exception as e:
            logger.error(f"Error generating fallback music: {e}")
            return None
    
    def get_available_genres(self):
        """Get list of available music genres"""
        return self.available_genres
    
    def get_genre_info(self, genre):
        """Get detailed information about a specific genre"""
        if genre in self.genre_params:
            return self.genre_params[genre]
        else:
            return None
