@echo off
echo 🌱 Starting Plant Disease Classifier in development mode...
echo This will start both React frontend and Flask backend
echo React will be available at: http://localhost:3000
echo Flask API will be available at: http://localhost:5000
echo.
echo Press Ctrl+C to stop both servers
echo.

REM Check if package.json exists
if not exist "package.json" (
    echo ❌ package.json not found. Please run this from the project root directory.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed. Please install Node.js first.
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Installing React dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo 🚀 Starting Flask backend on http://localhost:5000
start "Flask Backend" python app.py

REM Give Flask time to start
timeout /t 3 /nobreak >nul

echo ⚛️ Starting React development server on http://localhost:3000
npm start
