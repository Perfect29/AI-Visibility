# 🔍 AI Visibility Tool

A comprehensive tool to analyze your brand's visibility across AI platforms like ChatGPT, Perplexity, and more. Built with FastAPI backend and modern vanilla JavaScript frontend.

## ✨ Features

- **Smart Keyword Extraction**: Automatically extracts relevant keywords from your website
- **AI-Powered Analysis**: Simulates queries across multiple AI platforms
- **Comprehensive Metrics**: Detailed visibility scores, position analysis, and recommendations
- **Beautiful UI**: Modern, responsive design with smooth animations
- **Docker Ready**: Easy deployment with Docker Compose
- **Production Optimized**: Multi-stage Docker builds and security best practices

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Perfect29/AI-Visibility.git
   cd AI-Visibility
   ```

2. **Start the application**
   ```bash
   ./start.sh
   ```

3. **Open your browser**
   - Frontend: http://localhost:8000
   - API: http://localhost:8000/api

### Prerequisites

- Docker Desktop installed and running
- OpenAI API key

## 🌐 Deployment Options

### Option 1: Vercel (Recommended)
1. Fork this repository
2. Connect your GitHub account to [Vercel](https://vercel.com)
3. Import the repository
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy automatically

### Option 2: Railway
1. Connect your GitHub account to [Railway](https://railway.app)
2. Create new project from GitHub
3. Select this repository
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy automatically

### Option 3: Render
1. Connect your GitHub account to [Render](https://render.com)
2. Create new Web Service
3. Connect this repository
4. Add environment variable: `OPENAI_API_KEY`
5. Deploy automatically

### Option 4: Heroku
1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Login to Heroku: `heroku login`
3. Create app: `heroku create your-app-name`
4. Add environment variable: `heroku config:set OPENAI_API_KEY=your_key`
5. Deploy: `git push heroku main`

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd AI-Visibility
```

### 2. Configure Environment

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Or use the automated setup:

```bash
./start.sh
```

### 3. Run with Docker

```bash
# Build and start
docker-compose up --build

# Or use the test script for comprehensive testing
./test.sh
```

### 4. Access the Application

- **Frontend**: http://localhost:8000
- **API**: http://localhost:8000/api
- **Health Check**: http://localhost:8000/api/

## 🧪 Testing

Run the comprehensive test suite:

```bash
./test.sh
```

This will test:
- Docker build process
- Container startup
- API health checks
- Frontend accessibility
- Static file serving
- API endpoints

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework
- **OpenAI Integration**: GPT-4 powered analysis
- **Web Scraping**: BeautifulSoup for content extraction
- **Async Processing**: Concurrent API calls for better performance

### Frontend (Vanilla JS)
- **Modern JavaScript**: ES6+ features
- **Responsive Design**: Mobile-first approach
- **Smooth Animations**: CSS transitions and keyframes
- **Error Handling**: Beautiful notification system

### Docker Setup
- **Multi-stage Build**: Optimized production images
- **Security**: Non-root user execution
- **Health Checks**: Automatic container monitoring
- **Volume Mounting**: Development-friendly setup

## 📊 API Endpoints

### Core Endpoints

- `GET /api/` - Health check
- `POST /api/keywords` - Extract keywords from domain
- `POST /api/simulate` - Simulate AI platform queries
- `POST /api/analyze` - Complete end-to-end analysis

### Request/Response Examples

**Extract Keywords:**
```bash
curl -X POST http://localhost:8000/api/keywords \
  -H "Content-Type: application/json" \
  -d '{"brand_name": "Stripe", "domain": "https://stripe.com"}'
```

**Simulate Queries:**
```bash
curl -X POST http://localhost:8000/api/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name": "Stripe",
    "prompts": ["Best payment processing platforms", "Top fintech companies"],
    "platforms": ["chatgpt", "perplexity"]
  }'
```

## 🎨 UI/UX Features

### Design Principles
- **Clean & Modern**: Minimalist design with focus on content
- **Responsive**: Works perfectly on desktop, tablet, and mobile
- **Accessible**: Proper contrast ratios and keyboard navigation
- **Fast**: Optimized loading and smooth animations

### User Experience
- **Progressive Disclosure**: Step-by-step workflow
- **Real-time Feedback**: Loading states and progress indicators
- **Error Handling**: Beautiful error notifications
- **Success States**: Clear confirmation messages

### Visual Elements
- **Gradient Backgrounds**: Modern color schemes
- **Card-based Layout**: Clean content organization
- **Smooth Animations**: CSS transitions and keyframes
- **Interactive Elements**: Hover effects and micro-interactions

## 🔧 Development

### Local Development

```bash
# Backend development
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py

# Frontend development
cd frontend
# Edit files directly - changes reflect immediately
```

### Docker Development

```bash
# Start with volume mounting for live reload
docker-compose up --build

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

## 📁 Project Structure

```
AI-Visibility/
├── backend/
│   ├── app/
│   │   ├── api/           # API routes
│   │   ├── core/          # Configuration
│   │   ├── models/        # Pydantic models
│   │   └── services/      # Business logic
│   ├── Dockerfile         # Multi-stage Docker build
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── css/              # Stylesheets
│   ├── js/               # JavaScript
│   └── index.html        # Main HTML
├── docker-compose.yml    # Docker orchestration
├── .dockerignore         # Docker ignore rules
├── start.sh             # Quick start script
├── test.sh              # Comprehensive test suite
└── README.md            # This file
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup:**
   ```bash
   # Set production environment variables
   export OPENAI_API_KEY=your_production_key
   export DEBUG=false
   export HOST=0.0.0.0
   export PORT=8000
   ```

2. **Docker Production Build:**
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

3. **Health Monitoring:**
   ```bash
   # Check container health
   docker-compose ps
   
   # View logs
   docker-compose logs -f
   ```

### Cloud Deployment

The application is ready for deployment on:
- **AWS ECS/Fargate**
- **Google Cloud Run**
- **Azure Container Instances**
- **DigitalOcean App Platform**
- **Heroku Container Registry**

## 🔒 Security Features

- **Non-root User**: Container runs as non-privileged user
- **Input Validation**: Comprehensive request validation
- **CORS Configuration**: Proper cross-origin settings
- **Environment Variables**: Secure configuration management
- **Health Checks**: Container monitoring and auto-restart

## 📈 Performance Optimizations

- **Multi-stage Docker Build**: Smaller production images
- **Async Processing**: Concurrent API calls
- **Caching**: Docker layer caching
- **Static File Serving**: Optimized frontend delivery
- **Health Checks**: Automatic container monitoring

## 🐛 Troubleshooting

### Common Issues

1. **Docker not running:**
   ```bash
   # Start Docker Desktop
   # Check with: docker --version
   ```

2. **Port already in use:**
   ```bash
   # Change port in docker-compose.yml
   # Or stop conflicting services
   ```

3. **OpenAI API errors:**
   ```bash
   # Check API key in .env file
   # Verify API key has sufficient credits
   ```

4. **Build failures:**
   ```bash
   # Clean Docker cache
   docker system prune -a
   docker-compose build --no-cache
   ```

### Debug Mode

```bash
# Enable debug mode
export DEBUG=true
docker-compose up --build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `./test.sh`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent Python web framework
- **OpenAI** for powerful AI capabilities
- **Docker** for containerization
- **Modern CSS** for beautiful styling

---

**Built with ❤️ for better AI visibility**