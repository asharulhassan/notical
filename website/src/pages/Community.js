import React from 'react';
import { motion } from 'framer-motion';
import { UserGroupIcon, ChatBubbleLeftRightIcon, AcademicCapIcon } from '@heroicons/react/24/outline';

const Community = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-dark-100">Community</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card text-center">
          <UserGroupIcon className="w-16 h-16 text-primary-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-dark-100 mb-2">Study Groups</h3>
          <p className="text-dark-400 mb-4">Join virtual study rooms and collaborate with peers</p>
          <button className="btn-primary">Join Group</button>
        </div>
        
        <div className="card text-center">
          <ChatBubbleLeftRightIcon className="w-16 h-16 text-secondary-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-dark-100 mb-2">Forums</h3>
          <p className="text-dark-400 mb-4">Ask questions and share knowledge with the community</p>
          <button className="btn-secondary">Browse Forums</button>
        </div>
        
        <div className="card text-center">
          <AcademicCapIcon className="w-16 h-16 text-accent-500 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-dark-100 mb-2">Tutor Marketplace</h3>
          <p className="text-dark-400 mb-4">Find verified tutors for one-on-one sessions</p>
          <button className="btn-accent">Find Tutor</button>
        </div>
      </div>
    </div>
  );
};

export default Community;
