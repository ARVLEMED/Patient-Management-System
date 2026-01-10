# Patient Management System

<div align="center">

![HealthHub Logo](https://img.shields.io/badge/HealthHub-Patient_Management-667eea?style=for-the-badge&logo=health&logoColor=white)

**A secure, consent-based patient management system with integrated central registry**

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat-square&logo=docker&logoColor=white)](https://www.docker.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=flat-square&logo=react&logoColor=black)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3.3-3178C6?style=flat-square&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![MariaDB](https://img.shields.io/badge/MariaDB-11.2-003545?style=flat-square&logo=mariadb&logoColor=white)](https://mariadb.org/)

[Features](#-key-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [API Docs](#-api-documentation) • [Testing](#-testing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Default Credentials](#-default-test-credentials)
- [Project Structure](#-project-structure)
- [API Documentation](#-api-documentation)
- [Security Features](#-security-features)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Known Limitations](#-known-limitations)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

The **Patient Management System** is a comprehensive healthcare platform that enables secure, consent-based access to patient medical records. Built with modern web technologies and following healthcare data protection best practices, the system integrates with a mock Central Patient Registry and implements robust consent management workflows.

### Problem Statement

In modern healthcare, patients need:
- **Control** over who accesses their medical data
- **Transparency** about when and how their data is accessed
- **Security** to protect sensitive health information
- **Compliance** with healthcare regulations (HIPAA, GDPR)

### Solution

Our system provides:
- ✅ **Explicit consent management** - Patients grant/revoke access
- ✅ **Complete audit trails** - Every access attempt is logged
- ✅ **Role-based access control** - Different permissions for each user type
- ✅ **Integrated registry** - Seamless connection to central patient database
- ✅ **Modern UI** - Intuitive dashboards for all user types

---

## 🚀 Key Features

### For Patients
- 👤 **Personal Dashboard** - View all consents and access logs
- ✅ **Grant Consent** - Allow healthcare facilities to access your data
- ❌ **Revoke Consent** - Remove access at any time
- 📊 **Access History** - See who viewed your data and when
- 🔐 **Data Control** - Choose consent type (view, edit, share)

### For Healthcare Workers
- 🔍 **Patient Search** - Find patients by National ID
- 📋 **Secure Access** - View patient data with valid consent
- ⚕️ **Consent Validation** - Real-time consent checking
- 📈 **Access Logs** - Track your own data access history
- 🏥 **Facility Dashboard** - Manage patients with active consent

### For Administrators
- 📊 **System Statistics** - User counts, consent metrics, access rates
- 👥 **User Management** - View all registered users
- 🔍 **Audit Logs** - Complete system access history
- 📈 **Security Insights** - Consent effectiveness, access patterns
- 🛡️ **Compliance Monitoring** - Track denied access attempts

### System Features
- 🔒 **JWT Authentication** - Secure token-based auth with refresh tokens
- 🔐 **Data Encryption** - National IDs encrypted at rest
- 📝 **Input Validation** - Pydantic schemas prevent invalid data
- 🚦 **Rate Limiting** - Prevent abuse (100 requests/15min)
- 🐳 **Docker Compose** - One-command deployment
- 📚 **Auto API Docs** - Interactive Swagger documentation

---

## 💻 Technology Stack

### Backend
- **Framework:** FastAPI 0.109.0 (Python 3.11)
- **Database:** MariaDB 11.2
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Authentication:** JWT (python-jose)
- **Password Hashing:** bcrypt (12 rounds)
- **Encryption:** Fernet (cryptography)
- **Rate Limiting:** SlowAPI

### Frontend
- **Framework:** React 18.2 with TypeScript 5.3
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **State Management:** React Context API
- **Styling:** Custom CSS with animations

### Infrastructure
- **Containerization:** Docker & Docker Compose
- **Database Migrations:** Alembic
- **Web Server:** Uvicorn (ASGI)
- **Mock Registry:** FastAPI (separate service)

### Development Tools
- **API Testing:** Postman / Thunder Client
- **Version Control:** Git
- **Code Quality:** TypeScript strict mode, Python type hints

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Patient    │  │   Worker     │  │    Admin     │     │
│  │  Dashboard   │  │  Dashboard   │  │  Dashboard   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                    React Frontend (Port 3000)                │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTPS/REST API
┌────────────────────────────┴────────────────────────────────┐
│                      BACKEND API                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │    Auth     │  │   Consent   │  │   Access    │        │
│  │   Service   │  │   Service   │  │    Logs     │        │
│  └─────────────┘  └─────────────┘  └─────────────┘        │
│                                                              │
│           FastAPI Backend (Port 8000)                       │
└────────┬──────────────────────────────────┬────────────────┘
         │                                   │
         │ SQL Queries                       │ HTTP Requests
         ▼                                   ▼
┌─────────────────┐              ┌─────────────────────┐
│                 │              │   Mock Central      │
│   MariaDB       │              │   Patient Registry  │
│   Database      │              │   (Port 8001)       │
│                 │              │                     │
│  - Users        │              │  - 21 Mock Patients │
│  - Patients     │              │  - API Key Auth     │
│  - Consents     │              │  - Search by ID     │
│  - Access Logs  │              │                     │
└─────────────────┘              └─────────────────────┘
```

### Data Flow Example: Patient Data Access

```
1. Healthcare Worker → Search patient by National ID
                    ↓
2. Backend → Query Mock Registry (with API key)
                    ↓
3. Mock Registry → Return patient basic info
                    ↓
4. Worker → Request full patient data
                    ↓
5. Backend → Check active consent exists
                    ↓
6a. If consent exists → Fetch from registry → Log access (ALLOWED) → Return data
6b. If no consent → Log access (DENIED) → Return error 403
```

---

## 🚀 Quick Start

### Prerequisites

- **Docker Desktop** (v20.10+)
- **Docker Compose** (v2.0+)
- **Git**
- 4GB RAM minimum
- Ports available: 3000, 8000, 8001, 3306

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd patient-management-system
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Generate secure keys** (IMPORTANT!)
```bash
# JWT Secret Key
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"

# JWT Refresh Secret Key
python3 -c "import secrets; print('JWT_REFRESH_SECRET_KEY=' + secrets.token_urlsafe(32))"

# Encryption Key (for National IDs)
python3 -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"

# Registry API Key
python3 -c "import secrets; print('REGISTRY_API_KEY=' + secrets.token_urlsafe(32))"
```

Update `.env` with the generated keys.

4. **Start all services**
```bash
docker-compose up --build
```

**Wait 3-5 minutes** for first startup (building images, creating tables, seeding data).

5. **Access the application**

| Service | URL | Description |
|---------|-----|-------------|
| **Landing Page** | http://localhost:3000 | Modern landing page |
| **Frontend** | http://localhost:3000 | Main application |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/api/docs | Interactive Swagger UI |
| **Mock Registry** | http://localhost:8001 | Central patient registry |

---

## 🔑 Default Test Credentials

The system comes pre-seeded with test accounts:

### Patient Account
```
Email:    patient@test.com
Password: Test123!
Role:     Patient
```
**Features:** Grant/revoke consents, view access logs

### Healthcare Worker Account
```
Email:    doctor@test.com
Password: Test123!
Role:     Healthcare Worker
Facility: HealthHub Clinic
```
**Features:** Search patients, access data with consent

### Admin Account
```
Email:    admin@test.com
Password: Test123!
Role:     Administrator
```
**Features:** System statistics, audit logs, user management

### Additional Test Accounts

**Patients:**
- `sarah.wanjiku@test.com` / `Test123!`
- `james.ochieng@test.com` / `Test123!`
- `faith.akinyi@test.com` / `Test123!`

**Healthcare Workers:**
- `dr.smith@healthhub.com` / `Test123!`
- `dr.omondi@ngh.co.ke` / `Test123!`

---

## 📂 Project Structure

```
patient-management-system/
├── backend/                      # FastAPI Backend
│   ├── app/
│   │   ├── api/                 # API Routes
│   │   │   ├── v1/
│   │   │   │   ├── auth.py      # Authentication endpoints
│   │   │   │   ├── patients.py  # Patient data access
│   │   │   │   ├── consents.py  # Consent management
│   │   │   │   ├── facilities.py # Facility endpoints
│   │   │   │   ├── access_logs.py # Access log viewing
│   │   │   │   └── admin.py     # Admin endpoints
│   │   │   └── dependencies.py  # Auth dependencies
│   │   ├── core/                # Core functionality
│   │   │   ├── config.py        # Configuration
│   │   │   ├── database.py      # Database connection
│   │   │   └── security.py      # Security utilities
│   │   ├── models/              # SQLAlchemy Models
│   │   │   └── models.py        # All database models
│   │   ├── schemas/             # Pydantic Schemas
│   │   │   ├── user.py
│   │   │   ├── patient.py
│   │   │   ├── consent.py
│   │   │   ├── facility.py
│   │   │   └── access_log.py
│   │   ├── services/            # Business Logic
│   │   │   ├── consent_service.py
│   │   │   └── access_log_service.py
│   │   └── database/            # Database utilities
│   │       └── seed_data.py     # Initial seed data
│   ├── init_db.py               # Database initialization
│   ├── seed_manual.py           # Manual seeding script
│   ├── start.sh                 # Startup script
│   ├── Dockerfile
│   └── requirements.txt
│
├── mock-registry/               # Mock Central Registry
│   ├── app/
│   │   ├── main.py             # Registry API
│   │   └── data/
│   │       └── mock_patients.py # 21 mock patients
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── PrivateRoute.tsx
│   │   ├── context/
│   │   │   └── AuthContext.tsx
│   │   ├── pages/
│   │   │   ├── LandingPage.tsx  # Modern landing page
│   │   │   ├── Login.tsx
│   │   │   ├── Register.tsx
│   │   │   ├── PatientDashboard.tsx
│   │   │   ├── WorkerDashboard.tsx
│   │   │   └── AdminDashboard.tsx
│   │   ├── services/            # API Services
│   │   │   ├── api.ts
│   │   │   ├── authService.ts
│   │   │   ├── consentService.ts
│   │   │   ├── patientService.ts
│   │   │   ├── facilityService.ts
│   │   │   └── accessLogService.ts
│   │   ├── types/
│   │   │   └── index.ts         # TypeScript types
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── Dockerfile
│   ├── package.json
│   └── tsconfig.json
│
├── docker-compose.yml           # Service orchestration
├── .env.example                 # Environment template
├── .gitignore
└── README.md                    # This file
```

---

## 📚 API Documentation

### Interactive Documentation

Visit http://localhost:8000/api/docs for full interactive API documentation with:
- All endpoints listed
- Request/response schemas
- Try-it-out functionality
- Authentication testing

### Key Endpoints

#### Authentication
```
POST   /api/auth/register      Register new user
POST   /api/auth/login         Login and get tokens
POST   /api/auth/refresh       Refresh access token
GET    /api/auth/me            Get current user profile
```

#### Patients
```
GET    /api/patients/search?national_id={id}  Search patient
GET    /api/patients/{id}                     Get patient data (requires consent)
GET    /api/patients/me/profile               Get own profile
GET    /api/patients/me/full-data            Get own full data
```

#### Consents
```
POST   /api/consents                   Grant new consent
GET    /api/consents/patient/{id}      List patient's consents
PATCH  /api/consents/{id}/revoke       Revoke consent
POST   /api/consents/check             Check consent validity
GET    /api/consents/facility/{id}     List facility's consents
```

#### Facilities
```
GET    /api/facilities           List all facilities
GET    /api/facilities/{id}      Get facility details
```

#### Access Logs
```
GET    /api/access-logs/patient/{id}   Patient's access logs
GET    /api/access-logs/worker/me      Worker's access logs
GET    /api/access-logs/facility/{id}  Facility's access logs
```

#### Admin
```
GET    /api/admin/users           List all users
GET    /api/admin/audit-logs      System audit logs
GET    /api/admin/statistics      System statistics
GET    /api/admin/consents        All consents
```

### Authentication

All protected endpoints require a JWT token in the Authorization header:

```bash
Authorization: Bearer <your_access_token>
```

**Token Expiry:**
- Access Token: 15 minutes
- Refresh Token: 7 days

---

## 🔐 Security Features

### 1. Authentication & Authorization
- **JWT Tokens** with HS256 algorithm
- **Access tokens** expire in 15 minutes
- **Refresh tokens** expire in 7 days
- **Automatic token refresh** on frontend
- **Role-based access control** (Patient, Worker, Admin)

### 2. Data Protection
- **Password Hashing:** bcrypt with 12 rounds
- **National ID Encryption:** Fernet symmetric encryption at rest
- **Environment Variables:** All secrets in `.env` file
- **SQL Injection Prevention:** SQLAlchemy ORM with prepared statements
- **Input Validation:** Pydantic models validate all inputs

### 3. Rate Limiting
- **100 requests per 15 minutes** per user
- **Stricter limits** on authentication endpoints
- **IP-based tracking** for anonymous requests

### 4. Audit Logging
- **All access attempts logged** (allowed + denied)
- **Immutable logs** (append-only)
- **Detailed information:** Who, what, when, result, reason, IP address
- **Access log retention:** Indefinite (for compliance)

### 5. Consent Validation
- **Explicit patient consent** required before data access
- **Real-time validation** on every access attempt
- **Consent hierarchy:** share > edit > view
- **Automatic expiration** checking
- **Instant revocation** support

### 6. API Security
- **CORS Configuration:** Whitelist of allowed origins
- **Health Check Endpoint:** `/health` for monitoring
- **API Key Authentication:** Registry API requires key
- **HTTPS Ready:** Production deployment uses TLS

---

## 🗄️ Database Schema

### Entity Relationship Diagram

```
┌─────────────┐         ┌──────────────┐
│    Users    │────────>│   Patients   │
│             │   1:1   │              │
│ - user_id   │         │ - patient_id │
│ - email     │         │ - user_id    │
│ - role      │         │ - national_id│
└─────────────┘         └──────┬───────┘
       │                       │
       │ 1:1                   │ 1:N
       │                       │
       ▼                       ▼
┌──────────────────┐    ┌─────────────┐
│HealthcareWorkers │    │  Consents   │
│                  │    │             │
│ - worker_id      │    │ - consent_id│
│ - user_id        │    │ - patient_id│
│ - facility_id    │    │ - facility  │
└─────────┬────────┘    │ - type      │
          │             │ - status    │
          │ N:1         └──────┬──────┘
          │                    │
          ▼                    │
┌──────────────────┐           │
│HealthcareFacility│           │
│                  │           │
│ - facility_id    │───────────┘
│ - name           │    1:N
│ - type           │
└──────────────────┘
```

### Key Tables

**Users** - Authentication and role management
- Stores email, password hash, role, login history
- Links to Patient or HealthcareWorker profiles

**Patients** - Local patient records
- Encrypted National ID
- Links to central registry via patient_id
- Personal information (name, DOB)

**HealthcareFacilities** - Healthcare organizations
- Hospital, Clinic, or Pharmacy
- License information
- Location data

**HealthcareWorkers** - Healthcare provider profiles
- Links to facility
- License number and job title

**Consents** - Patient consent records
- Patient grants consent to facility
- Three types: view, edit, share
- Optional expiration date
- Can be revoked

**AccessLogs** - Audit trail
- Every data access attempt
- Records: who, what, when, result, reason
- Immutable for compliance

---

## 🧪 Testing

### Automated Testing with Postman/cURL

#### Test 1: Patient Grants Consent

```bash
# 1. Login as patient
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"patient@test.com","password":"Test123!"}'

# Save the access_token from response

# 2. Grant consent
curl -X POST "http://localhost:8000/api/consents" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "facility_id":"FAC-001",
    "consent_type":"view",
    "purpose":"For regular health checkup",
    "expires_at":"2026-12-31T23:59:59"
  }'
```

**Expected:** ✅ 201 Created with consent details

#### Test 2: Worker Accesses Patient Data (WITH Consent)

```bash
# 1. Login as healthcare worker
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@test.com","password":"Test123!"}'

# 2. Access patient data
curl -X GET "http://localhost:8000/api/patients/PAT-001234" \
  -H "Authorization: Bearer WORKER_ACCESS_TOKEN"
```

**Expected:** ✅ 200 OK with full patient data

#### Test 3: Worker Denied Access (NO Consent)

```bash
# Try to access patient without consent
curl -X GET "http://localhost:8000/api/patients/PAT-001236" \
  -H "Authorization: Bearer WORKER_ACCESS_TOKEN"
```

**Expected:** ❌ 403 Forbidden with clear reason

### Manual Testing Scenarios

#### Scenario 1: Complete Consent Workflow
1. Login as `patient@test.com`
2. Navigate to "Grant Consent"
3. Select "HealthHub Clinic" and consent type "view"
4. Enter purpose and grant consent
5. Verify consent appears in consent list
6. Logout and login as `doctor@test.com`
7. Search for patient with National ID `12345678`
8. Click "Access Full Patient Data"
9. **Expected:** ✅ Full patient details displayed

#### Scenario 2: Access Denied
1. Login as `doctor@test.com`
2. Search for patient with National ID `34567890` (James Ochieng)
3. Try to access full data
4. **Expected:** ❌ Access denied message
5. Login as `patient@test.com`
6. Check access logs
7. **Expected:** ✅ Denied access logged with reason

#### Scenario 3: Consent Revocation
1. Login as `patient@test.com`
2. Find active consent in list
3. Click "Revoke"
4. Confirm revocation
5. **Expected:** ✅ Status changes to "revoked"
6. Login as `doctor@test.com`
7. Try to access the patient
8. **Expected:** ❌ Access now denied

### Test Data

**Valid National IDs in Mock Registry:**
- 12345678 (John Kamau)
- 23456789 (Sarah Wanjiku)
- 34567890 (James Ochieng)
- 45678901 (Faith Akinyi)
- 56789012 (David Kipchoge)
- ... (17 more in `mock_patients.py`)

**Healthcare Facilities:**
- FAC-001: HealthHub Clinic
- FAC-002: Nairobi General Hospital
- FAC-003: MediCare Pharmacy

---

## 🚢 Deployment

### Production Deployment Checklist

- [ ] Generate strong secrets (32+ characters)
- [ ] Use HTTPS/TLS certificates
- [ ] Configure production database (not SQLite)
- [ ] Set `DEBUG=False` in backend
- [ ] Enable CORS for production domain only
- [ ] Configure proper logging
- [ ] Set up database backups
- [ ] Configure monitoring (Sentry, etc.)
- [ ] Use production-grade web server (Nginx)
- [ ] Implement rate limiting at reverse proxy level
- [ ] Set up CI/CD pipeline
- [ ] Configure environment-specific .env files

### Environment Variables for Production

```bash
# Production Settings
ENVIRONMENT=production
DEBUG=False

# Database (Use managed database service)
DATABASE_URL=mysql+pymysql://user:pass@prod-db-host:3306/pms

# Strong Secrets (Generate unique values)
JWT_SECRET_KEY=<64-character-random-string>
JWT_REFRESH_SECRET_KEY=<64-character-random-string>
ENCRYPTION_KEY=<fernet-key-base64>
REGISTRY_API_KEY=<64-character-random-string>

# CORS (Your production domains)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Rate Limiting (Adjust as needed)
RATE_LIMIT_PER_MINUTE=100
```

### Docker Production Build

```bash
# Build with production flag
docker-compose -f docker-compose.prod.yml build

# Run with production config
docker-compose -f docker-compose.prod.yml up -d
```

### Monitoring Endpoints

```bash
# Backend health
GET http://your-domain.com/health

# Response: {"status":"healthy","service":"patient-management-backend"}
```

---

## ⚠️ Known Limitations

### Current Version Limitations

1. **Email Verification**
   - Email verification not implemented
   - Users can register with any email
   - **Workaround:** Manual verification by admin

2. **Password Reset**
   - No "forgot password" functionality
   - **Workaround:** Admin can reset passwords manually

3. **File Uploads**
   - Cannot upload medical documents/images
   - **Planned:** Future version will support file attachments

4. **Real-time Updates**
   - No WebSocket support
   - **Workaround:** Manual page refresh to see updates

5. **Registry Integration**
   - Currently uses mock registry
   - **Production:** Replace with actual central registry API

6. **Multi-language Support**
   - English only
   - **Planned:** i18n support for Swahili, French

7. **Mobile App**
   - No native mobile apps
   - **Current:** Responsive web design works on mobile browsers

### Performance Considerations

- **Database:** Tested with up to 1000 users
- **Concurrent Users:** Handles 50-100 concurrent users
- **File Storage:** In-memory only (no persistent file storage)
- **Search:** Basic search only (no full-text search)

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue: Database connection refused

```bash
# Check database is healthy
docker-compose ps database

# View database logs
docker-compose logs database

# Restart database
docker-compose restart database
```

**Solution:** Ensure MariaDB container is healthy before backend starts.

#### Issue: Frontend can't connect to backend

```bash
# Check CORS settings in backend
# Verify REACT_APP_API_URL in frontend/.env

# Should be:
REACT_APP_API_URL=http://localhost:8000
```

**Solution:** Ensure frontend `.env` has correct backend URL.

#### Issue: "No active consent found" error

```bash
# Verify consent exists
docker exec -it pms_database mysql -u pms_user -ppms_password_change_me patient_management

# Run SQL:
SELECT * FROM consents WHERE patient_id='PAT-001234' AND status='active';
```

**Solution:** Patient must grant consent before worker can access data.

#### Issue: Seeding doesn't run

```bash
# Check backend logs
docker-compose logs backend | grep -i seed

# Manual seeding
docker exec -it pms_backend python seed_manual.py
```

**Solution:** See `SEEDING_TROUBLESHOOTING.md` for detailed fixes.

#### Issue: Port already in use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Change port in docker-compose.yml or stop conflicting service
```

### Getting Help

1. **Check Logs:**
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   docker-compose logs -f registry
   ```

2. **Verify All Services Running:**
   ```bash
   docker-compose ps
   ```

3. **Reset Everything:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

4. **Documentation:**
   - `SETUP_GUIDE.md` - Step-by-step setup
   - `TESTING_GUIDE.md` - Testing scenarios
   - `SEEDING_TROUBLESHOOTING.md` - Database issues

---

## 📈 Project Statistics

- **Total Lines of Code:** ~15,000+
- **Backend Files:** 33
- **Frontend Files:** 24
- **Mock Registry Files:** 6
- **Test Accounts:** 15 pre-seeded users
- **Mock Patients:** 21 in registry
- **API Endpoints:** 25+
- **Database Tables:** 6

---

## 🤝 Contributing

This is an assessment project. Contributions are not currently accepted.

For educational purposes, you may:
- Fork the repository
- Modify for learning
- Use as reference for your own projects

---

## 📄 License

This project is created for educational/assessment purposes only.

**© 2026 HealthHub Patient Management System**

---

## 👨‍💻 Development Team

Built as part of a Junior Developer Assessment Project

**Technologies Used:**
- Backend: FastAPI, SQLAlchemy, Pydantic, JWT
- Frontend: React, TypeScript, Axios
- Database: MariaDB
- Infrastructure: Docker, Docker Compose

---

## 🎓 Learning Outcomes

This project demonstrates proficiency in:
- ✅ Full-stack web development
- ✅ RESTful API design
- ✅ Database modeling and relationships
- ✅ Authentication and authorization
- ✅ Security best practices
- ✅ Docker containerization
- ✅ Healthcare data compliance
- ✅ Modern frontend development
- ✅ API documentation
- ✅ Testing and QA

---

## 📞 Support

For questions or issues:# Patient Management System

A healthcare patient management system with consent-based data access, integrating with a mock Central Patient Registry.

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│    Frontend     │─────▶│   Backend API   │─────▶│  Mock Registry  │
│  (React + TS)   │      │    (FastAPI)    │      │    (FastAPI)    │
│                 │      │                 │      │                 │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │                 │
                         │     MariaDB     │
                         │                 │
                         └─────────────────┘
```

## 📋 Prerequisites

- Docker Desktop (v20.10+)
- Docker Compose (v2.0+)
- Git
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

## 🚀 Quick Start (One Command Setup)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd patient-management-system
```

2. **Create environment file**
```bash
cp .env.example .env
```

3. **Generate secure keys** (IMPORTANT!)
```bash
# For JWT secrets (generate 32+ character strings)
python3 -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
python3 -c "import secrets; print('JWT_REFRESH_SECRET_KEY=' + secrets.token_urlsafe(32))"

# For encryption key (generate 32 bytes, base64 encoded)
python3 -c "from cryptography.fernet import Fernet; print('ENCRYPTION_KEY=' + Fernet.generate_key().decode())"

# For registry API key
python3 -c "import secrets; print('REGISTRY_API_KEY=' + secrets.token_urlsafe(32))"
```

Update `.env` with the generated keys.

4. **Start all services**
```bash
docker-compose up --build
```

**Note:** First startup takes 2-3 minutes to build images and initialize database.

Wait for all services to be healthy (check logs), then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/docs
- Mock Registry: http://localhost:8001

## 👥 Default Test Credentials

### Patient Account
- **Email:** patient@test.com
- **Password:** Test123!

### Healthcare Worker Account
- **Email:** doctor@test.com
- **Password:** Test123!

### Admin Account
- **Email:** admin@test.com
- **Password:** Test123!

## 📚 Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11)
- **Database:** MariaDB 11.2
- **ORM:** SQLAlchemy 2.0
- **Validation:** Pydantic v2
- **Authentication:** JWT with bcrypt
- **Rate Limiting:** SlowAPI

### Frontend
- **Framework:** React 18 with TypeScript
- **State Management:** React Context API
- **HTTP Client:** Axios
- **UI Components:** (TBD - Material-UI or Tailwind)

### DevOps
- **Containerization:** Docker & Docker Compose
- **Database Migrations:** Alembic

## 🏗️ Project Structure

```
patient-management-system/
├── frontend/                 # React frontend
│   ├── src/
│   │   ├── components/      # Reusable components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── contexts/        # React contexts
│   │   └── utils/           # Utility functions
│   ├── Dockerfile
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API routes
│   │   │   └── v1/          # API version 1
│   │   ├── core/            # Core functionality
│   │   │   ├── config.py    # Configuration
│   │   │   ├── database.py  # Database setup
│   │   │   └── security.py  # Security utilities
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── middleware/      # Custom middleware
│   │   └── main.py          # Application entry
│   ├── alembic/             # Database migrations
│   ├── tests/               # Unit tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── mock-registry/            # Mock central registry
│   ├── app/
│   │   ├── data/            # Mock patient data
│   │   ├── routes/          # Registry endpoints
│   │   └── main.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── docker-compose.yml        # Docker orchestration
├── .env.example             # Environment template
├── .gitignore
└── README.md                # This file
```

## 🔐 Security Features Implemented

1. **Authentication & Authorization**
   - JWT tokens with 15-minute expiry
   - Refresh token mechanism (7 days)
   - Role-based access control (Patient, Healthcare Worker, Admin)
   - Password hashing with bcrypt (12 rounds)

2. **Data Protection**
   - National ID encryption at rest (Fernet encryption)
   - Environment variables for secrets
   - SQL injection prevention (SQLAlchemy ORM)
   - Input validation (Pydantic)
   - Rate limiting (100 requests/15min per user)

3. **Audit Trail**
   - All patient data access logged
   - All consent changes logged
   - Immutable logs (append-only)
   - IP address tracking

4. **Consent Management**
   - Explicit patient consent required
   - Three consent types: view, edit, share
   - Consent expiration support
   - Instant consent revocation

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh access token
- `GET /api/auth/me` - Get current user

### Patients
- `GET /api/patients/search?national_id={id}` - Search patient in registry
- `GET /api/patients/{id}` - Get patient details (requires consent)
- `GET /api/patients/me` - Get current patient's data

### Consents
- `POST /api/consents` - Grant new consent
- `GET /api/consents/patient/{id}` - List patient's consents
- `PATCH /api/consents/{id}/revoke` - Revoke consent
- `GET /api/consents/check` - Check if consent exists

### Access Logs
- `GET /api/access-logs/patient/{id}` - Get patient's access logs
- `GET /api/access-logs/worker/{id}` - Get worker's access logs

### Admin
- `GET /api/admin/users` - List all users
- `GET /api/admin/audit-logs` - View system audit logs
- `GET /api/admin/statistics` - System statistics

### Facilities
- `GET /api/facilities` - List all facilities
- `GET /api/facilities/{id}` - Get facility details

## 🧪 Testing

### Manual Testing Scenarios

1. **Grant Consent Flow**
   - Login as patient
   - Navigate to consent management
   - Grant "view" consent to a facility
   - Verify consent appears in list

2. **Access Patient Data (With Consent)**
   - Login as healthcare worker
   - Search patient by National ID
   - Verify patient data is displayed
   - Check access log is created

3. **Access Denied (No Consent)**
   - Login as healthcare worker
   - Try to access patient without consent
   - Verify access is denied
   - Check denial is logged

4. **Revoke Consent**
   - Login as patient
   - Revoke existing consent
   - Verify status changes to "revoked"

5. **Access After Revocation**
   - Login as healthcare worker
   - Try to access previously consented patient
   - Verify access is now denied

### API Testing with Postman
Import the Postman collection from `/docs/postman-collection.json` (to be created)

## 🔧 Development

### Running Backend Locally
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Running Frontend Locally
```bash
cd frontend
npm install
npm start
```

### Database Migrations
```bash
cd backend
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## 🌱 Seed Data

The system includes seed data for:
- 15 users (5 patients, 8 healthcare workers, 2 admins)
- 3 healthcare facilities
- 20 mock registry patients
- 10 consent records
- 20 access logs

Seed data is automatically loaded on first startup.

## 🐛 Known Limitations

1. **Email Verification:** Currently not implemented (planned for future)
2. **Real-time Updates:** No WebSocket support yet
3. **File Uploads:** Not supported in current version
4. **Password Reset:** Basic implementation only

## 🤝 Contributing

This is an assessment project. Contributions are not accepted.

## 📝 License

This project is for educational/assessment purposes only.

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Check if database is healthy
docker-compose ps

# View database logs
docker-compose logs database

# Reset database
docker-compose down -v
docker-compose up --build
```

### Port Conflicts
If ports 3000, 8000, 8001, or 3306 are in use:
```bash
# Find process using port
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process or change port in docker-compose.yml
```

### Frontend Can't Reach Backend
Ensure environment variables are set correctly:
```bash
REACT_APP_API_URL=http://localhost:8000
```


**Built for Healthcare Innovation**