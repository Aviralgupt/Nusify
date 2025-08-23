import React from 'react';
import { motion } from 'framer-motion';

const GenreSelector = ({ selectedGenre, onGenreChange }) => {
  const genres = [
    { id: 'auto', name: 'Auto-Detect', description: 'AI determines best genre' },
    { id: 'pop', name: 'Pop', description: 'Catchy, mainstream music' },
    { id: 'rock', name: 'Rock', description: 'Energetic, guitar-driven' },
    { id: 'electronic', name: 'Electronic', description: 'Synthetic, rhythmic beats' },
    { id: 'jazz', name: 'Jazz', description: 'Smooth, improvisational' },
    { id: 'classical', name: 'Classical', description: 'Orchestral, sophisticated' },
    { id: 'country', name: 'Country', description: 'Twangy, storytelling' },
    { id: 'r&b', name: 'R&B', description: 'Soulful, rhythmic' },
    { id: 'hip-hop', name: 'Hip-Hop', description: 'Urban, beat-driven' },
    { id: 'ambient', name: 'Ambient', description: 'Atmospheric, relaxing' },
    { id: 'indie', name: 'Indie', description: 'Alternative, unique' },
    { id: 'ballad', name: 'Ballad', description: 'Slow, emotional' }
  ];

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold text-gray-800">Choose Music Genre</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {genres.map((genre) => (
          <motion.div
            key={genre.id}
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className={`p-3 rounded-lg border-2 cursor-pointer transition-all ${
              selectedGenre === genre.id
                ? 'border-green-500 bg-green-50'
                : 'border-gray-200 hover:border-gray-300'
            }`}
            onClick={() => onGenreChange(genre.id)}
          >
            <div className="flex items-center space-x-3">
              <div className={`w-4 h-4 rounded-full ${
                selectedGenre === genre.id ? 'bg-green-500' : 'bg-gray-300'
              }`} />
              <div>
                <h4 className="font-medium text-gray-900">{genre.name}</h4>
                <p className="text-sm text-gray-600">{genre.description}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default GenreSelector;
