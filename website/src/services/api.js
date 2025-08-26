const API_BASE_URL = 'http://localhost:8005'; // Your NOTICAL AI server

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    };

    try {
      const response = await fetch(url, { ...defaultOptions, ...options });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // NOTICAL AI Flashcard Generation
  async generateFlashcards(content, numCards = 5) {
    console.log('🚀 Generating flashcards with NOTICAL AI...');
    const response = await this.request('/generate-flashcards', {
      method: 'POST',
      body: JSON.stringify({
        content,
        num_cards: numCards
      }),
    });
    console.log('✅ NOTICAL AI response:', response);
    return response;
  }

  // Test endpoint
  async testAPI() {
    return this.request('/test');
  }

  // Legacy endpoints (for backward compatibility)
  async uploadPDF(file) {
    console.warn('uploadPDF is deprecated. Use generateFlashcards with content instead.');
    // For now, read the file and extract text
    const text = await this.extractTextFromFile(file);
    return this.generateFlashcards(text);
  }

  async extractTextFromFile(file) {
    // Simple text extraction for now
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        resolve(e.target.result);
      };
      reader.readAsText(file);
    });
  }

  // Placeholder endpoints for future features
  async analyzeContent(content) {
    console.warn('Content analysis coming soon!');
    return { analysis: 'Coming soon', content };
  }

  async getAIStatus() {
    console.warn('AI status coming soon!');
    return { status: 'Basic API working', ai: 'Coming soon' };
  }
}

export default new ApiService();
