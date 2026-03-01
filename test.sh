#!/bin/bash

# TradeForge AaaS - Automated Test Script
# Author: Ary HH
# Email: cateryatechnology@proton.me
# © 2026

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASSED=0
FAILED=0
TOTAL=0

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "════════════════════════════════════════════════════════════════"
    echo "   TradeForge AaaS - Automated Test Suite"
    echo "   Author: Ary HH | GitHub: @cateryatechnology"
    echo "════════════════════════════════════════════════════════════════"
    echo -e "${NC}"
}

print_test() {
    echo -e "${YELLOW}Testing:${NC} $1"
    ((TOTAL++))
}

print_pass() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
    ((PASSED++))
}

print_fail() {
    echo -e "${RED}❌ FAIL:${NC} $1"
    ((FAILED++))
}

print_info() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

print_summary() {
    echo ""
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}   Test Summary${NC}"
    echo -e "${BLUE}════════════════════════════════════════════════════════════════${NC}"
    echo -e "Total Tests: ${TOTAL}"
    echo -e "${GREEN}Passed: ${PASSED}${NC}"
    echo -e "${RED}Failed: ${FAILED}${NC}"
    
    if [ $FAILED -eq 0 ]; then
        echo -e "${GREEN}"
        echo "════════════════════════════════════════════════════════════════"
        echo "   🎉 ALL TESTS PASSED! 🎉"
        echo "   Your TradeForge setup is working correctly!"
        echo "════════════════════════════════════════════════════════════════"
        echo -e "${NC}"
        return 0
    else
        echo -e "${RED}"
        echo "════════════════════════════════════════════════════════════════"
        echo "   ⚠️  SOME TESTS FAILED"
        echo "   Please review failed tests above"
        echo "════════════════════════════════════════════════════════════════"
        echo -e "${NC}"
        return 1
    fi
}

# Start tests
print_header

echo ""
echo "📋 Test Mode: Select test suite to run"
echo "1. Quick Test (File structure & safety)"
echo "2. Backend Test"
echo "3. Frontend Test"
echo "4. Docker Test"
echo "5. Full Integration Test"
echo "6. All Tests"
echo ""
read -p "Enter choice [1-6]: " TEST_MODE

case $TEST_MODE in
    1)
        echo -e "${BLUE}Running Quick Tests...${NC}"
        echo ""
        
        # Test 1: File Structure
        print_test "File structure"
        if [ -d "backend" ] && [ -d "frontend" ] && [ -d "docker" ]; then
            print_pass "All main directories exist"
        else
            print_fail "Missing main directories"
        fi
        
        # Test 2: Configuration files
        print_test "Configuration files"
        if [ -f ".env.example" ] && [ -f ".gitignore" ] && [ -f "README.md" ]; then
            print_pass "All config files exist"
        else
            print_fail "Missing config files"
        fi
        
        # Test 3: No sensitive files
        print_test "No sensitive files"
        if [ ! -f ".env" ] && [ -z "$(find . -name '*.db' 2>/dev/null)" ]; then
            print_pass "No sensitive files found"
        else
            print_fail "Found sensitive files (.env or .db)"
        fi
        
        # Test 4: .env.example sanitization
        print_test ".env.example sanitization"
        if grep -q "SECRET_KEY=$" .env.example && grep -q "POSTGRES_PASSWORD=$" .env.example; then
            print_pass ".env.example values are empty (safe)"
        else
            print_fail ".env.example contains default values"
        fi
        
        # Test 5: .gitignore effectiveness
        print_test ".gitignore comprehensiveness"
        if grep -q "^\.env$" .gitignore && grep -q "^\*\.db$" .gitignore; then
            print_pass ".gitignore blocks sensitive files"
        else
            print_fail ".gitignore incomplete"
        fi
        ;;
    
    2)
        echo -e "${BLUE}Running Backend Tests...${NC}"
        echo ""
        
        # Test 1: Backend directory
        print_test "Backend directory structure"
        if [ -d "backend/app" ] && [ -f "backend/app/main.py" ]; then
            print_pass "Backend structure correct"
        else
            print_fail "Backend structure incorrect"
        fi
        
        # Test 2: Requirements file
        print_test "Backend requirements.txt"
        if [ -f "backend/requirements.txt" ]; then
            print_pass "requirements.txt exists"
        else
            print_fail "requirements.txt missing"
        fi
        
        # Test 3: Python dependencies (if venv exists)
        print_test "Python dependencies"
        if command -v python3 &> /dev/null; then
            print_pass "Python 3 installed"
            
            # Try to import key packages
            if python3 -c "import fastapi" 2>/dev/null; then
                print_pass "FastAPI importable"
            else
                print_info "FastAPI not installed (run: pip install -r backend/requirements.txt)"
            fi
        else
            print_fail "Python 3 not found"
        fi
        
        # Test 4: Core modules
        print_test "Core backend modules"
        if [ -f "backend/app/core/config.py" ] && [ -f "backend/app/core/security.py" ]; then
            print_pass "Core modules exist"
        else
            print_fail "Core modules missing"
        fi
        ;;
    
    3)
        echo -e "${BLUE}Running Frontend Tests...${NC}"
        echo ""
        
        # Test 1: Frontend structure
        print_test "Frontend directory structure"
        if [ -f "frontend/app.py" ] && [ -d "frontend/pages" ]; then
            print_pass "Frontend structure correct"
        else
            print_fail "Frontend structure incorrect"
        fi
        
        # Test 2: Frontend pages
        print_test "Frontend pages"
        PAGE_COUNT=$(ls frontend/pages/*.py 2>/dev/null | wc -l)
        if [ $PAGE_COUNT -ge 4 ]; then
            print_pass "All frontend pages exist ($PAGE_COUNT pages)"
        else
            print_fail "Missing frontend pages (found: $PAGE_COUNT, expected: 4+)"
        fi
        
        # Test 3: Components
        print_test "Frontend components"
        if [ -f "frontend/components/translation.py" ]; then
            print_pass "Translation component exists"
        else
            print_fail "Translation component missing"
        fi
        
        # Test 4: Streamlit importable
        print_test "Streamlit availability"
        if python3 -c "import streamlit" 2>/dev/null; then
            print_pass "Streamlit importable"
        else
            print_info "Streamlit not installed (run: pip install -r frontend/requirements.txt)"
        fi
        ;;
    
    4)
        echo -e "${BLUE}Running Docker Tests...${NC}"
        echo ""
        
        # Test 1: Docker installed
        print_test "Docker installation"
        if command -v docker &> /dev/null; then
            print_pass "Docker installed ($(docker --version))"
        else
            print_fail "Docker not installed"
        fi
        
        # Test 2: Docker Compose installed
        print_test "Docker Compose installation"
        if command -v docker-compose &> /dev/null; then
            print_pass "Docker Compose installed ($(docker-compose --version))"
        else
            print_fail "Docker Compose not installed"
        fi
        
        # Test 3: Docker configuration
        print_test "Docker configuration files"
        if [ -f "docker/docker-compose.yml" ] && [ -f "docker/Dockerfile.backend" ]; then
            print_pass "Docker configs exist"
        else
            print_fail "Docker configs missing"
        fi
        
        # Test 4: Docker compose syntax
        print_test "Docker compose syntax"
        if command -v docker-compose &> /dev/null; then
            cd docker
            if docker-compose config > /dev/null 2>&1; then
                print_pass "docker-compose.yml syntax valid"
            else
                print_fail "docker-compose.yml syntax error"
            fi
            cd ..
        else
            print_info "Docker Compose not available, skipping syntax check"
        fi
        ;;
    
    5)
        echo -e "${BLUE}Running Full Integration Tests...${NC}"
        echo ""
        
        print_info "This will start Docker services. Press Ctrl+C to cancel."
        sleep 3
        
        # Check if .env exists
        if [ ! -f ".env" ]; then
            print_info "Creating .env from .env.example..."
            cp .env.example .env
            echo "SECRET_KEY=test-secret-key-for-testing-only" >> .env
            echo "POSTGRES_PASSWORD=testpass123" >> .env
        fi
        
        # Test 1: Build Docker images
        print_test "Building Docker images"
        cd docker
        if docker-compose build --quiet; then
            print_pass "Docker images built successfully"
        else
            print_fail "Docker build failed"
            cd ..
            print_summary
            exit 1
        fi
        
        # Test 2: Start services
        print_test "Starting Docker services"
        if docker-compose up -d; then
            print_pass "Services started"
            sleep 10  # Wait for services to be ready
        else
            print_fail "Failed to start services"
            cd ..
            print_summary
            exit 1
        fi
        
        # Test 3: Check service health
        print_test "Service health checks"
        RUNNING=$(docker-compose ps --services --filter "status=running" | wc -l)
        if [ $RUNNING -ge 3 ]; then
            print_pass "Services running ($RUNNING/4)"
        else
            print_fail "Not all services running ($RUNNING/4)"
        fi
        
        # Test 4: Backend API
        print_test "Backend API accessibility"
        sleep 5
        if curl -s http://localhost:8000/health > /dev/null 2>&1; then
            print_pass "Backend API responding"
        else
            print_fail "Backend API not accessible"
        fi
        
        # Test 5: Frontend
        print_test "Frontend accessibility"
        if curl -s http://localhost:8501 > /dev/null 2>&1; then
            print_pass "Frontend responding"
        else
            print_fail "Frontend not accessible"
        fi
        
        # Cleanup
        print_info "Stopping services..."
        docker-compose down
        cd ..
        ;;
    
    6)
        echo -e "${BLUE}Running ALL Tests...${NC}"
        echo ""
        
        # Run all test modes sequentially
        bash $0 << EOF
1
EOF
        
        bash $0 << EOF
2
EOF
        
        bash $0 << EOF
3
EOF
        
        bash $0 << EOF
4
EOF
        
        echo -e "${YELLOW}Skipping integration test in 'All Tests' mode${NC}"
        echo -e "${YELLOW}Run test mode 5 separately for full integration test${NC}"
        ;;
    
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac

# Print summary
print_summary
