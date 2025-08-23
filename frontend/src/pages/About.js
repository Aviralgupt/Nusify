import React from 'react';
import { motion } from 'framer-motion';
import { Music, Heart, Shield, Users, Code, Globe } from 'lucide-react';

const About = () => {
  const features = [
    {
      icon: <Music className="w-8 h-8 text-blue-400" />,
      title: "AI Music Generation",
      description: "Advanced algorithms create unique background music based on lyrics mood and genre preferences."
    },
    {
      icon: <Users className="w-8 h-8 text-purple-400" />,
      title: "Voice Cloning",
      description: "Ethical AI technology that can clone voices while respecting artist rights and copyright."
    },
    {
      icon: <Code className="w-8 h-8 text-green-400" />,
      title: "Open Source",
      description: "Built entirely with open-source AI models and free APIs for complete transparency."
    },
    {
      icon: <Globe className="w-8 h-8 text-yellow-400" />,
      title: "Accessible",
      description: "Free to use for everyone, democratizing music creation and AI technology."
    }
  ];

  const ethicalPrinciples = [
    {
      icon: <Shield className="w-6 h-6 text-green-400" />,
      title: "Respect Copyright",
      description: "We respect intellectual property rights and encourage ethical use of voice cloning technology."
    },
    {
      icon: <Heart className="w-6 h-6 text-red-400" />,
      title: "Creative Expression",
      description: "Voice cloning is intended for educational and creative purposes, not for deception."
    },
    {
      icon: <Users className="w-6 h-6 text-blue-400" />,
      title: "Community Guidelines",
      description: "Users must follow community guidelines and use the technology responsibly."
    }
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="text-center py-20"
      >
        <h1 className="text-5xl font-bold text-white mb-6">
          About <span className="gradient-text">Nusify</span>
        </h1>
        <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
          Nusify is an innovative AI-powered music generation platform that transforms the way 
          people create music. Our mission is to democratize music creation by making advanced 
          AI technology accessible to everyone, completely free of charge.
        </p>
      </motion.div>

      {/* Mission Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="py-16"
      >
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <h2 className="text-3xl font-bold text-white mb-6 text-center">Our Mission</h2>
          <p className="text-lg text-gray-300 text-center leading-relaxed max-w-4xl mx-auto">
            We believe that music creation should be accessible to everyone, regardless of their 
            technical skills or financial resources. By combining cutting-edge AI technology with 
            user-friendly interfaces, we're breaking down the barriers to musical expression and 
            empowering creators worldwide.
          </p>
        </div>
      </motion.div>

      {/* Features Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.4 }}
        className="py-16"
      >
        <h2 className="text-3xl font-bold text-white mb-12 text-center">
          What Makes Nusify Special
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.6 + index * 0.1 }}
              className="card card-hover p-6"
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

      {/* Technology Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.8 }}
        className="py-16"
      >
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <h2 className="text-3xl font-bold text-white mb-6 text-center">Technology Stack</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Backend</h3>
              <ul className="text-gray-300 space-y-2">
                <li>• Python Flask API</li>
                <li>• Coqui TTS for voice synthesis</li>
                <li>• Magenta for music generation</li>
                <li>• YourTTS for voice cloning</li>
                <li>• Hugging Face Transformers</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-4">Frontend</h3>
              <ul className="text-gray-300 space-y-2">
                <li>• React.js with modern hooks</li>
                <li>• Framer Motion animations</li>
                <li>• Tailwind CSS styling</li>
                <li>• Responsive design</li>
                <li>• Progressive Web App</li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Ethical Considerations */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.0 }}
        className="py-16"
      >
        <h2 className="text-3xl font-bold text-white mb-12 text-center">
          Ethical Considerations
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {ethicalPrinciples.map((principle, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 1.2 + index * 0.1 }}
              className="text-center p-6 bg-white/5 rounded-xl border border-white/10"
            >
              <div className="flex justify-center mb-4">
                {principle.icon}
              </div>
              <h3 className="text-lg font-semibold text-white mb-3">
                {principle.title}
              </h3>
              <p className="text-gray-300 text-sm">
                {principle.description}
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Future Plans */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.2 }}
        className="py-16"
      >
        <div className="bg-gradient-to-r from-blue-600/20 to-purple-600/20 backdrop-blur-lg rounded-2xl p-8 border border-white/20">
          <h2 className="text-3xl font-bold text-white mb-6 text-center">Future Plans</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-gray-300">
            <div>
              <h3 className="text-xl font-semibold text-white mb-3">Short Term</h3>
              <ul className="space-y-2">
                <li>• Enhanced voice cloning models</li>
                <li>• More music genres and styles</li>
                <li>• Improved mood analysis</li>
                <li>• Mobile app development</li>
              </ul>
            </div>
            <div>
              <h3 className="text-xl font-semibold text-white mb-3">Long Term</h3>
              <ul className="space-y-2">
                <li>• Multi-language support</li>
                <li>• Collaborative music creation</li>
                <li>• Advanced AI composition</li>
                <li>• Integration with DAWs</li>
              </ul>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Contact Section */}
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 1.4 }}
        className="py-16 text-center"
      >
        <h2 className="text-3xl font-bold text-white mb-6">Get Involved</h2>
        <p className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto">
          Nusify is an open-source project, and we welcome contributions from the community. 
          Whether you're a developer, musician, or AI enthusiast, there are many ways to help 
          improve the platform.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <a
            href="https://github.com/your-username/nusify"
            target="_blank"
            rel="noopener noreferrer"
            className="btn-primary inline-flex items-center"
          >
            <Code className="mr-2" />
            View on GitHub
          </a>
          <a
            href="mailto:contact@nusify.ai"
            className="btn-secondary inline-flex items-center"
          >
            <Heart className="mr-2" />
            Contact Us
          </a>
        </div>
      </motion.div>
    </div>
  );
};

export default About;
