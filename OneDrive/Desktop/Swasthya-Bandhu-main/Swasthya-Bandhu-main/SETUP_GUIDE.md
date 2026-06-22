# Project Setup Guide

## Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL Server
- Git

## Backend Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Swasthya-Bandhu-main/backend
```

### 2. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env with your actual values
# Required:
# - DB_PASSWORD: Your MySQL root password
# - GEMINI_API_KEY: Get from https://makersuite.google.com/app/apikey
# - SECRET_KEY: Generate a strong random string
```

### 3. Setup Python Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Setup Database
```bash
# Make sure MySQL is running, then run:
python seed_data.py
```

### 6. Run the Backend Server
```bash
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd ../frontend-react
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Run Development Server
```bash
npm run dev
```

## Important Notes

⚠️ **Do NOT commit**:
- `.env` files with real credentials
- `node_modules/`
- `__pycache__/`
- ML model files (`*.pkl`, `*.pt`, etc.)
- Large training datasets
- Database files

✅ **Always commit**:
- `.env.example` (template for environment setup)
- `requirements.txt` and `package.json`
- Source code
- Configuration files

## Getting Credentials

1. **Google Gemini API Key**:
   - Go to https://makersuite.google.com/app/apikey
   - Create a new API key
   - Add it to your `.env` file

2. **Database Setup**:
   - Create a MySQL database named `swasthya_bandhu`
   - Update DB_PASSWORD in `.env` with your MySQL root password

## Troubleshooting

If you encounter import errors after pulling latest changes:
```bash
# Backend
pip install -r requirements.txt

# Frontend
rm -rf node_modules
npm install
```
