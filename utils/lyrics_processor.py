import re
import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

class LyricsProcessor:
    """Process and format lyrics for AI analysis and generation"""
    
    def __init__(self):
        # Common song structure patterns
        self.song_sections = [
            'verse', 'chorus', 'bridge', 'intro', 'outro', 
            'pre-chorus', 'post-chorus', 'interlude'
        ]
        
        # Common rhyming patterns
        self.rhyme_patterns = {
            'aabb': 'Couplet',
            'abab': 'Alternate',
            'abba': 'Enclosed',
            'aaba': 'Ballad',
            'abcb': 'Simple',
            'free': 'Free verse'
        }
        
        # Syllable counting patterns
        self.syllable_patterns = {
            'iambic': 'Unstressed-stressed',
            'trochaic': 'Stressed-unstressed',
            'anapestic': 'Unstressed-unstressed-stressed',
            'dactylic': 'Stressed-unstressed-unstressed'
        }
    
    def process_lyrics(self, raw_lyrics: str) -> Dict:
        """
        Process raw lyrics and extract useful information
        
        Args:
            raw_lyrics (str): Raw lyrics text
            
        Returns:
            Dict: Processed lyrics information
        """
        try:
            # Clean lyrics
            cleaned_lyrics = self._clean_lyrics(raw_lyrics)
            
            # Analyze structure
            structure = self._analyze_structure(cleaned_lyrics)
            
            # Count syllables and words
            metrics = self._calculate_metrics(cleaned_lyrics)
            
            # Detect rhyming patterns
            rhyme_info = self._detect_rhyming(cleaned_lyrics)
            
            # Identify themes and topics
            themes = self._identify_themes(cleaned_lyrics)
            
            return {
                'original': raw_lyrics,
                'cleaned': cleaned_lyrics,
                'structure': structure,
                'metrics': metrics,
                'rhyming': rhyme_info,
                'themes': themes,
                'processing_info': {
                    'total_lines': len(cleaned_lyrics.split('\n')),
                    'total_words': len(cleaned_lyrics.split()),
                    'total_characters': len(cleaned_lyrics)
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing lyrics: {e}")
            return {
                'original': raw_lyrics,
                'cleaned': raw_lyrics,
                'error': str(e)
            }
    
    def _clean_lyrics(self, lyrics: str) -> str:
        """Clean and normalize lyrics text"""
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', lyrics.strip())
        
        # Normalize line breaks
        cleaned = re.sub(r'[;|]', '\n', cleaned)
        
        # Remove common artifacts
        cleaned = re.sub(r'\[.*?\]', '', cleaned)  # Remove brackets
        cleaned = re.sub(r'\(.*?\)', '', cleaned)  # Remove parentheses
        
        # Clean up punctuation
        cleaned = re.sub(r'[^\w\s\n.,!?\'"-]', '', cleaned)
        
        # Normalize quotes
        cleaned = re.sub(r'["""]', '"', cleaned)
        cleaned = re.sub(r"[''']", "'", cleaned)
        
        # Fix spacing around punctuation
        cleaned = re.sub(r'\s+([.,!?])', r'\1', cleaned)
        
        return cleaned
    
    def _analyze_structure(self, lyrics: str) -> Dict:
        """Analyze the structure of the lyrics"""
        lines = lyrics.split('\n')
        structure = {
            'sections': [],
            'line_lengths': [],
            'repetition_patterns': []
        }
        
        # Analyze line lengths
        for line in lines:
            if line.strip():
                structure['line_lengths'].append(len(line.split()))
        
        # Detect potential sections based on repetition
        structure['repetition_patterns'] = self._find_repetitions(lines)
        
        # Identify section boundaries
        structure['sections'] = self._identify_sections(lines)
        
        return structure
    
    def _find_repetitions(self, lines: List[str]) -> List[Dict]:
        """Find repeated lines and patterns"""
        repetitions = []
        line_counts = {}
        
        for line in lines:
            clean_line = line.strip().lower()
            if clean_line:
                if clean_line in line_counts:
                    line_counts[clean_line] += 1
                else:
                    line_counts[clean_line] = 1
        
        # Find lines that repeat
        for line, count in line_counts.items():
            if count > 1:
                repetitions.append({
                    'line': line,
                    'count': count,
                    'type': 'chorus' if count >= 3 else 'verse'
                })
        
        return repetitions
    
    def _identify_sections(self, lines: List[str]) -> List[Dict]:
        """Identify different sections of the song"""
        sections = []
        current_section = {
            'type': 'verse',
            'start_line': 0,
            'end_line': 0,
            'lines': []
        }
        
        for i, line in enumerate(lines):
            if line.strip():
                current_section['lines'].append(line)
                current_section['end_line'] = i
            else:
                # Empty line might indicate section break
                if current_section['lines']:
                    sections.append(current_section.copy())
                    current_section = {
                        'type': self._guess_section_type(current_section['lines']),
                        'start_line': i + 1,
                        'end_line': i + 1,
                        'lines': []
                    }
        
        # Add final section
        if current_section['lines']:
            current_section['type'] = self._guess_section_type(current_section['lines'])
            sections.append(current_section)
        
        return sections
    
    def _guess_section_type(self, lines: List[str]) -> str:
        """Guess the type of a section based on its characteristics"""
        if not lines:
            return 'verse'
        
        # Check for chorus indicators
        chorus_indicators = ['chorus', 'refrain', 'hook']
        for line in lines:
            if any(indicator in line.lower() for indicator in chorus_indicators):
                return 'chorus'
        
        # Check for bridge indicators
        bridge_indicators = ['bridge', 'middle', 'break']
        for line in lines:
            if any(indicator in line.lower() for indicator in bridge_indicators):
                return 'bridge'
        
        # Check for intro/outro
        if len(lines) <= 2:
            return 'intro' if len(lines) == 1 else 'verse'
        
        # Default to verse
        return 'verse'
    
    def _calculate_metrics(self, lyrics: str) -> Dict:
        """Calculate various metrics for the lyrics"""
        lines = lyrics.split('\n')
        words = lyrics.split()
        
        metrics = {
            'total_lines': len([l for l in lines if l.strip()]),
            'total_words': len(words),
            'total_characters': len(lyrics),
            'average_line_length': 0,
            'syllable_count': 0,
            'word_diversity': 0
        }
        
        # Calculate average line length
        non_empty_lines = [l for l in lines if l.strip()]
        if non_empty_lines:
            metrics['average_line_length'] = sum(len(l.split()) for l in non_empty_lines) / len(non_empty_lines)
        
        # Estimate syllable count
        metrics['syllable_count'] = self._estimate_syllables(words)
        
        # Calculate word diversity
        unique_words = set(word.lower() for word in words)
        metrics['word_diversity'] = len(unique_words) / len(words) if words else 0
        
        return metrics
    
    def _estimate_syllables(self, words: List[str]) -> int:
        """Estimate syllable count for words"""
        total_syllables = 0
        
        for word in words:
            # Simple syllable estimation
            word_lower = word.lower()
            
            # Count vowels (rough approximation)
            vowels = len(re.findall(r'[aeiouy]', word_lower))
            
            # Adjust for common patterns
            if word_lower.endswith('e'):
                vowels -= 1  # Silent e
            
            if word_lower.endswith('le') and len(word_lower) > 2:
                vowels += 1  # Consonant + le
            
            # Ensure at least 1 syllable
            syllables = max(1, vowels)
            total_syllables += syllables
        
        return total_syllables
    
    def _detect_rhyming(self, lyrics: str) -> Dict:
        """Detect rhyming patterns in the lyrics"""
        lines = [l.strip() for l in lyrics.split('\n') if l.strip()]
        
        if len(lines) < 2:
            return {'pattern': 'single_line', 'rhymes': []}
        
        # Extract end words
        end_words = []
        for line in lines:
            words = line.split()
            if words:
                end_words.append(words[-1].lower())
        
        # Find rhyming pairs
        rhymes = []
        for i in range(len(end_words) - 1):
            if self._words_rhyme(end_words[i], end_words[i + 1]):
                rhymes.append({
                    'line1': i,
                    'line2': i + 1,
                    'word1': end_words[i],
                    'word2': end_words[i + 1]
                })
        
        # Determine rhyme pattern
        pattern = self._determine_rhyme_pattern(rhymes, len(lines))
        
        return {
            'pattern': pattern,
            'rhymes': rhymes,
            'total_rhymes': len(rhymes)
        }
    
    def _words_rhyme(self, word1: str, word2: str) -> bool:
        """Check if two words rhyme"""
        # Simple rhyming check based on ending sounds
        if word1 == word2:
            return False
        
        # Remove common suffixes
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 's', 'es']
        clean1 = word1
        clean2 = word2
        
        for suffix in suffixes:
            if clean1.endswith(suffix):
                clean1 = clean1[:-len(suffix)]
            if clean2.endswith(suffix):
                clean2 = clean2[:-len(suffix)]
        
        # Check if they end with similar sounds
        if len(clean1) >= 2 and len(clean2) >= 2:
            return clean1[-2:] == clean2[-2:]
        
        return False
    
    def _determine_rhyme_pattern(self, rhymes: List[Dict], total_lines: int) -> str:
        """Determine the overall rhyme pattern"""
        if not rhymes:
            return 'free'
        
        # Simple pattern detection
        if len(rhymes) >= total_lines // 2:
            # Check for common patterns
            if len(rhymes) == total_lines // 2:
                return 'aabb'  # Couplet
            elif len(rhymes) == total_lines - 1:
                return 'abab'  # Alternate
            else:
                return 'mixed'
        
        return 'partial'
    
    def _identify_themes(self, lyrics: str) -> List[str]:
        """Identify common themes in the lyrics"""
        themes = []
        
        # Common theme keywords
        theme_keywords = {
            'love': ['love', 'heart', 'kiss', 'romance', 'passion', 'sweet'],
            'heartbreak': ['break', 'pain', 'tears', 'lonely', 'hurt', 'sad'],
            'freedom': ['free', 'fly', 'escape', 'break', 'wild', 'adventure'],
            'party': ['dance', 'party', 'fun', 'good time', 'celebration'],
            'reflection': ['think', 'remember', 'dream', 'hope', 'wish'],
            'struggle': ['fight', 'battle', 'war', 'struggle', 'overcome'],
            'nature': ['sun', 'moon', 'stars', 'ocean', 'mountain', 'wind']
        }
        
        lyrics_lower = lyrics.lower()
        
        for theme, keywords in theme_keywords.items():
            if any(keyword in lyrics_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    def format_for_tts(self, lyrics: str) -> str:
        """Format lyrics for better text-to-speech quality"""
        # Add pauses between lines
        formatted = re.sub(r'\n+', '\n...\n', lyrics)
        
        # Add pauses between sections
        formatted = re.sub(r'([.!?])\s*\n', r'\1\n...\n', formatted)
        
        # Clean up multiple pauses
        formatted = re.sub(r'\.{3,}', '...', formatted)
        
        return formatted
    
    def get_lyrics_summary(self, processed_lyrics: Dict) -> str:
        """Generate a summary of the processed lyrics"""
        if 'error' in processed_lyrics:
            return f"Error processing lyrics: {processed_lyrics['error']}"
        
        summary = f"""
Lyrics Summary:
- Total lines: {processed_lyrics['processing_info']['total_lines']}
- Total words: {processed_lyrics['processing_info']['total_words']}
- Average line length: {processed_lyrics['metrics']['average_line_length']:.1f} words
- Estimated syllables: {processed_lyrics['metrics']['syllable_count']}
- Rhyme pattern: {processed_lyrics['rhyming']['pattern']}
- Main themes: {', '.join(processed_lyrics['themes']) if processed_lyrics['themes'] else 'None detected'}
- Structure: {len(processed_lyrics['structure']['sections'])} sections
        """.strip()
        
        return summary
