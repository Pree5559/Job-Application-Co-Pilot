# Frontend - Job Application Co-Pilot

## Overview

The frontend is a vanilla JavaScript single-page application (SPA) that provides the user interface for the Job Application Co-Pilot.

## Files

- **index.html** - Main HTML structure
- **app.js** - JavaScript application logic and API communication
- **styles.css** - CSS styling and responsive design

## Features

- User authentication (signup/login)
- Job application creation with resume upload
- Job description scraping from URLs
- View application history
- Download generated resumes and cover letters
- Regenerate specific sections (fit analysis, resume, cover letter, etc.)
- ATS score calculation
- Responsive design for mobile and desktop

## API Integration

The frontend communicates with the FastAPI backend at:
- Development: `http://localhost:8000`
- Production: Configured via backend deployment

All API calls use JWT token authentication stored in localStorage.

## Development

To develop locally:

1. Ensure the backend is running on port 8000
2. The frontend is served by the FastAPI backend from `/app/static/`
3. Open http://localhost:8000/ in your browser
4. Changes to HTML/CSS/JS require browser refresh

## Deployment

The frontend files are served as static files by the FastAPI backend. No separate deployment needed.

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- ES6+ JavaScript support required
