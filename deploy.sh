#!/bin/bash

echo "🚀 Nusify Deployment Script"
echo "=========================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Running git init..."
    git init
fi

# Check if remote origin exists
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote origin found."
    echo "Please add your GitHub repository as origin:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/nusify.git"
    echo ""
    read -p "Enter your GitHub repository URL: " repo_url
    if [ ! -z "$repo_url" ]; then
        git remote add origin "$repo_url"
        echo "✅ Remote origin added: $repo_url"
    else
        echo "❌ No URL provided. Exiting."
        exit 1
    fi
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
if npm run build; then
    echo "✅ Frontend built successfully"
else
    echo "❌ Frontend build failed"
    exit 1
fi
cd ..

# Add all changes
echo "📝 Staging changes..."
git add .

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "ℹ️  No changes to commit"
else
    # Commit changes
    echo "💾 Committing changes..."
    git commit -m "Deploy: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push to GitHub
    echo "🚀 Pushing to GitHub..."
    if git push origin main; then
        echo "✅ Successfully pushed to GitHub!"
        echo ""
        echo "🌐 Next steps:"
        echo "1. Go to your hosting platform (Render, Heroku, Vercel, etc.)"
        echo "2. Connect your GitHub repository"
        echo "3. Deploy your application"
        echo ""
        echo "📖 See DEPLOYMENT.md for detailed deployment instructions"
    else
        echo "❌ Failed to push to GitHub"
        exit 1
    fi
fi

echo ""
echo "🎉 Deployment script completed!"
