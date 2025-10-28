#!/usr/bin/env python3
"""
Comprehensive test script for AI Visibility Tool
Tests backend logic, API flow, and file structure
"""

import os
import sys
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(msg):
    print(f"{GREEN}✓ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}✗ {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠ {msg}{RESET}")

def test_project_structure():
    """Test that all required files and directories exist"""
    print_info("Testing project structure...")
    
    required_files = [
        "frontend/index.html",
        "frontend/css/style.css",
        "frontend/js/app.js",
        "frontend/vercel.json",
        "backend/run.py",
        "backend/requirements.txt",
        "backend/app/__init__.py",
        "backend/app/main.py",
        "backend/app/api/__init__.py",
        "backend/app/api/routes.py",
        "backend/app/core/__init__.py",
        "backend/app/core/config.py",
        "backend/app/services/__init__.py",
        "backend/app/services/scraper.py",
        "backend/app/services/openai_service.py",
        "backend/app/services/visibility_analyzer.py",
        "backend/app/models/__init__.py",
        "backend/app/models/schemas.py",
        "Dockerfile",
        "README.md",
        ".gitignore",
    ]
    
    root = Path(__file__).parent
    all_exist = True
    
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_python_syntax():
    """Test that all Python files have valid syntax"""
    print_info("\nTesting Python syntax...")
    
    root = Path(__file__).parent / "backend"
    python_files = list(root.rglob("*.py"))
    
    all_valid = True
    for py_file in python_files:
        if "__pycache__" in str(py_file):
            continue
        
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), str(py_file), 'exec')
            print_success(f"{py_file.relative_to(root.parent)}")
        except SyntaxError as e:
            print_error(f"{py_file.relative_to(root.parent)} - {e}")
            all_valid = False
    
    return all_valid

def test_api_endpoints():
    """Check that API endpoints are properly defined"""
    print_info("\nTesting API endpoint definitions...")
    
    routes_file = Path(__file__).parent / "backend" / "app" / "api" / "routes.py"
    
    with open(routes_file, 'r') as f:
        content = f.read()
    
    endpoints = [
        ('/keywords', 'extract_keywords_endpoint'),
        ('/prompts', 'generate_prompts_endpoint'),
        ('/simulate', 'simulate_visibility_endpoint'),
    ]
    
    all_found = True
    for endpoint, func_name in endpoints:
        if endpoint in content and func_name in content:
            print_success(f"{endpoint} → {func_name}")
        else:
            print_error(f"{endpoint} endpoint not found")
            all_found = False
    
    return all_found

def test_frontend_api_integration():
    """Check that frontend is calling correct API endpoints"""
    print_info("\nTesting frontend API integration...")
    
    app_js = Path(__file__).parent / "frontend" / "js" / "app.js"
    
    with open(app_js, 'r') as f:
        content = f.read()
    
    api_calls = [
        ('/api/keywords', 'extractKeywords'),
        ('/api/prompts', 'generatePrompts'),
        ('/api/simulate', 'runAnalysis'),
    ]
    
    all_found = True
    for endpoint, func_name in api_calls:
        if endpoint in content and func_name in content:
            print_success(f"{func_name} → {endpoint}")
        else:
            print_error(f"{func_name} function or {endpoint} call not found")
            all_found = False
    
    # Check for important features
    features = [
        'isValidUrl',
        'showError',
        'showSuccess',
        'setLoading',
        'maxlength',  # Character limits
        'getRecommendations',
    ]
    
    print_info("\nChecking frontend features...")
    for feature in features:
        if feature in content:
            print_success(f"{feature}")
        else:
            print_warning(f"{feature} might be missing")
    
    return all_found

def test_deployment_configs():
    """Test deployment configuration files"""
    print_info("\nTesting deployment configs...")
    
    root = Path(__file__).parent
    
    # Test Dockerfile
    dockerfile = root / "Dockerfile"
    if dockerfile.exists():
        with open(dockerfile, 'r') as f:
            content = f.read()
        if 'python' in content.lower() and 'run.py' in content:
            print_success("Dockerfile - valid")
        else:
            print_error("Dockerfile - invalid configuration")
            return False
    else:
        print_error("Dockerfile not found")
        return False
    
    # Test Vercel config
    vercel_json = root / "frontend" / "vercel.json"
    if vercel_json.exists():
        print_success("frontend/vercel.json - exists")
    else:
        print_error("frontend/vercel.json not found")
        return False
    
    # Test requirements.txt
    requirements = root / "backend" / "requirements.txt"
    if requirements.exists():
        with open(requirements, 'r') as f:
            deps = f.read().lower()
        required_deps = ['fastapi', 'uvicorn', 'openai', 'aiohttp', 'beautifulsoup4', 'pydantic']
        missing_deps = [dep for dep in required_deps if dep not in deps]
        
        if not missing_deps:
            print_success("requirements.txt - all dependencies present")
        else:
            print_error(f"requirements.txt - missing: {', '.join(missing_deps)}")
            return False
    else:
        print_error("requirements.txt not found")
        return False
    
    return True

def test_no_extra_files():
    """Check that there are no duplicate or extra files"""
    print_info("\nChecking for extra/duplicate files...")
    
    root = Path(__file__).parent
    
    # Files that should NOT exist
    should_not_exist = [
        "backend/Dockerfile",
        "vercel.json",  # Should only be in frontend/
        "frontend/package.json",
        "backend/frontend",
        "requirements.txt",  # Should only be in backend/
        "backend/main.py",  # Should be backend/app/main.py
        "main.py",
        "app.py",
        "public/",
    ]
    
    all_clean = True
    for path in should_not_exist:
        full_path = root / path
        if full_path.exists():
            print_warning(f"Extra file/directory found: {path}")
            all_clean = False
    
    if all_clean:
        print_success("No extra files found")
    
    return all_clean

def main():
    print(f"\n{BLUE}{'='*60}")
    print("🧪 AI Visibility Tool - Comprehensive Test Suite")
    print(f"{'='*60}{RESET}\n")
    
    tests = [
        ("Project Structure", test_project_structure),
        ("Python Syntax", test_python_syntax),
        ("API Endpoints", test_api_endpoints),
        ("Frontend Integration", test_frontend_api_integration),
        ("Deployment Configs", test_deployment_configs),
        ("Clean Files", test_no_extra_files),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{BLUE}{'─'*60}")
        print(f"Testing: {test_name}")
        print(f"{'─'*60}{RESET}")
        result = test_func()
        results.append((test_name, result))
    
    # Summary
    print(f"\n{BLUE}{'='*60}")
    print("📊 Test Summary")
    print(f"{'='*60}{RESET}\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"{test_name:<30} {status}")
    
    print(f"\n{BLUE}{'─'*60}{RESET}")
    
    if passed == total:
        print(f"{GREEN}✓ All tests passed! ({passed}/{total}){RESET}")
        print(f"{GREEN}🎉 Your project is ready for deployment!{RESET}\n")
        return 0
    else:
        print(f"{RED}✗ Some tests failed ({passed}/{total} passed){RESET}")
        print(f"{YELLOW}⚠ Please fix the issues above before deploying{RESET}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())

