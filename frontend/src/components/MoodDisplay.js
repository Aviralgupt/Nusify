import React from 'react';
import { motion } from 'framer-motion';

const MoodDisplay = ({ moodAnalysis }) => {
  if (!moodAnalysis) return null;

  const getMoodColor = (mood) => {
    const colors = {
      happy: 'bg-yellow-100 text-yellow-800 border-yellow-200',
      sad: 'bg-blue-100 text-blue-800 border-blue-200',
      angry: 'bg-red-100 text-red-800 border-red-200',
      energetic: 'bg-orange-100 text-orange-800 border-orange-200',
      romantic: 'bg-pink-100 text-pink-800 border-pink-200',
      calm: 'bg-green-100 text-green-800 border-green-200',
      mysterious: 'bg-purple-100 text-purple-800 border-purple-200',
      neutral: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[mood] || colors.neutral;
  };

  const getMoodEmoji = (mood) => {
    const emojis = {
      happy: '😊',
      sad: '😢',
      angry: '😠',
      energetic: '⚡',
      romantic: '💕',
      calm: '😌',
      mysterious: '🔮',
      neutral: '😐'
    };
    return emojis[mood] || emojis.neutral;
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow-lg p-6 space-y-4"
    >
      <h3 className="text-xl font-bold text-gray-800">Mood Analysis</h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Primary Mood */}
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-700">Primary Mood</h4>
          <div className={`inline-flex items-center space-x-2 px-3 py-2 rounded-full border ${getMoodColor(moodAnalysis.mood)}`}>
            <span className="text-xl">{getMoodEmoji(moodAnalysis.mood)}</span>
            <span className="font-medium capitalize">{moodAnalysis.mood}</span>
          </div>
          <p className="text-sm text-gray-600">
            Confidence: {(moodAnalysis.confidence * 100).toFixed(1)}%
          </p>
        </div>

        {/* Suggested Genre */}
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-700">Suggested Genre</h4>
          <div className="bg-blue-50 text-blue-800 px-3 py-2 rounded-lg border border-blue-200">
            <span className="font-medium capitalize">{moodAnalysis.suggested_genre}</span>
          </div>
        </div>
      </div>

      {/* Emotions Breakdown */}
      {moodAnalysis.emotions && moodAnalysis.emotions.length > 0 && (
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-700">Emotions Detected</h4>
          <div className="flex flex-wrap gap-2">
            {moodAnalysis.emotions.slice(0, 5).map((emotion, index) => (
              <span
                key={index}
                className="bg-gray-100 text-gray-700 px-2 py-1 rounded-full text-sm"
              >
                {emotion.label}: {(emotion.score * 100).toFixed(1)}%
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Sentiment Scores */}
      {moodAnalysis.sentiment_scores && (
        <div className="space-y-3">
          <h4 className="font-semibold text-gray-700">Sentiment Analysis</h4>
          <div className="grid grid-cols-3 gap-3">
            {Object.entries(moodAnalysis.sentiment_scores).map(([key, value]) => (
              <div key={key} className="text-center">
                <div className="text-sm text-gray-600 capitalize">{key}</div>
                <div className="text-lg font-semibold text-gray-800">
                  {(value * 100).toFixed(0)}%
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </motion.div>
  );
};

export default MoodDisplay;
