import os
import logging
import google.generativeai as genai
from typing import Dict, List, Any
import json
import numpy as np
import soundfile as sf
import re

logger = logging.getLogger(__name__)

class GeminiVoiceCloner:
    """AI-powered voice cloning using Google Gemini API for voice characteristics"""
    
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
        
        self.sample_rate = 22050
        self.available_voices = [
            'default', 'pop_female', 'pop_male', 'rock_male', 'country_female',
            'jazz_male', 'classical_female', 'rap_male', 'indie_female', 'soul_female'
        ]
        
        # Enhanced voice characteristics for different artists
        self.voice_profiles = {
            'default': {
                'pitch': 0, 'speed': 1.0, 'energy': 1.0, 'tone': 'neutral',
                'formant_shift': 0, 'breathiness': 0.1, 'vibrato': 0.05
            },
            'pop_female': {
                'pitch': 2, 'speed': 1.1, 'energy': 1.2, 'tone': 'bright',
                'formant_shift': 1.2, 'breathiness': 0.15, 'vibrato': 0.08
            },
            'pop_male': {
                'pitch': -2, 'speed': 0.9, 'energy': 1.1, 'tone': 'smooth',
                'formant_shift': 0.8, 'breathiness': 0.1, 'vibrato': 0.06
            },
            'rock_male': {
                'pitch': -3, 'speed': 0.8, 'energy': 1.5, 'tone': 'gritty',
                'formant_shift': 0.7, 'breathiness': 0.25, 'vibrato': 0.12
            },
            'country_female': {
                'pitch': 1, 'speed': 0.95, 'energy': 1.0, 'tone': 'warm',
                'formant_shift': 1.1, 'breathiness': 0.2, 'vibrato': 0.1
            },
            'jazz_male': {
                'pitch': -1, 'speed': 0.85, 'energy': 0.9, 'tone': 'smooth',
                'formant_shift': 0.9, 'breathiness': 0.15, 'vibrato': 0.15
            },
            'classical_female': {
                'pitch': 0, 'speed': 0.9, 'energy': 0.8, 'tone': 'refined',
                'formant_shift': 1.0, 'breathiness': 0.05, 'vibrato': 0.2
            },
            'rap_male': {
                'pitch': -1, 'speed': 1.3, 'energy': 1.4, 'tone': 'rhythmic',
                'formant_shift': 0.6, 'breathiness': 0.3, 'vibrato': 0.02
            },
            'indie_female': {
                'pitch': 1, 'speed': 1.0, 'energy': 0.9, 'tone': 'unique',
                'formant_shift': 1.05, 'breathiness': 0.18, 'vibrato': 0.07
            },
            'soul_female': {
                'pitch': 2, 'speed': 0.95, 'energy': 1.1, 'tone': 'rich',
                'formant_shift': 1.15, 'breathiness': 0.12, 'vibrato': 0.18
            }
        }
    
    def clone_voice(self, lyrics: str, artist_voice: str) -> str:
        """
        Clone voice for the given lyrics using Gemini for voice characteristics
        
        Args:
            lyrics (str): The lyrics to convert to speech
            artist_voice (str): The voice style to use
            
        Returns:
            str: Path to generated voice file
        """
        try:
            logger.info(f"Cloning voice for {artist_voice} style")
            
            # Clean and preprocess lyrics
            processed_lyrics = self._preprocess_lyrics(lyrics)
            
            # Get voice profile
            voice_profile = self.voice_profiles.get(artist_voice, self.voice_profiles['default'])
            
            # Get enhanced voice characteristics from Gemini
            enhanced_profile = self._get_enhanced_voice_profile(artist_voice, processed_lyrics)
            
            # Merge profiles
            final_profile = {**voice_profile, **enhanced_profile}
            
            # Generate speech-like audio with enhanced patterns
            audio_data = self._generate_enhanced_speech(processed_lyrics, final_profile)
            
            # Apply voice modifications
            modified_audio = self._apply_voice_modifications(audio_data, final_profile)
            
            # Save to file
            output_path = self._save_voice(modified_audio, artist_voice)
            
            logger.info(f"Voice generated successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error cloning voice: {e}")
            return self._generate_fallback_voice(lyrics)
    
    def _get_enhanced_voice_profile(self, artist_voice: str, lyrics: str) -> Dict[str, Any]:
        """Get enhanced voice characteristics from Gemini API"""
        try:
            if not self.api_available:
                return {}
            
            prompt = f"""
Analyze the following lyrics and suggest voice characteristics for a {artist_voice} style performance.

Lyrics: "{lyrics}"

Return a JSON object with voice characteristics:
{{
    "pitch_modifier": -3 to 3,
    "speed_modifier": 0.5 to 1.5,
    "energy_modifier": 0.5 to 1.5,
    "tone_enhancement": "bright", "warm", "gritty", "smooth", "refined", "rhythmic", "unique", "rich",
    "formant_shift": 0.5 to 1.5,
    "breathiness_modifier": 0.0 to 0.5,
    "vibrato_modifier": 0.0 to 0.3,
    "emotional_expression": "subtle", "moderate", "intense",
    "articulation_style": "crisp", "smooth", "slurred", "precise",
    "performance_notes": "brief description of the vocal approach"
}}

Consider the lyrics content, emotional tone, and the {artist_voice} style.
Return only the JSON object.
"""
            
            response = self.model.generate_content(prompt)
            return self._parse_voice_response(response.text)
            
        except Exception as e:
            logger.error(f"Error getting enhanced voice profile: {e}")
            return {}
    
    def _parse_voice_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's voice characteristics response"""
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
            logger.error(f"Error parsing voice response: {e}")
            return {}
    
    def _preprocess_lyrics(self, lyrics: str) -> str:
        """Clean and preprocess lyrics for better processing"""
        cleaned = re.sub(r'[^\w\s]', ' ', lyrics)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _generate_enhanced_speech(self, lyrics: str, voice_profile: Dict) -> np.ndarray:
        """Generate enhanced speech-like audio patterns"""
        # Calculate duration based on word count and speed
        word_count = len(lyrics.split())
        base_duration = word_count * 0.6
        speed_modifier = voice_profile.get('speed_modifier', 1.0)
        duration = base_duration / (voice_profile['speed'] * speed_modifier)
        
        # Generate time array
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        
        # Base frequency with pitch modifications
        base_pitch = voice_profile['pitch']
        pitch_modifier = voice_profile.get('pitch_modifier', 0)
        final_pitch = base_pitch + pitch_modifier
        base_freq = 220 * (2 ** (final_pitch / 12))
        
        # Generate main voice signal
        voice_signal = self._generate_voice_signal(t, base_freq, voice_profile)
        
        # Add formant structure
        formant_signal = self._add_formants(t, voice_profile)
        
        # Add breathiness
        breath_signal = self._add_breathiness(t, voice_profile)
        
        # Add vibrato
        vibrato_signal = self._add_vibrato(t, base_freq, voice_profile)
        
        # Combine all signals
        combined = voice_signal + formant_signal + breath_signal + vibrato_signal
        
        # Apply energy modifiers
        energy_modifier = voice_profile.get('energy_modifier', 1.0)
        combined *= voice_profile['energy'] * energy_modifier
        
        return combined
    
    def _generate_voice_signal(self, t: np.ndarray, base_freq: float, voice_profile: Dict) -> np.ndarray:
        """Generate the main voice signal"""
        fundamental = np.sin(2 * np.pi * base_freq * t)
        
        # Add harmonics for richness
        harmonic1 = np.sin(2 * np.pi * base_freq * 2 * t) * 0.5
        harmonic2 = np.sin(2 * np.pi * base_freq * 3 * t) * 0.3
        harmonic3 = np.sin(2 * np.pi * base_freq * 4 * t) * 0.2
        
        voice = fundamental + harmonic1 + harmonic2 + harmonic3
        
        # Apply envelope
        envelope = self._create_envelope(len(t))
        voice *= envelope
        
        return voice
    
    def _add_formants(self, t: np.ndarray, voice_profile: Dict) -> np.ndarray:
        """Add formant structure for vowel-like characteristics"""
        formant_shift = voice_profile.get('formant_shift', 1.0)
        formant_modifier = voice_profile.get('formant_shift', 1.0)
        final_shift = formant_shift * formant_modifier
        
        formant1 = 800 * final_shift
        formant2 = 1200 * final_shift
        formant3 = 2500 * final_shift
        
        f1 = np.sin(2 * np.pi * formant1 * t) * 0.2
        f2 = np.sin(2 * np.pi * formant2 * t) * 0.15
        f3 = np.sin(2 * np.pi * formant3 * t) * 0.1
        
        formants = f1 + f2 + f3
        envelope = self._create_envelope(len(t))
        formants *= envelope
        
        return formants
    
    def _add_breathiness(self, t: np.ndarray, voice_profile: Dict) -> np.ndarray:
        """Add breathiness to the voice"""
        breath_amount = voice_profile.get('breathiness', 0.1)
        breath_modifier = voice_profile.get('breathiness_modifier', 0.0)
        final_breath = breath_amount + breath_modifier
        
        breath = np.random.normal(0, 1, len(t))
        breath = np.convolve(breath, np.ones(100)/100, mode='same')
        
        envelope = self._create_envelope(len(t))
        breath = breath * envelope * final_breath
        
        return breath
    
    def _add_vibrato(self, t: np.ndarray, base_freq: float, voice_profile: Dict) -> np.ndarray:
        """Add vibrato (pitch modulation)"""
        vibrato_amount = voice_profile.get('vibrato', 0.05)
        vibrato_modifier = voice_profile.get('vibrato_modifier', 0.0)
        final_vibrato = vibrato_amount + vibrato_modifier
        
        vibrato_rate = 5.5
        vibrato_mod = np.sin(2 * np.pi * vibrato_rate * t) * final_vibrato
        vibrato_signal = np.sin(2 * np.pi * base_freq * 1.5 * t) * vibrato_mod * 0.1
        
        return vibrato_signal
    
    def _create_envelope(self, signal_length: int) -> np.ndarray:
        """Create an envelope for natural sound"""
        attack_samples = int(0.1 * signal_length)
        decay_samples = int(0.2 * signal_length)
        
        envelope = np.ones(signal_length)
        
        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        if decay_samples > 0:
            envelope[-decay_samples:] = np.linspace(1, 0, decay_samples)
        
        return envelope
    
    def _apply_voice_modifications(self, audio_data: np.ndarray, voice_profile: Dict) -> np.ndarray:
        """Apply voice modifications based on profile"""
        # Apply speed modification
        speed_modifier = voice_profile.get('speed_modifier', 1.0)
        if speed_modifier != 1.0:
            new_length = int(len(audio_data) / speed_modifier)
            audio_data = np.interp(
                np.linspace(0, len(audio_data), new_length),
                np.arange(len(audio_data)),
                audio_data
            )
        
        # Apply tone modifications
        tone_enhancement = voice_profile.get('tone_enhancement', voice_profile.get('tone', 'neutral'))
        
        if tone_enhancement == 'bright':
            t = np.linspace(0, len(audio_data) / self.sample_rate, len(audio_data))
            audio_data += 0.2 * np.sin(2 * np.pi * 1000 * t)
        elif tone_enhancement == 'warm':
            t = np.linspace(0, len(audio_data) / self.sample_rate, len(audio_data))
            audio_data += 0.2 * np.sin(2 * np.pi * 100 * t)
        elif tone_enhancement == 'gritty':
            audio_data += 0.1 * np.tanh(audio_data * 2)
        elif tone_enhancement == 'smooth':
            audio_data = np.convolve(audio_data, np.ones(50)/50, mode='same')
        
        # Apply articulation style
        articulation = voice_profile.get('articulation_style', 'smooth')
        if articulation == 'crisp':
            # Add sharp attacks
            pass  # Implement crisp articulation
        elif articulation == 'slurred':
            # Apply smoothing
            audio_data = np.convolve(audio_data, np.ones(100)/100, mode='same')
        
        # Normalize audio
        max_val = np.max(np.abs(audio_data))
        if max_val > 0:
            audio_data = audio_data / max_val * 0.8
        
        return audio_data
    
    def _save_voice(self, audio_data: np.ndarray, artist_voice: str) -> str:
        """Save generated voice audio to file"""
        try:
            os.makedirs('temp_audio', exist_ok=True)
            filename = f"temp_audio/voice_{artist_voice}_{hash(str(audio_data)) % 10000}.wav"
            sf.write(filename, audio_data, self.sample_rate)
            return filename
        except Exception as e:
            logger.error(f"Error saving voice: {e}")
            filename = f"temp_audio/voice_{artist_voice}_fallback.wav"
            sf.write(filename, audio_data, self.sample_rate)
            return filename
    
    def _generate_fallback_voice(self, lyrics: str) -> str:
        """Generate a simple fallback voice when main method fails"""
        try:
            duration = len(lyrics.split()) * 0.4
            t = np.linspace(0, duration, int(self.sample_rate * duration), False)
            
            audio = np.sin(2 * np.pi * 440 * t)
            audio += 0.3 * np.sin(2 * np.pi * 660 * t)
            audio += 0.2 * np.sin(2 * np.pi * 880 * t)
            
            filename = f"temp_audio/voice_fallback_{hash(lyrics) % 10000}.wav"
            os.makedirs('temp_audio', exist_ok=True)
            sf.write(filename, audio, self.sample_rate)
            return filename
        except Exception as e:
            logger.error(f"Error generating fallback voice: {e}")
            return None
    
    def get_available_voices(self) -> List[str]:
        """Get list of available artist voices"""
        return self.available_voices
    
    def get_voice_info(self, voice_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific voice"""
        if voice_name in self.voice_profiles:
            return self.voice_profiles[voice_name]
        else:
            return None
