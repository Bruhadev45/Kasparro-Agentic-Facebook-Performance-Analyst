#!/bin/bash
# Quick setup script for Kasparro Agentic FB Analyst

echo "🚀 Kasparro Agentic FB Analyst - Setup"
echo "======================================"

# Check Python version
python_version=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
required_version="3.10"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo "✅ Python $python_version detected"
else
    echo "❌ Python $required_version or higher required. Current: $python_version"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate and install dependencies
echo "📥 Installing dependencies..."
source .venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Create .env file with your API key:"
echo "   cp .env.example .env"
echo "   # Edit .env and add ANTHROPIC_API_KEY"
echo ""
echo "3. Run analysis:"
echo "   python run.py 'Analyze ROAS drop in last 7 days'"
echo ""
