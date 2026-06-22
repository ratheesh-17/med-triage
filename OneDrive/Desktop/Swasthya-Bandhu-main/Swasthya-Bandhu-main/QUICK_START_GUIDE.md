# SWASTHYA BANDHU - QUICK START GUIDE

## 🚀 Complete Application Setup

This guide will help you run the complete Swasthya Bandhu platform with both patient and doctor flows.

---

## 📋 PREREQUISITES

### Required Software
- **Node.js** (v16 or higher) - [Download](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download](https://www.python.org/)
- **MySQL** (v8.0 or higher) - [Download](https://dev.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/)

### API Keys Required
- **Google Gemini API Key** - [Get it here](https://makersuite.google.com/app/apikey)
  - Current key in project: `AIzaSyBitYVUj8P5uC9TSUW_Io7bj_CIFr0dPbI`

---

## 🗄️ DATABASE SETUP

### Step 1: Create Database
```sql
-- Open MySQL command line or MySQL Workbench
CREATE DATABASE swasthya_bandhu;
USE swasthya_bandhu;
```

### Step 2: Create Tables
```sql
-- Run the SQL schema from INTEGRATION_CHECKLIST.md
-- Or use the migrations in backend/migrations/ (if available)
```

### Step 3: Verify Database Credentials
Check `backend/.env` file:
```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Ratheesh@1703
DB_NAME=swasthya_bandhu
```

---

## 🔧 BACKEND SETUP

### Step 1: Navigate to Backend Directory
```bash
cd backend
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Environment Variables
Check `backend/.env`:
```env
# Database
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=Ratheesh@1703
DB_NAME=swasthya_bandhu

# AI Service
GEMINI_API_KEY=AIzaSyBitYVUj8P5uC9TSUW_Io7bj_CIFr0dPbI

# JWT
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=24

# Server
PORT=8000
```

### Step 5: Clear Python Cache (If Needed)
```bash
# Windows
del /s /q __pycache__
del /s /q *.pyc

# Mac/Linux
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete
```

### Step 6: Start Backend Server
```bash
# Make sure you're in the backend directory
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 7: Test Backend
Open browser and visit:
- http://localhost:8000 - Should show welcome message
- http://localhost:8000/health - Should show health status
- http://localhost:8000/docs - FastAPI interactive docs

---

## 💻 FRONTEND SETUP

### Step 1: Navigate to Frontend Directory
```bash
# Open a NEW terminal window
cd frontend-react
```

### Step 2: Install Dependencies
```bash
npm install
```

**Packages that should be installed:**
- react, react-dom, react-router-dom
- antd (Ant Design)
- axios
- recharts
- react-hot-toast
- dayjs
- leaflet, react-leaflet, @types/leaflet
- lucide-react
- typescript

### Step 3: Verify API Configuration
Check `frontend-react/src/services/api.ts`:
```typescript
const api = axios.create({
  baseURL: 'http://localhost:8000',  // Should point to backend
  headers: {
    'Content-Type': 'application/json',
  },
});
```

### Step 4: Start Frontend Development Server
```bash
npm run dev
```

**Expected Output:**
```
VITE v4.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 5: Open Application
Open browser and visit: **http://localhost:5173**

---

## 🎯 TESTING THE APPLICATION

### Test 1: Patient Flow
1. **Landing Page**
   - Visit http://localhost:5173
   - Should see hero section with 3 feature cards

2. **Patient Registration**
   - Click "Get Started" or navigate to /register
   - Fill form: name, phone, age, gender, emergency contact
   - Submit → should redirect to /patient/dashboard

3. **AI Symptom Chat**
   - Click "Describe Your Symptoms" on dashboard
   - Enter: "I have chest pain and difficulty breathing"
   - Submit → should see AI analysis with severity score

4. **Doctor Search**
   - Click "Find Doctors" in navbar
   - Should see list of doctors with distance
   - Toggle to map view → should see markers

5. **Book Appointment**
   - Click "Book Appointment" on any doctor
   - Select date, time slot, consultation type
   - Confirm → should see success screen

6. **View Appointments**
   - Click "Appointments" in navbar
   - Should see booked appointment in "Upcoming" tab

### Test 2: Doctor Flow
1. **Doctor Registration**
   - Navigate to /doctor/register
   - Complete Step 1: Personal details + photo
   - Complete Step 2: Professional credentials
   - Complete Step 3: Bio + availability grid
   - Submit → should see pending verification screen

2. **Doctor Login** (After Admin Approval)
   - Navigate to /login
   - Enter doctor phone + OTP
   - Should redirect to /doctor/dashboard

3. **Doctor Dashboard**
   - Should see 4 metric cards at top
   - Should see "Today's Appointment Queue"
   - Each appointment shows patient, symptoms, severity

4. **AI Pre-Consult Summary**
   - Click "View Full Triage Summary" on any appointment
   - Should see modal with:
     - Left: Patient info + health risk trend
     - Right: Complete AI analysis

5. **Slot Management**
   - Click "Manage Schedule" in navbar
   - Should see monthly calendar
   - Click any date → should see day detail panel
   - Click "Set Recurring Schedule" → fill form

6. **Performance Analytics**
   - Click "My Analytics" in navbar
   - Should see metrics, charts, ratings

### Test 3: Integration Points
1. **Patient Books → Doctor Sees**
   - Patient books appointment
   - Doctor dashboard shows appointment in queue
   - AI triage data visible to doctor

2. **Doctor Completes → Patient Sees**
   - Doctor marks appointment complete
   - Patient sees in "Past" appointments tab
   - Patient can rate doctor

3. **Rating Updates Analytics**
   - Patient submits 5-star rating
   - Doctor analytics updates average rating
   - Rating appears in doctor feedback section

---

## 🐛 TROUBLESHOOTING

### Backend Issues

**Problem: "Module not found" error**
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**Problem: "Database connection failed"**
```bash
# Solution: Check MySQL is running
# Windows: Open Services → MySQL80 → Start
# Mac: brew services start mysql
# Linux: sudo systemctl start mysql

# Verify credentials in backend/.env
```

**Problem: "Gemini API error"**
```bash
# Solution: Check API key in backend/.env
# Get new key from: https://makersuite.google.com/app/apikey
```

**Problem: "Port 8000 already in use"**
```bash
# Solution: Kill process on port 8000
# Windows: netstat -ano | findstr :8000
#          taskkill /PID <PID> /F
# Mac/Linux: lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Problem: "Cannot connect to backend"**
```bash
# Solution: Verify backend is running on port 8000
# Check api.ts baseURL is 'http://localhost:8000'
```

**Problem: "Module not found" error**
```bash
# Solution: Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem: "Port 5173 already in use"**
```bash
# Solution: Kill process or use different port
# Windows: netstat -ano | findstr :5173
#          taskkill /PID <PID> /F
# Mac/Linux: lsof -ti:5173 | xargs kill -9

# Or specify different port
npm run dev -- --port 3000
```

**Problem: "Map not displaying"**
```bash
# Solution: Install leaflet dependencies
npm install leaflet react-leaflet @types/leaflet

# Add to index.html:
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
```

### Common Errors

**CORS Error**
```bash
# Backend should have CORS middleware configured
# Check main.py has:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**JWT Token Error**
```bash
# Clear browser localStorage
# Open DevTools → Application → Local Storage → Clear
```

---

## 📁 PROJECT STRUCTURE

```
Swasthya-Bandhu-main/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables
│   ├── service/
│   │   └── ai_service.py      # Gemini AI integration
│   ├── routes/                # API endpoints
│   └── models/                # Database models
│
├── frontend-react/
│   ├── src/
│   │   ├── App.tsx            # Main app with routes
│   │   ├── pages/
│   │   │   ├── Landing.tsx
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── DoctorRegistration.tsx
│   │   │   ├── patient/       # 12 patient screens
│   │   │   │   ├── Dashboard.tsx
│   │   │   │   ├── DoctorSearch.tsx
│   │   │   │   ├── AppointmentBooking.tsx
│   │   │   │   ├── Appointments.tsx
│   │   │   │   ├── FamilyManagement.tsx
│   │   │   │   ├── ProfileSettings.tsx
│   │   │   │   └── HealthReport.tsx
│   │   │   └── doctor/        # 9 doctor screens
│   │   │       ├── Dashboard.tsx
│   │   │       ├── SlotManagement.tsx
│   │   │       ├── PatientHistory.tsx
│   │   │       ├── AppointmentHistory.tsx
│   │   │       ├── PerformanceAnalytics.tsx
│   │   │       ├── ProfileManagement.tsx
│   │   │       └── PendingVerification.tsx
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   │   └── Navbar.tsx
│   │   │   └── MapView.tsx
│   │   └── services/
│   │       ├── api.ts
│   │       └── auth.ts
│   ├── package.json
│   └── vite.config.ts
│
└── Documentation/
    ├── DOCTOR_FLOW_COMPLETE.md
    ├── DOCTOR_WORKFLOW_VISUAL.md
    └── INTEGRATION_CHECKLIST.md
```

---

## 🎬 DEMO PREPARATION

### Before Demo
1. **Seed Database** with sample data:
   - 5 patients
   - 10 doctors (various specializations)
   - 20 AI sessions
   - 15 appointments
   - 30 ratings

2. **Test All Flows**:
   - Patient registration → AI chat → booking
   - Doctor login → dashboard → triage view
   - Cross-role interactions

3. **Prepare Demo Script**:
   - Patient journey (5 min)
   - Doctor journey (5 min)
   - Integration demo (3 min)

### During Demo
1. **Start with Landing Page**
   - Show professional UI
   - Highlight key features

2. **Show Patient Flow**
   - AI symptom analysis
   - Doctor search with map
   - Appointment booking

3. **Show Doctor Flow**
   - Dashboard with AI triage
   - Patient history
   - Performance analytics

4. **Highlight Integration**
   - Same appointment from both views
   - AI data flowing between roles
   - Real-time updates

---

## ✅ VERIFICATION CHECKLIST

Before considering setup complete:
- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Database connected and tables created
- [ ] Can register as patient
- [ ] Can register as doctor
- [ ] Can login with both roles
- [ ] Patient dashboard loads
- [ ] Doctor dashboard loads
- [ ] AI chat works (Gemini API responding)
- [ ] Doctor search shows results
- [ ] Map displays correctly
- [ ] All navigation links work
- [ ] No console errors
- [ ] All charts render
- [ ] All modals open/close

---

## 📞 SUPPORT

### Common Questions

**Q: Where do I get the Gemini API key?**
A: Visit https://makersuite.google.com/app/apikey and create a new key

**Q: Can I use a different database?**
A: Yes, but you'll need to update the database connection in backend

**Q: How do I deploy this?**
A: See INTEGRATION_CHECKLIST.md → Deployment section

**Q: Where is the admin panel?**
A: Admin flow is separate - focus on patient and doctor for demo

**Q: How do I add more doctors?**
A: Use /doctor/register or seed database with SQL inserts

---

## 🎯 SUCCESS CRITERIA

Setup is successful when:
✅ Both backend and frontend running without errors
✅ Can access all patient screens (12 screens)
✅ Can access all doctor screens (9 screens)
✅ AI chat generates responses
✅ Doctor search shows results with distance
✅ Map displays with markers
✅ Appointments can be booked
✅ Navigation works for both roles
✅ No critical errors in console

---

## 🚀 NEXT STEPS

After successful setup:
1. Review DOCTOR_FLOW_COMPLETE.md for feature details
2. Review DOCTOR_WORKFLOW_VISUAL.md for workflow diagrams
3. Review INTEGRATION_CHECKLIST.md for testing
4. Seed database with demo data
5. Practice demo flow
6. Prepare presentation

---

## 📝 NOTES

- **Current Status**: Frontend 100% complete for both patient and doctor flows
- **Backend Status**: Core endpoints working, some integration endpoints may need implementation
- **Mock Data**: All screens use realistic mock data matching expected API structure
- **Production Ready**: UI/UX is polished and demo-ready
- **Integration**: Patient and doctor flows designed to work together seamlessly

---

**You're all set! 🎉**

The complete Swasthya Bandhu platform with patient and doctor flows is ready to run.
