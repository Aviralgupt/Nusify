import re
import logging
from textblob import TextBlob
from transformers import pipeline
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

logger = logging.getLogger(__name__)

class MoodAnalyzer:
    """AI-powered mood analyzer for lyrics"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
        # Initialize emotion classification pipeline
        try:
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True
            )
        except Exception as e:
            logger.warning(f"Could not load emotion classifier: {e}")
            self.emotion_classifier = None
        
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
            'mysterious': 'atmospheric'
        }
        
        # Emotion keywords for enhanced analysis
        self.emotion_keywords = {
            'happy': ['joy', 'happy', 'smile', 'laugh', 'dance', 'celebrate', 'sunshine', 'love'],
            'sad': ['tears', 'cry', 'lonely', 'heartbreak', 'pain', 'sadness', 'darkness', 'alone'],
            'angry': ['rage', 'anger', 'hate', 'fight', 'war', 'fire', 'storm', 'revenge'],
            'energetic': ['energy', 'power', 'strong', 'wild', 'free', 'run', 'jump', 'explode'],
            'romantic': ['love', 'heart', 'kiss', 'romance', 'beautiful', 'sweet', 'tender', 'passion'],
            'melancholic': ['nostalgia', 'memory', 'past', 'dream', 'wish', 'hope', 'longing'],
            'upbeat': ['fun', 'party', 'good time', 'excitement', 'adventure', 'discovery'],
            'calm': ['peace', 'quiet', 'gentle', 'soft', 'breeze', 'ocean', 'mountain'],
            'dramatic': ['epic', 'hero', 'battle', 'victory', 'defeat', 'destiny', 'fate'],
            'mysterious': ['secret', 'mystery', 'unknown', 'shadow', 'whisper', 'hidden']
        }
    
    def analyze(self, lyrics):
        """
        Analyze lyrics to determine mood, emotions, and suggested genre
        
        Args:
            lyrics (str): The lyrics to analyze
            
        Returns:
            dict: Analysis results with mood, confidence, emotions, and suggested genre
        """
        try:
            # Clean lyrics
            cleaned_lyrics = self._clean_lyrics(lyrics)
            
            # Basic sentiment analysis
            sentiment_scores = self._analyze_sentiment(cleaned_lyrics)
            
            # Emotion classification
            emotions = self._classify_emotions(cleaned_lyrics)
            
            # Keyword-based mood detection
            keyword_mood = self._detect_mood_by_keywords(cleaned_lyrics)
            
            # Combine all analyses
            final_mood = self._combine_analyses(sentiment_scores, emotions, keyword_mood)
            
            # Determine confidence
            confidence = self._calculate_confidence(sentiment_scores, emotions, keyword_mood)
            
            # Suggest genre based on mood
            suggested_genre = self.mood_genre_map.get(final_mood, 'pop')
            
            return {
                'mood': final_mood,
                'confidence': confidence,
                'emotions': emotions,
                'sentiment_scores': sentiment_scores,
                'suggested_genre': suggested_genre,
                'analysis_methods': {
                    'sentiment': sentiment_scores,
                    'emotions': emotions,
                    'keywords': keyword_mood
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing mood: {e}")
            return {
                'mood': 'neutral',
                'confidence': 0.0,
                'emotions': [],
                'suggested_genre': 'pop'
            }
    
    def _clean_lyrics(self, lyrics):
        """Clean and preprocess lyrics"""
        # Remove special characters but keep spaces
        cleaned = re.sub(r'[^\w\s]', ' ', lyrics)
        # Convert to lowercase
        cleaned = cleaned.lower()
        # Remove extra whitespace
        cleaned = ' '.join(cleaned.split())
        return cleaned
    
    def _analyze_sentiment(self, lyrics):
        """Analyze sentiment using TextBlob and NLTK"""
        # TextBlob sentiment
        blob = TextBlob(lyrics)
        textblob_polarity = blob.sentiment.polarity
        textblob_subjectivity = blob.sentiment.subjectivity
        
        # NLTK VADER sentiment
        vader_scores = self.sentiment_analyzer.polarity_scores(lyrics)
        
        return {
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu']
        }
    
    def _classify_emotions(self, lyrics):
        """Classify emotions using transformer model"""
        if not self.emotion_classifier:
            return []
        
        try:
            # Split lyrics into chunks if too long
            words = lyrics.split()
            if len(words) > 512:  # Model limit
                chunks = [' '.join(words[i:i+512]) for i in range(0, len(words), 512)]
            else:
                chunks = [lyrics]
            
            all_emotions = []
            for chunk in chunks:
                results = self.emotion_classifier(chunk)
                if results and len(results) > 0:
                    chunk_emotions = results[0]
                    all_emotions.extend(chunk_emotions)
            
            # Aggregate emotions across chunks
            emotion_scores = {}
            for emotion in all_emotions:
                label = emotion['label']
                score = emotion['score']
                if label in emotion_scores:
                    emotion_scores[label] = max(emotion_scores[label], score)
                else:
                    emotion_scores[label] = score
            
            # Return top emotions
            sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
            return [{'emotion': emotion, 'score': score} for emotion, score in sorted_emotions[:5]]
            
        except Exception as e:
            logger.warning(f"Error in emotion classification: {e}")
            return []
    
    def _detect_mood_by_keywords(self, lyrics):
        """Detect mood based on keyword presence"""
        mood_scores = {}
        
        for mood, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in lyrics:
                    score += 1
            if score > 0:
                mood_scores[mood] = score / len(keywords)
        
        return mood_scores
    
    def _combine_analyses(self, sentiment_scores, emotions, keyword_mood):
        """Combine different analysis methods to determine final mood"""
        # Start with sentiment-based mood
        vader_compound = sentiment_scores['vader_compound']
        
        if vader_compound >= 0.5:
            base_mood = 'happy'
        elif vader_compound <= -0.5:
            base_mood = 'sad'
        else:
            base_mood = 'neutral'
        
        # Override with keyword analysis if strong signals
        if keyword_mood:
            strongest_keyword_mood = max(keyword_mood.items(), key=lambda x: x[1])
            if strongest_keyword_mood[1] > 0.3:  # Threshold
                return strongest_keyword_mood[0]
        
        # Override with emotion classification if strong signals
        if emotions:
            top_emotion = emotions[0]
            if top_emotion['score'] > 0.7:  # High confidence
                emotion_mood_map = {
                    'joy': 'happy',
                    'love': 'romantic',
                    'anger': 'angry',
                    'sadness': 'sad',
                    'fear': 'mysterious',
                    'surprise': 'energetic',
                    'disgust': 'angry'
                }
                return emotion_mood_map.get(top_emotion['emotion'], base_mood)
        
        return base_mood
    
    def _calculate_confidence(self, sentiment_scores, emotions, keyword_mood):
        """Calculate confidence in the mood analysis"""
        confidence_factors = []
        
        # Sentiment confidence
        vader_compound = abs(sentiment_scores['vader_compound'])
        confidence_factors.append(vader_compound)
        
        # Emotion confidence
        if emotions:
            top_emotion_score = emotions[0]['score']
            confidence_factors.append(top_emotion_score)
        
        # Keyword confidence
        if keyword_mood:
            max_keyword_score = max(keyword_mood.values())
            confidence_factors.append(max_keyword_score)
        
        # Average confidence
        if confidence_factors:
            return sum(confidence_factors) / len(confidence_factors)
        else:
            return 0.5  # Default medium confidence
