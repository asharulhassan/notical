# 🌐 NOTICAL Website

A premium, liquid glass design website for NOTICAL flashcard platform, featuring Raycast.com and Railway.app inspired aesthetics.

## ✨ Features

- **Premium Liquid Glass Design**: Modern, sophisticated UI with glass morphism effects
- **Responsive Layout**: Optimized for all devices and screen sizes
- **Interactive Components**: Smooth animations and transitions
- **Brand Color Palette**: Rich Black, Charcoal Gray, Neon Green, Lime Accent, Electric Cyan, Sky Blue
- **GoodNotes-Style Flashcard System**: Nested folders, study modes, deck management

## 🎨 Design System

### Color Palette
```css
/* Primary Colors */
--rich-black: #0A0A0F      /* Background */
--charcoal: #1C1E22       /* Cards & Components */
--neon-green: #39FF14     /* Accents & Highlights */
--lime-accent: #32CD32    /* Secondary Accents */
--electric-cyan: #00F0FF  /* Interactive Elements */
--sky-blue: #38BDF8       /* Text & Links */
```

### Component Classes
- `.premium-card` - Glass morphism cards with backdrop blur
- `.liquid-glass` - Transparent glass effects
- `.neon-glow` - Neon green glow effects
- `.cyan-glow` - Electric cyan glow effects
- `.premium-button` - Enhanced button styles

### Animations
- `animate-float` - Floating animation for background elements
- `animate-pulse-slow` - Slow pulsing effects
- Custom keyframes for dynamic interactions

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd website
npm install
```

### 2. Start Development Server
```bash
npm start
```

The website will be available at `http://localhost:3000`

### 3. Build for Production
```bash
npm run build
```

## 🏗️ Project Structure

```
website/
├── src/                    # React source code
│   ├── components/         # Reusable components
│   │   ├── layout/        # Layout components
│   │   │   ├── Navbar.js  # Navigation bar
│   │   │   └── Sidebar.js # Sidebar navigation
│   │   └── ui/            # UI components
│   │       ├── Button.js  # Button components
│   │       └── Card.js    # Card components
│   ├── pages/             # Page components
│   │   ├── Landing.js     # Landing page
│   │   ├── Login.js       # Login page
│   │   ├── Signup.js      # Signup page
│   │   ├── Flashcards.js  # Flashcard system
│   │   └── Tests.js       # Test page
│   ├── services/          # API services
│   │   └── api.js         # API integration
│   ├── store/             # State management
│   │   └── useStore.js    # Custom hooks
│   ├── App.js             # Main app component
│   ├── index.js           # Entry point
│   └── index.css          # Global styles
├── public/                 # Public assets
├── package.json            # Dependencies
├── tailwind.config.js      # Tailwind configuration
└── postcss.config.js       # PostCSS configuration
```

## 🎯 Pages

### Landing Page (`/`)
- Hero section with animated background
- Feature showcase with liquid glass cards
- How it works section (Railway.app inspired)
- Testimonials and pricing
- Premium design elements

### Authentication
- **Login Page** (`/login`): Liquid glass form design
- **Signup Page** (`/signup`): Enhanced registration form
- Social login options
- Demo credentials

### Flashcard System (`/flashcards`)
- GoodNotes-style folder structure
- Nested folder organization
- AI-powered flashcard generation
- Study mode with deck combination
- Multiple card types and difficulty levels

### Tests Page (`/tests`)
- Premium design implementation
- Brand color integration
- Interactive components

## 🧠 AI Integration

### Flashcard Generation
- **Generation Modes**:
  - Text Understanding: Deep content analysis
  - Strict Text: Word-for-word accuracy
  - Online Research: External knowledge integration

- **Answer Styles**:
  - Professional: Academic tone
  - Simple: Clear explanations
  - Exam-Focused: Test preparation

- **Advanced Options**:
  - Exam board selection
  - Learning level adjustment
  - Difficulty balancing
  - Subject detection

### API Endpoints
- `POST /generate` - Generate flashcards
- `POST /analyze` - Content analysis
- `GET /ai/status` - AI pipeline status

## 🎨 Design Principles

### Liquid Glass Aesthetics
- **Transparency**: Subtle transparency effects
- **Backdrop Blur**: Modern glass morphism
- **Neon Accents**: Vibrant color highlights
- **Smooth Animations**: Fluid interactions

### User Experience
- **Intuitive Navigation**: Clear information hierarchy
- **Responsive Design**: Mobile-first approach
- **Accessibility**: WCAG compliant components
- **Performance**: Optimized loading and interactions

## 🔧 Configuration

### Tailwind CSS
```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        'rich-black': '#0A0A0F',
        'charcoal': '#1C1E22',
        'neon-green': '#39FF14',
        'lime-accent': '#32CD32',
        'electric-cyan': '#00F0FF',
        'sky-blue': '#38BDF8'
      },
      animation: {
        'float': 'float 6s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
      }
    }
  }
}
```

### Environment Variables
```bash
# API Configuration
REACT_APP_API_URL=http://localhost:8001
REACT_APP_WEBSITE_URL=http://localhost:3000

# Feature Flags
REACT_APP_ENABLE_AI=true
REACT_APP_ENABLE_TRAINING=false
```

## 📱 Responsive Design

### Breakpoints
- **Mobile**: 320px - 768px
- **Tablet**: 768px - 1024px
- **Desktop**: 1024px+
- **Large Desktop**: 1440px+

### Mobile-First Approach
- Touch-friendly interactions
- Optimized navigation
- Responsive typography
- Adaptive layouts

## 🚀 Performance

### Optimization
- **Code Splitting**: Lazy loading of components
- **Image Optimization**: WebP format support
- **Bundle Analysis**: Webpack bundle analyzer
- **Lighthouse Score**: 90+ performance rating

### Loading States
- Skeleton screens
- Progressive loading
- Smooth transitions
- Error boundaries

## 🧪 Testing

### Test Commands
```bash
# Run tests
npm test

# Run tests with coverage
npm test -- --coverage

# Run tests in watch mode
npm test -- --watch

# Run specific test file
npm test -- Flashcards.test.js
```

### Testing Strategy
- Unit tests for components
- Integration tests for pages
- E2E tests for user flows
- Accessibility testing

## 🔒 Security

### Authentication
- JWT token management
- Secure password handling
- Session management
- CSRF protection

### Data Protection
- Input validation
- XSS prevention
- Secure API communication
- Privacy compliance

## 📈 Analytics

### User Tracking
- Page views and navigation
- User interactions
- Performance metrics
- Error monitoring

### A/B Testing
- Feature flag system
- User experience testing
- Conversion optimization
- Data-driven decisions

## 🌍 Internationalization

### Multi-language Support
- English (default)
- Language detection
- RTL support
- Cultural adaptations

### Localization
- Date formatting
- Number formatting
- Currency display
- Time zones

## 🚀 Deployment

### Build Process
```bash
# Development
npm start

# Production build
npm run build

# Preview build
npm run preview

# Analyze bundle
npm run analyze
```

### Deployment Options
- **Vercel**: Zero-config deployment
- **Netlify**: Static site hosting
- **AWS S3**: Cloud hosting
- **Docker**: Containerized deployment

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Install dependencies
4. Make your changes
5. Run tests and linting
6. Submit a pull request

### Code Standards
- ESLint configuration
- Prettier formatting
- TypeScript support
- Component documentation

## 📚 Resources

### Design Inspiration
- [Raycast.com](https://raycast.com) - Premium design aesthetics
- [Railway.app](https://railway.app) - Product flow design
- [Glassmorphism](https://glassmorphism.com) - Glass design principles

### Documentation
- [React Documentation](https://reactjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Framer Motion](https://www.framer.com/motion)

## 🆘 Support

### Common Issues
- **Build Errors**: Check Node.js version and dependencies
- **Styling Issues**: Verify Tailwind CSS configuration
- **API Errors**: Check backend server status
- **Performance Issues**: Run bundle analysis

### Getting Help
- Check documentation
- Review error logs
- Test in different browsers
- Create detailed issue reports

---

**NOTICAL Website** - Premium design meets intelligent functionality. 🌐✨
