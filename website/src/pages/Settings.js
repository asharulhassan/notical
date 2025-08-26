import React from 'react';
import { motion } from 'framer-motion';
import { Cog6ToothIcon, UserIcon, BellIcon, ShieldCheckIcon } from '@heroicons/react/24/outline';

const Settings = () => {
  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-dark-100">Settings</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Profile Settings</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">Name</label>
              <input type="text" defaultValue="Student User" className="input-field w-full" />
            </div>
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">Email</label>
              <input type="email" defaultValue="student@example.com" className="input-field w-full" />
            </div>
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">Study Level</label>
              <select className="input-field w-full">
                <option>High School</option>
                <option>College</option>
                <option>University</option>
              </select>
            </div>
            <button className="btn-primary w-full">Save Changes</button>
          </div>
        </div>
        
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Study Preferences</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">Default Study Session Length</label>
              <select className="input-field w-full">
                <option>15 minutes</option>
                <option>30 minutes</option>
                <option>45 minutes</option>
                <option>60 minutes</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-dark-300 mb-2">Reminder Frequency</label>
              <select className="input-field w-full">
                <option>Daily</option>
                <option>Every 2 days</option>
                <option>Weekly</option>
              </select>
            </div>
            <div className="flex items-center space-x-3">
              <input type="checkbox" id="offline" className="rounded" defaultChecked />
              <label htmlFor="offline" className="text-sm text-dark-300">Enable Offline Mode</label>
            </div>
            <button className="btn-secondary w-full">Save Preferences</button>
          </div>
        </div>
      </div>
      
      <div className="card">
        <h2 className="text-xl font-semibold text-dark-100 mb-4">Export & Data</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button className="btn-secondary">
            Export Flashcards
          </button>
          <button className="btn-secondary">
            Export Notes
          </button>
          <button className="btn-secondary">
            Export Progress Data
          </button>
        </div>
      </div>
    </div>
  );
};

export default Settings;
