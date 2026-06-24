# Job Application Co-Pilot

A comprehensive AI-powered job application assistant that helps job seekers optimize their application materials and prepare for interviews.

## 🎯 Overview

Job Application Co-Pilot is a full-stack application that leverages AI to help users:
- Analyze job fit based on resume and job description
- Rewrite and optimize resumes for specific positions
- Generate tailored cover letters
- Prepare interview Q&A
- Calculate ATS (Applicant Tracking System) scores

## 🏗️ Project Structure

```
.
├── backend/          # FastAPI backend application
│   ├── app/          # Main application code
│   │   ├── agents/   # AI agent coordination
│   │   ├── static/   # Static files served by backend
│   │   ├── auth.py   # Authentication logic
│   │   ├── config.py # Configuration
│   │   ├── database.py # Database setup
│   │   ├── main.py   # FastAPI application
│   │   ├── models.py # SQLAlchemy models
│   │   └── schemas.py # Pydantic schemas
│   ├── alembic/      # Database migrations
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/         # Frontend static files
│   ├── index.html    # Main HTML interface
│   ├── app.js        # JavaScript application logic
│   └── styles.css    # CSS styling
│
├── render.yaml       # Render deployment configuration
├── runtime.txt       # Python version specification
└── DEPLOYMENT.md     # Deployment guide
```

## 🚀 Features

### Backend (FastAPI)
- **User Authentication**: JWT-based secure authentication
- **Application Management**: Create, track, and manage job applications
- **AI-Powered Pipeline**: Automated generation of application materials using Groq LLM
- **Document Processing**: PDF resume parsing and DOCX/PDF generation
- **Web Scraping**: Extract job descriptions from URLs
- **ATS Scoring**: Evaluate resume compatibility with job descriptions

### Frontend (Vanilla JavaScript)
- **Responsive UI**: Clean, modern interface
- **Real-time Feedback**: Instant validation and error handling
- **Document Downloads**: Export resumes and cover letters
- **Application Tracking**: View and manage all applications in one place

## 🛠️ Technology Stack

**Backend:**
- FastAPI - Modern Python web framework
- SQLAlchemy - ORM for database operations
- Groq AI - LLM integration for content generation
- PyJWT - JWT token authentication
- PyPDF & python-docx - Document processing
- BeautifulSoup4 - Web scraping

**Frontend:**
- Vanilla JavaScript
- HTML5 & CSS3
- Fetch API for backend communication

**Database:**
- SQLite (development/default)
- PostgreSQL (recommended for production)

## 📋 Prerequisites

- Python 3.11+
- Groq API Key ([Get one here](https://console.groq.com))
- Git

## 🏃 Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/Pree5559/Job-Application-Co-Pilot.git
cd Job-Application-Co-Pilot
```

### 2. Set Up Backend

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
copy .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### 3. Run the Application

```bash
# From the backend directory
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Access the Application

- **Frontend UI**: http://localhost:8000/
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 📝 Environment Variables

Create a `.env` file in the `backend` directory:

```env
DATABASE_URL=sqlite:///./job_copilot.db
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
GROQ_MODEL=llama-3.1-8b-instant
GROQ_MAX_TOKENS=800
GROQ_MAX_RETRIES=2
```

## 🌐 Deployment

### Deploy to Render

This project includes a `render.yaml` configuration for easy deployment.

**Option 1: Blueprint Deploy (Recommended)**

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New +** → **Blueprint**
3. Connect your GitHub repository
4. Render will auto-detect `render.yaml`
5. Set environment variables:
   - `GROQ_API_KEY`: Your Groq API key
   - `DATABASE_URL`: (Optional) PostgreSQL URL or use default SQLite
   - `SECRET_KEY`: Auto-generated or custom
6. Click **Apply**

**Option 2: Manual Deploy**

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Auto-Deploy on Push

Once connected to Render:
- ✅ **Automatic**: Every push to `main` branch triggers auto-deployment
- 🔄 **Build Time**: ~2-5 minutes
- 📊 **Monitoring**: View logs in Render dashboard

You can disable auto-deploy in Render settings if needed.

## 🧪 API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /token` - Login and get JWT token

### Applications
- `POST /applications` - Create new application with resume and JD
- `GET /applications` - List all user applications
- `GET /applications/{id}` - Get application details
- `PUT /applications/{id}/status` - Update application status
- `GET /applications/{id}/drafts` - Get generated drafts
- `PUT /applications/{id}/regenerate` - Regenerate specific section
- `POST /applications/{id}/ats-score` - Calculate ATS score

### Downloads
- `GET /applications/{id}/download/resume` - Download optimized resume (PDF)
- `GET /applications/{id}/download/cover-letter` - Download cover letter (DOCX)

Full API documentation available at `/docs` when running.

## 🗄️ Database Schema

### Users
- id, username, hashed_password, created_at

### Applications
- id, user_id, job_title, company, jd_text, jd_url
- original_resume_text, resume_sections, status, created_at

### Drafts
- id, application_id, fit_analysis, resume_rewrite
- cover_letter, interview_qa, ats_score, created_at

## 🔧 Development

### Database Migrations (Alembic)

```bash
# Initialize (already done)
alembic init alembic

# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head
```

### Code Structure

- `app/main.py` - FastAPI application and routes
- `app/models.py` - SQLAlchemy database models
- `app/schemas.py` - Pydantic request/response schemas
- `app/auth.py` - JWT authentication
- `app/agents/coordinator.py` - AI pipeline orchestration
- `app/agents/prompts.py` - LLM prompt templates

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Rate limit reached"
- **Solution**: Check Groq API quota at console.groq.com

**Issue**: "Database locked" (SQLite)
- **Solution**: Use PostgreSQL for production or ensure single instance

**Issue**: "Cannot extract text from PDF"
- **Solution**: Ensure PDF is text-based, not scanned images

**Issue**: Frontend not loading
- **Solution**: Check that static files are in `backend/app/static/`

## 📄 License

This project is created as a capstone project for educational purposes.

## 🤝 Contributing

This is a capstone project. For educational or personal use, feel free to fork and modify.

## 📧 Contact

For questions or issues, please open an issue on GitHub.

---

**Built with ❤️ using FastAPI, Groq AI, and modern web technologies**
