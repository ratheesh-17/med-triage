# DOCTOR WORKFLOW - VISUAL JOURNEY

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SWASTHYA BANDHU - DOCTOR FLOW                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: REGISTRATION & VERIFICATION                                        │
└─────────────────────────────────────────────────────────────────────────────┘

    Landing Page
         │
         ├──> Login Page
         │         │
         │         └──> "Register as Doctor" Link
         │                      │
         ▼                      ▼
    /doctor/register
    ┌─────────────────────────────────────┐
    │  STEP 1: Personal Details           │
    │  • Profile Photo Upload             │
    │  • Full Name, Phone, Email, Age     │
    └─────────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │  STEP 2: Professional Details       │
    │  • Medical Specialization           │
    │  • Medical Council Number 🔒        │
    │  • Years of Experience              │
    │  • Hospital Affiliation & Address   │
    │  • Location Coordinates (lat/lng)   │
    │  • Consultation Fee & Duration      │
    │  • Consultation Types (Online/In)   │
    └─────────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │  STEP 3: Bio & Availability         │
    │  • Professional Bio (300 chars)     │
    │  • Weekly Availability Grid         │
    │    Mon-Sun × Morning/Afternoon/Eve  │
    └─────────────────────────────────────┘
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │  ⏳ PENDING VERIFICATION SCREEN     │
    │  • Status: Pending                  │
    │  • Message: "Typically 24 hours"    │
    │  • All submitted details shown      │
    └─────────────────────────────────────┘
                   │
                   │ [Admin Reviews & Approves]
                   │
                   ▼
    ┌─────────────────────────────────────┐
    │  📱 OTP Sent to Registered Phone    │
    └─────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 2: LOGIN & DASHBOARD ACCESS                                           │
└─────────────────────────────────────────────────────────────────────────────┘

    Login Page
         │
         ├──> Enter Phone Number
         │         │
         │         ▼
         │    Enter OTP
         │         │
         │         ▼
         │    JWT Token (role: doctor)
         │         │
         ▼         ▼
    /doctor/dashboard
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  DOCTOR DASHBOARD (HOME)                                                 │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ TODAY'S OVERVIEW                                                 │    │
    │  │  [12 Total] [8 Completed] [4 Pending] [4.8★ Rating]            │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ TODAY'S APPOINTMENT QUEUE ⭐ PRIMARY SECTION                     │    │
    │  │                                                                   │    │
    │  │  ┌──────────────────────────────────────────────────────────┐   │    │
    │  │  │ 09:00 AM │ Rajesh Kumar, 45y │ In-Person │ Severity: 9  │   │    │
    │  │  │ Symptoms: Chest pain, shortness of breath                │   │    │
    │  │  │ [View Full Triage Summary] [Mark Complete]               │   │    │
    │  │  └──────────────────────────────────────────────────────────┘   │    │
    │  │                                                                   │    │
    │  │  ┌──────────────────────────────────────────────────────────┐   │    │
    │  │  │ 10:30 AM │ Priya Sharma, 32y │ Online │ Severity: 4     │   │    │
    │  │  │ Symptoms: Fever, cough for 3 days                        │   │    │
    │  │  │ [View Full Triage Summary] [Mark Complete]               │   │    │
    │  │  └──────────────────────────────────────────────────────────┘   │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ UPCOMING APPOINTMENTS (Next 7 Days Calendar)                     │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ WEEKLY PERFORMANCE                                               │    │
    │  │  • Bar Chart: Appointments per day                              │    │
    │  │  • Donut Chart: Severity distribution                           │    │
    │  │  • Avg Response Time: 12 mins                                   │    │
    │  │  • Patient Return Rate: 78%                                     │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ RECENT PATIENT FEEDBACK                                          │    │
    │  │  ⭐⭐⭐⭐⭐ "Very thorough examination" - Meera Singh            │    │
    │  │  ⭐⭐⭐⭐⭐ "Excellent doctor" - Karthik Reddy                   │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    └─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: AI PRE-CONSULT SUMMARY (CLINICAL INTELLIGENCE)                     │
└─────────────────────────────────────────────────────────────────────────────┘

    Click "View Full Triage Summary" from any appointment
                   │
                   ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  AI PRE-CONSULT SUMMARY MODAL                                            │
    │                                                                           │
    │  ┌──────────────────────┐  ┌────────────────────────────────────────┐   │
    │  │ PATIENT INFO         │  │ AI TRIAGE ANALYSIS                     │   │
    │  │                      │  │                                        │   │
    │  │ Name: Rajesh Kumar   │  │ Symptoms (Patient's Words):            │   │
    │  │ Age: 45 years        │  │ "Chest pain, shortness of breath"     │   │
    │  │ Gender: Male         │  │                                        │   │
    │  │                      │  │ Severity Score: [9/10] 🔴             │   │
    │  ├──────────────────────┤  │ Urgency: EMERGENCY                     │   │
    │  │ HEALTH RISK TREND    │  │                                        │   │
    │  │                      │  │ Risk Factors:                          │   │
    │  │ Last 6 Sessions:     │  │ • Cardiac history                      │   │
    │  │ [Trend Chart]        │  │ • Age > 40                             │   │
    │  │                      │  │                                        │   │
    │  │ Cardiac:    ████ 75% │  │ Differential Diagnoses:                │   │
    │  │ Metabolic:  ██   40% │  │ 1. Acute coronary syndrome             │   │
    │  │ Neuro:      █    30% │  │ 2. Pulmonary embolism                  │   │
    │  │ Respiratory:█    25% │  │ 3. Aortic dissection                   │   │
    │  │                      │  │                                        │   │
    │  └──────────────────────┘  │ Suggested Tests:                       │   │
    │                             │ ☑ ECG                                  │   │
    │                             │ ☑ Troponin levels                      │   │
    │                             │ ☑ Chest X-ray                          │   │
    │                             │                                        │   │
    │                             │ ⚠️ RED FLAG INDICATORS:                │   │
    │                             │ Immediate evaluation required.         │   │
    │                             │ Consider emergency protocols.          │   │
    │                             │                                        │   │
    │                             │ Doctor Notes:                          │   │
    │                             │ [Textarea for pre-consultation notes]  │   │
    │                             └────────────────────────────────────────┘   │
    │                                                                           │
    │  [Close]  [Start Consultation] ← Timestamps for metrics                  │
    └─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 4: SCHEDULE MANAGEMENT                                                │
└─────────────────────────────────────────────────────────────────────────────┘

    Navbar → "Manage Schedule"
                   │
                   ▼
    /doctor/slots
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  SLOT MANAGEMENT                                                         │
    │                                                                           │
    │  [Set Recurring Schedule] [Block Leave]                                  │
    │                                                                           │
    │  ┌──────────────────────┐  ┌────────────────────────────────────────┐   │
    │  │ MONTHLY CALENDAR     │  │ DAY DETAIL: 15 Jan 2024                │   │
    │  │                      │  │                                        │   │
    │  │  Jan 2024            │  │ ┌────────────────────────────────────┐ │   │
    │  │  S  M  T  W  T  F  S │  │ │ 09:00 AM  ✅ AVAILABLE             │ │   │
    │  │     1  2  3  4  5  6 │  │ │ Click to block                     │ │   │
    │  │  7  8  9 10 11 12 13 │  │ └────────────────────────────────────┘ │   │
    │  │ 14 [15]16 17 18 19 20│  │                                        │   │
    │  │     ↑                │  │ ┌────────────────────────────────────┐ │   │
    │  │  Selected            │  │ │ 09:30 AM  📅 BOOKED                │ │   │
    │  │                      │  │ │ Patient: Rajesh Kumar              │ │   │
    │  │  Each cell shows:    │  │ └────────────────────────────────────┘ │   │
    │  │  3 avail / 2 booked  │  │                                        │   │
    │  └──────────────────────┘  │ ┌────────────────────────────────────┐ │   │
    │                             │ │ 10:00 AM  ✅ AVAILABLE             │ │   │
    │                             │ └────────────────────────────────────┘ │   │
    │                             │                                        │   │
    │                             │ ┌────────────────────────────────────┐ │   │
    │                             │ │ 10:30 AM  🔒 BLOCKED               │ │   │
    │                             │ │ Click to make available            │ │   │
    │                             │ └────────────────────────────────────┘ │   │
    │                             │                                        │   │
    │                             │ Legend: 🟢 Available 🔵 Booked 🔘 Blocked│
    │                             └────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────┐
    │ SET RECURRING SCHEDULE MODAL        │
    │                                     │
    │ Days: [Mon] [Wed] [Fri]            │
    │ Morning: 09:00 - 13:00             │
    │ Afternoon: 14:00 - 17:00           │
    │ Evening: 18:00 - 20:00             │
    │                                     │
    │ [Apply for Next 30 Days]           │
    └─────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 5: PATIENT HISTORY (CLINICAL CONTEXT)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    Click "View Patient History" from appointment
                   │
                   ▼
    /doctor/patient-history/:patientId
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  PATIENT HISTORY                                                         │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ 👤 Rajesh Kumar, 45y, Male                                       │    │
    │  │ Phone: +91 9876543210 | Emergency: +91 9876543211               │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌──────────────────────┐  ┌────────────────────────────────────────┐   │
    │  │ AI SESSIONS TIMELINE │  │ PAST APPOINTMENTS                      │   │
    │  │                      │  │                                        │   │
    │  │ ● 2024-01-10         │  │ 2024-01-08                             │   │
    │  │   Chest pain         │  │ Dr. Meera Singh - Cardiologist         │   │
    │  │   Severity: 9/10     │  │ In-Person                              │   │
    │  │   → Cardiologist     │  │                                        │   │
    │  │                      │  │ 2023-12-22                             │   │
    │  │ ● 2024-01-05         │  │ Dr. Amit Verma - Pulmonologist         │   │
    │  │   Fever, body ache   │  │ Online                                 │   │
    │  │   Severity: 3/10     │  │                                        │   │
    │  │   → Gen. Physician   │  ├────────────────────────────────────────┤   │
    │  │                      │  │ FAMILY HEALTH OVERVIEW                 │   │
    │  │ ● 2023-12-20         │  │                                        │   │
    │  │   Persistent cough   │  │ Sunita Kumar (Spouse)                  │   │
    │  │   Severity: 5/10     │  │ Recent: Routine checkup - 2024-01-12   │   │
    │  │   → Pulmonologist    │  │                                        │   │
    │  └──────────────────────┘  │ Arjun Kumar (Son)                      │   │
    │                             │ Recent: Vaccination - 2024-01-05       │   │
    │                             └────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ PHASE 6: PERFORMANCE ANALYTICS                                              │
└─────────────────────────────────────────────────────────────────────────────┘

    Navbar → "My Analytics"
                   │
                   ▼
    /doctor/analytics
    ┌─────────────────────────────────────────────────────────────────────────┐
    │  PERFORMANCE ANALYTICS                                                   │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ OVERALL METRICS                                                  │    │
    │  │  [400 Patients] [4.8★ Rating] [28 mins Avg] [82% Response]     │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────────┐    │
    │  │ 📈 INSIGHT: You handled 8 high-severity cases this week,         │    │
    │  │    which is 23% above your monthly average. Excellent work!      │    │
    │  └─────────────────────────────────────────────────────────────────┘    │
    │                                                                           │
    │  ┌──────────────────────┐  ┌────────────────────────────────────────┐   │
    │  │ SEVERITY DISTRIBUTION│  │ WEEKLY TREND (Last 8 Weeks)            │   │
    │  │                      │  │                                        │   │
    │  │   [Pie Chart]        │  │   [Line Chart]                         │   │
    │  │   45% Low            │  │   Week 1: 45 → Week 8: 72              │   │
    │  │   30% Moderate       │  │   📈 Trending Up: 60% increase         │   │
    │  │   20% High           │  │                                        │   │
    │  │    5% Emergency      │  └────────────────────────────────────────┘   │
    │  └──────────────────────┘                                               │
    │                                                                           │
    │  ┌──────────────────────┐  ┌────────────────────────────────────────┐   │
    │  │ RATING DISTRIBUTION  │  │ RECENT REVIEWS                         │   │
    │  │                      │  │                                        │   │
    │  │      4.8 ⭐⭐⭐⭐⭐   │  │ ⭐⭐⭐⭐⭐ Meera Singh                  │   │
    │  │   Based on 357 reviews│  │ "Very thorough examination"            │   │
    │  │                      │  │                                        │   │
    │  │   [Bar Chart]        │  │ ⭐⭐⭐⭐⭐ Karthik Reddy                │   │
    │  │   5★: 250            │  │ "Excellent doctor"                     │   │
    │  │   4★:  80            │  │                                        │   │
    │  │   3★:  20            │  │ ⭐⭐⭐⭐ Anjali Nair                    │   │
    │  │   2★:   5            │  │ "Good consultation"                    │   │
    │  │   1★:   2            │  │                                        │   │
    │  └──────────────────────┘  └────────────────────────────────────────┘   │
    └─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ NAVIGATION BAR (Always Visible for Doctors)                                 │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────────────────────┐
    │ 🏥 Swasthya Bandhu                                                       │
    │                                                                           │
    │  [Dashboard] [Manage Schedule] [My Appointments] [My Analytics]          │
    │                                                                           │
    │                                              [Doctor] [Profile ▼]        │
    │                                                        • Profile Settings │
    │                                                        • Logout           │
    └─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────────┐
│ COMPLETE DAILY WORKFLOW                                                     │
└─────────────────────────────────────────────────────────────────────────────┘

    Morning:
    1. Login → Dashboard
    2. Check "Today's Overview" metrics
    3. Review "Today's Appointment Queue"
    4. For each appointment:
       a. Click "View Full Triage Summary"
       b. Review AI analysis + patient health trend
       c. Read symptoms in patient's own words
       d. Check severity score and urgency
       e. Review differential diagnoses and suggested tests
       f. Add pre-consultation notes
       g. Click "Start Consultation" (timestamps for metrics)
    
    During Day:
    5. Complete consultations
    6. Click "Mark Complete" after each consultation
    7. Check upcoming appointments on calendar
    
    Weekly:
    8. Navigate to "My Analytics"
    9. Review severity distribution
    10. Check weekly appointment trends
    11. Read patient feedback
    
    As Needed:
    12. Navigate to "Manage Schedule"
    13. Set recurring patterns or block specific slots
    14. Block leave periods
    15. Update profile (bio, fees, availability)


┌─────────────────────────────────────────────────────────────────────────────┐
│ KEY DIFFERENTIATORS FOR JUDGES                                              │
└─────────────────────────────────────────────────────────────────────────────┘

    ✅ AI Pre-Consult Summary
       → Doctors never start blind
       → Patient health trend visible before consultation
       → Risk factors and differential diagnoses ready
    
    ✅ Verified Badge Architecture
       → Medical Council Number verification is locked
       → Trust is structural, not cosmetic
       → Visible on every screen
    
    ✅ Slot Management Intelligence
       → Recurring patterns prevent manual setup
       → Double-booking is structurally impossible
       → One-click leave blocking
    
    ✅ Performance Analytics
       → Measurable practice metrics
       → Contextual insights ("23% above average")
       → Platform feels intelligent
    
    ✅ Patient History Timeline
       → Longitudinal health data
       → Family health context
       → Complete clinical picture
    
    ✅ Professional Environment
       → Not just a listing platform
       → Doctors have dashboards, analytics, efficiency metrics
       → Professional practice records


┌─────────────────────────────────────────────────────────────────────────────┐
│ INTEGRATION WITH PATIENT FLOW                                               │
└─────────────────────────────────────────────────────────────────────────────┘

    Patient Side                          Doctor Side
    ────────────                          ───────────
    
    1. Patient uses AI Symptom Chat  →   AI triage data stored
    2. Patient searches doctors      →   Doctor profiles with distance
    3. Patient books appointment     →   Appears in doctor's queue
    4. Patient sees appointment      →   Doctor sees in dashboard
    5. Consultation happens          →   Doctor marks complete
    6. Patient rates doctor          →   Appears in doctor analytics
    
    Both flows work simultaneously and perfectly integrated.
```

---

## 🎯 DEMO SCRIPT FOR JUDGES

**"Let me show you how Swasthya Bandhu serves doctors..."**

1. **Registration:** "Doctor registers with Medical Council Number → pending verification screen"
2. **Dashboard:** "After admin approval, doctor sees today's queue with AI triage badges"
3. **AI Summary:** "Click any appointment → complete AI analysis + patient health trend"
4. **Clinical Context:** "Doctor sees patient's last 6 sessions, severity progression, family health"
5. **Schedule:** "Set recurring pattern once → auto-populates 30 days → one-click leave blocking"
6. **Analytics:** "Doctor sees measurable impact → severity distribution → contextual insights"
7. **Trust:** "Verified badge everywhere → Medical Council Number locked after verification"

**"This isn't just a listing platform. It's a professional environment that makes doctors more effective, more prepared, and more accountable simultaneously."**
