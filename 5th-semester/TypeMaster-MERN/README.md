# 🚀 TypeMaster - Master Your Typing Speed

<div align="center">

![TypeMaster](./images/01_index.png)

**The Ultimate Full-Stack Typing Test Application | MERN Stack**

A modern, feature-rich typing speed test platform with real-time analytics, competitive leaderboards, and detailed progress tracking.

[![Made with Node.js](https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white)](https://nodejs.org/)
[![Express.js](https://img.shields.io/badge/Express.js-000000?style=flat-square&logo=express&logoColor=white)](https://expressjs.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-13aa52?style=flat-square&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Vanilla JS](https://img.shields.io/badge/Vanilla%20JS-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

[Features](#features) • [Tech Stack](#tech-stack) • [Installation](#installation) • [Usage](#usage) • [API Documentation](#api-documentation) • [Known Issues](#known-issues)

</div>

---

## 📸 Screenshots

### Landing Page & Authentication
<div align="center">
<table>
<tr>
<td><img src="./images/01_index.png" alt="Landing Page" width="300"/></td>
<td><img src="./images/02_login.png" alt="Login" width="300"/></td>
<td><img src="./images/03_register.png" alt="Register" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Landing Page</b></td>
<td align="center"><b>Login</b></td>
<td align="center"><b>Registration</b></td>
</tr>
</table>
</div>

### Typing Test Experience
<div align="center">
<table>
<tr>
<td><img src="./images/04_dashboard.png" alt="Dashboard" width="300"/></td>
<td><img src="./images/05_typing test.png" alt="Typing Test Ready" width="300"/></td>
<td><img src="./images/06_typing test - running.png" alt="Typing Test Running" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Dashboard & Stats</b></td>
<td align="center"><b>Test Ready</b></td>
<td align="center"><b>Test in Progress</b></td>
</tr>
</table>
</div>

### Leaderboards & User Profile
<div align="center">
<table>
<tr>
<td><img src="./images/07_leaderboard.png" alt="Global Leaderboard" width="300"/></td>
<td><img src="./images/08_profile - edit.png" alt="Profile Edit" width="300"/></td>
<td><img src="./images/09_profile - overview.png" alt="Profile Overview" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Global Leaderboard</b></td>
<td align="center"><b>Profile Settings</b></td>
<td align="center"><b>Profile Overview</b></td>
</tr>
</table>
</div>

### Admin & Additional Features
<div align="center">
<table>
<tr>
<td><img src="./images/10_profile - settings.png" alt="Account Settings" width="300"/></td>
<td><img src="./images/11_profile - test history.png" alt="Test History" width="300"/></td>
<td><img src="./images/12_admin.png" alt="Admin Panel" width="300"/></td>
</tr>
<tr>
<td align="center"><b>Account Settings</b></td>
<td align="center"><b>Test History</b></td>
<td align="center"><b>Admin Panel</b></td>
</tr>
</table>
</div>

---

## ✨ Features

### 🎯 Core Typing Features
- **Customizable Tests**: Choose difficulty (Easy, Medium, Hard) and duration (30s, 60s, 120s)
- **Real-time Statistics**: Live WPM, Accuracy, Mistakes, and Time tracking
- **Practice Mode**: Test without saving to leaderboard
- **Paste & Cut Prevention**: Ensures honest testing without shortcuts
- **Auto-focus**: Click anywhere to focus the typing area
- **Progress Visualization**: Real-time progress bar showing test completion

### 📊 Analytics & Tracking
- **Personal Dashboard**: View total tests, average WPM, best score, and total time spent
- **Progress Charts**: Visual representation of WPM improvement over time
- **Improvement Percentage**: Track your progress between first and last attempts
- **Test History**: Complete record of all typing tests with detailed metrics
- **Performance Metrics**: WPM, Accuracy, Time Taken, and Mistakes for each test

### 🏆 Competitive Features
- **Global Leaderboard**: Rank against other users worldwide
- **Filtered Rankings**: Filter by difficulty, duration, and time period (Today, Week, Month, All-time)
- **Personal Ranking**: See your exact position on the leaderboard
- **Best Scores**: System tracks your best WPM and accuracy separately

### 👤 User Management
- **Secure Authentication**: JWT-based authentication with bcrypt password hashing
- **User Profiles**: Customize your name and view your statistics
- **Account Settings**: Change password and manage account preferences
- **Role-Based Access**: User and Admin roles with permission controls

### 🛠️ Admin Dashboard
- **Paragraph Management**: Add, edit, and manage typing test paragraphs
- **User Management**: View all registered users and their statistics
- **Test Analytics**: Access all user test results with detailed information
- **Activity Control**: Enable/disable paragraphs to manage test content

---

## 🏗️ Tech Stack

### Backend
- **Runtime**: Node.js
- **Framework**: Express.js (v5.2.1)
- **Database**: MongoDB with Mongoose ODM
- **Authentication**: JWT (JSON Web Tokens) with bcryptjs
- **Validation**: Express-validator
- **CORS**: Enabled for cross-origin requests

### Frontend
- **Languages**: HTML5, CSS3, Vanilla JavaScript (ES6+)
- **Styling**: Custom CSS with CSS variables for theming
- **Storage**: localStorage for token and user session management
- **Architecture**: Component-based with modular JavaScript

### Development Tools
- **Package Manager**: npm
- **Development Server**: Nodemon for hot-reload
- **Database Seeding**: Custom seed script with sample data
- **Environment Management**: dotenv for configuration

---

## 🚀 Installation & Setup

### Prerequisites
- **Node.js** (v14 or higher)
- **MongoDB** (v4.4 or higher) - Local or Atlas
- **npm** (comes with Node.js)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd TypeMaster\ -\ MERN
```

### Step 2: Setup Backend

#### 2.1 Navigate to Server Directory
```bash
cd server
```

#### 2.2 Install Dependencies
```bash
npm install
```

#### 2.3 Configure Environment Variables
Create a `.env` file in the `server` directory using `.env.example` as reference:

```env
# Server Configuration
PORT=5000
NODE_ENV=development

# Database Configuration
MONGO_URI=mongodb://127.0.0.1:27017/typemaster
# For MongoDB Atlas (cloud):
# MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/typemaster

# Authentication
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production
JWT_EXPIRES_IN=7d

# Frontend URL (for CORS)
CLIENT_URL=http://localhost:5173
# For production, update to your frontend URL:
# CLIENT_URL=https://yourdomain.com
```

#### 2.4 Seed Initial Data (Optional)
```bash
npm run seed
```

This creates:
- **Admin User**: `admin@typemaster.com` / `Admin1234`
- **Demo User**: `demo@example.com` / `Demo1234`
- **15 Typing Paragraphs**: Easy, Medium, and Hard difficulties

#### 2.5 Start Backend Server
```bash
# Development (with hot-reload)
npm run dev

# Production
npm start
```

Server will run on `http://localhost:5000`

### Step 3: Setup Frontend

The frontend is served as static HTML files. You can serve them in multiple ways:

#### Option A: Using Python (Simple HTTP Server)
```bash
# From project root
python -m http.server 5173
# or Python 3
python3 -m http.server 5173
```

#### Option B: Using Node.js http-server
```bash
npm install -g http-server
http-server . -p 5173
```

#### Option C: Using VS Code Live Server Extension
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

#### Option D: Docker (Full Stack)
```bash
# If you have Docker setup
docker-compose up
```

### Step 4: Access the Application

Open your browser and navigate to:
- **Frontend**: `http://localhost:5173`
- **API Health Check**: `http://localhost:5000/api/health`

---

## 📖 Usage Guide

### For Users

#### 1. Register an Account
- Navigate to the Registration page
- Enter name, email, and password (minimum 8 characters)
- Confirm registration and automatically logged in

#### 2. Take a Typing Test
- Go to "Typing Test" page
- Select difficulty level (Easy/Medium/Hard)
- Choose test duration (30s/60s/120s)
- Click "Start" and begin typing
- Test stops automatically when time runs out
- View detailed results and performance metrics

#### 3. Track Progress
- View Dashboard with personal statistics
- See progress charts showing WPM improvement
- Check total time spent typing and improvement percentage
- Review complete test history

#### 4. Compete on Leaderboard
- View Global Leaderboard with top performers
- Filter by difficulty, duration, and time period
- See your personal ranking
- Compare with other users

#### 5. Manage Profile
- View and edit your display name
- Check account settings and preferences
- Review all your test results
- Change password and security settings

### For Administrators

#### 1. Access Admin Panel
- Login with admin account
- Navigate to Admin Dashboard (if user role is 'admin')

#### 2. Manage Content
- **Add Paragraphs**: Create new typing test paragraphs
- **Edit Paragraphs**: Modify existing paragraphs
- **Disable Paragraphs**: Remove paragraphs from rotation

#### 3. Monitor Activity
- View all registered users
- Check user test results
- Access system-wide analytics
- Monitor platform activity

---

## 🔌 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Health Check
```
GET /health
```

### Authentication Endpoints

#### Register User
```
POST /auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response: { token, user }
```

#### Login User
```
POST /auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "SecurePass123"
}

Response: { token, user }
```

#### Get Current User
```
GET /auth/me
Authorization: Bearer <token>

Response: { user }
```

### Typing Endpoints

#### Get Random Paragraph
```
GET /typing/paragraphs/random?difficulty=medium
Response: { paragraph }
```

#### Get All Paragraphs
```
GET /typing/paragraphs?difficulty=easy
Response: { count, paragraphs }
```

### Results Endpoints

#### Submit Test Result
```
POST /results
Authorization: Bearer <token>
Content-Type: application/json

{
  "paragraph": "paragraph_id",
  "difficulty": "medium",
  "duration": 60,
  "wpm": 75,
  "accuracy": 95.5,
  "mistakes": 5,
  "charsTyped": 450,
  "timeTaken": 60
}

Response: { result }
```

#### Get My Results
```
GET /results/me
Authorization: Bearer <token>
Response: { count, results }
```

#### Get My Stats
```
GET /results/me/stats
Authorization: Bearer <token>
Response: { totalTests, averageWpm, bestWpm, averageAccuracy, improvementPercentage, recentTests }
```

### Leaderboard Endpoints

#### Get Global Leaderboard
```
GET /leaderboard?difficulty=medium&duration=60&time=week
Response: { count, leaderboard }

Query Parameters:
- difficulty: easy | medium | hard (optional)
- duration: 30 | 60 | 120 (optional)
- time: today | week | month | all (default: all)
```

#### Get My Leaderboard Rank
```
GET /leaderboard/me
Authorization: Bearer <token>
Response: { rank, bestWpm, bestAccuracy, testsTaken }
```

### User Endpoints

#### Get Profile
```
GET /users/profile
Authorization: Bearer <token>
Response: { user, stats }
```

#### Update Profile
```
PUT /users/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Name"
}

Response: { user }
```

### Admin Endpoints (Requires Admin Role)

#### Get All Users
```
GET /admin/users
Authorization: Bearer <admin-token>
Response: { count, users }
```

#### Get All Results
```
GET /admin/results
Authorization: Bearer <admin-token>
Response: { count, results }
```

#### Get All Paragraphs
```
GET /admin/paragraphs
Authorization: Bearer <admin-token>
Response: { count, paragraphs }
```

#### Create Paragraph
```
POST /admin/paragraphs
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "text": "Paragraph content here",
  "difficulty": "medium"
}

Response: { paragraph }
```

#### Update Paragraph
```
PUT /admin/paragraphs/:id
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "text": "Updated content",
  "difficulty": "hard",
  "isActive": true
}

Response: { paragraph }
```

#### Disable Paragraph
```
DELETE /admin/paragraphs/:id
Authorization: Bearer <admin-token>
Response: { paragraph }
```

---

## 📁 Project Structure

```
TypeMaster - MERN/
├── server/                          # Backend Node.js application
│   ├── src/
│   │   ├── config/
│   │   │   └── db.js               # MongoDB connection setup
│   │   ├── controllers/             # Business logic handlers
│   │   │   ├── authController.js
│   │   │   ├── typingController.js
│   │   │   ├── resultController.js
│   │   │   ├── leaderboardController.js
│   │   │   ├── userController.js
│   │   │   └── adminController.js
│   │   ├── models/                  # Mongoose schemas
│   │   │   ├── User.js
│   │   │   ├── TestResult.js
│   │   │   └── TypingParagraph.js
│   │   ├── routes/                  # API route handlers
│   │   │   ├── authRoutes.js
│   │   │   ├── typingRoutes.js
│   │   │   ├── resultRoutes.js
│   │   │   ├── leaderboardRoutes.js
│   │   │   ├── userRoutes.js
│   │   │   └── adminRoutes.js
│   │   ├── middleware/              # Express middleware
│   │   │   ├── authMiddleware.js
│   │   │   ├── roleMiddleware.js
│   │   │   ├── errorHandler.js
│   │   │   └── validateRequest.js
│   │   ├── validators/              # Input validation rules
│   │   │   ├── adminValidators.js
│   │   │   ├── resultValidators.js
│   │   │   ├── typingValidators.js
│   │   │   └── userValidators.js
│   │   ├── services/                # Utility services
│   │   │   └── statsService.js
│   │   ├── seed/
│   │   │   └── seedParagraphs.js   # Database seeding script
│   │   ├── app.js                   # Express app configuration
│   │   └── server.js                # Server entry point
│   ├── .env.example                 # Environment variables template
│   └── package.json                 # Dependencies
├── assets/
│   ├── css/                         # Stylesheets
│   │   ├── variables.css            # CSS custom properties
│   │   ├── main.css                 # Global styles
│   │   ├── components.css           # Component styles
│   │   └── pages/
│   │       ├── typing.css
│   │       ├── login.css
│   │       ├── dashboard.css
│   │       ├── leaderboard.css
│   │       └── profile.css
│   └── js/                          # Frontend JavaScript
│       ├── api.js                   # API client
│       ├── auth.js                  # Authentication manager
│       ├── typing.js                # Typing test logic
│       ├── dashboard.js             # Dashboard functionality
│       ├── leaderboard.js           # Leaderboard logic
│       ├── profile.js               # Profile management
│       ├── components.js            # Component utilities
│       ├── admin.js                 # Admin panel logic
│       └── utils.js                 # Helper functions
├── components/                      # Reusable HTML components
│   ├── navbar.html
│   └── footer.html
├── images/                          # Screenshot assets
│   └── [12 UI screenshots]
├── index.html                       # Landing page
├── login.html                       # Login page
├── register.html                    # Registration page
├── dashboard.html                   # User dashboard
├── typing-test.html                 # Typing test page
├── leaderboard.html                 # Leaderboard page
├── profile.html                     # User profile page
├── admin.html                       # Admin panel
└── README.md                        # This file
```

---

## 🔐 Security Features

- **Password Hashing**: bcryptjs with salt rounds for secure password storage
- **JWT Authentication**: Stateless authentication with configurable expiration
- **CORS Protection**: Controlled cross-origin requests
- **Input Validation**: Server-side validation using express-validator
- **Authorization Middleware**: Role-based access control (User/Admin)
- **Secure Headers**: Best practices for HTTP headers
- **Password Selection**: Passwords not returned in API responses

---

## 🐛 Known Issues & Improvements Needed

### ✅ Recently Fixed Issues
The following issues have been successfully resolved:
- ✅ ISSUE-3: CORS Configuration - Now uses `CLIENT_URL` environment variable
- ✅ ISSUE-4: Hardcoded API URL - Now dynamically detects localhost vs production
- ✅ ISSUE-5: Rate Limiting - Added `express-rate-limit` on auth endpoints
- ✅ ISSUE-6: Error Handling - Enhanced with user-friendly messages and loading states
- ✅ ISSUE-8: Loading States - Added global loading spinner with animations
- ✅ ISSUE-9: Rate Limiting - Fully implemented with 5 requests per 15 minutes
- ✅ ISSUE-10: Admin Dashboard - Complete CRUD functionality for paragraph management

### Remaining Improvements (Optional)

**Low Priority - Nice to Have**:

1. **Input Sanitization**
   - Issue: Potential XSS in user-generated content (paragraph text)
   - Current: Basic text rendering, no HTML execution risk
   - Recommendation: Add DOMPurify for additional safety
   ```bash
   npm install dompurify
   ```

2. **Hardcoded Demo Credentials in Seed File**
   - Issue: Demo credentials visible in seed script
   - Current: Works as intended for development/testing
   - Recommendation: Move to environment variables for production
   ```env
   SEED_ADMIN_EMAIL=admin@typemaster.com
   SEED_ADMIN_PASSWORD=Admin1234
   ```

3. **Advanced Features (Future Roadmap)**
   - Social features (friend comparison, challenges)
   - Advanced analytics and insights
   - Mobile-responsive improvements
   - Multiplayer competitions
   - AI-powered recommendations

---

## 📊 Performance Considerations

- **Database Indexing**: Recommended indexes on `User.email`, `TestResult.user`, `TestResult.createdAt`
- **Pagination**: Consider implementing pagination for leaderboard with large user bases
- **Caching**: Implement Redis caching for leaderboard queries and paragraph lists
- **Connection Pooling**: MongoDB connection pool configured automatically by Mongoose
- **Frontend Optimization**: Consider lazy loading and code splitting for large deployments

---

## 🚀 Deployment Guide

### Deploy Backend (Heroku Example)
```bash
# 1. Create Heroku app
heroku create typemaster-app

# 2. Set environment variables
heroku config:set JWT_SECRET=your_secret_key
heroku config:set MONGO_URI=mongodb+srv://user:pass@cluster.mongodb.net/typemaster
heroku config:set NODE_ENV=production
heroku config:set CLIENT_URL=https://yourdomain.com

# 3. Deploy
git push heroku main
```

### Deploy Frontend (Netlify/Vercel Example)
```bash
# 1. Build a production-ready version
# 2. Push to Git repository
# 3. Connect to Netlify/Vercel
# 4. Update CLIENT_URL in backend to match frontend domain
```

### Environment Variables for Production
```env
NODE_ENV=production
PORT=5000
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/typemaster
JWT_SECRET=your_long_random_secret_key_minimum_32_characters
JWT_EXPIRES_IN=7d
CLIENT_URL=https://yourdomain.com
```

---

## 📝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/AmazingFeature`
3. Commit changes: `git commit -m 'Add AmazingFeature'`
4. Push to branch: `git push origin feature/AmazingFeature`
5. Open a Pull Request

### Development Guidelines
- Write clear commit messages
- Test features before submitting PRs
- Update documentation for new features
- Follow existing code style and structure

---

## 🧪 Testing

Currently, the project uses manual testing. For future improvements:

```bash
# Backend testing (to be implemented)
npm install --save-dev jest supertest

# Frontend testing (to be implemented)
npm install --save-dev vitest @testing-library/dom
```

---

## 📞 Support & Contact

- **Issues**: Create an issue on GitHub for bugs or feature requests
- **Documentation**: See inline code comments and this README

---

## 📄 License

This project is licensed under the ISC License - see the `package.json` file for details.

---

## 🙏 Acknowledgments

- **MongoDB**: Powerful NoSQL database
- **Express.js**: Minimal and flexible web framework
- **Mongoose**: Elegant MongoDB object modeling
- **JWT**: Secure token-based authentication
- All contributors and users of this project

---

## 📊 Metrics & Statistics

### Project Stats
- **Lines of Code**: ~3000+
- **Number of API Endpoints**: 20+
- **Database Models**: 3 (User, TestResult, TypingParagraph)
- **Frontend Pages**: 8 (Landing, Login, Register, Dashboard, Test, Leaderboard, Profile, Admin)
- **Reusable Components**: 2 (Navbar, Footer)

### Feature Completeness
- ✅ User Authentication
- ✅ Typing Test Engine
- ✅ Real-time Statistics
- ✅ Leaderboard System
- ✅ User Profiles
- ✅ Admin Dashboard
- ✅ Progress Tracking
- ⚠️ Advanced Analytics (Future)
- ⚠️ Social Features (Future)
- ⚠️ Mobile App (Future)

---

<div align="center">

**Made with ❤️ for typing enthusiasts**

⭐ If you find this project helpful, please give it a star on GitHub!

</div>
