import os
import logging
import google.generativeai as genai
from typing import Dict, List, Any
import json
import re

logger = logging.getLogger(__name__)

class GeminiMoodAnalyzer:
    """AI-powered mood analyzer using Google Gemini API"""
    
    def __init__(self):
        # Initialize Gemini API
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.warning("GEMINI_API_KEY not found in environment variables")
            # For development, you can set it here temporarily
            # api_key = "your-api-key-here"
        
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.api_available = True
        else:
            self.api_available = False
            logger.error("Gemini API not configured")
        
        # Mood to genre mapping
        self.mood_genre_map = {
            'happy': 'pop',
            'sad': 'ballad',
            'angry': 'rock',
            'energetic': 'electronic',
            'romantic': 'r&b',
            'melancholic': 'indie',
            'upbeat': 'dance',
            'calm': 'ambient',
            'dramatic': 'orchestral',
            'mysterious': 'atmospheric',
            'neutral': 'pop'
        }
    
    def analyze(self, lyrics: str) -> Dict[str, Any]:
        """
        Analyze lyrics to determine mood, emotions, and suggested genre using Gemini
        
        Args:
            lyrics (str): The lyrics to analyze
            
        Returns:
            dict: Analysis results with mood, confidence, emotions, and suggested genre
        """
        try:
            if not self.api_available:
                return self._fallback_analysis(lyrics)
            
            # Clean lyrics
            cleaned_lyrics = self._clean_lyrics(lyrics)
            
            # Create prompt for Gemini
            prompt = self._create_analysis_prompt(cleaned_lyrics)
            
            # Get response from Gemini
            response = self.model.generate_content(prompt)
            
            # Parse the response
            analysis_result = self._parse_gemini_response(response.text)
            
            # Add confidence calculation
            analysis_result['confidence'] = self._calculate_confidence(analysis_result)
            
            # Add suggested genre
            analysis_result['suggested_genre'] = self.mood_genre_map.get(
                analysis_result['mood'], 'pop'
            )
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing mood with Gemini: {e}")
            return self._fallback_analysis(lyrics)
    
    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean and preprocess lyrics"""
        # Remove special characters but keep spaces and basic punctuation
        cleaned = re.sub(r'[^\w\s.,!?\'"-]', ' ', lyrics)
        # Convert to lowercase
        cleaned = cleaned.lower()
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    def _create_analysis_prompt(self, lyrics: str) -> str:
        """Create a detailed prompt for Gemini analysis"""
        return f"""
Analyze the following song lyrics and provide a detailed mood analysis in JSON format.

Lyrics: "{lyrics}"

Please analyze and return a JSON object with the following structure:
{{
    "mood": "primary mood (happy, sad, angry, energetic, romantic, melancholic, upbeat, calm, dramatic, mysterious, neutral)",
    "emotions": [
        {{"emotion": "emotion_name", "intensity": 0.0-1.0}},
        {{"emotion": "emotion_name", "intensity": 0.0-1.0}}
    ],
    "sentiment_score": -1.0 to 1.0,
    "energy_level": 0.0 to 1.0,
    "themes": ["theme1", "theme2", "theme3"],
    "analysis_notes": "brief explanation of the analysis"
}}

Consider:
- Overall emotional tone and mood
- Specific emotions present
- Energy and intensity level
- Main themes and topics
- Sentiment polarity (positive/negative)
- Musical style implications

Return only the JSON object, no additional text.
"""
    
    def _parse_gemini_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response and extract analysis data"""
        try:
            # Clean the response to extract JSON
            response_text = response_text.strip()
            
            # Find JSON in the response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                analysis_data = json.loads(json_str)
                
                # Ensure required fields exist
                result = {
                    'mood': analysis_data.get('mood', 'neutral'),
                    'emotions': analysis_data.get('emotions', []),
                    'sentiment_score': analysis_data.get('sentiment_score', 0.0),
                    'energy_level': analysis_data.get('energy_level', 0.5),
                    'themes': analysis_data.get('themes', []),
                    'analysis_notes': analysis_data.get('analysis_notes', ''),
                    'sentiment_scores': {
                        'polarity': analysis_data.get('sentiment_score', 0.0),
                        'energy': analysis_data.get('energy_level', 0.5)
                    }
                }
                
                return result
            else:
                raise ValueError("No valid JSON found in response")
                
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return self._fallback_analysis("")
    
    def _calculate_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate confidence in the mood analysis"""
        try:
            # Base confidence on sentiment score strength and emotion intensity
            sentiment_strength = abs(analysis_result.get('sentiment_score', 0.0))
            energy_level = analysis_result.get('energy_level', 0.5)
            
            # Average confidence factors
            confidence = (sentiment_strength + energy_level) / 2
            
            # Ensure confidence is between 0 and 1
            return max(0.0, min(1.0, confidence))
            
        except Exception as e:
            logger.error(f"Error calculating confidence: {e}")
            return 0.5
    
    def _fallback_analysis(self, lyrics: str) -> Dict[str, Any]:
        """Fallback analysis when Gemini API is not available"""
        logger.warning("Using fallback mood analysis")
        
        # Simple keyword-based analysis
        lyrics_lower = lyrics.lower()
        
        # Basic mood detection
        happy_words = ['happy', 'joy', 'smile', 'laugh', 'dance', 'celebrate', 'sunshine', 'love']
        sad_words = ['sad', 'cry', 'tears', 'lonely', 'heartbreak', 'pain', 'darkness', 'alone']
        angry_words = ['angry', 'rage', 'hate', 'fight', 'war', 'fire', 'storm', 'revenge']
        energetic_words = ['energy', 'power', 'strong', 'wild', 'free', 'run', 'jump', 'explode']
        
        mood_scores = {
            'happy': sum(1 for word in happy_words if word in lyrics_lower),
            'sad': sum(1 for word in sad_words if word in lyrics_lower),
            'angry': sum(1 for word in angry_words if word in lyrics_lower),
            'energetic': sum(1 for word in energetic_words if word in lyrics_lower)
        }
        
        # Determine primary mood
        if not any(mood_scores.values()):
            primary_mood = 'neutral'
            confidence = 0.3
        else:
            primary_mood = max(mood_scores.items(), key=lambda x: x[1])[0]
            confidence = min(0.8, 0.3 + (max(mood_scores.values()) * 0.1))
        
        return {
            'mood': primary_mood,
            'confidence': confidence,
            'emotions': [{'emotion': primary_mood, 'intensity': confidence}],
            'sentiment_scores': {
                'polarity': 0.5 if primary_mood in ['happy', 'energetic'] else -0.5,
                'energy': 0.8 if primary_mood == 'energetic' else 0.5
            },
            'themes': [],
            'analysis_notes': 'Fallback analysis - Gemini API not available',
            'suggested_genre': self.mood_genre_map.get(primary_mood, 'pop')
        }
    
    def get_available_moods(self) -> List[str]:
        """Get list of available mood categories"""
        return list(self.mood_genre_map.keys())
    
    def get_mood_genre_mapping(self) -> Dict[str, str]:
        """Get mood to genre mapping"""
        return self.mood_genre_map.copy()
