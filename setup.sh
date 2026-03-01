#!/bin/bash

# TradeForge AaaS - Setup Script
# Author: Ary HH
# Email: cateryatechnology@proton.me
# GitHub: https://github.com/cateryatechnology
# © 2026

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "════════════════════════════════════════════════════════════════"
echo "   TradeForge AaaS - Complete Setup Script"
echo "   Author: Ary HH | GitHub: @cateryatechnology"
echo "════════════════════════════════════════════════════════════════"
echo -e "${NC}"

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check system requirements
print_info "Checking system requirements..."

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_success "Python $PYTHON_VERSION found"
else
    print_error "Python 3.11+ is required but not installed"
    exit 1
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version | cut -d' ' -f3 | tr -d ',')
    print_success "Docker $DOCKER_VERSION found"
    HAS_DOCKER=true
else
    print_warning "Docker not found. Will setup for local development"
    HAS_DOCKER=false
fi

# Check Docker Compose (optional)
if command -v docker-compose &> /dev/null; then
    print_success "Docker Compose found"
    HAS_DOCKER_COMPOSE=true
else
    HAS_DOCKER_COMPOSE=false
fi

echo ""
print_info "Select installation method:"
echo "1. Docker (Recommended - Requires Docker & Docker Compose)"
echo "2. Local Development (Manual setup)"
echo "3. Production (Docker with optimizations)"
echo ""
read -p "Enter choice [1-3]: " INSTALL_METHOD

case $INSTALL_METHOD in
    1)
        if [ "$HAS_DOCKER" = false ] || [ "$HAS_DOCKER_COMPOSE" = false ]; then
            print_error "Docker and Docker Compose are required for this option"
            exit 1
        fi
        
        print_info "Setting up with Docker..."
        
        # Create .env if not exists
        if [ ! -f .env ]; then
            print_info "Creating .env file..."
            cp .env.example .env
            print_success ".env file created"
            print_warning "Please edit .env file with your API keys and secrets"
            print_info "Opening .env file..."
            ${EDITOR:-nano} .env
        fi
        
        # Build and start services
        print_info "Building Docker images..."
        cd docker
        docker-compose build
        
        print_info "Starting services..."
        docker-compose up -d
        
        print_success "TradeForge AaaS is now running!"
        echo ""
        echo "Access points:"
        echo "  • Frontend: http://localhost:8501"
        echo "  • Backend API: http://localhost:8000"
        echo "  • API Docs: http://localhost:8000/docs"
        echo ""
        ;;
    
    2)
        print_info "Setting up for local development..."
        
        # Create .env
        if [ ! -f .env ]; then
            cp .env.example .env
            print_success ".env file created"
        fi
        
        # Setup backend
        print_info "Setting up backend..."
        cd backend
        
        # Check for Poetry
        if command -v poetry &> /dev/null; then
            print_info "Using Poetry for dependency management..."
            poetry install
        else
            print_info "Poetry not found. Using pip..."
            python3 -m venv venv
            source venv/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
        fi
        
        cd ..
        
        # Setup frontend
        print_info "Setting up frontend..."
        cd frontend
        pip install -r requirements.txt
        cd ..
        
        print_success "Local development setup complete!"
        echo ""
        echo "To run the application:"
        echo "  1. Backend:  cd backend && poetry run uvicorn app.main:app --reload"
        echo "  2. Frontend: cd frontend && streamlit run app.py"
        echo ""
        ;;
    
    3)
        print_info "Setting up for production..."
        print_warning "Make sure to:"
        echo "  1. Change SECRET_KEY in .env"
        echo "  2. Generate ENCRYPTION_KEY"
        echo "  3. Use strong database passwords"
        echo "  4. Enable SSL/TLS"
        echo "  5. Set up reverse proxy (Nginx)"
        echo ""
        
        read -p "Continue? [y/N]: " CONTINUE
        if [ "$CONTINUE" != "y" ] && [ "$CONTINUE" != "Y" ]; then
            exit 0
        fi
        
        # Production setup
        cp .env.example .env
        print_warning "Please edit .env with production values"
        ${EDITOR:-nano} .env
        
        cd docker
        docker-compose -f docker-compose.yml build
        docker-compose -f docker-compose.yml up -d
        
        print_success "Production deployment started"
        ;;
    
    *)
        print_error "Invalid choice"
        exit 1
        ;;
esac

echo ""
print_info "Additional setup steps:"
echo "  1. Edit .env file: nano .env"
echo "  2. Run database migrations: make migrate"
echo "  3. Create admin user (TODO: implement)"
echo "  4. Configure notifications (optional)"
echo ""

print_success "Setup complete! 🎉"
print_info "For more information, see README.md"
echo ""
print_info "Author: Ary HH"
print_info "Email: cateryatechnology@proton.me"
print_info "GitHub: https://github.com/cateryatechnology"
echo ""
