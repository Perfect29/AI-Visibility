#!/bin/bash

# AI Visibility Tool - Comprehensive Test Script
# Tests Docker build, API endpoints, and frontend functionality

set -e  # Exit on any error

echo "🧪 AI Visibility Tool - Comprehensive Testing Suite"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0
TOTAL_TESTS=0

# Function to run a test
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    echo -e "\n${BLUE}Testing: ${test_name}${NC}"
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if eval "$test_command"; then
        echo -e "${GREEN}✅ PASSED: ${test_name}${NC}"
        TESTS_PASSED=$((TESTS_PASSED + 1))
    else
        echo -e "${RED}❌ FAILED: ${test_name}${NC}"
        TESTS_FAILED=$((TESTS_FAILED + 1))
    fi
}

# Function to check if Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Docker is running${NC}"
}

# Function to check if .env file exists
check_env() {
    if [ ! -f .env ]; then
        echo -e "${YELLOW}⚠️  .env file not found. Creating from template...${NC}"
        if [ -f env.example ]; then
            cp env.example .env
            echo -e "${YELLOW}📝 Created .env from template${NC}"
        else
            cat > .env << EOF
# OpenAI API Key (required)
OPENAI_API_KEY=your_openai_api_key_here

# Optional: Override default settings
# HOST=0.0.0.0
# PORT=8000
# DEBUG=false
EOF
            echo -e "${YELLOW}📝 Created .env template${NC}"
        fi
        echo -e "${YELLOW}📝 Please edit .env file and add your OpenAI API key${NC}"
        echo -e "${YELLOW}   Then run this script again${NC}"
        exit 1
    fi
    
    if grep -q "your_openai_api_key_here" .env; then
        echo -e "${YELLOW}⚠️  Please set your OpenAI API key in .env file${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ .env file is properly configured${NC}"
}

# Function to test Docker build
test_docker_build() {
    echo "🔧 Building Docker image..."
    docker-compose build --no-cache
    echo "✅ Docker build completed successfully"
}

# Function to test Docker container startup
test_docker_startup() {
    echo "🚀 Starting Docker container..."
    docker-compose up -d
    
    # Wait for container to be ready
    echo "⏳ Waiting for container to be ready..."
    sleep 10
    
    # Check if container is running
    if docker-compose ps | grep -q "Up"; then
        echo "✅ Container is running"
    else
        echo "❌ Container failed to start"
        docker-compose logs
        return 1
    fi
}

# Function to test API health check
test_api_health() {
    echo "🔍 Testing API health check..."
    
    # Wait a bit more for the API to be ready
    sleep 5
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/api/ || echo "000")
    
    if [ "$response" = "200" ]; then
        echo "✅ API health check passed"
    else
        echo "❌ API health check failed (HTTP $response)"
        return 1
    fi
}

# Function to test frontend accessibility
test_frontend() {
    echo "🌐 Testing frontend accessibility..."
    
    local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/ || echo "000")
    
    if [ "$response" = "200" ] || [ "$response" = "302" ]; then
        echo "✅ Frontend is accessible"
    else
        echo "❌ Frontend accessibility failed (HTTP $response)"
        return 1
    fi
}

# Function to test API endpoints
test_api_endpoints() {
    echo "🔌 Testing API endpoints..."
    
    # Test keywords endpoint
    local keywords_response=$(curl -s -X POST http://localhost:8000/api/keywords \
        -H "Content-Type: application/json" \
        -d '{"brand_name": "Test Brand", "domain": "https://example.com"}' \
        -w "%{http_code}" -o /dev/null || echo "000")
    
    if [ "$keywords_response" = "200" ]; then
        echo "✅ Keywords endpoint working"
    else
        echo "❌ Keywords endpoint failed (HTTP $keywords_response)"
        return 1
    fi
}

# Function to test static files
test_static_files() {
    echo "📁 Testing static files..."
    
    local css_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/css/style.css || echo "000")
    local js_response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/static/js/app.js || echo "000")
    
    if [ "$css_response" = "200" ] && [ "$js_response" = "200" ]; then
        echo "✅ Static files are accessible"
    else
        echo "❌ Static files failed (CSS: $css_response, JS: $js_response)"
        return 1
    fi
}

# Function to clean up
cleanup() {
    echo "🧹 Cleaning up..."
    docker-compose down
    echo "✅ Cleanup completed"
}

# Function to show test results
show_results() {
    echo -e "\n${BLUE}📊 Test Results Summary${NC}"
    echo "=========================="
    echo -e "Total Tests: ${TOTAL_TESTS}"
    echo -e "${GREEN}Passed: ${TESTS_PASSED}${NC}"
    echo -e "${RED}Failed: ${TESTS_FAILED}${NC}"
    
    if [ $TESTS_FAILED -eq 0 ]; then
        echo -e "\n${GREEN}🎉 All tests passed! Your application is ready to use.${NC}"
        echo -e "${BLUE}🌐 Frontend: http://localhost:8000${NC}"
        echo -e "${BLUE}🔗 API: http://localhost:8000/api${NC}"
    else
        echo -e "\n${RED}❌ Some tests failed. Please check the errors above.${NC}"
        exit 1
    fi
}

# Main test execution
main() {
    echo "Starting comprehensive testing..."
    
    # Pre-flight checks
    check_docker
    check_env
    
    # Run tests
    run_test "Docker Build" "test_docker_build"
    run_test "Docker Startup" "test_docker_startup"
    run_test "API Health Check" "test_api_health"
    run_test "Frontend Accessibility" "test_frontend"
    run_test "API Endpoints" "test_api_endpoints"
    run_test "Static Files" "test_static_files"
    
    # Show results
    show_results
    
    # Keep container running for manual testing
    echo -e "\n${YELLOW}💡 Container is still running for manual testing${NC}"
    echo -e "${YELLOW}   To stop: docker-compose down${NC}"
    echo -e "${YELLOW}   To view logs: docker-compose logs -f${NC}"
}

# Trap to ensure cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"
