import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useStore = create(
  persist(
    (set, get) => ({
      // User state
      user: null,
      isAuthenticated: false,
      
      // Study data
      flashcards: [],
      notes: [],
      tests: [],
      studySessions: [],
      
      // UI state
      sidebarCollapsed: false,
      currentTheme: 'dark',
      
      // Study progress
      studyStreak: 0,
      totalStudyTime: 0,
      subjects: [],
      
      // Actions
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      
      addFlashcard: (flashcard) => set((state) => ({
        flashcards: [...state.flashcards, flashcard]
      })),
      
      addNote: (note) => set((state) => ({
        notes: [...state.notes, note]
      })),
      
      addTest: (test) => set((state) => ({
        tests: [...state.tests, test]
      })),
      
      updateStudyStreak: (streak) => set({ studyStreak: streak }),
      
      addStudyTime: (minutes) => set((state) => ({
        totalStudyTime: state.totalStudyTime + minutes
      })),
      
      toggleSidebar: () => set((state) => ({
        sidebarCollapsed: !state.sidebarCollapsed
      })),
      
      setTheme: (theme) => set({ currentTheme: theme }),
      
      // Computed values
      getFlashcardsBySubject: (subject) => {
        const state = get();
        return state.flashcards.filter(f => f.subject === subject);
      },
      
      getNotesBySubject: (subject) => {
        const state = get();
        return state.notes.filter(n => n.subject === subject);
      },
      
      getTotalCards: () => {
        const state = get();
        return state.flashcards.length;
      },
      
      getTotalNotes: () => {
        const state = get();
        return state.notes.length;
      },
      
      getStudyProgress: () => {
        const state = get();
        const totalSessions = state.studySessions.length;
        const completedSessions = state.studySessions.filter(s => s.completed).length;
        return totalSessions > 0 ? (completedSessions / totalSessions) * 100 : 0;
      },
    }),
    {
      name: 'notical-storage',
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
        flashcards: state.flashcards,
        notes: state.notes,
        tests: state.tests,
        studySessions: state.studySessions,
        studyStreak: state.studyStreak,
        totalStudyTime: state.totalStudyTime,
        subjects: state.subjects,
        currentTheme: state.currentTheme,
      }),
    }
  )
);

export default useStore;
