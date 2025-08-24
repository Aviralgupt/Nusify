import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { Music, Mic, Sparkles, Play, Users, Zap } from 'lucide-react';

const Home = () => {
  const features = [
    {
      icon: <Mic className="w-8 h-8 text-blue-400" />,
      title: "Lyrics to Song",
      description: "Transform any lyrics into a complete musical composition with AI-generated background music."
    },
    {
      icon: <Music className="w-8 h-8 text-purple-400" />,
      title: "AI Background Music",
      description: "Automatically generates music based on song mood - happy, sad, energetic, and more."
    },
    {
      icon: <Users className="w-8 h-8 text-green-400" />,
      title: "Voice Cloning",
      description: "Clone voices of famous artists with ethical AI technology for creative expression."
    },
    {
      icon: <Zap className="w-8 h-8 text-yellow-400" />,
      title: "Zero Cost",
      description: "Built entirely with open-source AI models and free APIs - no hidden costs."
    }
  ];

  const stats = [
    { number: "100%", label: "Free to Use" },
    { number: "24/7", label: "AI Available" },
    { number: "∞", label: "Possibilities" }
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-20"
      >
        <motion.div
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="inline-block mb-8"
        >
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full blur-3xl opacity-30 animate-pulse"></div>
            <div className="relative bg-gradient-to-r from-blue-600 to-purple-600 p-6 rounded-full">
              <Music className="w-16 h-16 text-white" />
            </div>
          </div>
        </motion.div>

        <h1 className="text-6xl md:text-7xl font-bold text-white mb-6">
          <span className="gradient-text">Nusify</span>
        </h1>
        
        <p className="text-2xl md:text-3xl text-gray-300 mb-8 max-w-4xl mx-auto leading-relaxed">
          Transform your lyrics into complete songs with{' '}
          <span className="text-yellow-400 font-semibold">AI-powered</span> background music 
          and <span className="text-purple-400 font-semibold">voice cloning</span> capabilities
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
          <Link
            to="/generator"
            className="btn-primary text-lg px-8 py-4 flex items-center group"
          >
            <Sparkles className="mr-2 group-hover:rotate-12 transition-transform" />
            Start Creating Music
          </Link>
          
          <Link
            to="/about"
            className="btn-secondary text-lg px-8 py-4"
          >
            Learn More
          </Link>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-2xl mx-auto">
          {stats.map((stat, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
              className="text-center"
            >
              <div className="text-3xl font-bold text-white mb-2">{stat.number}</div>
              <div className="text-gray-400">{stat.label}</div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.6 }}
        className="py-20"
      >
        <h2 className="text-4xl font-bold text-white text-center mb-16">
          Powered by Advanced AI Technology
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
              className="card card-hover p-8"
            >
              <div className="flex items-start space-x-4">
                <div className="flex-shrink-0">
                  {feature.icon}
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-white mb-3">
                    {feature.title}
                  </h3>
                  <p className="text-gray-300 leading-relaxed">
                    {feature.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* How It Works Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.0 }}
        className="py-20"
      >
        <h2 className="text-4xl font-bold text-white text-center mb-16">
          How It Works
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: "1",
              title: "Write Lyrics",
              description: "Enter your lyrics in the text area. Be creative and expressive!"
            },
            {
              step: "2",
              title: "AI Analysis",
              description: "Our AI analyzes the mood and suggests the perfect music style."
            },
            {
              step: "3",
              title: "Generate & Download",
              description: "Get your complete song with AI-generated music and cloned voice."
            }
          ].map((step, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.2 + index * 0.1 }}
              className="text-center"
            >
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto text-white text-2xl font-bold">
                  {step.step}
                </div>
                {index < 2 && (
                  <div className="hidden md:block absolute top-1/2 left-full w-full h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 transform -translate-y-1/2"></div>
                )}
              </div>
              <h3 className="text-xl font-semibold text-white mb-3">{step.title}</h3>
              <p className="text-gray-300">{step.description}</p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* CTA Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.4 }}
        className="py-20 text-center"
      >
        <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-lg rounded-3xl p-12 border border-white/20">
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Create Your First AI Song?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join thousands of creators who are already using Nusify to bring their musical ideas to life.
          </p>
          <Link
            to="/generator"
            className="btn-primary text-xl px-10 py-5 inline-flex items-center group"
          >
            <Play className="mr-3 group-hover:scale-110 transition-transform" />
            Start Creating Now
          </Link>
        </div>
      </motion.div>
    </div>
  );
};

export default Home;
