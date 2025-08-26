import React, { useState } from 'react';
import { motion } from 'framer-motion';
import {
  UsersIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  ShieldCheckIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  ExclamationTriangleIcon,
  CheckCircleIcon,
  XCircleIcon,
  EyeIcon,
  PencilIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';

const Admin = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedUser, setSelectedUser] = useState(null);

  const tabs = [
    { id: 'overview', name: 'Overview', icon: ChartBarIcon },
    { id: 'users', name: 'User Management', icon: UsersIcon },
    { id: 'content', name: 'Content Moderation', icon: DocumentTextIcon },
    { id: 'tutors', name: 'Tutor Verification', icon: AcademicCapIcon },
    { id: 'system', name: 'System Settings', icon: Cog6ToothIcon },
  ];

  const stats = [
    {
      name: 'Total Users',
      value: '12,847',
      change: '+12%',
      changeType: 'positive',
      icon: UsersIcon,
      color: 'primary',
    },
    {
      name: 'Active Sessions',
      value: '2,341',
      change: '+8%',
      changeType: 'positive',
      icon: AcademicCapIcon,
      color: 'accent',
    },
    {
      name: 'Content Generated',
      value: '45,892',
      change: '+23%',
      changeType: 'positive',
      icon: DocumentTextIcon,
      color: 'secondary',
    },
    {
      name: 'System Health',
      value: '99.9%',
      change: '0%',
      changeType: 'neutral',
      icon: ShieldCheckIcon,
      color: 'accent',
    },
  ];

  const recentUsers = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      role: 'Student',
      status: 'active',
      joined: '2 hours ago',
      lastActive: '1 hour ago',
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      role: 'Tutor',
      status: 'pending',
      joined: '4 hours ago',
      lastActive: 'Never',
    },
    {
      id: 3,
      name: 'Mike Johnson',
      email: 'mike@example.com',
      role: 'Student',
      status: 'active',
      joined: '1 day ago',
      lastActive: '30 minutes ago',
    },
  ];

  const pendingTutors = [
    {
      id: 1,
      name: 'Dr. Sarah Wilson',
      email: 'sarah@university.edu',
      subject: 'Biology',
      credentials: 'PhD Biology, 10 years experience',
      status: 'pending',
      submitted: '2 days ago',
    },
    {
      id: 2,
      name: 'Prof. Robert Chen',
      email: 'robert@college.edu',
      subject: 'Mathematics',
      credentials: 'MSc Mathematics, 8 years experience',
      status: 'pending',
      submitted: '3 days ago',
    },
  ];

  const renderTabContent = () => {
    switch (activeTab) {
      case 'overview':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">System Overview</h2>
            
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {stats.map((stat, index) => (
                <motion.div
                  key={stat.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="card"
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-dark-400">{stat.name}</p>
                      <p className="text-2xl font-bold text-dark-100 mt-1">{stat.value}</p>
                      <div className="flex items-center mt-2">
                        <span className={`text-sm font-medium ${
                          stat.changeType === 'positive' ? 'text-accent-500' : 
                          stat.changeType === 'negative' ? 'text-red-500' : 'text-dark-400'
                        }`}>
                          {stat.change}
                        </span>
                      </div>
                    </div>
                    <div className={`p-3 rounded-lg bg-${stat.color}-500/10`}>
                      <stat.icon className={`w-8 h-8 text-${stat.color}-500`} />
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>

            {/* Recent Activity */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-lg font-semibold text-dark-100 mb-4">Recent Users</h3>
                <div className="space-y-3">
                  {recentUsers.map((user) => (
                    <div key={user.id} className="flex items-center justify-between p-3 bg-dark-700/50 rounded-lg">
                      <div>
                        <p className="font-medium text-dark-100">{user.name}</p>
                        <p className="text-sm text-dark-400">{user.email}</p>
                      </div>
                      <div className="text-right">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          user.status === 'active' ? 'bg-accent-500/20 text-accent-400' :
                          'bg-yellow-500/20 text-yellow-400'
                        }`}>
                          {user.status}
                        </span>
                        <p className="text-xs text-dark-400 mt-1">{user.joined}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-semibold text-dark-100 mb-4">System Alerts</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3 p-3 bg-green-500/10 border border-green-500/30 rounded-lg">
                    <CheckCircleIcon className="w-5 h-5 text-green-500" />
                    <div>
                      <p className="text-sm font-medium text-green-400">System running normally</p>
                      <p className="text-xs text-green-500">All services operational</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3 p-3 bg-yellow-500/10 border border-yellow-500/30 rounded-lg">
                    <ExclamationTriangleIcon className="w-5 h-5 text-yellow-500" />
                    <div>
                      <p className="text-sm font-medium text-yellow-400">High memory usage</p>
                      <p className="text-xs text-yellow-500">Consider scaling up</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'users':
        return (
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-bold text-dark-100">User Management</h2>
              <button className="btn-primary">Add User</button>
            </div>
            
            <div className="card">
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-dark-700">
                      <th className="text-left p-3 text-sm font-medium text-dark-300">User</th>
                      <th className="text-left p-3 text-sm font-medium text-dark-300">Role</th>
                      <th className="text-left p-3 text-sm font-medium text-dark-300">Status</th>
                      <th className="text-left p-3 text-sm font-medium text-dark-300">Joined</th>
                      <th className="text-left p-3 text-sm font-medium text-dark-300">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {recentUsers.map((user) => (
                      <tr key={user.id} className="border-b border-dark-700/50">
                        <td className="p-3">
                          <div>
                            <p className="font-medium text-dark-100">{user.name}</p>
                            <p className="text-sm text-dark-400">{user.email}</p>
                          </div>
                        </td>
                        <td className="p-3">
                          <span className="px-2 py-1 text-xs bg-dark-700 text-dark-300 rounded-full">
                            {user.role}
                          </span>
                        </td>
                        <td className="p-3">
                          <span className={`px-2 py-1 text-xs rounded-full ${
                            user.status === 'active' ? 'bg-accent-500/20 text-accent-400' :
                            'bg-yellow-500/20 text-yellow-400'
                          }`}>
                            {user.status}
                          </span>
                        </td>
                        <td className="p-3 text-sm text-dark-400">{user.joined}</td>
                        <td className="p-3">
                          <div className="flex space-x-2">
                            <button className="p-1 text-dark-400 hover:text-dark-200 hover:bg-dark-700 rounded">
                              <EyeIcon className="w-4 h-4" />
                            </button>
                            <button className="p-1 text-dark-400 hover:text-dark-200 hover:bg-dark-700 rounded">
                              <PencilIcon className="w-4 h-4" />
                            </button>
                            <button className="p-1 text-red-400 hover:text-red-300 hover:bg-red-500/10 rounded">
                              <TrashIcon className="w-4 h-4" />
                            </button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        );

      case 'tutors':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">Tutor Verification</h2>
            
            <div className="card">
              <div className="space-y-4">
                {pendingTutors.map((tutor) => (
                  <div key={tutor.id} className="p-4 border border-dark-700 rounded-lg">
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-dark-100">{tutor.name}</h3>
                        <p className="text-dark-400">{tutor.email}</p>
                        <p className="text-sm text-dark-300 mt-1">
                          <span className="font-medium">Subject:</span> {tutor.subject}
                        </p>
                        <p className="text-sm text-dark-300">
                          <span className="font-medium">Credentials:</span> {tutor.credentials}
                        </p>
                        <p className="text-xs text-dark-400 mt-2">Submitted: {tutor.submitted}</p>
                      </div>
                      <div className="flex space-x-2 ml-4">
                        <button className="btn-accent px-4 py-2">
                          <CheckCircleIcon className="w-4 h-4 mr-2" />
                          Approve
                        </button>
                        <button className="btn-secondary px-4 py-2">
                          <XCircleIcon className="w-4 h-4 mr-2" />
                          Reject
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        );

      case 'system':
        return (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-dark-100">System Settings</h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-lg font-semibold text-dark-100 mb-4">General Settings</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      Site Name
                    </label>
                    <input
                      type="text"
                      defaultValue="NOTICAL"
                      className="input-field w-full"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      Maintenance Mode
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" className="rounded border-dark-600 text-primary-600 focus:ring-primary-500" />
                      <span className="ml-2 text-sm text-dark-300">Enable maintenance mode</span>
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      AI Model Version
                    </label>
                    <select className="input-field w-full">
                      <option>GPT-4 (Latest)</option>
                      <option>GPT-3.5 (Stable)</option>
                      <option>Local Model (Offline)</option>
                    </select>
                  </div>
                </div>
              </div>
              
              <div className="card">
                <h3 className="text-lg font-semibold text-dark-100 mb-4">Security Settings</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      Session Timeout (minutes)
                    </label>
                    <input
                      type="number"
                      defaultValue="30"
                      className="input-field w-full"
                    />
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      Two-Factor Authentication
                    </label>
                    <label className="flex items-center">
                      <input type="checkbox" defaultChecked className="rounded border-dark-600 text-primary-600 focus:ring-primary-500" />
                      <span className="ml-2 text-sm text-dark-300">Require 2FA for admin accounts</span>
                    </label>
                  </div>
                  
                  <div>
                    <label className="block text-sm font-medium text-dark-300 mb-2">
                      Rate Limiting
                    </label>
                    <select className="input-field w-full">
                      <option>Strict (100 requests/hour)</option>
                      <option>Moderate (500 requests/hour)</option>
                      <option>Relaxed (1000 requests/hour)</option>
                    </select>
                  </div>
                </div>
              </div>
            </div>
            
            <div className="card">
              <div className="flex justify-end space-x-3">
                <button className="btn-secondary">Reset to Defaults</button>
                <button className="btn-primary">Save Changes</button>
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
          <h1 className="text-3xl font-bold text-dark-100">Admin Dashboard</h1>
          <p className="text-dark-400 mt-1">Manage users, content, and system settings</p>
        </div>
        <div className="flex items-center space-x-3">
          <span className="text-sm text-dark-400">Admin User</span>
          <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-sm">A</span>
          </div>
        </div>
      </div>

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

export default Admin;
