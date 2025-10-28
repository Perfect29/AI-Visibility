# 🔍 AI Visibility Tool

> Track your brand's visibility across AI platforms like ChatGPT, Claude, and Perplexity

## 🏗️ Architecture

Clean separation of frontend and backend for independent scaling:

- **Frontend**: Static site (HTML/CSS/JS) → Deploy on **Vercel**
- **Backend**: FastAPI Python API → Deploy on **Railway**

## 📁 Project Structure

```
AI-Visibility/
├── frontend/              # Static frontend
│   ├── index.html        # Main page
│   ├── css/
│   │   └── style.css     # Styles
│   ├── js/
│   │   └── app.js        # Frontend logic
│   └── vercel.json       # Vercel config
│
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py # API endpoints
│   │   ├── core/
│   │   │   └── config.py # Settings
│   │   ├── services/
│   │   │   ├── scraper.py
│   │   │   ├── openai_service.py
│   │   │   └── visibility_analyzer.py
│   │   ├── models/
│   │   │   └── schemas.py # Pydantic models
│   │   └── main.py        # FastAPI app
│   ├── run.py             # Entry point
│   └── requirements.txt   # Python dependencies
│
├── Dockerfile             # Railway deployment
└── README.md             # This file
```

## 🚀 Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run
python run.py
```

Backend will run on `http://localhost:8000`

### Frontend

```bash
cd frontend
python -m http.server 3000
```

Frontend will run on `http://localhost:3000`

Update `frontend/js/app.js` to point to local backend:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 🌐 Deployment

### Frontend → Vercel

1. Push code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Import your repository
4. Set **Root Directory** to `frontend`
5. Deploy!

Your frontend will be at: `https://your-app.vercel.app`

### Backend → Railway

1. Push code to GitHub
2. Go to [railway.app](https://railway.app)
3. Create new project from GitHub repo
4. Add environment variable:
   - `OPENAI_API_KEY`: Your OpenAI API key
5. Railway will auto-detect the Dockerfile and deploy

Your backend will be at: `https://your-app.up.railway.app`

### Connect Frontend to Backend

After deploying backend, update `frontend/js/app.js`:

```javascript
const API_BASE_URL = 'https://your-app.up.railway.app';
```

Commit and push - Vercel will auto-redeploy.

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/keywords` | POST | Extract keywords from brand website |
| `/api/prompts` | POST | Generate search prompts from keywords |
| `/api/simulate` | POST | Run AI visibility analysis |

## 🎯 Features

- ✅ Clean, modern UI with gradient design
- ✅ Real-time input validation
- ✅ Character limits on inputs
- ✅ Error handling with toast notifications
- ✅ Loading states & animations
- ✅ Responsive design
- ✅ Production-ready code
- ✅ Scalable architecture

## 🛠️ Tech Stack

**Frontend:**
- Vanilla JavaScript (no frameworks)
- CSS3 with modern features
- Responsive design

**Backend:**
- Python 3.10+
- FastAPI (async web framework)
- OpenAI API
- BeautifulSoup4 (web scraping)
- Pydantic (validation)

## 📊 How It Works

1. **Extract Keywords**: Scrapes your brand website and uses AI to extract relevant keywords
2. **Generate Prompts**: Creates natural search queries based on keywords
3. **Analyze Visibility**: Simulates AI responses to see how often your brand appears
4. **Get Recommendations**: Provides actionable insights to improve visibility

## 🔐 Environment Variables

Backend requires:
- `OPENAI_API_KEY`: Your OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

## 📝 License

MIT License - feel free to use for your projects!

---

Made with ❤️ for better AI visibility
