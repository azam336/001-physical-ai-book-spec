# Physical AI Book - Quick Start Guide

## ✅ System Status: WORKING

All features are now functional:
- ✅ User Registration & Login
- ✅ Session-based Authentication
- ✅ Protected Book Routes
- ✅ Email Verification System (ready to enable)
- ✅ Password Reset (ready to enable)
- ✅ Rate Limiting
- ✅ Secure Password Hashing

---

## 🚀 Daily Startup

### Start Both Servers

**Terminal 1 - Backend:**
```bash
cd backend
start-server.bat
```
*Keep this running!*

**Terminal 2 - Frontend:**
```bash
npm start
```
*Keep this running!*

### Access the App
- **Frontend:** http://localhost:3000/001-physical-ai-book-spec/
- **Backend API:** http://localhost:8000/api/health
- **Login Page:** http://localhost:3000/001-physical-ai-book-spec/login

---

## 🔑 How It Works

### Authentication Flow

1. **Register** → Creates account (email verification email ready but disabled in dev)
2. **Login** → Receives session token (stored in sessionStorage)
3. **Access Book** → Token validated, content accessible
4. **Refresh Page** → Token persists, stays logged in
5. **Close Browser** → Session cleared, must login again

### Protected Routes

All book/documentation pages require authentication:
- `/docs/*` - All documentation
- Book chapters
- Any Docusaurus content pages

**Automatic redirect:** Unauthenticated users → Login page → Back to intended page after login

---

## 📁 Important Files

### Configuration
- `backend/.env` - Environment variables (SMTP, database, secrets)
- `backend/requirements.txt` - Python dependencies
- `package.json` - Node.js dependencies

### Backend Core
- `backend/app/main.py` - API endpoints, rate limiting
- `backend/app/auth.py` - Password hashing, JWT tokens
- `backend/app/database.py` - Database models
- `backend/app/email_service.py` - Email sending (Gmail SMTP)
- `backend/app/token_manager.py` - Email/password reset tokens

### Frontend Core
- `src/contexts/AuthContext.jsx` - Authentication state (sessionStorage)
- `src/components/ProtectedRoute.jsx` - Route protection
- `src/pages/login.jsx` - Login page
- `src/pages/register.jsx` - Registration page
- `src/theme/DocItem/Layout/index.js` - Wraps docs with auth

---

## 🛠️ Common Tasks

### Add New Users (Backend)
```python
# Run Python in backend with venv activated
from app.database import SessionLocal, User
from app.auth import hash_password

db = SessionLocal()
user = User(
    full_name="John Doe",
    email="john@example.com",
    password_hash=hash_password("password123"),
    email_verified=True
)
db.add(user)
db.commit()
```

### Check Database
```bash
cd backend
.venv\Scripts\activate
python
>>> from app.database import SessionLocal, User
>>> db = SessionLocal()
>>> users = db.query(User).all()
>>> for u in users:
...     print(f"{u.email} - Verified: {u.email_verified}")
```

### Clear All Sessions (Force Re-login)
```bash
cd backend
.venv\Scripts\activate
python
>>> from app.database import SessionLocal, Session
>>> db = SessionLocal()
>>> db.query(Session).delete()
>>> db.commit()
```

### Enable Email Verification

1. Get Gmail App Password:
   - https://myaccount.google.com/apppasswords
   - Enable 2FA first
   - Create app password

2. Edit `backend/.env`:
   ```bash
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your-email@gmail.com
   SMTP_PASSWORD=your-16-char-app-password
   FROM_EMAIL=noreply@physicalaibook.com
   ```

3. Restart backend
4. Registration now sends verification emails ✅

---

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:8000/api/health
```
**Expected:** `{"status":"ok","message":"Physical AI Book Assistant is running"}`

### Test Registration
```bash
cd backend
.venv\Scripts\activate
python test-registration.py
```

### Test Login Flow
1. Go to login page
2. Try wrong password → Error shown
3. Try correct password → Logged in
4. Navigate to `/docs/intro` → Accessible
5. Logout → Redirected to login
6. Try `/docs/intro` → Redirected to login

---

## 🔒 Security Features

### Implemented
- ✅ **Session-based auth** - Token cleared when browser closes
- ✅ **Password hashing** - bcrypt with salt
- ✅ **Rate limiting** - Prevents brute force (5 reg/hour, 10 login/min)
- ✅ **CORS protection** - Only localhost:3000 allowed
- ✅ **Input validation** - Email, password strength checks
- ✅ **SQL injection protection** - SQLAlchemy ORM
- ✅ **Token expiration** - Verification (24h), Reset (1h)

### Session Storage Keys
- `auth_token` - JWT authentication token
- `auth_redirect` - URL to redirect after login

Both cleared on:
- Logout
- Browser/tab close
- Token expiration

---

## 📊 Database Schema

### Tables

**users**
- id (UUID)
- full_name
- email (unique)
- password_hash
- is_active
- email_verified
- email_verified_at
- created_at
- last_login

**sessions**
- id (UUID)
- user_id (FK)
- token (unique)
- expires_at
- created_at

**email_verification_tokens**
- id (UUID)
- user_id
- token (unique)
- expires_at
- created_at
- used_at

**password_reset_tokens**
- id (UUID)
- user_id
- token (unique)
- expires_at
- created_at
- used_at

**conversations** (chatbot)
- id
- session_id
- user_message
- assistant_message
- context_used
- created_at

---

## 🐛 Troubleshooting

### "Failed to fetch" Error
**Problem:** Backend not running
**Solution:** Start backend with `start-server.bat`

### "Creating Account..." Hangs
**Problem:** SMTP timeout
**Solution:** SMTP credentials should be commented out in `.env`

### bcrypt Version Error
**Problem:** Incompatible bcrypt 5.x
**Solution:** Run `backend/fix-bcrypt.bat`

### Can't Access Book Pages
**Problem:** Not authenticated
**Solution:** Login first at `/login`

### Session Lost on Refresh
**Problem:** Backend not responding
**Solution:** Check backend logs, restart if needed

### Rate Limit Errors
**Problem:** Too many requests
**Solution:** Wait 1 hour (register) or 1 minute (login)

---

## 📚 Documentation Files

Created during implementation:
- `IMPLEMENTATION_SUMMARY.md` - Complete feature implementation
- `AUTH_IMPLEMENTATION.md` - Session-based auth details
- `TROUBLESHOOTING.md` - "Failed to fetch" error guide
- `BCRYPT_FIX.md` - bcrypt compatibility fix
- `QUICK_START.md` - This file

---

## 🎯 Production Deployment Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` in `.env` to random 32+ characters
- [ ] Update CORS to allow production domain
- [ ] Configure real SMTP credentials
- [ ] Set `FRONTEND_URL` to production domain
- [ ] Enable HTTPS
- [ ] Set up proper database backups
- [ ] Configure Redis for rate limiting (multi-server)
- [ ] Add monitoring/logging
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Review and test all security features
- [ ] Enable email verification requirement
- [ ] Set up proper session management

---

## 🚀 Next Steps (Optional Enhancements)

### Features Ready to Enable
1. **Email Verification** - Just add SMTP credentials
2. **Password Reset** - Already implemented, needs SMTP
3. **Resend Verification Email** - Endpoint ready

### Potential Additions
- [ ] Remember me checkbox (localStorage option)
- [ ] Session timeout warning
- [ ] Logout button in navigation
- [ ] User profile page
- [ ] Change password functionality
- [ ] Admin dashboard
- [ ] User management
- [ ] 2FA/MFA support
- [ ] OAuth login (Google, GitHub)
- [ ] Password history (prevent reuse)

---

## 📞 Quick Commands Reference

```bash
# Start backend
cd backend && start-server.bat

# Start frontend
npm start

# Test backend
cd backend && .venv\Scripts\activate && python test-connection.py

# Test registration
cd backend && .venv\Scripts\activate && python test-registration.py

# Fix bcrypt
cd backend && fix-bcrypt.bat

# View backend logs
# (Just watch the terminal where backend is running)

# Stop servers
# Press Ctrl+C in each terminal
```

---

## ✅ System Health Check

Run these to verify everything works:

```bash
# 1. Backend running?
curl http://localhost:8000/api/health

# 2. Frontend running?
# Open: http://localhost:3000/001-physical-ai-book-spec/

# 3. Can register?
# Open: http://localhost:3000/001-physical-ai-book-spec/register

# 4. Can login?
# Open: http://localhost:3000/001-physical-ai-book-spec/login

# 5. Book protected?
# Try: http://localhost:3000/001-physical-ai-book-spec/docs/intro
# Should redirect to login if not authenticated
```

---

**Everything is set up and working!** 🎉

Enjoy your secure, authenticated Physical AI Book application!
