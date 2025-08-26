import React, { useState } from 'react';
import { motion } from 'framer-motion';
import apiService from '../services/api';
import {
  PlusIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  PhotoIcon,
  MicrophoneIcon,
  BookOpenIcon,
  PlayIcon,
  PauseIcon,
  ArrowLeftIcon,
  ArrowRightIcon,
  CheckIcon,
  XMarkIcon,
  SparklesIcon,
  FolderIcon,
  FolderPlusIcon,
  ChevronRightIcon,
  ChevronDownIcon,
  MagnifyingGlassIcon,
  Cog6ToothIcon,
  ShareIcon,
  TrashIcon,
  StarIcon,
  DocumentIcon,
  DocumentArrowUpIcon,
  SpeakerWaveIcon,
} from '@heroicons/react/24/outline';

const Flashcards = () => {
  const [activeTab, setActiveTab] = useState('folders');
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedCards, setGeneratedCards] = useState([]);
  const [inputText, setInputText] = useState('');
  const [currentCardIndex, setCurrentCardIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);
  const [isStudyMode, setIsStudyMode] = useState(false);
  const [selectedFolders, setSelectedFolders] = useState([]);
  const [expandedFolders, setExpandedFolders] = useState(new Set());
  const [searchQuery, setSearchQuery] = useState('');
  
  // AI Generation Settings
  const [selectedCardTypes, setSelectedCardTypes] = useState(['definition', 'explanation', 'cloze']);
  const [numCards, setNumCards] = useState(5);
  const [difficultyBalance, setDifficultyBalance] = useState('balanced');
  const [selectedSubject, setSelectedSubject] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [fileType, setFileType] = useState('text');
  
  // Enhanced AI generation options
  const [generationMode, setGenerationMode] = useState('text_understanding');
  const [answerStyle, setAnswerStyle] = useState('professional');
  const [examBoard, setExamBoard] = useState('');
  const [learningLevel, setLearningLevel] = useState('university');

  const tabs = [
    { id: 'folders', name: 'Folders', icon: FolderIcon },
    { id: 'study-mode', name: 'Study Mode', icon: AcademicCapIcon },
    { id: 'create-new', name: 'Create New', icon: PlusIcon },
    { id: 'import', name: 'Import', icon: DocumentTextIcon },
  ];

  const cardTypeOptions = [
    { id: 'definition', name: 'Definition', description: 'What is the meaning of...', color: '#39FF14' },
    { id: 'explanation', name: 'Explanation', description: 'How does... work?', color: '#00F0FF' },
    { id: 'cloze', name: 'Cloze', description: 'Fill in the blank', color: '#AFFF00' },
    { id: 'comparison', name: 'Comparison', description: 'Compare and contrast', color: '#38BDF8' },
    { id: 'analysis', name: 'Analysis', description: 'Critical thinking questions', color: '#FF6B6B' },
  ];

  const difficultyOptions = [
    { id: 'easy', name: 'Easy', description: 'Basic recall and simple concepts', color: '#39FF14' },
    { id: 'medium', name: 'Medium', description: 'Comprehension and application', color: '#FFA500' },
    { id: 'hard', name: 'Hard', description: 'Complex analysis and synthesis', color: '#FF6B6B' },
    { id: 'balanced', name: 'Balanced', description: 'Mix of all difficulty levels', color: '#00F0FF' },
  ];

  const subjectOptions = [
    'Physics', 'Chemistry', 'Biology', 'Mathematics', 'History', 'Literature',
    'Computer Science', 'Economics', 'Psychology', 'Geography', 'Other'
  ];

  // GoodNotes-style folder structure with unlimited nesting
  const folderStructure = [
    {
      id: 'biology',
      name: 'Biology',
      type: 'folder',
      color: '#39FF14',
      children: [
        {
          id: 'cell-biology',
          name: 'Cell Biology',
          type: 'folder',
          color: '#AFFF00',
          children: [
            {
              id: 'mitochondria',
              name: 'Mitochondria',
              type: 'deck',
              cardCount: 24,
              lastStudied: '2 hours ago',
              progress: 85,
            },
            {
              id: 'cell-division',
              name: 'Cell Division',
              type: 'deck',
              cardCount: 31,
              lastStudied: '1 day ago',
              progress: 62,
            }
          ]
        },
        {
          id: 'genetics',
          name: 'Genetics',
          type: 'folder',
          color: '#00F0FF',
          children: [
            {
              id: 'dna-structure',
              name: 'DNA Structure',
              type: 'deck',
              cardCount: 18,
              lastStudied: '3 days ago',
              progress: 45,
            }
          ]
        }
      ]
    },
    {
      id: 'chemistry',
      name: 'Chemistry',
      type: 'folder',
      color: '#38BDF8',
      children: [
        {
          id: 'organic-chem',
          name: 'Organic Chemistry',
          type: 'deck',
          cardCount: 42,
          lastStudied: '5 hours ago',
          progress: 73,
        }
      ]
    },
    {
      id: 'mathematics',
      name: 'Mathematics',
      type: 'folder',
      color: '#AFFF00',
      children: [
        {
          id: 'calculus',
          name: 'Calculus',
          type: 'folder',
          color: '#39FF14',
          children: [
            {
              id: 'derivatives',
              name: 'Derivatives',
              type: 'deck',
              cardCount: 28,
              lastStudied: '1 week ago',
              progress: 38,
            }
          ]
        }
      ]
    }
  ];

  const toggleFolder = (folderId) => {
    const newExpanded = new Set(expandedFolders);
    if (newExpanded.has(folderId)) {
      newExpanded.delete(folderId);
    } else {
      newExpanded.add(folderId);
    }
    setExpandedFolders(newExpanded);
  };

  const handleCardTypeToggle = (cardType) => {
    setSelectedCardTypes(prev => 
      prev.includes(cardType)
        ? prev.filter(type => type !== cardType)
        : [...prev, cardType]
    );
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setUploadedFile(file);
      
      // Detect file type
      if (file.name.endsWith('.pdf')) {
        setFileType('pdf');
      } else if (file.name.match(/\.(mp3|wav|m4a|aac)$/)) {
        setFileType('audio');
      } else if (file.name.match(/\.(txt|md|doc|docx)$/)) {
        setFileType('text');
      }
    }
  };

  const handleAIGeneration = async () => {
    if (!inputText.trim()) {
      alert('Please provide content to generate flashcards');
      return;
    }
    
    setIsGenerating(true);
    
    try {
      console.log('🚀 Starting NOTICAL AI generation...');
      
      // Call your NOTICAL AI server
      const response = await apiService.generateFlashcards(inputText, numCards);
      
      console.log('✅ NOTICAL AI generated flashcards:', response);
      
      // Set the generated cards
      setGeneratedCards(response.flashcards || []);
      
      // Switch to view generated cards
      setActiveTab('create-new');
      
      console.log(`🎯 Generated ${response.flashcards?.length || 0} flashcards in ${response.generation_time?.toFixed(2) || 0}s`);
      
    } catch (error) {
      console.error('❌ NOTICAL AI generation failed:', error);
      alert('Failed to generate flashcards. Make sure your NOTICAL server is running on port 8004.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateIntelligentCards = async (content, cardTypes, numCards, generationMode = 'text_understanding', answerStyle = 'professional', examBoard = '', learningLevel = 'university') => {
    try {
      // Call your enhanced AI backend
      const response = await fetch('http://localhost:8002/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content: content,
          card_types: cardTypes,
          num_cards: numCards === 0 ? 999 : numCards,
          subject: selectedSubject || 'general',
          generation_mode: generationMode,
          style: answerStyle,
          exam_board: examBoard || undefined,
          learning_level: learningLevel
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data.flashcards || [];
      
    } catch (error) {
      console.error('Error calling AI backend:', error);
      
      // Fallback to a smarter local function if backend fails
      return generateSmartLocalCards(content, cardTypes, numCards);
    }
  };


  // Fallback function if backend fails - much smarter than the old random word picker
  const generateSmartLocalCards = (content, cardTypes, numCards) => {
    const cards = [];
    
    // Extract meaningful concepts (not random words)
    const sentences = content.split(/[.!?]+/).filter(s => s.trim().length > 20);
    const technicalTerms = content.match(/\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b/g) || [];
    const acronyms = content.match(/\b[A-Z]{2,}\b/g) || [];
    
    const concepts = [...new Set([...technicalTerms, ...acronyms])].filter(c => c.length > 2);
    
    if (concepts.length === 0) {
      // Fallback to sentence-based cards
      return sentences.slice(0, numCards).map((sentence, i) => ({
        question: `What is the main idea in this statement?`,
        answer: sentence.trim(),
        hint: `Focus on the key concept being described`,
        card_type: 'definition',
        difficulty: 'medium'
      }));
    }
    
    // Generate cards based on actual concepts found
    cardTypes.forEach((cardType, typeIndex) => {
      const cardsPerType = Math.ceil(numCards / cardTypes.length);
      
      for (let i = 0; i < cardsPerType && cards.length < numCards; i++) {
        const concept = concepts[i % concepts.length];
        
        let card;
        switch (cardType) {
          case 'definition':
            card = {
              question: `What is ${concept}?`,
              answer: `Based on the content, ${concept} is a technical term or concept that appears in the provided material.`,
              hint: `Look for the definition or explanation of ${concept} in the text`,
              card_type: 'definition',
              difficulty: 'medium'
            };
            break;
            
          case 'cloze':
            const sentence = sentences.find(s => s.includes(concept));
            if (sentence) {
              const clozeQuestion = sentence.replace(new RegExp(concept, 'gi'), '_____');
              card = {
                question: `Complete: "${clozeQuestion.trim()}"`,
                answer: concept,
                hint: `The missing word is ${concept}`,
                card_type: 'cloze',
                difficulty: 'easy'
              };
            } else {
              card = {
                question: `Complete: "The concept of _____ is important in this context."`,
                answer: concept,
                hint: `Think about technical terms mentioned in the text`,
                card_type: 'cloze',
                difficulty: 'easy'
              };
            }
            break;
            
          default:
            card = {
              question: `What is ${concept}?`,
              answer: `${concept} is a key concept from the provided content.`,
              hint: `Look for ${concept} in the text`,
              card_type: 'definition',
              difficulty: 'medium'
            };
        }
        
        cards.push(card);
      }
    });
    
    return cards.slice(0, numCards);
  };



  const startStudySession = (selectedItems = []) => {
    let allCards = [];
    
    if (selectedItems.length > 0) {
      selectedItems.forEach(item => {
        if (item.type === 'deck') {
          allCards.push(...generateDeckCards(item));
        }
      });
    } else {
      allCards = generatedCards;
    }
    
    if (allCards.length === 0) {
      allCards = [
        {
          question: "What is the capital of France?",
          answer: "Paris",
          type: 'geography',
          difficulty: 'easy'
        },
        {
          question: "What is 2 + 2?",
          answer: "4",
          type: 'math',
          difficulty: 'easy'
        },
        {
          question: "What is photosynthesis?",
          answer: "The process by which plants convert sunlight into energy",
          type: 'biology',
          difficulty: 'medium'
        }
      ];
    }
    
    setGeneratedCards(allCards);
    setCurrentCardIndex(0);
    setShowAnswer(false);
    setIsStudyMode(true);
    setActiveTab('study-mode');
  };

  const generateDeckCards = (deck) => {
    const cards = [];
    const subjects = {
      'mitochondria': ['What is the powerhouse of the cell?', 'Mitochondria'],
      'cell-division': ['What are the phases of mitosis?', 'Prophase, Metaphase, Anaphase, Telophase'],
      'dna-structure': ['What is the shape of DNA?', 'Double helix'],
      'organic-chem': ['What is a functional group?', 'A group of atoms that gives characteristic properties to molecules'],
      'derivatives': ['What is the derivative of x²?', '2x']
    };
    
    for (let i = 0; i < deck.cardCount; i++) {
      const subject = deck.name.toLowerCase();
      const question = subjects[subject] ? subjects[subject][0] : `Question ${i + 1} about ${deck.name}`;
      const answer = subjects[subject] ? subjects[subject][1] : `Answer ${i + 1} about ${deck.name}`;
      
      cards.push({
        question,
        answer,
        type: 'definition',
        difficulty: ['easy', 'medium', 'hard'][Math.floor(Math.random() * 3)],
        confidence: 0.9
      });
    }
    
    return cards;
  };

  const nextCard = () => {
    if (currentCardIndex < generatedCards.length - 1) {
      setCurrentCardIndex(currentCardIndex + 1);
      setShowAnswer(false);
    }
  };

  const previousCard = () => {
    if (currentCardIndex > 0) {
      setCurrentCardIndex(currentCardIndex - 1);
      setShowAnswer(false);
    }
  };

  const renderFolderItem = (item, level = 0) => {
    const isExpanded = expandedFolders.has(item.id);
    const isFolder = item.type === 'folder';
    
    return (
      <div key={item.id} className="space-y-2">
        <div 
          className={`flex items-center space-x-3 p-3 rounded-xl hover:bg-[#1C1E22]/50 transition-all duration-200 cursor-pointer group ${
            isFolder ? 'hover:scale-105' : ''
          }`}
          style={{ paddingLeft: `${level * 20 + 12}px` }}
        >
          {isFolder ? (
            <button
              onClick={() => toggleFolder(item.id)}
              className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors"
            >
              {isExpanded ? (
                <ChevronDownIcon className="w-5 h-5" />
              ) : (
                <ChevronRightIcon className="w-5 h-5" />
              )}
            </button>
          ) : (
            <div className="w-5 h-5" />
          )}
          
          <div 
            className="w-8 h-8 rounded-lg flex items-center justify-center"
            style={{ backgroundColor: item.color + '20', border: `1px solid ${item.color}40` }}
          >
            {isFolder ? (
              <FolderIcon className="w-5 h-5" style={{ color: item.color }} />
            ) : (
              <BookOpenIcon className="w-5 h-5" style={{ color: item.color }} />
            )}
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-white truncate">{item.name}</h3>
            {!isFolder && (
              <div className="flex items-center space-x-4 text-sm text-[#38BDF8]">
                <span>{item.cardCount} cards</span>
                <span>{item.lastStudied}</span>
                <span>{item.progress}%</span>
              </div>
            )}
          </div>
          
          {!isFolder && (
            <div className="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
              <button 
                onClick={() => startStudySession([item])}
                className="p-2 text-[#39FF14] hover:text-[#AFFF00] hover:bg-[#39FF14]/10 rounded-lg transition-all"
              >
                <PlayIcon className="w-4 h-4" />
              </button>
              <button className="p-2 text-[#00F0FF] hover:text-[#38BDF8] hover:bg-[#00F0FF]/10 rounded-lg transition-all">
                <StarIcon className="w-4 h-4" />
              </button>
              <button className="p-2 text-[#AFFF00] hover:text-[#39FF14] hover:bg-[#AFFF00]/10 rounded-lg transition-all">
                <ShareIcon className="w-4 h-4" />
              </button>
            </div>
          )}
        </div>
        
        {isFolder && isExpanded && item.children && (
          <div className="space-y-1">
            {item.children.map(child => renderFolderItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  const renderTabContent = () => {
    switch (activeTab) {
      case 'folders':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-bold text-white">My Flashcard Folders</h2>
                <p className="text-[#38BDF8] mt-1">Organize your knowledge with unlimited nested folders</p>
              </div>
              <div className="flex items-center space-x-3">
                <button className="premium-button">
                  <FolderPlusIcon className="w-5 h-5 mr-2" />
                  New Folder
                </button>
                <button 
                  onClick={() => setActiveTab('create-new')}
                  className="premium-button"
                >
                  <PlusIcon className="w-5 h-5 mr-2" />
                  New Deck
                </button>
              </div>
            </div>
            
            {/* Search Bar */}
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-[#38BDF8]" />
              <input
                type="text"
                placeholder="Search folders, decks, or cards..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-[#1C1E22]/50 border border-[#39FF14]/20 rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200"
              />
            </div>
            
            {/* Folder Structure */}
            <div className="bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-3xl p-6">
              <div className="space-y-2">
                {folderStructure.map(item => renderFolderItem(item))}
              </div>
            </div>
          </div>
        );

      case 'study-mode':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">Study Mode</h2>
              <button 
                onClick={() => setIsStudyMode(false)}
                className="btn-secondary"
              >
                Exit Study Mode
              </button>
            </div>
            
            {generatedCards.length > 0 ? (
              <div className="max-w-4xl mx-auto">
                <div className="premium-card text-center">
                  <div className="mb-6">
                    <span className="text-sm text-[#38BDF8]">
                      Card {currentCardIndex + 1} of {generatedCards.length}
                    </span>
                  </div>
                  
                  <div className="mb-8">
                    <h3 className="text-2xl font-bold text-white mb-4">
                      {generatedCards[currentCardIndex]?.question}
                    </h3>
                    
                    {showAnswer && (
                      <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="mt-6 p-6 bg-[#1C1E22]/50 rounded-xl border border-[#39FF14]/20"
                      >
                        <h4 className="text-lg font-semibold text-white mb-2">Answer:</h4>
                        <p className="text-[#38BDF8] text-lg">
                          {generatedCards[currentCardIndex]?.answer}
                        </p>
                        {generatedCards[currentCardIndex]?.hint && (
                          <div className="mt-4 p-3 bg-[#00F0FF]/10 rounded-lg border border-[#00F0FF]/20">
                            <p className="text-sm text-[#00F0FF]">
                              💡 Hint: {generatedCards[currentCardIndex]?.hint}
                            </p>
                          </div>
                        )}
                      </motion.div>
                    )}
                  </div>
                  
                  <div className="flex items-center justify-center space-x-4">
                    <button
                      onClick={previousCard}
                      disabled={currentCardIndex === 0}
                      className="btn-secondary disabled:opacity-50"
                    >
                      <ArrowLeftIcon className="w-5 h-5" />
                    </button>
                    
                    <button
                      onClick={() => setShowAnswer(!showAnswer)}
                      className="premium-button px-8"
                    >
                      {showAnswer ? 'Hide Answer' : 'Show Answer'}
                    </button>
                    
                    <button
                      onClick={nextCard}
                      disabled={currentCardIndex === generatedCards.length - 1}
                      className="btn-secondary disabled:opacity-50"
                    >
                      <ArrowRightIcon className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <AcademicCapIcon className="w-16 h-16 text-[#38BDF8] mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No Cards to Study</h3>
                <p className="text-[#38BDF8] mb-6">Create a new deck or import existing cards to start studying.</p>
                <button 
                  onClick={() => setActiveTab('create-new')}
                  className="premium-button"
                >
                  Create New Deck
                </button>
              </div>
            )}
          </div>
        );

      case 'create-new':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-white">Create New Flashcards</h2>
              <button 
                onClick={() => setActiveTab('folders')}
                className="btn-secondary"
              >
                Back to Folders
              </button>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* AI Generation Settings */}
              <div className="premium-card">
                <div className="flex items-center space-x-3 mb-6">
                  <div className="w-10 h-10 bg-gradient-to-r from-[#39FF14] to-[#AFFF00] rounded-xl flex items-center justify-center">
                    <SparklesIcon className="w-6 h-6 text-[#0A0A0F]" />
                  </div>
                  <h3 className="text-xl font-bold text-white">AI Generation Settings</h3>
                </div>
                
                <div className="space-y-6">
                  {/* Card Types Selection */}
                  <div>
                    <label className="block text-sm font-medium text-[#38BDF8] mb-3">
                      Card Types
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      {cardTypeOptions.map((option) => (
                        <button
                          key={option.id}
                          onClick={() => handleCardTypeToggle(option.id)}
                          className={`p-3 rounded-lg border-2 transition-all ${
                            selectedCardTypes.includes(option.id)
                              ? 'border-[#39FF14] bg-[#39FF14]/10'
                              : 'border-[#1C1E22] hover:border-[#39FF14]/50'
                          }`}
                        >
                          <div className="text-left">
                            <div className="font-medium text-white">{option.name}</div>
                            <div className="text-xs text-[#38BDF8]">{option.description}</div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  {/* Number of Cards */}
                              <div>
              <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                Number of Cards: {numCards === 0 ? 'Unlimited' : numCards}
              </label>
              <div className="flex items-center space-x-4">
                <input
                  type="range"
                  min="3"
                  max="50"
                  value={numCards === 0 ? 25 : numCards}
                  onChange={(e) => setNumCards(parseInt(e.target.value))}
                  className="flex-1 h-2 bg-[#1C1E22] rounded-lg appearance-none cursor-pointer slider"
                />
                <button
                  onClick={() => setNumCards(numCards === 0 ? 10 : 0)}
                  className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                    numCards === 0
                      ? 'bg-[#39FF14] text-[#0A0A0F]'
                      : 'bg-[#1C1E22] text-[#38BDF8] border border-[#39FF14]/20'
                  }`}
                >
                  {numCards === 0 ? 'Limited' : 'Unlimited'}
                </button>
              </div>
              <div className="flex justify-between text-xs text-[#38BDF8] mt-1">
                <span>3</span>
                <span>50</span>
              </div>
            </div>

            {/* Enhanced AI Generation Options */}
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Generation Mode
                </label>
                <select
                  value={generationMode}
                  onChange={(e) => setGenerationMode(e.target.value)}
                  className="w-full bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-xl px-4 py-3 text-[#38BDF8] focus:outline-none focus:border-[#39FF14] transition-colors"
                >
                  <option value="text_understanding">Smart Understanding (Recommended)</option>
                  <option value="strict_text">Strict Text (Word-to-Word)</option>
                  <option value="online_research">Online Research (Coming Soon)</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Answer Style
                </label>
                <select
                  value={answerStyle}
                  onChange={(e) => setAnswerStyle(e.target.value)}
                  className="w-full bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-xl px-4 py-3 text-[#38BDF8] focus:outline-none focus:border-[#39FF14] transition-colors"
                >
                  <option value="professional">Professional/Academic</option>
                  <option value="simple">Simple & Clear</option>
                  <option value="exam_focused">Exam-Focused</option>
                </select>
              </div>

              {answerStyle === 'exam_focused' && (
                <div>
                  <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                    Exam Board
                  </label>
                  <select
                    value={examBoard}
                    onChange={(e) => setExamBoard(e.target.value)}
                    className="w-full bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-xl px-4 py-3 text-[#38BDF8] focus:outline-none focus:border-[#39FF14] transition-colors"
                  >
                    <option value="">Select Exam Board</option>
                    <option value="AQA">AQA</option>
                    <option value="OCR">OCR</option>
                    <option value="Edexcel">Edexcel</option>
                    <option value="Cambridge">Cambridge</option>
                    <option value="IB">International Baccalaureate</option>
                  </select>
                </div>
              )}

              <div>
                <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Learning Level
                </label>
                <select
                  value={learningLevel}
                  onChange={(e) => setLearningLevel(e.target.value)}
                  className="w-full bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-xl px-4 py-3 text-[#38BDF8] focus:outline-none focus:border-[#39FF14] transition-colors"
                >
                  <option value="high_school">High School</option>
                  <option value="university">University</option>
                  <option value="postgraduate">Postgraduate</option>
                </select>
              </div>
            </div>
                  
                  {/* Difficulty Balance */}
                  <div>
                    <label className="block text-sm font-medium text-[#38BDF8] mb-3">
                      Difficulty Balance
                    </label>
                    <div className="grid grid-cols-2 gap-3">
                      {difficultyOptions.map((option) => (
                        <button
                          key={option.id}
                          onClick={() => setDifficultyBalance(option.id)}
                          className={`p-3 rounded-lg border-2 transition-all ${
                            difficultyBalance === option.id
                              ? 'border-[#39FF14] bg-[#39FF14]/10'
                              : 'border-[#1C1E22] hover:border-[#39FF14]/50'
                          }`}
                        >
                          <div className="text-left">
                            <div className="font-medium text-white">{option.name}</div>
                            <div className="text-xs text-[#38BDF8]">{option.description}</div>
                          </div>
                        </button>
                      ))}
                    </div>
                  </div>
                  
                  {/* Subject Selection */}
                  <div>
                    <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                      Subject (Optional)
                    </label>
                    <select
                      value={selectedSubject}
                      onChange={(e) => setSelectedSubject(e.target.value)}
                      className="w-full px-4 py-3 bg-[#1C1E22]/50 border border-[#39FF14]/20 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200"
                    >
                      <option value="">Auto-detect</option>
                      {subjectOptions.map((subject) => (
                        <option key={subject} value={subject}>{subject}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
              
              {/* Content Input */}
              <div className="premium-card">
                <h3 className="text-xl font-bold text-white mb-6">Content Input</h3>
                
                <div className="space-y-4">
                  {/* File Upload */}
                  <div>
                    <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                      Upload File (PDF, Audio, Text)
                    </label>
                    <div className="border-2 border-dashed border-[#39FF14]/30 rounded-xl p-6 text-center hover:border-[#39FF14]/50 transition-colors">
                      <input
                        type="file"
                        onChange={handleFileUpload}
                        accept=".pdf,.mp3,.wav,.m4a,.txt,.md,.doc,.docx"
                        className="hidden"
                        id="file-upload"
                      />
                      <label htmlFor="file-upload" className="cursor-pointer">
                        {uploadedFile ? (
                          <div className="space-y-2">
                            <DocumentIcon className="w-12 h-12 text-[#39FF14] mx-auto" />
                            <div className="text-white font-medium">{uploadedFile.name}</div>
                            <div className="text-sm text-[#38BDF8] capitalize">{fileType} file</div>
                          </div>
                        ) : (
                          <div className="space-y-2">
                            <DocumentArrowUpIcon className="w-12 h-12 text-[#38BDF8] mx-auto" />
                            <div className="text-white">Click to upload or drag and drop</div>
                            <div className="text-sm text-[#38BDF8]">PDF, Audio, or Text files</div>
                          </div>
                        )}
                      </label>
                    </div>
                  </div>
                  
                  {/* Text Input */}
                  <div>
                    <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                      Or paste text directly
                    </label>
                    <textarea
                      value={inputText}
                      onChange={(e) => setInputText(e.target.value)}
                      placeholder="Paste your study material, textbook content, or notes here..."
                      className="w-full h-32 px-4 py-3 bg-[#1C1E22]/50 border border-[#39FF14]/20 rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 resize-none"
                    />
                  </div>
                  
                  {/* Generate Button */}
                  <button
                    onClick={handleAIGeneration}
                    disabled={(!inputText.trim() && !uploadedFile) || selectedCardTypes.length === 0 || isGenerating}
                    className="premium-button w-full"
                  >
                    {isGenerating ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-[#0A0A0F] mr-2"></div>
                        Generating Cards...
                      </div>
                    ) : (
                      <>
                        <SparklesIcon className="w-5 h-5 mr-2" />
                        Generate Flashcards with AI
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
            
            {/* Generated Cards Preview */}
            {generatedCards.length > 0 && (
              <div className="premium-card">
                <h3 className="text-xl font-bold text-white mb-6">Generated Cards</h3>
                
                <div className="space-y-4">
                  {generatedCards.map((card, index) => (
                    <div key={index} className="p-4 bg-[#1C1E22]/50 rounded-lg border border-[#39FF14]/20">
                      <div className="flex items-start justify-between mb-2">
                        <span className="text-xs bg-[#00F0FF]/20 text-[#00F0FF] px-2 py-1 rounded-full">
                          {card.card_type}
                        </span>
                        <span className="text-xs bg-[#39FF14]/20 text-[#39FF14] px-2 py-1 rounded-full">
                          {card.difficulty}
                        </span>
                      </div>
                      <h4 className="font-medium text-white mb-2">{card.question}</h4>
                      <p className="text-sm text-[#38BDF8] mb-2">{card.answer}</p>
                      {card.hint && (
                        <p className="text-xs text-[#AFFF00]">💡 {card.hint}</p>
                      )}
                    </div>
                  ))}
                  
                  <div className="flex space-x-3 pt-4">
                    <button 
                      onClick={() => startStudySession()}
                      className="premium-button flex-1"
                    >
                      <PlayIcon className="w-4 h-4 mr-2" />
                      Start Studying
                    </button>
                    <button className="btn-secondary">
                      <DocumentTextIcon className="w-4 h-4 mr-2" />
                      Export
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        );

      case 'import':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-white">Import Flashcards</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="premium-card text-center p-8 hover:scale-105 transition-transform duration-300 cursor-pointer">
                <DocumentTextIcon className="w-16 h-16 text-[#00F0FF] mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Text Import</h3>
                <p className="text-[#38BDF8] mb-4">Import from plain text or markdown files</p>
                <button className="premium-button">Import Text</button>
              </div>
              
              <div className="premium-card text-center p-8 hover:scale-105 transition-transform duration-300 cursor-pointer">
                <PhotoIcon className="w-16 h-16 text-[#39FF14] mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Image Import</h3>
                <p className="text-[#38BDF8] mb-4">Upload images and extract text</p>
                <button className="premium-button">Import Images</button>
              </div>
              
              <div className="premium-card text-center p-8 hover:scale-105 transition-transform duration-300 cursor-pointer">
                <SpeakerWaveIcon className="w-16 h-16 text-[#AFFF00] mx-auto mb-4" />
                <h3 className="text-xl font-bold text-white mb-2">Audio Import</h3>
                <p className="text-[#38BDF8] mb-4">Convert speech to text</p>
                <button className="premium-button">Import Audio</button>
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
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-white">Flashcards</h1>
          <p className="text-[#38BDF8] mt-1">Create, study, and master your knowledge with AI-powered flashcards</p>
        </div>
      </div>

      {/* Tab Navigation */}
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

      {/* Tab Content */}
      <motion.div
        key={activeTab}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -20 }}
        transition={{ duration: 0.2 }}
      >
        {renderTabContent()}
      </motion.div>
    </div>
  );
};

export default Flashcards;
