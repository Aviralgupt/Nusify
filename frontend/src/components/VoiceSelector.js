import React from 'react';
import { motion } from 'framer-motion';

const VoiceSelector = ({ selectedVoice, onVoiceChange }) => {
  const voices = [
    { id: 'default', name: 'Default Voice', description: 'Standard text-to-speech' },
    { id: 'pop_female', name: 'Pop Female', description: 'Bright, energetic female voice' },
    { id: 'pop_male', name: 'Pop Male', description: 'Smooth, melodic male voice' },
    { id: 'rock_male', name: 'Rock Male', description: 'Powerful, gritty male voice' },
    { id: 'country_female', name: 'Country Female', description: 'Warm, twangy female voice' },
    { id: 'jazz_male', name: 'Jazz Male', description: 'Smooth, soulful male voice' },
    { id: 'classical_female', name: 'Classical Female', description: 'Elegant, refined female voice' },
    { id: 'rap_male', name: 'Rap Male', description: 'Fast, rhythmic male voice' },
    { id: 'indie_female', name: 'Indie Female', description: 'Unique, alternative female voice' },
    { id: 'soul_female', name: 'Soul Female', description: 'Rich, emotional female voice' }
  ];

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">Choose Voice Style</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {voices.map((voice) => (
          <motion.div
            key={voice.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
              selectedVoice === voice.id
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => onVoiceChange(voice.id)}
          >
            <div className="flex items-center space-x-3">
              <div className={`w-4 h-4 rounded-full ${
                selectedVoice === voice.id ? 'bg-blue-500' : 'bg-gray-300'
              }`} />
              <div>
                <h4 className="font-medium text-gray-900">{voice.name}</h4>
                <p className="text-sm text-gray-600">{voice.description}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default VoiceSelector;
