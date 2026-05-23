# 🚀 TypeMaster - Quick Start Guide

Get TypeMaster up and running in **5 minutes**!

## Prerequisites
- Node.js (v14+)
- MongoDB (local or Atlas)
- Git

## 1️⃣ Clone & Install Backend

```bash
# Clone repository
git clone <repository-url>
cd TypeMaster\ -\ MERN

# Setup backend
cd server
npm install
```

## 2️⃣ Configure Environment

Create `server/.env`:

```env
PORT=5000
NODE_ENV=development
MONGO_URI=mongodb://127.0.0.1:27017/typemaster
JWT_SECRET=your_secret_key_here_minimum_32_chars
JWT_EXPIRES_IN=7d
CLIENT_URL=http://localhost:5173
```

### Using MongoDB Atlas (Cloud)?
```env
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/typemaster
```

## 3️⃣ Seed Database (Optional)

```bash
npm run seed
```

This creates:
- **Admin**: admin@typemaster.com / Admin1234
- **Demo**: demo@example.com / Demo1234
- **15 typing paragraphs** with different difficulties

## 4️⃣ Start Backend Server

```bash
# Development (with hot-reload)
npm run dev

# Production
npm start
```

✅ Server running on `http://localhost:5000`

## 5️⃣ Start Frontend (New Terminal)

From project root:

```bash
# Using Python (Recommended)
python -m http.server 5173

# Or Python 3
python3 -m http.server 5173

# Or Node http-server
npm install -g http-server
http-server . -p 5173
```

✅ Frontend available at `http://localhost:5173`

---

## 🧪 Test the Application

### 1. Visit Landing Page
- Open `http://localhost:5173` in your browser

### 2. Create Account
- Click "Sign Up"
- Enter: Name, Email, Password (8+ chars)
- Click "Register"

### 3. Or Login with Demo Account
- Email: `demo@example.com`
- Password: `Demo1234`

### 4. Take a Typing Test
- Click "Typing Test"
- Select difficulty and duration
- Click "Start" and type the paragraph
- View results when complete

### 5. Check Dashboard
- View your stats and progress
- See recent test history

### 6. View Leaderboard
- See global rankings
- Filter by difficulty, duration, and time period

### 7. Admin Features (Demo)
- Login with admin@typemaster.com / Admin1234
- Access Admin Panel
- Add/edit typing paragraphs

---

## 🔧 Troubleshooting

### Backend Won't Connect to MongoDB
```
Error: MongoDB connection failed
```

**Solutions**:
1. Ensure MongoDB is running:
   ```bash
   # Windows (if using MongoDB locally)
   net start MongoDB
   
   # Mac
   brew services start mongodb-community
   ```

2. Check MONGO_URI format
3. Verify connection string in `.env`

### CORS Error
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution**: 
- Ensure `CLIENT_URL=http://localhost:5173` in `.env`
- Restart backend server

### Port Already in Use
```
Error: listen EADDRINUSE :::5000
```

**Solution**:
```bash
# Kill process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9

# Or use different port
PORT=5001 npm run dev
```

### Frontend Files Not Loading
- Ensure you're in the project root directory
- Check that assets/ folder exists
- Verify http server is running

---

## 📊 API Health Check

```bash
# Check if API is running
curl http://localhost:5000/api/health
```

Expected response:
```json
{
  "success": true,
  "message": "TypeMaster API is healthy",
  "timestamp": "2026-05-09T..."
}
```

---

## 📱 Example API Calls

### Register User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

### Login User
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

Response will include a JWT token to use in authenticated requests.

### Get Random Paragraph
```bash
curl http://localhost:5000/api/typing/paragraphs/random?difficulty=medium
```

### Submit Test Result
```bash
curl -X POST http://localhost:5000/api/results \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "paragraph": "paragraph_id",
    "difficulty": "medium",
    "duration": 60,
    "wpm": 75,
    "accuracy": 95.5,
    "mistakes": 5,
    "charsTyped": 450,
    "timeTaken": 60
  }'
```

### Get Leaderboard
```bash
curl http://localhost:5000/api/leaderboard?difficulty=medium&time=week
```

---

## 🎯 Next Steps

1. ✅ Application is running
2. 📖 Read full [README.md](./README.md)
3. 🐛 Check [CODE_REVIEW_REPORT.md](./CODE_REVIEW_REPORT.md) for improvements
4. 🚀 Deploy to production
5. 📊 Monitor and scale

---

## 📚 Helpful Resources

- **MongoDB**: https://docs.mongodb.com/
- **Express.js**: https://expressjs.com/
- **JWT**: https://jwt.io/
- **Mongoose**: https://mongoosejs.com/

---

## 💡 Pro Tips

1. **Development Mode**: Use `npm run dev` to auto-reload on changes
2. **Database Visualization**: Use MongoDB Compass to view data
3. **API Testing**: Use Postman or Insomnia for API testing
4. **Logs**: Check browser console and server terminal for debugging
5. **Seed Frequently**: Use `npm run seed` to reset data during development

---

## ✅ You're Ready!

Your TypeMaster application is now running! 🎉

**Next**: Read the full README.md for comprehensive documentation.

Happy typing! 🚀
