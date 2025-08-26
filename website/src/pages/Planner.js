import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CalendarIcon, ClockIcon, ChartBarIcon } from '@heroicons/react/24/outline';

const Planner = () => {
  const [examDate, setExamDate] = useState('');
  const [studyHours, setStudyHours] = useState(2);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-dark-100">Study Planner</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">AI Study Schedule</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Exam Date
              </label>
              <input
                type="date"
                value={examDate}
                onChange={(e) => setExamDate(e.target.value)}
                className="input-field w-full"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">
                Daily Study Hours
              </label>
              <input
                type="number"
                min="1"
                max="8"
                value={studyHours}
                onChange={(e) => setStudyHours(parseInt(e.target.value))}
                className="input-field w-full"
              />
            </div>
            
            <button className="btn-primary w-full">
              Generate AI Schedule
            </button>
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Today's Schedule</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-dark-700/50 rounded-lg">
              <div className="flex items-center space-x-3">
                <ClockIcon className="w-5 h-5 text-primary-500" />
                <span className="text-dark-100">9:00 AM - Biology</span>
              </div>
              <span className="text-sm text-dark-400">45 min</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-dark-700/50 rounded-lg">
              <div className="flex items-center space-x-3">
                <ClockIcon className="w-5 h-5 text-secondary-500" />
                <span className="text-dark-100">2:00 PM - Chemistry</span>
              </div>
              <span className="text-sm text-dark-400">60 min</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-dark-700/50 rounded-lg">
              <div className="flex items-center space-x-3">
                <ClockIcon className="w-5 h-5 text-accent-500" />
                <span className="text-dark-100">7:00 PM - Math</span>
              </div>
              <span className="text-sm text-dark-400">30 min</span>
            </div>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 className="text-xl font-semibold text-dark-100 mb-4">Study Progress</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-primary-500/20 flex items-center justify-center">
              <span className="text-xl font-bold text-primary-500">75%</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Schedule Adherence</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-accent-500/20 flex items-center justify-center">
              <span className="text-xl font-bold text-accent-500">12</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Days Remaining</p>
          </div>
          
          <div className="text-center">
            <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-secondary-500/20 flex items-center justify-center">
              <span className="text-xl font-bold text-secondary-500">24</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Hours This Week</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Planner;
