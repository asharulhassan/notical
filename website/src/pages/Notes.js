import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  PlusIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  DocumentArrowDownIcon,
  SparklesIcon,
  PencilIcon,
  EyeIcon,
  EyeSlashIcon,
  TrashIcon,
  ShareIcon,
  BookOpenIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/react/24/outline';

const Notes = () => {
  const [activeTab, setActiveTab] = useState('my-notes');
  const [selectedNote, setSelectedNote] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const tabs = [
    { id: 'my-notes', name: 'My Notes', icon: DocumentTextIcon },
    { id: 'ai-generate', name: 'AI Generate', icon: SparklesIcon },
    { id: 'templates', name: 'Templates', icon: BookOpenIcon },
    { id: 'import', name: 'Import', icon: DocumentArrowDownIcon },
  ];

  const noteTemplates = [
    {
      id: 1,
      name: 'Cornell Method',
      description: 'Classic note-taking method with cues, notes, and summary',
      icon: BookOpenIcon,
      color: 'primary',
    },
    {
      id: 2,
      name: 'Mind Map',
      description: 'Visual organization of concepts and relationships',
      icon: AcademicCapIcon,
      color: 'secondary',
    },
    {
      id: 3,
      name: 'Outline',
      description: 'Hierarchical structure for organized information',
      icon: DocumentTextIcon,
      color: 'accent',
    },
    {
      id: 4,
      name: 'Flow Chart',
      description: 'Step-by-step process visualization',
      icon: ClipboardDocumentListIcon,
      color: 'secondary',
    },
  ];

  const myNotes = [
    {
      id: 1,
      title: 'Biology: Cell Biology Chapter 3',
      subject: 'Biology',
      template: 'Cornell Method',
      lastModified: '2 hours ago',
      wordCount: 1247,
      tags: ['Cell Biology', 'High School'],
      content: 'This is a sample note content...',
    },
    {
      id: 2,
      title: 'Chemistry: Organic Compounds',
      subject: 'Chemistry',
      template: 'Mind Map',
      lastModified: '1 day ago',
      wordCount: 892,
      tags: ['Organic Chemistry', 'College'],
      content: 'This is a sample note content...',
    },
    {
      id: 3,
      title: 'Mathematics: Calculus Derivatives',
      subject: 'Mathematics',
      template: 'Outline',
      lastModified: '3 days ago',
      wordCount: 1567,
      tags: ['Calculus', 'University'],
      content: 'This is a sample note content...',
    },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'my-notes':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-dark-100">My Notes</h2>
              <div className="flex space-x-3">
                <button className="btn-secondary flex items-center space-x-2">
                  <DocumentArrowDownIcon className="w-5 h-5" />
                  <span>Export All</span>
                </button>
                <button className="btn-primary flex items-center space-x-2">
                  <PlusIcon className="w-5 h-5" />
                  <span>New Note</span>
                </button>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {myNotes.map((note, index) => (
                <motion.div
                  key={note.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="card hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
                  onClick={() => setSelectedNote(note)}
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="w-12 h-12 rounded-lg bg-primary-500/10 flex items-center justify-center">
                      <DocumentTextIcon className="w-6 h-6 text-primary-500" />
                    </div>
                    <div className="flex space-x-2">
                      <button className="p-2 text-dark-400 hover:text-dark-200 hover:bg-dark-700 rounded-lg transition-colors">
                        <ShareIcon className="w-4 h-4" />
                      </button>
                      <button className="p-2 text-dark-400 hover:text-dark-200 hover:bg-dark-700 rounded-lg transition-colors">
                        <DocumentArrowDownIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-lg font-semibold text-dark-100 mb-2 group-hover:text-primary-400 transition-colors">
                    {note.title}
                  </h3>
                  <p className="text-sm text-dark-400 mb-3">{note.subject}</p>

                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-dark-300">{note.template}</span>
                    <span className="text-sm text-dark-400">{note.lastModified}</span>
                  </div>

                  <div className="flex items-center justify-between mb-4">
                    <span className="text-sm text-dark-300">{note.wordCount} words</span>
                    <span className="text-sm text-dark-400">{note.subject}</span>
                  </div>

                  <div className="flex flex-wrap gap-2">
                    {note.tags.map((tag, tagIndex) => (
                      <span
                        key={tagIndex}
                        className="px-2 py-1 text-xs bg-dark-700 text-dark-300 rounded-md"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        );

      case 'ai-generate':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">AI Note Generation</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Input Section */}
              <div className="space-y-6">
                <div className="card">
                  <h3 className="text-xl font-semibold text-dark-100 mb-4">Input Content</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-dark-300 mb-2">
                        Upload Content
                      </label>
                      <div className="border-2 border-dashed border-dark-600 rounded-lg p-6 text-center hover:border-primary-500/50 transition-colors cursor-pointer">
                        <DocumentArrowDownIcon className="w-12 h-12 text-dark-400 mx-auto mb-2" />
                        <p className="text-dark-400">Drop PDF, images, or text here</p>
                        <p className="text-sm text-dark-500 mt-1">AI will generate structured notes</p>
                      </div>
                    </div>
                    
                    <div>
                      <label className="block text-sm font-medium text-dark-300 mb-2">
                        Or paste text directly
                      </label>
                      <textarea
                        className="input-field w-full h-32"
                        placeholder="Paste your content here for AI processing..."
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-dark-300 mb-2">
                        Note Template
                      </label>
                      <select className="input-field w-full">
                        <option>Cornell Method</option>
                        <option>Mind Map</option>
                        <option>Outline</option>
                        <option>Flow Chart</option>
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-dark-300 mb-2">
                        Subject
                      </label>
                      <select className="input-field w-full">
                        <option>Biology</option>
                        <option>Chemistry</option>
                        <option>Mathematics</option>
                        <option>Physics</option>
                        <option>History</option>
                      </select>
                    </div>

                    <button 
                      className="w-full btn-primary flex items-center justify-center space-x-2"
                      onClick={() => setIsGenerating(true)}
                    >
                      <SparklesIcon className="w-5 h-5" />
                      <span>Generate Notes with AI</span>
                    </button>
                  </div>
                </div>

                {/* Note Optimization */}
                <div className="card">
                  <h3 className="text-xl font-semibold text-dark-100 mb-4">Note Optimization</h3>
                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-dark-300 mb-2">
                        Upload existing notes for AI optimization
                      </label>
                      <div className="border-2 border-dashed border-dark-600 rounded-lg p-6 text-center hover:border-primary-500/50 transition-colors cursor-pointer">
                        <DocumentArrowDownIcon className="w-12 h-12 text-dark-400 mx-auto mb-2" />
                        <p className="text-dark-400">Drop your notes here</p>
                        <p className="text-sm text-dark-500 mt-1">AI will clean and optimize them</p>
                      </div>
                    </div>
                    <button className="w-full btn-secondary">
                      Optimize Notes
                    </button>
                  </div>
                </div>
              </div>

              {/* Output Section */}
              <div className="card">
                <h3 className="text-xl font-semibold text-dark-100 mb-4">Generated Notes</h3>
                
                {isGenerating ? (
                  <div className="text-center py-12">
                    <div className="animate-spin w-12 h-12 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
                    <p className="text-dark-400">AI is generating your notes...</p>
                    <p className="text-sm text-dark-500 mt-1">This may take a few moments</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="text-center py-12 text-dark-400">
                      <DocumentTextIcon className="w-16 h-16 mx-auto mb-4 opacity-50" />
                      <p>Your AI-generated notes will appear here</p>
                    </div>
                  </div>
                )}

                {isGenerating && (
                  <div className="mt-6 pt-6 border-t border-dark-700">
                    <div className="flex space-x-3">
                      <button className="flex-1 btn-secondary">
                        Save Draft
                      </button>
                      <button className="flex-1 btn-primary">
                        Export Notes
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        );

      case 'templates':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">Note Templates</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {noteTemplates.map((template, index) => (
                <motion.div
                  key={template.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="card hover:shadow-xl transition-all duration-300 hover:-translate-y-1 cursor-pointer group"
                >
                  <div className="text-center">
                    <div className={`w-16 h-16 mx-auto mb-4 rounded-lg bg-${template.color}-500/10 flex items-center justify-center`}>
                      <template.icon className={`w-8 h-8 text-${template.color}-500`} />
                    </div>
                    
                    <h3 className="text-lg font-semibold text-dark-100 mb-2 group-hover:text-primary-400 transition-colors">
                      {template.name}
                    </h3>
                    
                    <p className="text-sm text-dark-400 mb-4">
                      {template.description}
                    </p>
                    
                    <button className="btn-primary w-full">
                      Use Template
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>
        );

      case 'import':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">Import Notes</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-xl font-semibold text-dark-100 mb-4">From File</h3>
                <div className="space-y-4">
                  <div className="border-2 border-dashed border-dark-600 rounded-lg p-6 text-center">
                    <DocumentArrowDownIcon className="w-12 h-12 text-dark-400 mx-auto mb-2" />
                    <p className="text-dark-400">Upload DOC, TXT, PDF, or other formats</p>
                  </div>
                  <button className="w-full btn-primary">Choose File</button>
                </div>
              </div>

              <div className="card">
                <h3 className="text-xl font-semibold text-dark-100 mb-4">From URL</h3>
                <div className="space-y-4">
                  <input
                    type="url"
                    placeholder="https://example.com/notes"
                    className="input-field w-full"
                  />
                  <button className="w-full btn-primary">Import from URL</button>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="space-y-6">
      {/* Tab Navigation */}
      <div className="border-b border-dark-700">
        <nav className="flex space-x-8">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                activeTab === tab.id
                  ? 'border-primary-500 text-primary-400'
                  : 'border-transparent text-dark-400 hover:text-dark-300 hover:border-dark-600'
              }`}
            >
              <tab.icon className="w-5 h-5" />
              <span>{tab.name}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <AnimatePresence mode="wait">
        <motion.div
          key={activeTab}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -20 }}
          transition={{ duration: 0.2 }}
        >
          {renderTabContent()}
        </motion.div>
      </AnimatePresence>
    </div>
  );
};

export default Notes;
