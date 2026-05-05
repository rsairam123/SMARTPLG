#!/bin/bash

# SmartPLG Accelerator - Railway Deployment Script
# This script helps you deploy the backend to Railway

echo "============================================================"
echo "SmartPLG Accelerator - Railway Deployment Helper"
echo "============================================================"
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Error: Git is not installed"
    echo "Please install Git first: https://git-scm.com/downloads"
    exit 1
fi

echo "✅ Git is installed"
echo ""

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "============================================================"
echo "Step 1: Prepare for GitHub"
echo "============================================================"
echo ""
echo "Before continuing, you need to:"
echo "1. Create a GitHub repository at: https://github.com/new"
echo "2. Name it: smartplg-accelerator"
echo "3. Keep it Public or Private (your choice)"
echo ""
read -p "Have you created the GitHub repository? (y/n): " created_repo

if [ "$created_repo" != "y" ]; then
    echo ""
    echo "Please create the repository first, then run this script again."
    exit 0
fi

echo ""
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "❌ Error: GitHub username is required"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 2: Commit and Push to GitHub"
echo "============================================================"
echo ""

# Add all files
echo "📦 Adding files to git..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Deploy SmartPLG Accelerator to Railway" || echo "No changes to commit"

# Add remote if not exists
if ! git remote | grep -q origin; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin "https://github.com/$github_username/smartplg-accelerator.git"
else
    echo "✅ GitHub remote already exists"
fi

# Push to GitHub
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ Successfully pushed to GitHub!"
else
    echo "❌ Error pushing to GitHub"
    echo "You may need to authenticate or check your repository URL"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 3: Deploy to Railway"
echo "============================================================"
echo ""
echo "Now follow these steps:"
echo ""
echo "1. Go to: https://railway.app"
echo "2. Sign up with GitHub (if not already signed up)"
echo "3. Click 'New Project'"
echo "4. Select 'Deploy from GitHub repo'"
echo "5. Choose: $github_username/smartplg-accelerator"
echo "6. Railway will automatically deploy your backend"
echo "7. Wait 2-3 minutes for deployment to complete"
echo "8. Go to Settings > Domains to get your backend URL"
echo ""
echo "Your backend URL will look like:"
echo "https://smartplg-accelerator-production.up.railway.app"
echo ""
read -p "Press Enter when you have your Railway backend URL..."

echo ""
read -p "Enter your Railway backend URL (without /api): " railway_url

if [ -z "$railway_url" ]; then
    echo "❌ Error: Railway URL is required"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 4: Update Frontend with Backend URL"
echo "============================================================"
echo ""

# Update index.html with Railway URL
if [ -f "index.html" ]; then
    echo "📝 Updating index.html with Railway backend URL..."
    
    # Create backup
    cp index.html index.html.backup
    
    # Update API_BASE_URL
    sed -i.bak "s|const API_BASE_URL = 'http://localhost:5001/api';|const API_BASE_URL = '$railway_url/api';|g" index.html
    
    # Remove backup file
    rm -f index.html.bak
    
    echo "✅ Updated index.html with Railway URL"
else
    echo "❌ Error: index.html not found"
    exit 1
fi

echo ""
echo "============================================================"
echo "Step 5: Redeploy Frontend to Vercel"
echo "============================================================"
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "⚠️  Vercel CLI not found"
    echo "Installing Vercel CLI..."
    npm install -g vercel
fi

echo "🚀 Deploying to Vercel..."
vercel --prod --yes

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "🎉 DEPLOYMENT COMPLETE!"
    echo "============================================================"
    echo ""
    echo "Your SmartPLG Accelerator is now LIVE!"
    echo ""
    echo "Frontend (Vercel):"
    echo "https://smartplg-accelerator.vercel.app"
    echo ""
    echo "Backend (Railway):"
    echo "$railway_url"
    echo ""
    echo "Test your app:"
    echo "1. Open: https://smartplg-accelerator.vercel.app"
    echo "2. Upload a PDF file"
    echo "3. Generate DDF from CSV"
    echo ""
    echo "✅ All done! Your app is ready to use!"
    echo "============================================================"
else
    echo "❌ Error deploying to Vercel"
    echo "You can manually deploy by running: vercel --prod"
fi

# Made with Bob
