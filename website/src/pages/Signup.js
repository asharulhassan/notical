import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Link, useNavigate } from 'react-router-dom';
import {
  AcademicCapIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowLeftIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';

const Signup = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    studyLevel: '',
    subjects: [],
    agreeToTerms: false,
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const studyLevels = [
    'High School',
    'College',
    'University',
    'Graduate School',
    'Professional Development',
  ];

  const availableSubjects = [
    'Biology', 'Chemistry', 'Mathematics', 'Physics', 'History',
    'Literature', 'Computer Science', 'Economics', 'Psychology', 'Engineering',
  ];

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (type === 'checkbox') {
      setFormData(prev => ({
        ...prev,
        [name]: checked,
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: value,
      }));
    }
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const handleSubjectToggle = (subject) => {
    setFormData(prev => ({
      ...prev,
      subjects: prev.subjects.includes(subject)
        ? prev.subjects.filter(s => s !== subject)
        : [...prev.subjects, subject],
    }));
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }
    
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }
    
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Email is invalid';
    }
    
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Password must contain uppercase, lowercase, and number';
    }
    
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    if (!formData.studyLevel) {
      newErrors.studyLevel = 'Please select your study level';
    }
    
    if (formData.subjects.length === 0) {
      newErrors.subjects = 'Please select at least one subject';
    }
    
    if (!formData.agreeToTerms) {
      newErrors.agreeToTerms = 'You must agree to the terms and conditions';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }
    
    setIsLoading(true);
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // For demo purposes, just navigate to dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error('Signup failed:', error);
      setErrors({ general: 'Signup failed. Please try again.' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0A0A0F] flex items-center justify-center px-6 relative overflow-hidden">
      {/* Animated Background Elements - Raycast Style */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute top-20 left-20 w-96 h-96 bg-[#39FF14]/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-[500px] h-[500px] bg-[#00F0FF]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-[#AFFF00]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
        <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-[#38BDF8]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </div>

      <div className="w-full max-w-2xl relative z-10">
        {/* Back to Landing */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-8"
        >
          <Link
            to="/"
            className="inline-flex items-center text-[#38BDF8] hover:text-[#00F0FF] transition-colors group"
          >
            <ArrowLeftIcon className="w-4 h-4 mr-2 group-hover:-translate-x-1 transition-transform" />
            Back to Home
          </Link>
        </motion.div>

        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-center mb-8"
        >
          <div className="w-20 h-20 bg-gradient-to-br from-[#39FF14] to-[#AFFF00] rounded-3xl flex items-center justify-center mx-auto mb-6 shadow-2xl shadow-[#39FF14]/25">
            <AcademicCapIcon className="w-10 h-10 text-[#0A0A0F]" />
          </div>
          <h1 className="text-4xl font-bold text-white mb-2">Join NOTICAL</h1>
          <p className="text-[#38BDF8] text-lg">Start your AI-powered learning journey today</p>
        </motion.div>

        {/* Signup Form */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-3xl p-8 shadow-2xl shadow-[#39FF14]/10"
        >
          <form onSubmit={handleSubmit} className="space-y-6">
            {errors.general && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="p-4 bg-red-500/10 border border-red-500/30 rounded-xl text-red-400 text-sm flex items-center"
              >
                <SparklesIcon className="w-5 h-5 mr-2" />
                {errors.general}
              </motion.div>
            )}

            {/* Name Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="firstName" className="block text-sm font-medium text-[#38BDF8] mb-2">
                  First Name
                </label>
                <input
                  type="text"
                  id="firstName"
                  name="firstName"
                  value={formData.firstName}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-3 bg-[#1C1E22]/50 border rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                    errors.firstName ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                  }`}
                  placeholder="Enter your first name"
                />
                {errors.firstName && (
                  <motion.p
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-red-400 text-sm mt-2 flex items-center"
                  >
                    <SparklesIcon className="w-4 h-4 mr-1" />
                    {errors.firstName}
                  </motion.p>
                )}
              </div>

              <div>
                <label htmlFor="lastName" className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Last Name
                </label>
                <input
                  type="text"
                  id="lastName"
                  name="lastName"
                  value={formData.lastName}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-3 bg-[#1C1E22]/50 border rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                    errors.lastName ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                  }`}
                  placeholder="Enter your last name"
                />
                {errors.lastName && (
                  <motion.p
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-red-400 text-sm mt-2 flex items-center"
                  >
                    <SparklesIcon className="w-4 h-4 mr-1" />
                    {errors.lastName}
                  </motion.p>
                )}
              </div>
            </div>

            {/* Email */}
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-[#38BDF8] mb-2">
                Email Address
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                className={`w-full px-4 py-3 bg-[#1C1E22]/50 border rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                  errors.email ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                }`}
                placeholder="Enter your email"
              />
              {errors.email && (
                <motion.p
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-red-400 text-sm mt-2 flex items-center"
                >
                  <SparklesIcon className="w-4 h-4 mr-1" />
                  {errors.email}
                </motion.p>
              )}
            </div>

            {/* Password Fields */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="password" className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Password
                </label>
                <div className="relative">
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleInputChange}
                    className={`w-full px-4 py-3 pr-12 bg-[#1C1E22]/50 border rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                      errors.password ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                    }`}
                    placeholder="Create a password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-[#38BDF8] hover:text-[#00F0FF] transition-colors p-1"
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="w-5 h-5" />
                    ) : (
                      <EyeIcon className="w-5 h-5" />
                    )}
                  </button>
                </div>
                {errors.password && (
                  <motion.p
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-red-400 text-sm mt-2 flex items-center"
                  >
                    <SparklesIcon className="w-4 h-4 mr-1" />
                    {errors.password}
                  </motion.p>
                )}
              </div>

              <div>
                <label htmlFor="confirmPassword" className="block text-sm font-medium text-[#38BDF8] mb-2">
                  Confirm Password
                </label>
                <div className="relative">
                  <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    className={`w-full px-4 py-3 pr-12 bg-[#1C1E22]/50 border rounded-xl text-white placeholder-[#38BDF8]/60 focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                      errors.confirmPassword ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                    }`}
                    placeholder="Confirm your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    className="absolute right-3 top-1/2 transform -translate-y-1/2 text-[#38BDF8] hover:text-[#00F0FF] transition-colors p-1"
                  >
                    {showConfirmPassword ? (
                      <EyeSlashIcon className="w-5 h-5" />
                    ) : (
                      <EyeIcon className="w-5 h-5" />
                    )}
                  </button>
                </div>
                {errors.confirmPassword && (
                  <motion.p
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="text-red-400 text-sm mt-2 flex items-center"
                  >
                    <SparklesIcon className="w-4 h-4 mr-1" />
                    {errors.confirmPassword}
                  </motion.p>
                )}
              </div>
            </div>

            {/* Study Level */}
            <div>
              <label htmlFor="studyLevel" className="block text-sm font-medium text-[#38BDF8] mb-2">
                Study Level
              </label>
              <select
                id="studyLevel"
                name="studyLevel"
                value={formData.studyLevel}
                onChange={handleInputChange}
                className={`w-full px-4 py-3 bg-[#1C1E22]/50 border rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-[#39FF14]/50 focus:border-transparent transition-all duration-200 ${
                  errors.studyLevel ? 'border-red-500 focus:ring-red-500/50' : 'border-[#39FF14]/20'
                }`}
              >
                <option value="">Select your study level</option>
                {studyLevels.map(level => (
                  <option key={level} value={level}>{level}</option>
                ))}
              </select>
              {errors.studyLevel && (
                <motion.p
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-red-400 text-sm mt-2 flex items-center"
                >
                  <SparklesIcon className="w-4 h-4 mr-1" />
                  {errors.studyLevel}
                </motion.p>
              )}
            </div>

            {/* Subjects */}
            <div>
              <label className="block text-sm font-medium text-[#38BDF8] mb-2">
                Subjects of Interest
              </label>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {availableSubjects.map(subject => (
                  <label key={subject} className="flex items-center space-x-2 cursor-pointer group">
                    <input
                      type="checkbox"
                      checked={formData.subjects.includes(subject)}
                      onChange={() => handleSubjectToggle(subject)}
                      className="rounded border-[#39FF14]/20 text-[#39FF14] focus:ring-[#39FF14]/50 bg-[#1C1E22]/50"
                    />
                    <span className="text-sm text-[#38BDF8] group-hover:text-white transition-colors">{subject}</span>
                  </label>
                ))}
              </div>
              {errors.subjects && (
                <motion.p
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="text-red-400 text-sm mt-2 flex items-center"
                >
                  <SparklesIcon className="w-4 h-4 mr-1" />
                  {errors.subjects}
                </motion.p>
              )}
            </div>

            {/* Terms */}
            <div className="flex items-start space-x-3">
              <input
                type="checkbox"
                id="agreeToTerms"
                name="agreeToTerms"
                checked={formData.agreeToTerms}
                onChange={handleInputChange}
                className="mt-1 rounded border-[#39FF14]/20 text-[#39FF14] focus:ring-[#39FF14]/50 bg-[#1C1E22]/50"
              />
              <label htmlFor="agreeToTerms" className="text-sm text-[#38BDF8]">
                I agree to the{' '}
                <Link to="/terms" className="text-[#39FF14] hover:text-[#AFFF00] transition-colors">
                  Terms of Service
                </Link>{' '}
                and{' '}
                <Link to="/privacy" className="text-[#39FF14] hover:text-[#AFFF00] transition-colors">
                  Privacy Policy
                </Link>
              </label>
            </div>
            {errors.agreeToTerms && (
              <motion.p
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="text-red-400 text-sm -mt-2 flex items-center"
              >
                <SparklesIcon className="w-4 h-4 mr-1" />
                {errors.agreeToTerms}
              </motion.p>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] py-3 px-6 rounded-xl font-semibold hover:shadow-lg hover:shadow-[#39FF14]/25 transition-all duration-300 transform hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              {isLoading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-[#0A0A0F] mr-2"></div>
                  Creating account...
                </div>
              ) : (
                'Create Account'
              )}
            </button>
          </form>

          <div className="mt-8 text-center">
            <p className="text-[#38BDF8]">
              Already have an account?{' '}
              <Link
                to="/login"
                className="text-[#39FF14] hover:text-[#AFFF00] font-medium transition-colors hover:underline"
              >
                Sign in
              </Link>
            </p>
          </div>
        </motion.div>

        {/* Social Login */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="mt-8"
        >
          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-[#1C1E22]" />
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-[#0A0A0F] text-[#38BDF8]">Or continue with</span>
            </div>
          </div>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <button className="flex items-center justify-center px-4 py-3 bg-[#1C1E22]/50 border border-[#39FF14]/20 rounded-xl text-[#38BDF8] hover:bg-[#1C1E22] hover:text-white transition-all duration-200 hover:scale-105">
              <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
                <path
                  fill="currentColor"
                  d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                />
                <path
                  fill="currentColor"
                  d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                />
                <path
                  fill="currentColor"
                  d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                />
                <path
                  fill="currentColor"
                  d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                />
              </svg>
              Google
            </button>
            <button className="flex items-center justify-center px-4 py-3 bg-[#1C1E22]/50 border border-[#39FF14]/20 rounded-xl text-[#38BDF8] hover:bg-[#1C1E22] hover:text-white transition-all duration-200 hover:scale-105">
              <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z"/>
              </svg>
              Twitter
            </button>
          </div>
        </motion.div>

        {/* Demo Credentials */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
          className="mt-8 p-4 bg-[#39FF14]/10 border border-[#39FF14]/30 rounded-xl"
        >
          <p className="text-[#39FF14] text-sm text-center">
            <strong>Demo:</strong> Use any information to explore the platform
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default Signup;
