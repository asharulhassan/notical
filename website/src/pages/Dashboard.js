import React from 'react';
import { motion } from 'framer-motion';
import {
  AcademicCapIcon,
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  ChartBarIcon,
  FireIcon,
  ClockIcon,
  ArrowTrendingUpIcon,
} from '@heroicons/react/24/outline';

const Dashboard = () => {
  const stats = [
    {
      name: 'Total Flashcards',
      value: '1,247',
      change: '+12%',
      changeType: 'positive',
      icon: AcademicCapIcon,
      color: 'primary',
    },
    {
      name: 'Study Sessions',
      value: '89',
      change: '+23%',
      changeType: 'positive',
      icon: ClockIcon,
      color: 'accent',
    },
    {
      name: 'Test Score',
      value: '87%',
      change: '+5%',
      changeType: 'positive',
      icon: ChartBarIcon,
      color: 'secondary',
    },
    {
      name: 'Study Streak',
      value: '12 days',
      change: '+2 days',
      changeType: 'positive',
      icon: FireIcon,
      color: 'accent',
    },
  ];

  const recentActivity = [
    {
      id: 1,
      type: 'flashcard',
      title: 'Completed Biology Chapter 3',
      time: '2 hours ago',
      icon: AcademicCapIcon,
      color: 'primary',
    },
    {
      id: 2,
      type: 'note',
      title: 'Created Chemistry Notes',
      time: '4 hours ago',
      icon: DocumentTextIcon,
      color: 'secondary',
    },
    {
      id: 3,
      type: 'test',
      title: 'Scored 92% on Math Quiz',
      time: '1 day ago',
      icon: ClipboardDocumentListIcon,
      color: 'accent',
    },
  ];

  const quickActions = [
    {
      name: 'Create Flashcards',
      description: 'Generate AI-powered flashcards from your notes',
      icon: AcademicCapIcon,
      color: 'primary',
      href: '/flashcards',
    },
    {
      name: 'Study Now',
      description: 'Continue your current study session',
      icon: ClockIcon,
      color: 'accent',
      href: '/flashcards',
    },
    {
      name: 'Take a Test',
      description: 'Test your knowledge with AI-generated quizzes',
      icon: ClipboardDocumentListIcon,
      color: 'secondary',
      href: '/tests',
    },
    {
      name: 'AI Tutor',
      description: 'Get help with difficult concepts',
      icon: ChartBarIcon,
      color: 'secondary',
      href: '/tutor',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-dark-100">Welcome back!</h1>
          <p className="text-dark-400 mt-1">Here's what's happening with your studies today.</p>
        </div>
        <div className="flex items-center space-x-3">
          <span className="text-sm text-dark-400">Last study session:</span>
          <span className="text-sm font-medium text-dark-200">2 hours ago</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={stat.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="card hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-dark-400">{stat.name}</p>
                <p className="text-2xl font-bold text-dark-100 mt-1">{stat.value}</p>
                <div className="flex items-center mt-2">
                  <ArrowTrendingUpIcon className="w-4 h-4 text-accent-500 mr-1" />
                  <span className="text-sm text-accent-500 font-medium">{stat.change}</span>
                </div>
              </div>
              <div className={`p-3 rounded-lg bg-${stat.color}-500/10`}>
                <stat.icon className={`w-8 h-8 text-${stat.color}-500`} />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quick Actions */}
        <div className="lg:col-span-2">
          <div className="card">
            <h2 className="text-xl font-semibold text-dark-100 mb-4">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {quickActions.map((action, index) => (
                <motion.button
                  key={action.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="p-4 rounded-lg border border-dark-700 hover:border-primary-500/30 hover:bg-dark-700/50 transition-all duration-200 text-left group"
                >
                  <div className="flex items-center space-x-3">
                    <div className={`p-2 rounded-lg bg-${action.color}-500/10 group-hover:bg-${action.color}-500/20 transition-colors`}>
                      <action.icon className={`w-6 h-6 text-${action.color}-500`} />
                    </div>
                    <div>
                      <h3 className="font-medium text-dark-100 group-hover:text-primary-400 transition-colors">
                        {action.name}
                      </h3>
                      <p className="text-sm text-dark-400 mt-1">{action.description}</p>
                    </div>
                  </div>
                </motion.button>
              ))}
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="card">
          <h2 className="text-xl font-semibold text-dark-100 mb-4">Recent Activity</h2>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <motion.div
                key={activity.id}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
                className="flex items-center space-x-3 p-3 rounded-lg hover:bg-dark-700/50 transition-colors"
              >
                <div className={`p-2 rounded-lg bg-${activity.color}-500/10`}>
                  <activity.icon className={`w-5 h-5 text-${activity.color}-500`} />
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-dark-100">{activity.title}</p>
                  <p className="text-xs text-dark-400">{activity.time}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      {/* Study Progress */}
      <div className="card">
        <h2 className="text-xl font-semibold text-dark-100 mb-4">Study Progress</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center">
              <span className="text-2xl font-bold text-white">87%</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Overall Progress</p>
            <p className="text-xs text-dark-400 mt-1">Biology, Chemistry, Math</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-gradient-to-br from-accent-500 to-green-500 flex items-center justify-center">
              <span className="text-2xl font-bold text-white">12</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Day Streak</p>
            <p className="text-xs text-dark-400 mt-1">Keep it up!</p>
          </div>
          <div className="text-center">
            <div className="w-20 h-20 mx-auto mb-3 rounded-full bg-gradient-to-br from-secondary-500 to-purple-500 flex items-center justify-center">
              <span className="text-2xl font-bold text-white">24</span>
            </div>
            <p className="text-sm font-medium text-dark-100">Hours This Week</p>
            <p className="text-xs text-dark-400 mt-1">Goal: 30 hours</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
