import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { AcademicCapIcon, ChatBubbleLeftRightIcon, PlayIcon } from '@heroicons/react/24/outline';

const Tutor = () => {
  const [isChatting, setIsChatting] = useState(false);
  const [isQuizzing, setIsQuizzing] = useState(false);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-dark-100">AI Tutor</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Explain Like I'm 5</h2>
          <p className="text-dark-400 mb-4">Get simple explanations of complex concepts</p>
          <button 
            className="btn-primary w-full"
            onClick={() => setIsChatting(true)}
          >
            Start Chat
          </button>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Quiz Me</h2>
          <p className="text-dark-400 mb-4">Test your knowledge with AI-generated questions</p>
          <button 
            className="btn-secondary w-full"
            onClick={() => setIsQuizzing(true)}
          >
            Start Quiz
          </button>
        </div>
      </div>
      
      {isChatting && (
        <div className="card">
          <h3 className="text-lg font-semibold text-dark-100 mb-4">AI Chat</h3>
          <div className="space-y-4">
            <div className="bg-dark-700 p-4 rounded-lg">
              <p className="text-dark-100">Ask me anything! I'll explain it in simple terms.</p>
            </div>
            <input 
              type="text" 
              placeholder="Type your question here..."
              className="input-field w-full"
            />
            <button className="btn-primary">Send</button>
          </div>
        </div>
      )}
      
      {isQuizzing && (
        <div className="card">
          <h3 className="text-lg font-semibold text-dark-100 mb-4">Quiz Session</h3>
          <p className="text-dark-400">AI will generate questions based on your syllabus and performance.</p>
          <button className="btn-primary mt-4">Generate Questions</button>
        </div>
      )}
    </div>
  );
};

export default Tutor;
