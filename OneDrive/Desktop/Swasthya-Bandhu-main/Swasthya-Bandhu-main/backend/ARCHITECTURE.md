# Backend Architecture - Clean Layered Structure

```
backend/
├── config/              # Configuration Layer
│   ├── database.py      # SQLAlchemy setup, connection pooling
│   └── auth.py          # JWT token generation, OTP management
│
├── entity/              # Entity Layer (Domain Models)
│   └── models.py        # SQLAlchemy ORM models (9 tables)
│
├── repository/          # Repository Layer (Data Access)
│   └── repositories.py  # Database CRUD operations
│                        # - UserRepository
│                        # - DoctorRepository
│                        # - ChatSessionRepository
│                        # - HealthRiskRepository
│                        # - AppointmentRepository
│                        # - FamilyMemberRepository
│                        # - DoctorSlotRepository
│                        # - AuditLogRepository
│
├── service/             # Service Layer (Business Logic)
│   ├── services.py      # Core business services
│   │                    # - AuthService
│   │                    # - ChatService
│   │                    # - DoctorService
│   │                    # - AdminService
│   ├── ai_service.py    # OpenAI GPT-3.5 integration
│   ├── emergency.py     # Emergency keyword detection
│   ├── analytics.py     # Dashboard analytics, outbreak detection
│   ├── pdf_service.py   # PDF report generation
│   └── utils.py         # Haversine distance, nearest hospital
│
├── controller/          # Controller Layer (API Endpoints)
│   └── controllers.py   # FastAPI routes (20+ endpoints)
│
├── app.py               # Application entry point
├── seed_data.py         # Demo data population
├── requirements.txt     # Dependencies
└── .env                 # Environment variables
```

## Layer Responsibilities

### 1. Config Layer
- Database connection management
- Authentication utilities (JWT, OTP)
- Environment configuration

### 2. Entity Layer
- Domain models (User, Doctor, Appointment, etc.)
- Database table definitions
- Relationships between entities

### 3. Repository Layer
- Direct database operations (CRUD)
- Query building
- Data persistence
- No business logic

### 4. Service Layer
- Business logic implementation
- Orchestrates multiple repositories
- Calls external services (OpenAI, PDF generation)
- Transaction management

### 5. Controller Layer
- HTTP request/response handling
- Input validation (Pydantic schemas)
- Route definitions
- Delegates to service layer

## Request Flow

```
Client Request
      ↓
Controller (controllers.py)
      ↓
Service (services.py)
      ↓
Repository (repositories.py)
      ↓
Entity (models.py)
      ↓
Database (MySQL)
```

## Example: Patient Registration Flow

```
POST /auth/patient/register
      ↓
controllers.py → register_patient()
      ↓
services.py → AuthService.register_patient()
      ↓
repositories.py → UserRepository.create()
      ↓
models.py → User entity
      ↓
database.py → MySQL insert
```

## Benefits of This Architecture

1. **Separation of Concerns**: Each layer has a single responsibility
2. **Testability**: Easy to mock repositories and services
3. **Maintainability**: Changes in one layer don't affect others
4. **Scalability**: Can add caching, message queues at service layer
5. **Reusability**: Services can be used by multiple controllers
6. **Clean Code**: Clear dependencies and data flow

## Design Patterns Used

- **Repository Pattern**: Data access abstraction
- **Service Pattern**: Business logic encapsulation
- **Dependency Injection**: FastAPI's Depends()
- **Factory Pattern**: Database session creation
- **Strategy Pattern**: Different auth strategies (patient, doctor, admin)
