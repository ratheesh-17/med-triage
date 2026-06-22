# SWASTHYA BANDHU - SYSTEM ARCHITECTURE

## 🏗️ COMPLETE TECHNICAL ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SWASTHYA BANDHU PLATFORM                           │
│                    AI-Powered Healthcare Platform Architecture               │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ FRONTEND LAYER (React + TypeScript)                                         │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ PATIENT INTERFACE (12 Screens)                                       │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Landing Page                    • Appointments List                │
    │ • Patient Registration            • Family Management                │
    │ • Patient Dashboard               • Health Report                    │
    │ • AI Symptom Chat                 • Profile Settings                 │
    │ • Doctor Search + Map             • Login (Shared)                   │
    │ • Appointment Booking                                                │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ DOCTOR INTERFACE (9 Screens)                                         │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Doctor Registration (3-step)    • Appointment History              │
    │ • Pending Verification            • Performance Analytics            │
    │ • Doctor Dashboard                • Profile Management               │
    │ • AI Pre-Consult Summary          • Login (Shared)                   │
    │ • Slot Management                 • Patient History                  │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ SHARED COMPONENTS                                                     │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Navbar (Role-based)             • Protected Routes                 │
    │ • Auth Service                    • API Client (Axios)               │
    │ • Map Component (Leaflet)         • Chart Components (Recharts)      │
    └──────────────────────────────────────────────────────────────────────┘

                                      ↓ HTTP/REST ↓

┌─────────────────────────────────────────────────────────────────────────────┐
│ API GATEWAY LAYER (FastAPI)                                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ AUTHENTICATION & AUTHORIZATION                                        │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • JWT Token Generation            • Role-Based Access Control        │
    │ • OTP Verification                • Token Validation Middleware      │
    │ • Session Management              • CORS Configuration               │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ API ENDPOINTS                                                         │
    ├──────────────────────────────────────────────────────────────────────┤
    │ Patient APIs:                     Doctor APIs:                       │
    │ • POST /auth/patient/register     • POST /auth/doctor/register       │
    │ • POST /chat (AI triage)          • GET /doctor/dashboard            │
    │ • GET /doctors/search             • GET /doctor/appointments         │
    │ • POST /appointments              • PUT /doctor/appointments/:id     │
    │ • GET /appointments               • GET /doctor/slots                │
    │ • POST /appointments/:id/rate     • POST /doctor/slots               │
    │ • GET /health-risk                • GET /doctor/patient-history/:id  │
    │ • GET /family                     • GET /doctor/analytics            │
    │                                                                       │
    │ Shared APIs:                      Admin APIs:                        │
    │ • POST /auth/login                • GET /admin/pending-doctors       │
    │ • POST /auth/verify-otp           • POST /admin/approve-doctor/:id   │
    │ • GET /profile                    • POST /admin/reject-doctor/:id    │
    │ • PUT /profile                                                        │
    └──────────────────────────────────────────────────────────────────────┘

                                      ↓ ↓ ↓

┌─────────────────────────────────────────────────────────────────────────────┐
│ BUSINESS LOGIC LAYER                                                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ AI SERVICE (Google Gemini)                                            │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Symptom Analysis                • Risk Factor Identification        │
    │ • Severity Scoring (1-10)         • Differential Diagnoses            │
    │ • Urgency Classification          • Suggested Diagnostic Tests        │
    │ • Fallback Logic (Rule-based)     • Emergency Detection               │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ DISTANCE CALCULATION SERVICE                                          │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Haversine Formula               • Proximity Sorting                 │
    │ • Geolocation Processing          • Route Calculation                 │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ APPOINTMENT MANAGEMENT SERVICE                                        │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Slot Availability Check         • Booking Confirmation              │
    │ • Double-Booking Prevention       • Status Management                 │
    │ • Recurring Schedule Generation   • Cancellation Handling             │
    └──────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ ANALYTICS SERVICE                                                     │
    ├──────────────────────────────────────────────────────────────────────┤
    │ • Metric Calculation              • Trend Analysis                    │
    │ • Rating Aggregation              • Performance Insights              │
    │ • Health Risk Scoring             • Report Generation                 │
    └──────────────────────────────────────────────────────────────────────┘

                                      ↓ SQL ↓

┌─────────────────────────────────────────────────────────────────────────────┐
│ DATA LAYER (MySQL 8.0)                                                      │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ DATABASE TABLES                                                       │
    ├──────────────────────────────────────────────────────────────────────┤
    │ Core Tables:                      Operational Tables:                │
    │ • users                           • appointments                      │
    │ • patients                        • doctor_slots                      │
    │ • doctors                         • ratings                           │
    │ • family_members                  • doctor_availability_patterns      │
    │ • ai_sessions                                                         │
    └──────────────────────────────────────────────────────────────────────┘

                                      ↓ ↓ ↓

┌─────────────────────────────────────────────────────────────────────────────┐
│ EXTERNAL SERVICES                                                           │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────────────────────┐
    │ • Google Gemini AI API            • SMS Gateway (OTP)                │
    │ • OpenStreetMap (Leaflet)         • Email Service (Notifications)    │
    └──────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 DATA FLOW DIAGRAMS

### 1. Patient Symptom Analysis Flow

```
Patient enters symptoms
        ↓
Frontend validates input
        ↓
POST /chat → Backend
        ↓
AI Service (Gemini API)
        ↓
Generate triage data:
  • Severity score (1-10)
  • Urgency classification
  • Risk factors
  • Differential diagnoses
  • Suggested tests
        ↓
Store in ai_sessions table
        ↓
Return to frontend
        ↓
Display in patient dashboard
Update health risk index
Show in health report
```

### 2. Doctor Search & Booking Flow

```
Patient searches doctors
        ↓
GET /doctors/search?specialization=X&lat=Y&lng=Z
        ↓
Backend queries doctors table
        ↓
Calculate distance for each doctor:
  distance = Haversine(patient_lat, patient_lng, doctor_lat, doctor_lng)
        ↓
Sort by distance
        ↓
Return doctor list
        ↓
Frontend displays:
  • List view with distance
  • Map view with markers
        ↓
Patient selects doctor
        ↓
Navigate to booking page
        ↓
Patient selects date/time/type
        ↓
POST /appointments
        ↓
Backend:
  • Validates slot availability
  • Creates appointment record
  • Updates slot status to "booked"
  • Links to ai_session_id
        ↓
Return confirmation
        ↓
Frontend shows success screen
```

### 3. Doctor Dashboard & Triage Flow

```
Doctor logs in
        ↓
GET /doctor/dashboard
        ↓
Backend queries:
  • Today's appointments
  • Joins with patients table
  • Joins with ai_sessions table
        ↓
Return appointments with:
  • Patient details
  • Symptoms
  • Severity score
  • AI triage data
        ↓
Frontend displays appointment queue
        ↓
Doctor clicks "View Full Triage"
        ↓
GET /doctor/appointments/:id/triage
        ↓
Backend queries:
  • Complete AI session data
  • Patient health history
  • Past appointments
  • Health risk trends
        ↓
Return comprehensive data
        ↓
Frontend displays modal:
  • Left: Patient info + health trend
  • Right: Complete AI analysis
        ↓
Doctor adds notes
        ↓
Doctor clicks "Start Consultation"
        ↓
PUT /doctor/appointments/:id/start
        ↓
Backend records timestamp
        ↓
[Consultation happens]
        ↓
Doctor clicks "Mark Complete"
        ↓
PUT /doctor/appointments/:id/complete
        ↓
Backend:
  • Updates status to "completed"
  • Records completion timestamp
  • Calculates duration
        ↓
Appointment moves to history
```

### 4. Rating & Analytics Flow

```
Patient completes appointment
        ↓
Navigate to /patient/appointments
        ↓
Click "Rate" on completed appointment
        ↓
Patient gives rating (1-5) + comment
        ↓
POST /appointments/:id/rate
        ↓
Backend:
  • Creates rating record
  • Updates doctor.total_ratings
  • Recalculates doctor.avg_rating
        ↓
Return success
        ↓
Frontend shows confirmation
        ↓
[Meanwhile, doctor side]
        ↓
Doctor navigates to /doctor/analytics
        ↓
GET /doctor/analytics
        ↓
Backend calculates:
  • Total appointments
  • Severity distribution
  • Average rating
  • Response times
  • Weekly trends
        ↓
Return metrics
        ↓
Frontend displays:
  • Charts (bar, line, pie)
  • Metric cards
  • Recent reviews
  • Contextual insights
```

---

## 🔐 SECURITY ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ AUTHENTICATION FLOW                                                         │
└─────────────────────────────────────────────────────────────────────────────┘

Patient/Doctor Registration
        ↓
POST /auth/patient/register or /auth/doctor/register
        ↓
Backend:
  • Validates input
  • Hashes password (if applicable)
  • Creates user record with role
  • For doctors: status = "pending"
        ↓
Return success
        ↓
[For doctors: Admin approval required]
        ↓
Admin approves doctor
        ↓
POST /admin/approve-doctor/:id
        ↓
Backend:
  • Updates status to "approved"
  • Sends OTP to phone
        ↓
Doctor receives OTP
        ↓
Login Flow:
        ↓
POST /auth/login (phone)
        ↓
Backend:
  • Validates phone exists
  • Generates OTP
  • Sends OTP (SMS)
        ↓
POST /auth/verify-otp (phone, otp)
        ↓
Backend:
  • Validates OTP
  • Generates JWT token with:
    - user_id
    - role (patient/doctor/admin)
    - expiration (24 hours)
        ↓
Return { token, role }
        ↓
Frontend:
  • Stores token in localStorage
  • Stores role in localStorage
  • Redirects based on role
        ↓
Protected Route Access:
        ↓
Frontend checks:
  • Token exists?
  • Role matches allowed roles?
        ↓
If yes: Render component
If no: Redirect to /login
        ↓
API Request:
        ↓
Frontend adds header:
  Authorization: Bearer <token>
        ↓
Backend middleware:
  • Validates token signature
  • Checks expiration
  • Extracts user_id and role
  • Attaches to request context
        ↓
Route handler:
  • Accesses current_user
  • Enforces role-based permissions
        ↓
Return response
```

---

## 📊 TECHNOLOGY STACK DETAILS

### Frontend Stack
```
React 18.2.0
├── TypeScript 5.0+
├── React Router 6.x (Routing)
├── Ant Design 5.x (UI Components)
├── Recharts 2.x (Data Visualization)
├── Leaflet 1.9.x (Maps)
├── Axios 1.x (HTTP Client)
├── Day.js 1.x (Date Handling)
├── React Hot Toast (Notifications)
├── Lucide React (Icons)
└── Tailwind CSS 3.x (Utility Styles)

Build Tools:
├── Vite 4.x (Build Tool)
├── ESLint (Linting)
└── TypeScript Compiler
```

### Backend Stack
```
FastAPI 0.100+
├── Python 3.8+
├── Pydantic (Data Validation)
├── python-jose (JWT)
├── passlib (Password Hashing)
├── google-generativeai 0.3.2 (Gemini AI)
├── httpx 0.24.1 (HTTP Client)
├── python-dotenv (Environment Variables)
└── uvicorn (ASGI Server)

Database:
└── MySQL 8.0
    ├── mysql-connector-python
    └── SQLAlchemy (ORM - optional)
```

### External Services
```
Google Gemini AI
├── Model: gemini-pro
├── API Key: AIzaSyBitYVUj8P5uC9TSUW_Io7bj_CIFr0dPbI
└── Endpoint: https://generativelanguage.googleapis.com

OpenStreetMap (via Leaflet)
├── Tile Server: https://{s}.tile.openstreetmap.org
└── Free, no API key required

SMS Gateway (for OTP)
└── To be integrated (Twilio/AWS SNS)
```

---

## 🚀 DEPLOYMENT ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ PRODUCTION DEPLOYMENT                                                       │
└─────────────────────────────────────────────────────────────────────────────┘

Frontend (Static Hosting)
├── Vercel / Netlify / AWS S3 + CloudFront
├── Build: npm run build
├── Output: dist/ folder
└── Environment: VITE_API_URL=https://api.swasthyabandhu.com

Backend (Server Hosting)
├── AWS EC2 / Heroku / DigitalOcean
├── Server: Uvicorn + Gunicorn
├── Process Manager: Supervisor / PM2
├── Reverse Proxy: Nginx
└── SSL: Let's Encrypt

Database (Managed Service)
├── AWS RDS MySQL / DigitalOcean Managed Database
├── Automated Backups
├── Read Replicas (for scaling)
└── Connection Pooling

CI/CD Pipeline
├── GitHub Actions / GitLab CI
├── Automated Testing
├── Build & Deploy on Push
└── Environment-specific Configs
```

---

## 📈 SCALABILITY CONSIDERATIONS

### Horizontal Scaling
- **Frontend**: CDN distribution, multiple edge locations
- **Backend**: Load balancer + multiple API servers
- **Database**: Read replicas, sharding by region

### Caching Strategy
- **Frontend**: Browser caching, service workers
- **Backend**: Redis for session data, API response caching
- **Database**: Query result caching, materialized views

### Performance Optimization
- **Frontend**: Code splitting, lazy loading, image optimization
- **Backend**: Database indexing, query optimization, async processing
- **AI Service**: Response caching, batch processing

---

## 🔧 DEVELOPMENT WORKFLOW

```
Local Development
├── Frontend: npm run dev (http://localhost:5173)
├── Backend: python main.py (http://localhost:8000)
└── Database: MySQL local instance

Version Control
├── Git repository
├── Feature branches
├── Pull request reviews
└── Main branch protection

Testing
├── Unit Tests (Jest for frontend, pytest for backend)
├── Integration Tests (API endpoint testing)
├── E2E Tests (Playwright/Cypress)
└── Manual Testing (QA checklist)

Deployment
├── Staging Environment (testing)
├── Production Environment (live)
└── Rollback Strategy (version tagging)
```

---

## ✅ ARCHITECTURE BENEFITS

### Modularity
- Clear separation of concerns
- Independent component development
- Easy to maintain and extend

### Scalability
- Horizontal scaling capability
- Microservices-ready architecture
- Database optimization ready

### Security
- JWT-based authentication
- Role-based access control
- Input validation at multiple layers
- HTTPS enforcement

### Performance
- Optimized API responses
- Efficient database queries
- Frontend code splitting
- CDN distribution

### Maintainability
- Clean code structure
- Comprehensive documentation
- Type safety (TypeScript)
- Consistent coding standards

---

**This architecture supports the complete Swasthya Bandhu platform with 21 screens, real AI integration, and production-ready deployment.**
