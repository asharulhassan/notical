# 🔄 NOTICAL Development Workflow

> **How to work seamlessly between your Mac and RTX 4070 laptop**

## 🎯 **Your Setup:**
- **Mac**: Development, testing, website work
- **RTX 4070 Laptop**: AI training, model development, heavy computation
- **GitHub**: Central repository for syncing

## 🚀 **Initial Setup (One-time):**

### **1. Create GitHub Repository**
```bash
# On GitHub.com, create a new repo called "notical"
# Copy the repository URL
```

### **2. Push from Mac (Current)**
```bash
git remote add origin https://github.com/YOUR_USERNAME/notical.git
git branch -M main
git push -u origin main
```

### **3. Clone on RTX 4070 Laptop**
```bash
git clone https://github.com/YOUR_USERNAME/notical.git
cd notical
./setup.sh
```

## 🔄 **Daily Workflow:**

### **Starting Work (Any Laptop):**
```bash
# Always pull latest changes first
git pull origin main
```

### **Working on Mac:**
```bash
# 1. Make changes
# 2. Test locally
# 3. Commit and push
git add .
git commit -m "Description of changes"
git push origin main
```

### **Working on RTX 4070 Laptop:**
```bash
# 1. Pull latest changes
git pull origin main

# 2. Work on AI models
cd ai-pipeline
source venv/bin/activate
python training/trainer.py

# 3. Test improvements
# 4. Commit and push
git add .
git commit -m "AI model improvements"
git push origin main
```

## 📁 **What to Work On Where:**

### **Mac (Development & Testing):**
```
✅ Website frontend (React)
✅ API testing and debugging
✅ User interface improvements
✅ Documentation updates
✅ Bug fixes
✅ Testing with users
```

### **RTX 4070 Laptop (AI & Training):**
```
✅ AI model training
✅ Model fine-tuning
✅ Training data collection
✅ Performance optimization
✅ Heavy computation tasks
✅ Model evaluation
```

## 🚨 **Important Rules:**

### **1. Always Pull Before Working**
```bash
git pull origin main
# Never start coding without this!
```

### **2. Commit Frequently**
```bash
# Small, frequent commits are better than big, rare ones
git add .
git commit -m "Brief description"
git push origin main
```

### **3. Use Descriptive Commit Messages**
```bash
# Good:
git commit -m "Fix flashcard generation bug in AI pipeline"

# Bad:
git commit -m "fix stuff"
```

### **4. Test Before Pushing**
```bash
# Always test your changes before pushing
# Don't break the build for others
```

## 🔧 **Troubleshooting:**

### **Merge Conflicts:**
```bash
# If you get merge conflicts:
git status                    # See what's conflicted
# Edit conflicted files manually
git add .                     # Mark as resolved
git commit -m "Resolve merge conflicts"
git push origin main
```

### **Forgot to Pull:**
```bash
# If you forgot to pull and have local changes:
git stash                    # Save your changes
git pull origin main         # Get latest
git stash pop               # Reapply your changes
# Resolve any conflicts, then commit
```

### **Broken Build:**
```bash
# If something breaks:
git log --oneline           # Find the last working commit
git reset --hard HEAD~1     # Go back one commit
git push --force origin main # Force push (be careful!)
```

## 📱 **Quick Commands Reference:**

### **Start Work:**
```bash
git pull origin main
```

### **Save Work:**
```bash
git add .
git commit -m "Description"
git push origin main
```

### **Check Status:**
```bash
git status
git log --oneline -5
```

### **Switch Branches:**
```bash
git checkout -b feature-name    # Create new branch
git checkout main               # Switch to main
git branch -d feature-name      # Delete branch
```

## 🎯 **Best Practices:**

### **1. Work in Small Chunks**
- Make small, focused changes
- Commit after each logical unit
- Test frequently

### **2. Communicate Changes**
- Use clear commit messages
- Update README when needed
- Document major changes

### **3. Keep Dependencies Updated**
- Update requirements.txt when adding packages
- Update package.json when adding npm packages
- Document version changes

### **4. Backup Important Work**
- Push to GitHub frequently
- Don't rely only on local files
- Use branches for experimental features

## 🚀 **Pro Tips:**

### **1. Use Branches for Features**
```bash
git checkout -b new-feature
# Work on feature
git push origin new-feature
# Create pull request on GitHub
```

### **2. Use GitHub Issues**
- Track bugs and features
- Reference issues in commits
- Keep organized

### **3. Regular Sync Schedule**
- Pull every morning
- Push every evening
- Don't let changes accumulate

## 🎉 **You're All Set!**

Now you can work seamlessly between both laptops:

1. **Mac**: Website development, testing, user interface
2. **RTX 4070**: AI training, model development, heavy computation
3. **GitHub**: Central sync point for both

**Happy coding! 🚀**

---

*Remember: Pull → Work → Test → Commit → Push → Repeat!*
