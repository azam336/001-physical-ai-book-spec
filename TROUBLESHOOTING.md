# Troubleshooting Guide - "Failed to fetch" Error

## Problem

Getting "Failed to fetch" or "Cannot connect to server" error on login/register pages.

## Root Cause

The **backend API server is not running** on `http://localhost:8000`.

---

## Solution 1: Start Backend Server (Quick)

### Option A: Use Batch File (Windows - Easiest)

1. Navigate to the `backend` folder
2. Double-click `start-server.bat`
3. Wait for message: `Application startup complete`
4. Keep this window open while using the app

### Option B: Command Line

```bash
# Open terminal in backend folder
cd backend

# Activate virtual environment
.venv\Scripts\activate

# Start server
uvicorn app.main:app --reload
```

### Expected Output:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

---

## Solution 2: Verify Backend is Running

### Test Script (Automatic)

```bash
cd backend
.venv\Scripts\activate
python test-connection.py
```

### Expected Output:

```
============================================================
Testing Backend API Connection
============================================================

Test 1: Health Check Endpoint
GET http://localhost:8000/api/health
✓ SUCCESS - Backend is running!
  Response: {'status': 'ok', 'message': 'Physical AI Book Assistant is running'}

Test 2: CORS Configuration
✓ SUCCESS - CORS configured correctly
  Allow-Origin: http://localhost:3000

Test 3: Auth Endpoints
✓ /api/auth/register - EXISTS
✓ /api/auth/login - EXISTS
✓ /api/auth/logout - EXISTS
```

### Manual Test (Browser)

1. Open browser
2. Go to: `http://localhost:8000/api/health`
3. Should see: `{"status":"ok","message":"Physical AI Book Assistant is running"}`

---

## Common Issues & Fixes

### Issue 1: Port 8000 Already in Use

**Error:**
```
ERROR:    [Errno 10048] error while attempting to bind on address ('0.0.0.0', 8000):
only one usage of each socket address (protocol/network address/port) is normally permitted
```

**Solution:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or use different port
uvicorn app.main:app --reload --port 8001
```

If using different port, update frontend API URL in `src/contexts/AuthContext.jsx`:
```javascript
const API_URL = 'http://localhost:8001';  // Change 8000 to 8001
```

### Issue 2: Module Not Found Errors

**Error:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend
.venv\Scripts\activate
pip install -r requirements.txt
```

### Issue 3: Database Connection Error

**Error:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Solution:**
Check `backend/.env` has correct `NEON_DATABASE_URL`:
```bash
NEON_DATABASE_URL=postgresql://user:pass@host/db
```

### Issue 4: CORS Error (Different from Failed to Fetch)

**Error in Browser Console:**
```
Access to fetch at 'http://localhost:8000/api/auth/login' from origin 'http://localhost:3000'
has been blocked by CORS policy
```

**Solution:**
Verify CORS in `backend/app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 5: Frontend on Different Port

**If frontend runs on port other than 3000:**

1. Update CORS in `backend/app/main.py`:
   ```python
   allow_origins=["http://localhost:3001"],  # Change to your port
   ```

2. Restart backend server

---

## Complete Setup Checklist

- [ ] Backend virtual environment activated
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Backend `.env` file configured
- [ ] Database migration run (`python scripts/add_verification_tables.py`)
- [ ] Backend server running (`uvicorn app.main:app --reload`)
- [ ] Backend health check works (`http://localhost:8000/api/health`)
- [ ] Frontend running (`npm start`)
- [ ] Frontend on `http://localhost:3000`

---

## Step-by-Step: First Time Setup

### 1. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migration
python scripts/add_verification_tables.py

# Start server
uvicorn app.main:app --reload
```

Keep this terminal open!

### 2. Frontend Setup (New Terminal)

```bash
# Navigate to project root
cd D:\AgenticAI\HackThon1\001-physical-ai-book-spec

# Install dependencies (if not done)
npm install

# Start frontend
npm start
```

### 3. Verify Both Running

**Backend:**
- Terminal shows: `Application startup complete`
- Browser: `http://localhost:8000/api/health` returns JSON

**Frontend:**
- Terminal shows: `webpack compiled successfully`
- Browser: `http://localhost:3000/001-physical-ai-book-spec/` loads

### 4. Test Login

1. Go to: `http://localhost:3000/001-physical-ai-book-spec/login`
2. Enter credentials
3. Should NOT see "Failed to fetch"
4. Should see either success or "Invalid email or password"

---

## Quick Diagnostic Commands

### Check if Backend is Running

```bash
# Windows
netstat -ano | findstr :8000

# Should show LISTENING on port 8000
```

### Check Backend Logs

Look at the terminal where `uvicorn` is running:
- `200 POST /api/auth/login` = Success
- `401 POST /api/auth/login` = Wrong credentials
- `500 POST /api/auth/login` = Server error

### Check Browser Console

1. Open browser DevTools (F12)
2. Go to Console tab
3. Try to login
4. Look for errors:
   - `Failed to fetch` = Backend not running
   - `CORS error` = CORS misconfigured
   - `401 Unauthorized` = Wrong credentials (backend is working!)

---

## Still Having Issues?

### Collect Debug Info

Run these commands and share the output:

```bash
# 1. Check if backend is running
netstat -ano | findstr :8000

# 2. Test health endpoint
curl http://localhost:8000/api/health

# 3. Test login endpoint
curl -X POST http://localhost:8000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"

# 4. Check Python version
python --version

# 5. Check if in virtual environment
where python
```

### Check These Files

1. `backend/.env` - Database URL configured?
2. `backend/app/main.py` - CORS settings correct?
3. `src/contexts/AuthContext.jsx` - API_URL correct?

---

## Success Indicators

✅ **Backend Running:**
- Terminal shows: `Application startup complete`
- `http://localhost:8000/api/health` returns JSON
- `netstat -ano | findstr :8000` shows LISTENING

✅ **Frontend Running:**
- Browser shows app at `http://localhost:3000`
- No build errors in terminal

✅ **Connection Working:**
- Login page doesn't show "Failed to fetch"
- Browser console shows `POST http://localhost:8000/api/auth/login 401` (credentials wrong but connection works!)
- Or shows `200` (login successful!)

---

## Production Deployment Notes

When deploying to production:

1. Update `src/contexts/AuthContext.jsx`:
   ```javascript
   const getApiUrl = () => {
     if (typeof window !== 'undefined') {
       // Use environment variable or same domain in production
       return window.location.origin + '/api';
     }
     return 'http://localhost:8000';
   };
   ```

2. Update CORS in `backend/app/main.py`:
   ```python
   allow_origins=[
       "http://localhost:3000",  # Development
       "https://your-domain.com"  # Production
   ],
   ```

3. Use environment variables for sensitive data
4. Enable HTTPS in production
