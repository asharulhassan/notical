import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  HomeIcon,
  AcademicCapIcon,
  DocumentTextIcon,
  ClipboardDocumentListIcon,
  UserGroupIcon,
  AcademicCapIcon as TutorIcon,
  CalendarIcon,
  Cog6ToothIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  ShieldCheckIcon,
} from '@heroicons/react/24/outline';

const Sidebar = () => {
  const [collapsed, setCollapsed] = useState(false);

  const navigation = [
    { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    { name: 'Flashcards', href: '/flashcards', icon: AcademicCapIcon },
    { name: 'Notes', href: '/notes', icon: DocumentTextIcon },
    { name: 'Tests', href: '/tests', icon: ClipboardDocumentListIcon },
    { name: 'Community', href: '/community', icon: UserGroupIcon },
    { name: 'AI Tutor', href: '/tutor', icon: TutorIcon },
    { name: 'Study Planner', href: '/planner', icon: CalendarIcon },
    { name: 'Settings', href: '/settings', icon: Cog6ToothIcon },
    { name: 'Admin', href: '/admin', icon: ShieldCheckIcon, admin: true },
  ];

  return (
    <motion.div
      initial={{ width: 280 }}
      animate={{ width: collapsed ? 80 : 280 }}
      className="bg-dark-900 border-r border-dark-700 flex flex-col"
    >
      {/* Logo */}
      <div className="flex items-center justify-between p-6 border-b border-dark-700">
        {!collapsed && (
          <motion.h1
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="text-2xl font-bold text-gradient"
          >
            NOTICAL
          </motion.h1>
        )}
        <button
          onClick={() => setCollapsed(!collapsed)}
          className="p-2 rounded-lg hover:bg-dark-800 transition-colors"
        >
          {collapsed ? (
            <ChevronRightIcon className="w-5 h-5 text-dark-400" />
          ) : (
            <ChevronLeftIcon className="w-5 h-5 text-dark-400" />
          )}
        </button>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-2">
        {navigation.map((item) => (
          <NavLink
            key={item.name}
            to={item.href}
            className={({ isActive }) =>
              `flex items-center px-3 py-3 rounded-lg transition-all duration-200 group ${
                isActive
                  ? 'bg-primary-600/20 text-primary-400 border border-primary-500/30'
                  : 'text-dark-300 hover:bg-dark-800 hover:text-dark-100'
              } ${item.admin ? 'border-l-4 border-l-secondary-500' : ''}`
            }
          >
            <item.icon className="w-6 h-6 flex-shrink-0" />
            {!collapsed && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="ml-3 font-medium"
              >
                {item.name}
              </motion.span>
            )}
          </NavLink>
        ))}
      </nav>

      {/* User Profile */}
      <div className="p-4 border-t border-dark-700">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-full flex items-center justify-center">
            <span className="text-white font-semibold text-sm">U</span>
          </div>
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="ml-3"
            >
              <p className="text-sm font-medium text-dark-100">User</p>
              <p className="text-xs text-dark-400">Student</p>
            </motion.div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default Sidebar;
