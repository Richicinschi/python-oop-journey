#!/bin/bash
# Kimi Claw Setup Script for Python OOP Journey
# Run this script after cloning the repository

set -e

echo "🚀 Setting up Python OOP Journey for Kimi Claw..."

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Navigate to website-playground
cd website-playground

echo -e "${YELLOW}Step 1: Checking prerequisites...${NC}"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js not found. Installing...${NC}"
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
    source ~/.bashrc
    nvm install 20
    nvm use 20
fi
echo -e "${GREEN}✓ Node.js $(node --version)${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python not found. Please install Python 3.11+${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $(python3 --version)${NC}"

echo -e "${YELLOW}Step 2: Installing dependencies...${NC}"

# Install root dependencies
echo "Installing root dependencies..."
npm install

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd apps/web
npm install
cd ../..

# Install backend dependencies
echo "Installing backend dependencies..."
cd apps/api
pip install -r requirements.txt
cd ../..

echo -e "${GREEN}✓ Dependencies installed${NC}"

echo -e "${YELLOW}Step 3: Setting up environment...${NC}"

# Create env files if they don't exist
if [ ! -f apps/api/.env.local ]; then
    echo "Creating apps/api/.env.local..."
    cp apps/api/.env.production.example apps/api/.env.local
    echo -e "${YELLOW}⚠ Please edit apps/api/.env.local with your configuration${NC}"
fi

if [ ! -f apps/web/.env.local ]; then
    echo "Creating apps/web/.env.local..."
    cp apps/web/.env.example apps/web/.env.local
    echo -e "${YELLOW}⚠ Please edit apps/web/.env.local with your configuration${NC}"
fi

echo -e "${GREEN}✓ Environment files created${NC}"

echo -e "${YELLOW}Step 4: Building project...${NC}"

# Build frontend
cd apps/web
npm run type-check || echo -e "${YELLOW}⚠ TypeScript warnings (non-blocking)${NC}"
npm run build
cd ../..

echo -e "${GREEN}✓ Build complete${NC}"

echo ""
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Edit environment files:"
echo "   - apps/api/.env.local"
echo "   - apps/web/.env.local"
echo ""
echo "2. Start development servers:"
echo "   Terminal 1: cd apps/api && python -m uvicorn api.main:app --reload"
echo "   Terminal 2: cd apps/web && npm run dev"
echo ""
echo "3. Open http://localhost:3000"
echo ""
echo "For full documentation, see KIMI_CLAW_SETUP_GUIDE.md"
