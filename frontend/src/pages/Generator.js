import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Music, Mic, Download, Play, Pause, Loader2, Sparkles } from 'lucide-react';
import toast from 'react-hot-toast';
import axios from 'axios';
import VoiceSelector from '../components/VoiceSelector';
import GenreSelector from '../components/GenreSelector';
import MoodDisplay from '../components/MoodDisplay';
import AudioPlayer from '../components/AudioPlayer';

const Generator = () => {
  const [lyrics, setLyrics] = useState('');
  const [selectedVoice, setSelectedVoice] = useState('default');
  const [selectedGenre, setSelectedGenre] = useState('auto');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedSong, setGeneratedSong] = useState(null);
  const [moodAnalysis, setMoodAnalysis] = useState(null);
  const [availableVoices, setAvailableVoices] = useState([]);
  const [availableGenres, setAvailableGenres] = useState([]);

  useEffect(() => {
    fetchAvailableOptions();
  }, []);

  const fetchAvailableOptions = async () => {
    try {
      const [voicesRes, genresRes] = await Promise.all([
        axios.get('/api/available-voices'),
        axios.get('/api/available-genres')
      ]);
      setAvailableVoices(voicesRes.data.voices);
      setAvailableGenres(genresRes.data.genres);
    } catch (error) {
      console.error('Error fetching options:', error);
      toast.error('Failed to load available options');
    }
  };

  const analyzeMood = async () => {
    if (!lyrics.trim()) {
      toast.error('Please enter some lyrics first');
      return;
    }

    try {
      const response = await axios.post('/api/analyze-mood', { lyrics });
      setMoodAnalysis(response.data);
      toast.success('Mood analysis completed!');
    } catch (error) {
      console.error('Error analyzing mood:', error);
      toast.error('Failed to analyze mood');
    }
  };

  const generateSong = async () => {
    if (!lyrics.trim()) {
      toast.error('Please enter some lyrics first');
      return;
    }

    setIsGenerating(true);
    toast.loading('Generating your song... This may take a few minutes.');

    try {
      const response = await axios.post('/api/create-song', {
        lyrics,
        artist_voice: selectedVoice,
        genre: selectedGenre
      });

      setGeneratedSong(response.data);
      toast.dismiss();
      toast.success('Song generated successfully!');
    } catch (error) {
      console.error('Error generating song:', error);
      toast.dismiss();
      toast.error('Failed to generate song. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const downloadSong = async () => {
    if (!generatedSong) return;

    try {
      const response = await axios.get(generatedSong.download_url, {
        responseType: 'blob'
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `nusify_song_${Date.now()}.wav`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);

      toast.success('Song downloaded successfully!');
    } catch (error) {
      console.error('Error downloading song:', error);
      toast.error('Failed to download song');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="text-center mb-12"
      >
        <h1 className="text-5xl font-bold text-white mb-4">
          <Sparkles className="inline-block mr-3 text-yellow-400" />
          AI Music Generator
        </h1>
        <p className="text-xl text-gray-300 max-w-2xl mx-auto">
          Transform your lyrics into complete songs with AI-generated background music 
          and voice cloning capabilities
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column - Input */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="lg:col-span-2"
        >
          <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
            <h2 className="text-2xl font-semibold text-white mb-6 flex items-center">
              <Mic className="mr-3 text-blue-400" />
              Enter Your Lyrics
            </h2>
            
            <textarea
              value={lyrics}
              onChange={(e) => setLyrics(e.target.value)}
              placeholder="Write your lyrics here...\n\nExample:\nI'm walking down this lonely road\nTrying to find my way back home\nEvery step I take feels heavy\nBut I know I'm not alone..."
              className="w-full h-64 p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <div className="flex flex-wrap gap-4 mt-6">
              <button
                onClick={analyzeMood}
                disabled={!lyrics.trim()}
                className="px-6 py-3 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors flex items-center"
              >
                <Music className="mr-2" size={20} />
                Analyze Mood
              </button>

              <button
                onClick={generateSong}
                disabled={!lyrics.trim() || isGenerating}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-600 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-all flex items-center"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="mr-2 animate-spin" size={20} />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="mr-2" size={20} />
                    Generate Song
                  </>
                )}
              </button>
            </div>
          </div>
        </motion.div>

        {/* Right Column - Settings & Results */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="space-y-6"
        >
          {/* Voice Selection */}
          <VoiceSelector
            selectedVoice={selectedVoice}
            onVoiceChange={setSelectedVoice}
            availableVoices={availableVoices}
          />

          {/* Genre Selection */}
          <GenreSelector
            selectedGenre={selectedGenre}
            onGenreChange={setSelectedGenre}
            availableGenres={availableGenres}
          />

          {/* Mood Analysis Display */}
          {moodAnalysis && (
            <MoodDisplay moodData={moodAnalysis} />
          )}

          {/* Generated Song Player */}
          {generatedSong && (
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 border border-white/20">
              <h3 className="text-xl font-semibold text-white mb-4 flex items-center">
                <Music className="mr-2 text-green-400" />
                Your Generated Song
              </h3>
              
              <div className="space-y-4">
                <div className="text-sm text-gray-300">
                  <p><strong>Mood:</strong> {generatedSong.mood}</p>
                  <p><strong>Genre:</strong> {generatedSong.genre}</p>
                  <p><strong>Duration:</strong> {generatedSong.duration}s</p>
                </div>

                <AudioPlayer audioUrl={generatedSong.download_url} />

                <button
                  onClick={downloadSong}
                  className="w-full px-4 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors flex items-center justify-center"
                >
                  <Download className="mr-2" size={20} />
                  Download Song
                </button>
              </div>
            </div>
          )}
        </motion.div>
      </div>

      {/* Tips Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.6 }}
        className="mt-12 bg-white/5 backdrop-blur-lg rounded-2xl p-6 border border-white/10"
      >
        <h3 className="text-xl font-semibold text-white mb-4">💡 Tips for Better Results</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-gray-300">
          <div>
            <h4 className="font-medium text-white mb-2">Lyrics Writing</h4>
            <ul className="text-sm space-y-1">
              <li>• Use clear, emotional language</li>
              <li>• Include repetition for choruses</li>
              <li>• Consider rhythm and flow</li>
            </ul>
          </div>
          <div>
            <h4 className="font-medium text-white mb-2">Voice & Genre</h4>
            <ul className="text-sm space-y-1">
              <li>• Match voice to song style</li>
              <li>• Let AI suggest genre based on mood</li>
              <li>• Experiment with different combinations</li>
            </ul>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default Generator;
