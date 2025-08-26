import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import Sidebar from './components/layout/Sidebar';
import Navbar from './components/layout/Navbar';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import Flashcards from './pages/Flashcards';
import Notes from './pages/Notes';
import Tests from './pages/Tests';
import Community from './pages/Community';
import Tutor from './pages/Tutor';
import Planner from './pages/Planner';
import Settings from './pages/Settings';
import Admin from './pages/Admin';
import { useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();
  const isAuthPage = ['/', '/login', '/signup'].includes(location.pathname);
  const isAdminPage = location.pathname === '/admin';

  if (isAuthPage) {
    return (
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    );
  }

  return (
    <div className="flex h-screen bg-dark-950">
      {!isAdminPage && <Sidebar />}
      <div className="flex-1 flex flex-col overflow-hidden">
        {!isAdminPage && <Navbar />}
        <main className="flex-1 overflow-y-auto bg-dark-950">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.3 }}
              className={isAdminPage ? '' : 'p-6'}
            >
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/flashcards" element={<Flashcards />} />
                <Route path="/notes" element={<Notes />} />
                <Route path="/tests" element={<Tests />} />
                <Route path="/community" element={<Community />} />
                <Route path="/tutor" element={<Tutor />} />
                <Route path="/planner" element={<Planner />} />
                <Route path="/settings" element={<Settings />} />
                <Route path="/admin" element={<Admin />} />
              </Routes>
            </motion.div>
          </AnimatePresence>
        </main>
      </div>
    </div>
  );
}

export default App;
