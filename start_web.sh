#!/bin/bash

# SmartCSV Web Application Startup Script

echo "=========================================="
echo "SmartCSV Web Application"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"
echo ""

# Start the Flask backend
echo "🚀 Starting Flask backend server..."
echo "   Backend will run on: http://localhost:5000"
echo ""
echo "📱 To access the web interface:"
echo "   1. Open index.html in your browser, OR"
echo "   2. Run: python3 -m http.server 8000"
echo "      Then visit: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 app.py

# Made with Bob
