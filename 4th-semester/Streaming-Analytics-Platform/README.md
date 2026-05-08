# 🎬 Streaming Analytics Platform (SAP)

A **NoSQL-based Streaming Analytics Platform** built with **MongoDB Atlas** and **Python Flask** for the Advanced Database Systems (ADS) course. This project demonstrates core NoSQL concepts including CRUD operations, aggregation pipelines, concurrency control, transactions, schema validation, and role-based access control.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Project Scope](#project-scope)
- [Database Schema](#database-schema)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Modules](#modules)
- [Technical Highlights](#technical-highlights)
- [Limitations](#limitations)
- [Project Stakeholders](#project-stakeholders)

---

## 📖 Overview

Online streaming platforms like Netflix, Amazon Prime, and IMDb generate vast amounts of semi-structured data. This project implements a **scalable NoSQL-based solution** that addresses common challenges in streaming systems:

- **Rigid Schemas**: Flexible MongoDB schemas support evolving media structures
- **Scalability Issues**: NoSQL approach enables horizontal scaling
- **Nested Data**: JSON documents naturally represent complex relationships
- **Real-time Analytics**: Aggregation pipelines power dynamic dashboards
- **Concurrent Access**: Application-level locking and versioning ensure consistency

The system demonstrates how modern NoSQL technologies can build data-driven web applications similar to real-world streaming platforms.

---

## ✨ Key Features

### 🔐 Authentication & Authorization
- **Secure Login/Register** with bcrypt salted password hashing
- **Session-based authentication** with CSRF protection
- **Role-Based Access Control (RBAC)** for Admin, User, and Guest users

### 👨‍💼 Admin Dashboard
- 📊 **Analytics Dashboard**: Total users, movies, subscriptions, ratings
- 📈 **Performance Metrics**: Genre distribution, revenue charts, trending movies
- 🎬 **Movies Management**: Full CRUD operations with pagination
- 👥 **Users Management**: View all users with country distribution
- 💳 **Subscriptions & Payments**: Track active subscriptions and payments
- 🛠️ **Data Studio**: Dynamic CRUD tool for all collections
- 📋 **Materialized Views**: Pre-computed analytics data

### 👤 User Dashboard
- 🎥 **Browse Movies**: View personalized movie catalog
- ⭐ **Rate Movies**: Submit ratings with optimistic locking
- 📝 **Watchlist**: Save and manage favorite movies
- 👨 **Profile Management**: Update personal information and preferences
- 📊 **Engagement Metrics**: View watch history and activity stats

### 🌐 Guest Functionality
- Browse limited movie content
- Read-only access (no modifications)

### 💪 Backend Features
- ✅ **CRUD Operations**: Full create, read, update, delete across all collections
- 🔄 **Optimistic Locking**: Version fields prevent conflicting updates
- 🔐 **Pessimistic Locking**: Resource locks collection for critical operations
- ✔️ **JSON Schema Validation**: Enforce data structure consistency
- 💬 **Multi-Document Transactions**: ACID properties across collections
- 🔑 **Access Control**: Role-based permissions enforced at API level
- 🛡️ **NoSQL Injection Prevention**: Parameterized queries and input validation

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Database** | MongoDB Atlas (Cloud) |
| **Backend** | Python Flask 3.0.3 |
| **ODM** | PyMongo 4.8.0 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+) |
| **Charts** | Chart.js |
| **UI Framework** | Bootstrap 5 |
| **Security** | Werkzeug 3.0.4, bcrypt |
| **Environment** | python-dotenv 1.0.1 |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (UI Layer)                      │
│  HTML Templates + Bootstrap + Chart.js + JavaScript ES6+    │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 Flask Backend (API Layer)                   │
│  - Authentication & Authorization (RBAC)                    │
│  - CRUD Route Handlers                                      │
│  - Aggregation Pipeline Executors                           │
│  - Concurrency Control (Optimistic & Pessimistic Locking)   │
│  - Transaction Management                                   │
│  - Input Validation & Security                              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              MongoDB Atlas (Data Layer)                     │
│  - 11 Collections with JSON Schema Validation               │
│  - Materialized Views for Analytics                         │
│  - Resource Locks Collection for Pessimistic Locking        │
│  - Transactions Support (Multi-document ACID)               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Project Scope

### ✅ Supported Functionalities

**Admin Module:**
- ✔️ CRUD operations (Movies, Users, Subscriptions)
- ✔️ Data Studio access (Dynamic CRUD tool)
- ✔️ Performance dashboard & analytics
- ✔️ Aggregation-based insights
- ✔️ Materialized views management

**User Module:**
- ✔️ Watchlist management
- ✔️ Browse and view movies
- ✔️ Submit and view ratings
- ✔️ Update profile information

**Guest Module:**
- ✔️ Browse limited content
- ✔️ No modification access

**Backend Features:**
- ✔️ Optimistic locking via version fields
- ✔️ Pessimistic locking via resource_locks collection
- ✔️ JSON schema validation
- ✔️ Transactions for multi-document updates
- ✔️ Authentication + salted hashing
- ✔️ Role-based access control

---

## 📊 Database Schema

The project uses **11 MongoDB collections** with strict JSON Schema validation:

### Collections Overview

| Collection | Purpose | Key Fields |
|-----------|---------|-----------|
| **users** | User profiles & auth | _id, username, email, password_hash, role, created_at |
| **movies** | Movie metadata | _id, title, year, genre, rating, director, actors |
| **ratings** | User movie ratings | _id, user_id, movie_id, score, review, timestamp, version |
| **watchlist** | User favorites | _id, user_id, movie_id, added_at |
| **subscriptions** | Active plans | _id, user_id, plan_type, amount, start_date, end_date |
| **payments** | Payment records | _id, subscription_id, amount, date, status |
| **actors** | Actor information | _id, name, birth_year, nationality |
| **genres** | Genre definitions | _id, name, description |
| **reviews** | User reviews | _id, user_id, movie_id, content, timestamp |
| **resource_locks** | Concurrency control | _id, resource_type, resource_id, locked_by, locked_at |
| **activity_log** | User activities | _id, user_id, action, timestamp, details |

**Key Schema Features:**
- ✅ JSON Schema Validation for data integrity
- ✅ Version fields for optimistic locking
- ✅ Timestamp fields for audit trails
- ✅ Role-based field visibility
- ✅ Embedded documents for related data
- ✅ Array fields for relationships

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.8+
- MongoDB Atlas Account (Free tier available)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Streaming_App
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory:
```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<database>?retryWrites=true&w=majority
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Step 5: Create MongoDB Collections
The collections will be automatically created with JSON Schema validation on first run. Seed data can be loaded via the admin panel or by importing the dataset folder.

### Step 6: Run the Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## 🚀 Usage

### Default Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

**Test User Account:**
- Username: `testuser`
- Password: `password123`

### Accessing Different Sections

| Role | URL | Features |
|------|-----|----------|
| **Admin** | `/admin` | Dashboard, Analytics, CRUD, Data Studio |
| **User** | `/user` | Dashboard, Movies, Watchlist, Profile |
| **Guest** | `/browse` | Limited movie browsing |
| **Login** | `/` | Authentication entry point |

---

## 📸 Screenshots

### 🔑 Authentication

![Login Page](images/login_page.png)

*Secure login page with username/password authentication and role-based redirection.*

---

### 👨‍💼 Admin Dashboard

#### Overview & Analytics
![Admin Dashboard](images/Admin/admin_dashboard.png)

*Main admin dashboard showing key metrics: total users, movies, subscriptions, and real-time analytics.*

#### Movies Management
![Admin Movies Management](images/Admin/admin_movies_management.png)

*CRUD interface for managing movie catalog with pagination, filtering, and inline editing.*

#### Users Management
![Admin Users Management](images/Admin/admin_users_management.png)

*User administration panel with country distribution analytics and subscription tracking.*

#### Subscriptions & Payments
![Admin Subscriptions Management](images/Admin/admin_subscriptions_management.png)

*Subscription and payment tracking dashboard with plan distribution and revenue analytics.*

#### Data Studio (Dynamic CRUD)
![Admin Data Studio Add](images/Admin/admin_studio_add.png)

*Dynamic CRUD tool for adding new documents to any collection with JSON validation.*

![Admin Data Studio Manage](images/Admin/admin_studio_manage.png)

*Data Studio document management with search, filter, update, and delete capabilities.*

#### Analytics & Performance
![Admin Performance Analytics](images/Admin/admin_performance.png)

*Performance dashboard showing system metrics, query analytics, and database statistics.*

#### Admin Profile
![Admin Profile](images/Admin/admin_profile.png)

*Admin user profile with account settings and activity logs.*

---

### 👤 User Dashboard

#### Main Dashboard
![User Dashboard](images/User/user_dashboard.png)

*Personalized user dashboard with subscription info, statistics, preferences, and recent activity.*

#### Movies Section
![User Movies](images/User/user_movies.png)

*Browse movies with ratings, year filters, and quick add-to-watchlist functionality.*

#### Watchlist
![User Watchlist](images/User/user_watchlist.png)

*Manage saved movies with details, ratings, and remove options.*

#### User Profile
![User Profile](images/User/user_profile.png)

*User profile management with account info, subscription plan, and preferences.*

#### Subscription & Statistics
![User Profile & Subscription](images/User/user_profile_subscription.png)

*Subscription plan details with monthly billing information and renewal dates.*

![User Statistics](images/User/user_statistics.png)

*Engagement metrics: movies watched, ratings submitted, hours watched, reviews written.*

#### Activity Tracking
![User Activity](images/User/user_activity.png)

*Recent user activities including ratings, reviews, and watch history.*

---

### 📐 Database Schema
![Database Schema](images/database_schema.png)

*Complete MongoDB collection schema diagram showing relationships and data structure.*

---

## 🧩 Modules

### Module 1: Authentication & Authorization
**Features:**
- Secure login and registration
- Password hashing using bcrypt with salted hashes
- Session-based authentication
- CSRF protection meta tokens
- Role-based navigation and access control

**Key Implementation:**
```python
# Password hashing
from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash(password)
is_valid = check_password_hash(password_hash, password)
```

### Module 2: Admin Dashboard
**Features:**
- Real-time statistics (users, movies, subscriptions)
- Rating analytics and genre distribution
- Revenue charts and trending movies
- Aggregation pipelines for insights

**Example Aggregation Pipeline:**
```python
pipeline = [
    {"$group": {"_id": "$genre", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 5}
]
results = db.movies.aggregate(pipeline)
```

### Module 3: Movies Module
**Features:**
- Full CRUD operations
- Pagination and sampling
- Chart visualization (movies by year, rating distribution)
- Advanced filtering and search

### Module 4: Users Module
**Features:**
- Admin-only paginated user list
- Country distribution visualization
- User activity tracking
- Subscription status monitoring

### Module 5: Subscriptions & Payments
**Features:**
- Active subscription tracking
- Subscription plan distribution
- Payment history with status
- Revenue analytics

### Module 6: Data Studio (Dynamic CRUD)
**Features:**
- Dynamic CRUD for all collections
- MongoDB Views support (read-only)
- JSON editor for insert/update operations
- Pagination for large datasets
- Search and filtering capabilities

### Module 7: User Dashboard
**Features:**
- Personalized movie recommendations
- Watchlist management
- Movie ratings with optimistic locking
- Engagement score calculation
- Activity history

---

## 💡 Technical Highlights

### 🔄 Concurrency Control

**Optimistic Locking:**
```python
# Version field prevents conflicting updates
update = {
    "$inc": {"version": 1},
    "$set": {"score": new_score}
}
result = db.ratings.update_one(
    {"_id": rating_id, "version": current_version},
    update
)
```

**Pessimistic Locking:**
```python
# Resource locks collection prevents concurrent access
lock = {
    "_id": f"{resource_type}:{resource_id}",
    "locked_by": user_id,
    "locked_at": datetime.now()
}
db.resource_locks.insert_one(lock)
```

### 💬 Transactions
Multi-document transactions ensure ACID properties across collections:
```python
from pymongo import HAVE_ASYNC
session = client.start_session()

with session.start_transaction():
    db.users.update_one({"_id": user_id}, {"$inc": {"balance": -amount}})
    db.subscriptions.insert_one(subscription_data)
```

### ✔️ JSON Schema Validation
```javascript
{
  "bsonType": "object",
  "required": ["title", "year", "genre"],
  "properties": {
    "title": {"bsonType": "string"},
    "year": {"bsonType": "int", "minimum": 1900, "maximum": 2100},
    "genre": {"bsonType": "array", "items": {"bsonType": "string"}}
  }
}
```

### 🛡️ Security Measures
- **Input Validation**: All inputs validated before database queries
- **Parameterized Queries**: PyMongo's query interface prevents injection
- **Password Hashing**: Werkzeug's bcrypt-based hashing with salts
- **CSRF Protection**: Meta tokens in forms
- **Session Security**: Secure session cookies with httponly flags
- **NoSQL Injection Prevention**: Type checking and schema validation

### 📊 Aggregation Pipelines
Real-time analytics through MongoDB aggregation:
```python
pipeline = [
    {"$match": {"status": "completed"}},
    {"$group": {
        "_id": "$user_id",
        "total_spent": {"$sum": "$amount"},
        "transaction_count": {"$sum": 1}
    }},
    {"$sort": {"total_spent": -1}},
    {"$limit": 10}
]
top_users = list(db.subscriptions.aggregate(pipeline))
```

---

## ⚠️ Limitations

### 1. **No Sharding**
- Horizontal scaling through sharding was not implemented as per course requirements
- Limits the system's ability to distribute data across multiple nodes
- Suitable for academic purposes and small-scale deployments

### 2. **Limited Concurrency Simulation**
- Concurrency control demonstrations (locking, transactions) are simulated at the application level
- Not tested at large scale due to resource constraints
- Real-world production would require additional load testing

### 3. **MongoDB Atlas Free Tier**
- Storage and query limitations on free tier
- No advanced replication or backup features
- Suitable for development and demonstration purposes

### 4. **Single-Instance Deployment**
- Entire application runs on a single Flask instance
- Not designed for high-availability or failover scenarios
- Intended for academic demonstration rather than production use

---

## 👥 Project Stakeholders

| Stakeholder | Role | Responsibilities |
|------------|------|-----------------|
| **Student/Developer** | Project Creator | Design, implement, test system |
| **Instructor** | Course Supervisor | Provide requirements, evaluate project |
| **Admin Users** | System Administrator | Manage data, monitor analytics, CRUD operations |
| **Regular Users** | Content Consumers | Browse movies, rate content, manage watchlist |
| **Guests** | Limited Users | Read-only access to public content |

---

## 📚 Learning Outcomes

This project demonstrates proficiency in:

✅ **NoSQL Database Design**
- Flexible schema modeling with MongoDB
- Embedded vs. referenced documents
- Index optimization for performance

✅ **Advanced Database Concepts**
- CRUD operations at scale
- Aggregation pipelines for analytics
- Concurrency control (optimistic & pessimistic locking)
- Multi-document transactions
- JSON Schema validation

✅ **Web Application Development**
- RESTful API design
- Session management and authentication
- Role-based access control
- Security best practices

✅ **Data Visualization**
- Real-time dashboards with Chart.js
- Analytics and reporting
- User engagement metrics

✅ **Cloud Database Management**
- MongoDB Atlas integration
- Cloud deployment and configuration
- Scalability considerations

---

## 📝 License

This project is created for educational purposes as part of the Advanced Database Systems (ADS) course.

---

## 🤝 Contributing

This is an academic project. For improvements or feedback, please contact the course instructor.

---

## 📧 Contact

For questions or clarifications about this project, please refer to the course instructor or the project documentation.

---

**Last Updated:** December 2025  
**Course:** Advanced Database Systems (ADS)  
**Institution:** COMSATS University Islamabad

---

*"Demonstrating the power of NoSQL: Scalability, Flexibility, and Real-time Analytics"* 🚀
