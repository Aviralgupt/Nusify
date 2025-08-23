import os
import logging
import numpy as np
import soundfile as sf
from pydub import AudioSegment
from pydub.effects import normalize

logger = logging.getLogger(__name__)

class AudioMixer:
    """Audio mixing and mastering for final song creation"""

    def __init__(self):
        self.sample_rate = 44100
        self.bit_depth = 16

        # Enhanced mixing parameters
        self.default_mix_params = {
            'voice_volume': 0.8,      # Voice track volume
            'music_volume': 0.6,      # Background music volume
            'voice_pan': 0.0,         # Voice panning (0 = center)
            'music_pan': 0.0,         # Music panning
            'reverb': 0.2,            # Reverb amount
            'compression': 0.3,       # Compression amount
            'eq_low': 1.0,            # Low frequency boost
            'eq_mid': 1.0,            # Mid frequency boost
            'eq_high': 1.1,           # High frequency boost
            'mastering_limiter': 0.95, # Final limiting threshold
            'stereo_width': 1.1       # Stereo enhancement
        }

        # Enhanced genre-specific mixing presets
        self.genre_mix_presets = {
            'pop': {
                'voice_volume': 0.9,
                'music_volume': 0.7,
                'compression': 0.4,
                'eq_high': 1.2,
                'stereo_width': 1.2,
                'reverb': 0.15
            },
            'rock': {
                'voice_volume': 0.85,
                'music_volume': 0.8,
                'compression': 0.5,
                'eq_low': 1.3,
                'eq_high': 1.1,
                'stereo_width': 1.3
            },
            'electronic': {
                'voice_volume': 0.75,
                'music_volume': 0.85,
                'compression': 0.6,
                'eq_low': 1.4,
                'eq_high': 1.3,
                'stereo_width': 1.4
            },
            'jazz': {
                'voice_volume': 0.8,
                'music_volume': 0.65,
                'compression': 0.2,
                'eq_mid': 1.2,
                'reverb': 0.4,
                'stereo_width': 1.0
            },
            'classical': {
                'voice_volume': 0.7,
                'music_volume': 0.8,
                'compression': 0.1,
                'eq_low': 1.1,
                'eq_high': 1.1,
                'reverb': 0.6
            },
            'ambient': {
                'voice_volume': 0.6,
                'music_volume': 0.9,
                'compression': 0.1,
                'reverb': 0.8,
                'stereo_width': 1.5
            }
        }

    def mix_audio(self, voice_path, music_path, genre='pop', custom_params=None):
        """
        Mix voice and background music into final song

        Args:
            voice_path (str): Path to voice audio file
            music_path (str): Path to background music file
            genre (str): Music genre for mixing preset
            custom_params (dict): Custom mixing parameters

        Returns:
            str: Path to final mixed song
        """
        try:
            logger.info(f"Mixing audio: voice={voice_path}, music={music_path}, genre={genre}")

            # Load audio files
            voice_audio = self._load_audio(voice_path)
            music_audio = self._load_audio(music_path)

            if voice_audio is None or music_audio is None:
                raise Exception("Failed to load audio files")

            # Get mixing parameters
            mix_params = self._get_mix_params(genre, custom_params)

            # Process voice track
            processed_voice = self._process_voice(voice_audio, mix_params)

            # Process music track
            processed_music = self._process_music(music_audio, mix_params)

            # Synchronize tracks
            synced_voice, synced_music = self._synchronize_tracks(processed_voice, processed_music)

            # Mix tracks
            mixed_audio = self._mix_tracks(synced_voice, synced_music, mix_params)

            # Apply final mastering
            mastered_audio = self._master_audio(mixed_audio, mix_params)

            # Save final song
            output_path = self._save_song(mastered_audio, genre)

            logger.info(f"Audio mixing completed: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Error mixing audio: {e}")
            # Return a simple mixed version
            return self._create_simple_mix(voice_path, music_path)

    def _load_audio(self, file_path):
        """Load audio file and convert to numpy array"""
        try:
            if not os.path.exists(file_path):
                logger.error(f"Audio file not found: {file_path}")
                return None

            # Load audio using soundfile
            audio_data, sample_rate = sf.read(file_path)
            
            # Convert to mono if stereo
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Resample if needed
            if sample_rate != self.sample_rate:
                audio_data = self._resample_audio(audio_data, sample_rate, self.sample_rate)
            
            return audio_data

        except Exception as e:
            logger.error(f"Error loading audio {file_path}: {e}")
            return None

    def _resample_audio(self, audio, old_rate, new_rate):
        """Resample audio to new sample rate"""
        try:
            # Simple resampling using numpy
            if old_rate == new_rate:
                return audio
            
            # Calculate new length
            new_length = int(len(audio) * new_rate / old_rate)
            
            # Resample using linear interpolation
            old_indices = np.linspace(0, len(audio) - 1, len(audio))
            new_indices = np.linspace(0, len(audio) - 1, new_length)
            
            resampled = np.interp(new_indices, old_indices, audio)
            return resampled
            
        except Exception as e:
            logger.warning(f"Resampling failed: {e}")
            return audio

    def _get_mix_params(self, genre, custom_params):
        """Get mixing parameters for the genre"""
        # Start with default parameters
        params = self.default_mix_params.copy()
        
        # Apply genre-specific presets
        if genre in self.genre_mix_presets:
            params.update(self.genre_mix_presets[genre])
        
        # Apply custom parameters if provided
        if custom_params:
            params.update(custom_params)
        
        return params

    def _process_voice(self, voice_audio, mix_params):
        """Process voice track with effects"""
        processed = voice_audio.copy()
        
        # Apply EQ
        processed = self._apply_eq(processed, mix_params)
        
        # Apply compression
        if mix_params['compression'] > 0:
            processed = self._apply_compression(processed, mix_params['compression'])
        
        # Apply reverb
        if mix_params['reverb'] > 0:
            processed = self._apply_reverb(processed, mix_params['reverb'])
        
        # Apply volume
        processed *= mix_params['voice_volume']
        
        return processed

    def _process_music(self, music_audio, mix_params):
        """Process music track with effects"""
        processed = music_audio.copy()
        
        # Apply EQ
        processed = self._apply_eq(processed, mix_params)
        
        # Apply stereo width enhancement
        if mix_params['stereo_width'] > 1.0:
            processed = self._apply_stereo_width(processed, mix_params['stereo_width'])
        
        # Apply volume
        processed *= mix_params['music_volume']
        
        return processed

    def _apply_eq(self, audio, mix_params):
        """Apply equalization to audio"""
        try:
            # Simple EQ using frequency domain processing
            # Convert to frequency domain
            fft = np.fft.fft(audio)
            freqs = np.fft.fftfreq(len(audio), 1/self.sample_rate)
            
            # Apply EQ filters
            # Low frequencies (below 200 Hz)
            low_mask = np.abs(freqs) < 200
            fft[low_mask] *= mix_params['eq_low']
            
            # Mid frequencies (200 Hz - 2 kHz)
            mid_mask = (np.abs(freqs) >= 200) & (np.abs(freqs) < 2000)
            fft[mid_mask] *= mix_params['eq_mid']
            
            # High frequencies (above 2 kHz)
            high_mask = np.abs(freqs) >= 2000
            fft[high_mask] *= mix_params['eq_high']
            
            # Convert back to time domain
            processed = np.real(np.fft.ifft(fft))
            
            return processed
            
        except Exception as e:
            logger.warning(f"EQ processing failed: {e}")
            return audio

    def _apply_compression(self, audio, amount):
        """Apply dynamic range compression"""
        try:
            # Simple compression using threshold and ratio
            threshold = 0.5
            ratio = 1 + (amount * 3)  # Ratio from 1:1 to 4:1
            
            # Find peaks above threshold
            peaks = np.abs(audio) > threshold
            
            # Apply compression
            compressed = audio.copy()
            compressed[peaks] = np.sign(compressed[peaks]) * (
                threshold + (np.abs(compressed[peaks]) - threshold) / ratio
            )
            
            return compressed
            
        except Exception as e:
            logger.warning(f"Compression failed: {e}")
            return audio

    def _apply_reverb(self, audio, amount):
        """Apply reverb effect"""
        try:
            # Simple reverb using delay and decay
            delay_samples = int(0.1 * self.sample_rate)  # 100ms delay
            decay = 0.3 * amount
            
            # Create delayed signal
            delayed = np.zeros_like(audio)
            delayed[delay_samples:] = audio[:-delay_samples] * decay
            
            # Add more delays for longer reverb
            delayed2 = np.zeros_like(audio)
            delayed2[delay_samples * 2:] = audio[:-delay_samples * 2] * (decay ** 2)
            
            # Combine original and reverb
            reverb_audio = audio + delayed + delayed2
            
            # Normalize
            max_val = np.max(np.abs(reverb_audio))
            if max_val > 0:
                reverb_audio = reverb_audio / max_val * 0.9
            
            return reverb_audio
            
        except Exception as e:
            logger.warning(f"Reverb failed: {e}")
            return audio

    def _apply_stereo_width(self, audio, width):
        """Apply stereo width enhancement"""
        try:
            # Convert mono to stereo-like effect
            # Create left and right channels with slight differences
            left = audio.copy()
            right = audio.copy()
            
            # Add slight phase shift to right channel
            phase_shift = int(0.001 * self.sample_rate)  # 1ms shift
            right = np.roll(right, phase_shift)
            
            # Apply width enhancement
            left = left * (1 + (width - 1) * 0.5)
            right = right * (1 + (width - 1) * 0.5)
            
            # Combine channels
            stereo = np.column_stack((left, right))
            
            # Convert back to mono by averaging
            return np.mean(stereo, axis=1)
            
        except Exception as e:
            logger.warning(f"Stereo width failed: {e}")
            return audio

    def _synchronize_tracks(self, voice_audio, music_audio):
        """Synchronize voice and music tracks"""
        try:
            # Ensure both tracks have the same length
            max_length = max(len(voice_audio), len(music_audio))
            
            # Pad shorter track with silence
            if len(voice_audio) < max_length:
                voice_audio = np.pad(voice_audio, (0, max_length - len(voice_audio)), 'constant')
            
            if len(music_audio) < max_length:
                music_audio = np.pad(music_audio, (0, max_length - len(music_audio)), 'constant')
            
            return voice_audio, music_audio
            
        except Exception as e:
            logger.warning(f"Track synchronization failed: {e}")
            return voice_audio, music_audio

    def _mix_tracks(self, voice_audio, music_audio, mix_params):
        """Mix voice and music tracks together"""
        try:
            # Simple mixing with volume control
            mixed = voice_audio + music_audio
            
            # Normalize to prevent clipping
            max_val = np.max(np.abs(mixed))
            if max_val > 0:
                mixed = mixed / max_val * 0.8
            
            return mixed
            
        except Exception as e:
            logger.warning(f"Track mixing failed: {e}")
            return voice_audio + music_audio

    def _master_audio(self, audio, mix_params):
        """Apply final mastering effects"""
        try:
            mastered = audio.copy()
            
            # Apply final limiting
            limit_threshold = mix_params['mastering_limiter']
            peaks = np.abs(mastered) > limit_threshold
            
            if np.any(peaks):
                mastered[peaks] = np.sign(mastered[peaks]) * limit_threshold
            
            # Final normalization
            max_val = np.max(np.abs(mastered))
            if max_val > 0:
                mastered = mastered / max_val * 0.95
            
            return mastered
            
        except Exception as e:
            logger.warning(f"Mastering failed: {e}")
            return audio

    def _save_song(self, audio_data, genre):
        """Save the final mixed song"""
        try:
            # Create output directory
            os.makedirs('generated_songs', exist_ok=True)
            
            # Generate filename
            filename = f"generated_songs/nusify_song_{genre}_{hash(str(audio_data)) % 10000}.wav"
            
            # Save audio
            sf.write(filename, audio_data, self.sample_rate)
            
            return filename
            
        except Exception as e:
            logger.error(f"Error saving song: {e}")
            # Fallback filename
            filename = f"generated_songs/nusify_song_{genre}_fallback.wav"
            sf.write(filename, audio_data, self.sample_rate)
            return filename

    def _create_simple_mix(self, voice_path, music_path):
        """Create a simple mixed version when main mixing fails"""
        try:
            # Load audio files
            voice_audio = self._load_audio(voice_path)
            music_audio = self._load_audio(music_path)
            
            if voice_audio is None or music_audio is None:
                return None
            
            # Simple mixing
            max_length = max(len(voice_audio), len(music_audio))
            
            # Pad tracks to same length
            if len(voice_audio) < max_length:
                voice_audio = np.pad(voice_audio, (0, max_length - len(voice_audio)), 'constant')
            if len(music_audio) < max_length:
                music_audio = np.pad(music_audio, (0, max_length - len(music_audio)), 'constant')
            
            # Mix with basic volumes
            mixed = voice_audio * 0.7 + music_audio * 0.5
            
            # Normalize
            max_val = np.max(np.abs(mixed))
            if max_val > 0:
                mixed = mixed / max_val * 0.8
            
            # Save
            filename = f"generated_songs/nusify_song_simple_mix_{hash(str(mixed)) % 10000}.wav"
            os.makedirs('generated_songs', exist_ok=True)
            sf.write(filename, mixed, self.sample_rate)
            
            return filename
            
        except Exception as e:
            logger.error(f"Simple mixing failed: {e}")
            return None
    
    def get_mix_presets(self):
        """Get available mixing presets"""
        return {
            'default': self.default_mix_params,
            'genre_presets': self.genre_mix_presets
        }
    
    def create_custom_preset(self, name, parameters):
        """Create a custom mixing preset"""
        self.genre_mix_presets[name] = parameters
        logger.info(f"Created custom preset: {name}")
    
    def remove_preset(self, name):
        """Remove a mixing preset"""
        if name in self.genre_mix_presets and name not in ['pop', 'rock', 'ballad']:
            del self.genre_mix_presets[name]
            logger.info(f"Removed preset: {name}")
        else:
            logger.warning(f"Cannot remove preset: {name}")
