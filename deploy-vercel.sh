#!/bin/bash

echo "=========================================="
echo "SmartPLG Accelerator - Vercel Deployment"
echo "=========================================="
echo ""

# Check if vercel CLI is installed
if ! command -v vercel &> /dev/null
then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
    echo "✅ Vercel CLI installed"
else
    echo "✅ Vercel CLI found"
fi

echo ""
echo "📝 Before deploying, make sure you have:"
echo "   1. Deployed your backend to Railway/Render/PythonAnywhere"
echo "   2. Updated API_BASE_URL in index.html with your backend URL"
echo ""

read -p "Have you completed the above steps? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "🚀 Deploying to Vercel..."
    echo ""
    
    vercel --prod
    
    echo ""
    echo "✅ Deployment complete!"
    echo ""
    echo "📱 Your app is now live on Vercel"
    echo "🔗 Check the URL provided above"
    echo ""
else
    echo ""
    echo "⚠️  Deployment cancelled"
    echo "📖 Please read DEPLOYMENT.md for detailed instructions"
    echo ""
fi

# Made with Bob
