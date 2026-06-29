# 🌾 Smart Agro — AI-Powered Agriculture Management System

> A production-ready full-stack web application for modern agriculture management with AI-powered crop recommendations, disease detection, yield prediction, and more.

![Smart Agro Banner](https://img.shields.io/badge/Smart%20Agro-Agriculture%20AI-2E7D32?style=for-the-badge&logo=leaf)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask)
![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=flat&logo=mysql)
![MUI](https://img.shields.io/badge/MUI-v5-007FFF?style=flat&logo=mui)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Demo Credentials](#demo-credentials)
- [API Documentation](#api-documentation)
- [AI Modules](#ai-modules)
- [Deployment](#deployment)

---

## ✨ Features

### 👥 Four User Roles
| Role | Key Features |
|------|-------------|
| **Farmer** | Crop management, loan applications, AI tools, weather, complaints |
| **Expert** | Answer farmer queries, disease diagnosis, recommendations |
| **Bank Officer** | Review & approve/reject loan applications, loan reports |
| **Admin** | User management, crop prices, complaints, system analytics |

### 🤖 AI Modules
- **Crop Recommendation** — Input soil & climate data → get best crop suggestion
- **Disease Detection** — Upload leaf image → get disease name, confidence & treatment
- **Yield Prediction** — Input crop & farm data → predict expected yield
- **Fertilizer Recommendation** — Input soil NPK → get fertilizer & dosage

### 🌦️ Weather Integration
Real-time weather data with 5-day forecast (OpenWeatherMap API)

### 🔐 Security
- JWT Authentication with role-based access control
- Password hashing with Werkzeug (PBKDF2-SHA256)
- Protected routes on both frontend and backend

---

## 🛠️ Tech Stack

**Frontend:**
- ReactJS 18 (Vite)
- Material UI (MUI) v5
- React Router v6
- Axios
- Recharts
- React Toastify

**Backend:**
- Python 3.10+
- Flask 3.0
- Flask-SQLAlchemy
- Flask-JWT-Extended
- Flask-Migrate
- Flask-CORS

**Database:**
- MySQL 8.0

**AI/ML:**
- scikit-learn
- NumPy / Pandas
- Pillow (image processing)

---

## 📁 Project Structure

```
smart_agro/
├── 📁 backend/
│   ├── run.py                    # App entry point
│   ├── seed_data.py              # Database seeder
│   ├── requirements.txt          # Python dependencies
│   ├── .env.example              # Environment variables template
│   └── app/
│       ├── __init__.py           # Flask app factory
│       ├── config/settings.py    # Config classes
│       ├── models/               # SQLAlchemy models (12 models)
│       ├── routes/               # API blueprints (9 route files)
│       ├── controllers/          # Business logic
│       ├── middleware/           # JWT & role middleware
│       ├── services/             # Reusable services
│       ├── utils/                # Helpers & validators
│       └── ml/                   # AI/ML modules
│           ├── crop_recommender.py
│           ├── yield_predictor.py
│           ├── fertilizer_recommender.py
│           └── disease_detector.py
├── 📁 frontend/
│   ├── src/
│   │   ├── api/                  # Axios API layer
│   │   ├── context/              # React Context (Auth)
│   │   ├── hooks/                # Custom hooks
│   │   ├── routes/               # Protected route component
│   │   ├── components/           # Reusable UI components
│   │   │   ├── layout/           # Sidebar, Navbar, MainLayout
│   │   │   ├── common/           # Cards, Dialogs, Spinners
│   │   │   └── charts/           # Chart widgets
│   │   └── pages/                # 20+ page components
│   │       ├── public/           # Landing, Login, Register
│   │       ├── farmer/           # All farmer pages
│   │       ├── expert/           # All expert pages
│   │       ├── bank/             # All bank pages
│   │       └── admin/            # All admin pages
│   └── package.json
└── 📁 database/
    └── schema.sql                # MySQL schema
```

---

## 🔧 Prerequisites

Make sure you have installed:
- **Node.js** v18+ ([nodejs.org](https://nodejs.org))
- **Python** 3.10+ ([python.org](https://python.org))
- **MySQL** 8.0+ ([mysql.com](https://mysql.com))
- **Git** ([git-scm.com](https://git-scm.com))

---

## 🚀 Installation

### Step 1 — Clone / Open Project
```bash
cd d:/smart_agro
```

### Step 2 — Setup MySQL Database
```bash
# Login to MySQL
mysql -u root -p

# Run the schema script
source d:/smart_agro/database/schema.sql
```

Or using MySQL Workbench: File → Run SQL Script → select `database/schema.sql`

### Step 3 — Setup Backend

```bash
cd d:/smart_agro/backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env
# Edit .env with your database credentials
```

### Step 4 — Configure Backend Environment

Edit `d:/smart_agro/backend/.env`:
```env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost/smart_agro_db
WEATHER_API_KEY=your-openweathermap-api-key-optional
UPLOAD_FOLDER=uploads
MAX_CONTENT_LENGTH=16777216
```

### Step 5 — Initialize Database & Seed Data

```bash
cd d:/smart_agro/backend

# Initialize Flask-Migrate
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed demo data
python seed_data.py
```

### Step 6 — Setup Frontend

```bash
cd d:/smart_agro/frontend

# Install dependencies (if not already done)
npm install

# Copy environment file
copy .env.example .env
```

Edit `d:/smart_agro/frontend/.env`:
```env
VITE_API_URL=http://localhost:5000
```

---

## ▶️ Running the Application

### Start Backend (Terminal 1)
```bash
cd d:/smart_agro/backend
venv\Scripts\activate        # Windows
python run.py
```
Backend runs at: **http://localhost:5000**

### Start Frontend (Terminal 2)
```bash
cd d:/smart_agro/frontend
npm run dev
```
Frontend runs at: **http://localhost:5173**

---

## 🔑 Demo Credentials

All demo accounts use password: **`Password@123`**

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@smartagro.com | Password@123 |
| Farmer | farmer@smartagro.com | Password@123 |
| Expert | expert@smartagro.com | Password@123 |
| Bank Officer | bank@smartagro.com | Password@123 |

---

## 📡 API Documentation

### Base URL: `http://localhost:5000`

#### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Register new user |
| POST | /api/auth/login | Login → returns JWT |
| POST | /api/auth/logout | Logout |
| GET | /api/auth/me | Get current user |
| PUT | /api/auth/me/password | Change password |

#### Farmer
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET/PUT | /api/farmer/profile | Get/Update profile |
| GET/POST | /api/farmer/crops | List/Add crops |
| GET/PUT/DELETE | /api/farmer/crops/:id | Crop operations |
| GET/POST | /api/farmer/loans | List/Apply loans |
| GET/POST | /api/farmer/complaints | List/Raise complaints |
| GET/POST | /api/farmer/queries | List/Submit queries |

#### AI
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/ai/crop-recommend | Crop recommendation |
| POST | /api/ai/disease-detect | Disease detection (image) |
| POST | /api/ai/yield-predict | Yield prediction |
| POST | /api/ai/fertilizer-recommend | Fertilizer recommendation |

#### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/admin/dashboard-stats | System statistics |
| GET/POST | /api/admin/users | List/Create users |
| PUT/DELETE | /api/admin/users/:id | Update/Delete user |
| GET/POST/PUT/DELETE | /api/admin/crop-prices | Manage crop prices |
| GET/PUT | /api/admin/complaints | Manage complaints |

---

## 🤖 AI Modules

### Crop Recommendation
```json
POST /api/ai/crop-recommend
{
  "soil_type": "Loamy",
  "temperature": 28,
  "rainfall": 150,
  "humidity": 70,
  "nitrogen": 90,
  "phosphorus": 42,
  "potassium": 43
}
```

### Disease Detection
```
POST /api/ai/disease-detect
Content-Type: multipart/form-data
body: { image: <file>, crop_type: "wheat" }
```

### Yield Prediction
```json
POST /api/ai/yield-predict
{
  "crop_name": "Wheat",
  "area": 5,
  "rainfall": 120,
  "fertilizer_amount": 200,
  "temperature": 22,
  "season": "Rabi"
}
```

### Fertilizer Recommendation
```json
POST /api/ai/fertilizer-recommend
{
  "soil_type": "Loamy",
  "crop_type": "Wheat",
  "nitrogen": 40,
  "phosphorus": 20,
  "potassium": 30,
  "ph_level": 6.5
}
```

---

## 🌦️ Weather API Setup (Optional)

1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Add to `.env`: `WEATHER_API_KEY=your_key_here`

If no API key is set, the app uses realistic mock weather data.

---

## 🏗️ Deployment

### Backend (Gunicorn + Nginx)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend (Build)
```bash
cd frontend
npm run build
# Serve dist/ folder with Nginx or any static server
```

### Environment Variables for Production
```env
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
JWT_SECRET_KEY=<strong-random-jwt-key>
DATABASE_URL=mysql+pymysql://user:password@db-host/smart_agro_db
```

---

## 📝 License

MIT License — Smart Agro AI Agriculture Management System

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to branch
5. Open a Pull Request

---

*Built with ❤️ for Indian Farmers*
