@echo off
start cmd /k "cd backend && uvicorn main:app --reload"
start cmd /k "cd frontend && npm run dev"
echo Project started! Backend running on http://127.0.0.1:8000, Frontend on http://localhost:5173
