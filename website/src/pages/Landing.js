import React, { useRef } from 'react';
import { motion, useScroll, useTransform, useInView } from 'framer-motion';
import { Link } from 'react-router-dom';
import {
  AcademicCapIcon,
  SparklesIcon,
  UserGroupIcon,
  ChartBarIcon,
  ArrowRightIcon,
  PlayIcon,
  StarIcon,
  RocketLaunchIcon,
  LightBulbIcon,
  ClockIcon,
  GlobeAltIcon,
  CpuChipIcon,
  BookOpenIcon,
} from '@heroicons/react/24/outline';

const Landing = () => {
  const { scrollYProgress } = useScroll();
  const y = useTransform(scrollYProgress, [0, 1], [0, -50]);
  
  const heroRef = useRef(null);
  const isHeroInView = useInView(heroRef, { once: true });

  const stats = [
    { number: '50K+', label: 'Active Students', color: '#39FF14' },
    { number: '1M+', label: 'Flashcards Created', color: '#AFFF00' },
    { number: '95%', label: 'Success Rate', color: '#00F0FF' },
    { number: '24/7', label: 'AI Support', color: '#38BDF8' },
  ];

  const features = [
    {
      icon: LightBulbIcon,
      title: 'AI-Powered Learning',
      description: 'Our advanced AI analyzes your study materials and automatically generates personalized flashcards, notes, and practice tests.',
      color: '#39FF14',
      gradient: 'from-[#39FF14] to-[#AFFF00]',
    },
    {
      icon: ClockIcon,
      title: 'Smart Study Planning',
      description: 'AI-driven study schedules that adapt to your learning pace, using spaced repetition to maximize retention.',
      color: '#00F0FF',
      gradient: 'from-[#00F0FF] to-[#38BDF8]',
    },
    {
      icon: UserGroupIcon,
      title: 'Community Learning',
      description: 'Connect with peers, join study groups, and learn from verified tutors in our thriving educational community.',
      color: '#AFFF00',
      gradient: 'from-[#AFFF00] to-[#39FF14]',
    },
    {
      icon: ChartBarIcon,
      title: 'Progress Analytics',
      description: 'Track your learning journey with detailed insights, identify weak areas, and celebrate your achievements.',
      color: '#38BDF8',
      gradient: 'from-[#38BDF8] to-[#00F0FF]',
    },
  ];

  const productFlow = [
    {
      step: '01',
      title: 'Upload Your Notes',
      description: 'Simply drag and drop your study materials - PDFs, images, or text files.',
      icon: BookOpenIcon,
      color: '#39FF14',
    },
    {
      step: '02',
      title: 'AI Analysis',
      description: 'Our AI processes your content, identifies key concepts, and creates structured learning materials.',
      icon: CpuChipIcon,
      color: '#00F0FF',
    },
    {
      step: '03',
      title: 'Generate Content',
      description: 'Get personalized flashcards, notes, and practice tests tailored to your learning style.',
      icon: SparklesIcon,
      color: '#AFFF00',
    },
    {
      step: '04',
      title: 'Study & Track',
      description: 'Study with spaced repetition and track your progress with detailed analytics.',
      icon: ChartBarIcon,
      color: '#38BDF8',
    },
  ];

  const testimonials = [
    {
      name: 'Sarah Chen',
      role: 'Medical Student',
      content: 'NOTICAL helped me ace my anatomy exam! The AI-generated flashcards were incredibly accurate and saved me hours of study time.',
      avatar: 'SC',
      rating: 5,
    },
    {
      name: 'Marcus Rodriguez',
      role: 'Engineering Student',
      content: 'The study planner is genius. It automatically adjusted my schedule based on my performance and helped me stay on track.',
      avatar: 'MR',
      rating: 5,
    },
    {
      name: 'Aisha Patel',
      role: 'Law Student',
      content: 'I love how the AI tutor explains complex legal concepts in simple terms. It\'s like having a personal tutor available 24/7.',
      avatar: 'AP',
      rating: 5,
    },
  ];

  const pricingPlans = [
    {
      name: 'Free',
      price: '$0',
      period: '/month',
      description: 'Perfect for getting started',
      features: [
        '5 AI-generated flashcard decks',
        'Basic note templates',
        'Community access',
        'Mobile app access',
      ],
      buttonText: 'Get Started Free',
      popular: false,
      color: '#1C1E22',
    },
    {
      name: 'Pro',
      price: '$9.99',
      period: '/month',
      description: 'For serious students',
      features: [
        'Unlimited AI generation',
        'Advanced study analytics',
        'Priority AI tutor access',
        'Export to multiple formats',
        'Custom study schedules',
      ],
      buttonText: 'Start Pro Trial',
      popular: true,
      color: '#39FF14',
    },
    {
      name: 'Team',
      price: '$29.99',
      period: '/month',
      description: 'For study groups & classes',
      features: [
        'Everything in Pro',
        'Group study sessions',
        'Teacher dashboard',
        'Progress sharing',
        'White-label options',
      ],
      buttonText: 'Contact Sales',
      popular: false,
      color: '#00F0FF',
    },
  ];

  return (
    <div className="min-h-screen bg-[#0A0A0F] overflow-hidden">
      {/* Animated Background Elements */}
      <motion.div
        style={{ y }}
        className="fixed inset-0 opacity-20 pointer-events-none"
      >
        <div className="absolute top-20 left-20 w-96 h-96 bg-[#39FF14]/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute top-40 right-20 w-[500px] h-[500px] bg-[#00F0FF]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}}></div>
        <div className="absolute bottom-20 left-1/2 w-80 h-80 bg-[#AFFF00]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '4s'}}></div>
        <div className="absolute top-1/2 left-1/4 w-64 h-64 bg-[#38BDF8]/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '1s'}}></div>
      </motion.div>

      {/* Navigation */}
      <nav className="relative z-50 px-6 py-6">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center space-x-3"
          >
            <div className="w-12 h-12 bg-gradient-to-br from-[#39FF14] to-[#AFFF00] rounded-2xl flex items-center justify-center shadow-lg shadow-[#39FF14]/25">
              <AcademicCapIcon className="w-7 h-7 text-[#0A0A0F]" />
            </div>
            <span className="text-3xl font-bold bg-gradient-to-r from-[#39FF14] to-[#AFFF00] bg-clip-text text-transparent">
              NOTICAL
            </span>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="hidden md:flex items-center space-x-8"
          >
            <button className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors">Features</button>
            <button className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors">How it Works</button>
            <button className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors">Pricing</button>
            <Link to="/login" className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors">
              Sign In
            </Link>
            <Link to="/signup" className="bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] px-6 py-3 rounded-xl font-medium hover:shadow-lg hover:shadow-[#39FF14]/25 transition-all duration-300">
              Get Started
            </Link>
          </motion.div>
        </div>
      </nav>

      {/* Hero Section */}
      <section ref={heroRef} className="relative px-6 py-20 lg:py-32">
        <div className="max-w-7xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.2 }}
            className="mb-8"
          >
            <div className="inline-flex items-center space-x-2 bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-full px-4 py-2 mb-6">
              <SparklesIcon className="w-5 h-5 text-[#39FF14]" />
              <span className="text-[#38BDF8] text-sm font-medium">AI-Powered Learning Platform</span>
            </div>
          </motion.div>

          <motion.h1
            initial={{ opacity: 0, y: 30 }}
            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.4 }}
            className="text-5xl md:text-7xl lg:text-8xl font-bold text-white mb-8 leading-tight"
          >
            Study Smarter,
            <span className="block bg-gradient-to-r from-[#39FF14] via-[#AFFF00] to-[#00F0FF] bg-clip-text text-transparent">
              Not Harder
            </span>
          </motion.h1>
          
          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.6 }}
            className="text-xl lg:text-2xl text-[#38BDF8] mb-12 max-w-4xl mx-auto leading-relaxed"
          >
            NOTICAL combines cutting-edge AI with proven learning science to create personalized study experiences. 
            Generate flashcards, create notes, and track your progress—all powered by intelligent algorithms.
          </motion.p>
          
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 0.8 }}
            className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-6 mb-16"
          >
            <Link to="/signup" className="group bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] text-lg px-8 py-4 rounded-xl font-semibold hover:shadow-2xl hover:shadow-[#39FF14]/25 transition-all duration-300 transform hover:scale-105">
              Start Learning Free
              <ArrowRightIcon className="w-5 h-5 ml-2 inline group-hover:translate-x-1 transition-transform" />
            </Link>
            <button 
              className="flex items-center space-x-3 bg-[#1C1E22]/80 backdrop-blur-md border border-[#00F0FF]/20 text-[#00F0FF] px-8 py-4 rounded-xl font-semibold hover:bg-[#1C1E22] hover:border-[#00F0FF]/40 transition-all duration-300"
            >
              <PlayIcon className="w-5 h-5" />
              <span>Watch Demo</span>
            </button>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
            transition={{ delay: 1.0 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
          >
            {stats.map((stat, index) => (
              <motion.div 
                key={stat.label} 
                className="text-center"
                initial={{ opacity: 0, scale: 0.8 }}
                animate={isHeroInView ? { opacity: 1, scale: 1 } : {}}
                transition={{ delay: 1.2 + index * 0.1 }}
              >
                <div className="text-3xl md:text-4xl font-bold mb-2" style={{color: stat.color}}>{stat.number}</div>
                <div className="text-[#38BDF8] text-sm">{stat.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* How It Works Section - Railway.app inspired */}
      <section id="how-it-works" className="px-6 py-20 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              How NOTICAL Works
            </h2>
            <p className="text-xl text-[#38BDF8] max-w-3xl mx-auto">
              Our AI-powered pipeline transforms your study materials into personalized learning experiences
            </p>
          </motion.div>
          
          <div className="relative">
            {/* Connection Line */}
            <div className="absolute top-1/2 left-0 right-0 h-0.5 bg-gradient-to-r from-[#39FF14] via-[#AFFF00] to-[#00F0FF] opacity-30 hidden md:block"></div>
            
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative z-10">
              {productFlow.map((step, index) => (
                <motion.div
                  key={step.step}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: index * 0.2 }}
                  viewport={{ once: true }}
                  className="text-center group"
                >
                  <div className="relative mb-6">
                    <div className="w-20 h-20 mx-auto bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-2xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
                      <step.icon className="w-10 h-10" style={{color: step.color}} />
                    </div>
                    <div className="absolute -top-2 -right-2 w-8 h-8 bg-gradient-to-r from-[#39FF14] to-[#AFFF00] rounded-full flex items-center justify-center text-[#0A0A0F] font-bold text-sm">
                      {step.step}
                    </div>
                  </div>
                  <h3 className="text-xl font-bold text-white mb-3">{step.title}</h3>
                  <p className="text-[#38BDF8] leading-relaxed">{step.description}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="px-6 py-20 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-8">
              Everything You Need to Succeed
            </h2>
            <p className="text-xl text-[#38BDF8] max-w-3xl mx-auto">
              Our comprehensive platform covers every aspect of your learning journey, 
              from content creation to progress tracking.
            </p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={feature.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group relative"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-[#1C1E22] to-[#0A0A0F] rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                <div className="relative p-8 rounded-3xl border border-[#39FF14]/20 bg-[#1C1E22]/80 backdrop-blur-md hover:border-[#39FF14]/40 transition-all duration-300 group-hover:scale-105">
                  <div className={`w-16 h-16 bg-gradient-to-r ${feature.gradient} rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className="w-8 h-8 text-[#0A0A0F]" />
                  </div>
                  <h3 className="text-2xl font-bold text-white mb-4">{feature.title}</h3>
                  <p className="text-[#38BDF8] leading-relaxed">{feature.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="px-6 py-20 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Loved by Students Worldwide
            </h2>
            <p className="text-xl text-[#38BDF8] max-w-2xl mx-auto">
              Join thousands of students who have transformed their learning with NOTICAL
            </p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={testimonial.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-3xl p-8 hover:border-[#39FF14]/40 transition-all duration-300"
              >
                <div className="flex items-center space-x-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <StarIcon key={i} className="w-5 h-5 text-[#AFFF00] fill-current" />
                  ))}
                </div>
                <p className="text-[#38BDF8] mb-6 leading-relaxed">"{testimonial.content}"</p>
                <div className="flex items-center space-x-4">
                  <div className="w-12 h-12 bg-gradient-to-r from-[#39FF14] to-[#AFFF00] rounded-full flex items-center justify-center text-[#0A0A0F] font-semibold">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="font-semibold text-white">{testimonial.name}</div>
                    <div className="text-[#38BDF8] text-sm">{testimonial.role}</div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="px-6 py-20 relative">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
              Choose Your Plan
            </h2>
            <p className="text-xl text-[#38BDF8] max-w-2xl mx-auto">
              Start free and upgrade as you grow. No hidden fees, cancel anytime.
            </p>
          </motion.div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
            {pricingPlans.map((plan, index) => (
              <motion.div
                key={plan.name}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: index * 0.1 }}
                viewport={{ once: true }}
                className={`relative ${plan.popular ? 'scale-105' : ''}`}
              >
                {plan.popular && (
                  <div className="absolute -top-4 left-1/2 transform -translate-x-1/2 bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] px-4 py-2 rounded-full text-sm font-medium">
                    Most Popular
                  </div>
                )}
                <div className="bg-[#1C1E22]/80 backdrop-blur-md border border-[#39FF14]/20 rounded-3xl p-8 h-full hover:border-[#39FF14]/40 transition-all duration-300">
                  <div className="text-center mb-8">
                    <h3 className="text-2xl font-bold text-white mb-2">{plan.name}</h3>
                    <div className="flex items-baseline justify-center space-x-1">
                      <span className="text-4xl font-bold text-white">{plan.price}</span>
                      <span className="text-[#38BDF8]">{plan.period}</span>
                    </div>
                    <p className="text-[#38BDF8] mt-2">{plan.description}</p>
                  </div>
                  
                  <ul className="space-y-4 mb-8">
                    {plan.features.map((feature, i) => (
                      <li key={i} className="flex items-center space-x-3">
                        <div className="w-5 h-5 bg-[#39FF14] rounded-full flex items-center justify-center">
                          <svg className="w-3 h-3 text-[#0A0A0F]" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                          </svg>
                        </div>
                        <span className="text-[#38BDF8]">{feature}</span>
                      </li>
                    ))}
                  </ul>
                  
                  <button className={`w-full py-4 rounded-xl font-semibold transition-all duration-300 ${
                    plan.popular
                      ? 'bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] hover:shadow-lg hover:shadow-[#39FF14]/25'
                      : 'bg-[#1C1E22] text-white hover:bg-[#0A0A0F] border border-[#39FF14]/20 hover:border-[#39FF14]/40'
                  }`}>
                    {plan.buttonText}
                  </button>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="px-6 py-20 relative">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            viewport={{ once: true }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-r from-[#39FF14]/10 to-[#00F0FF]/10 rounded-3xl"></div>
            <div className="relative p-12 border border-[#39FF14]/30 rounded-3xl bg-[#1C1E22]/80 backdrop-blur-md">
              <RocketLaunchIcon className="w-16 h-16 text-[#39FF14] mx-auto mb-6" />
              <h2 className="text-4xl md:text-6xl font-bold text-white mb-6">
                Ready to Transform Your Learning?
              </h2>
              <p className="text-xl text-[#38BDF8] mb-8 max-w-2xl mx-auto">
                Join thousands of students already using NOTICAL to ace their exams and master new subjects.
              </p>
              <Link to="/signup" className="inline-flex items-center bg-gradient-to-r from-[#39FF14] to-[#AFFF00] text-[#0A0A0F] text-lg px-8 py-4 rounded-xl font-semibold hover:shadow-2xl hover:shadow-[#39FF14]/25 transition-all duration-300 transform hover:scale-105">
                Get Started Now
                <ArrowRightIcon className="w-5 h-5 ml-2" />
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="px-6 py-16 border-t border-[#1C1E22] relative">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-10 h-10 bg-gradient-to-br from-[#39FF14] to-[#AFFF00] rounded-xl flex items-center justify-center">
                  <AcademicCapIcon className="w-6 h-6 text-[#0A0A0F]" />
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-[#39FF14] to-[#AFFF00] bg-clip-text text-transparent">
                  NOTICAL
                </span>
              </div>
              <p className="text-[#38BDF8] mb-4">
                Empowering students worldwide with AI-powered learning tools.
              </p>
              <div className="flex space-x-4">
                <button className="text-[#38BDF8] hover:text-[#00F0FF] transition-colors">
                  <GlobeAltIcon className="w-5 h-5" />
                </button>
              </div>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-[#38BDF8]">
                <li><button className="hover:text-[#00F0FF] transition-colors">Features</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Pricing</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">API</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Integrations</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-4xl font-bold text-white mb-4">Company</h4>
              <ul className="space-y-2 text-[#38BDF8]">
                <li><button className="hover:text-[#00F0FF] transition-colors">About</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Blog</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Careers</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Contact</button></li>
              </ul>
            </div>
            
            <div>
              <h4 className="text-white font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-[#38BDF8]">
                <li><button className="hover:text-[#00F0FF] transition-colors">Help Center</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Community</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Status</button></li>
                <li><button className="hover:text-[#00F0FF] transition-colors">Security</button></li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-[#1C1E22] pt-8 flex flex-col md:flex-row items-center justify-between">
            <p className="text-[#38BDF8] text-sm mb-4 md:mb-0">
              © 2024 NOTICAL. All rights reserved.
            </p>
            <div className="flex space-x-6 text-sm text-[#38BDF8]">
              <button className="hover:text-[#00F0FF] transition-colors">Privacy Policy</button>
              <button className="hover:text-[#00F0FF] transition-colors">Terms of Service</button>
              <button className="hover:text-[#00F0FF] transition-colors">Cookie Policy</button>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
