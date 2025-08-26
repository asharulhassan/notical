import React, { useState } from 'react';
import {
  PlusIcon,
  ClipboardDocumentListIcon,
  DocumentTextIcon,
  ChartBarIcon,
} from '@heroicons/react/24/outline';

const Tests = () => {
  const [activeTab, setActiveTab] = useState('my-tests');

  const tabs = [
    { id: 'my-tests', name: 'My Tests', icon: ClipboardDocumentListIcon },
    { id: 'create', name: 'Create Test', icon: PlusIcon },
    { id: 'past-papers', name: 'Past Papers', icon: DocumentTextIcon },
    { id: 'performance', name: 'Performance', icon: ChartBarIcon },
  ];

  return (
    <div className="space-y-6">
      <div className="border-b border-[#1C1E22]">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-[#39FF14] text-[#39FF14]'
                  : 'border-transparent text-[#38BDF8] hover:text-[#00F0FF] hover:border-[#1C1E22]'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.name}</span>
            </button>
          ))}
        </nav>
      </div>

      <div className="premium-card">
        <h2 className="text-2xl font-bold text-white mb-4">AI Test Generation</h2>
        <p className="text-[#38BDF8] mb-6">Create tests from your notes, flashcards, and textbooks using AI.</p>
        <button className="premium-button">Generate Test</button>
      </div>
    </div>
  );
};

export default Tests;
