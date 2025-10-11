# Quick Start Script for Learning Activity Management System
# Run this script to quickly start the application

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Learning Activity Management System - Quick Start" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Check if .env file exists
Write-Host ""
Write-Host "[2/5] Checking environment configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✓ .env file found" -ForegroundColor Green
    
    # Check if MongoDB URI is configured
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "MONGODB_URI=mongodb\+srv://.*\.mongodb\.net") {
        Write-Host "✓ MongoDB connection string configured" -ForegroundColor Green
    } else {
        Write-Host "⚠ MongoDB connection string needs configuration" -ForegroundColor Yellow
    }
    
    # Check if OpenAI API key is configured
    if ($envContent -match "OPENAI_API_KEY=sk-") {
        Write-Host "✓ OpenAI API key configured" -ForegroundColor Green
    } else {
        Write-Host "⚠ OpenAI API key needs configuration" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠ .env file not found. Creating from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created. Please edit it with your credentials." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "1. Edit .env file with your MongoDB and OpenAI credentials" -ForegroundColor White
    Write-Host "2. Run this script again" -ForegroundColor White
    exit 0
}

# Check if dependencies are installed
Write-Host ""
Write-Host "[3/5] Checking Python dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1
if ($pipList -match "Flask" -and $pipList -match "pymongo" -and $pipList -match "openai") {
    Write-Host "✓ Required packages are installed" -ForegroundColor Green
} else {
    Write-Host "⚠ Some packages are missing. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "✓ Dependencies installed" -ForegroundColor Green
}

# Initialize database
Write-Host ""
Write-Host "[4/5] Checking database initialization..." -ForegroundColor Yellow
$initDb = Read-Host "Do you want to initialize the database? (y/n) [Default: n]"
if ($initDb -eq "y" -or $initDb -eq "Y") {
    Write-Host "Initializing database..." -ForegroundColor Yellow
    python init_db.py
    
    $sampleData = Read-Host "Do you want to create sample data for testing? (y/n) [Default: n]"
    if ($sampleData -eq "y" -or $sampleData -eq "Y") {
        python init_db.py --sample
    }
} else {
    Write-Host "✓ Skipping database initialization" -ForegroundColor Green
}

# Start the application
Write-Host ""
Write-Host "[5/5] Starting the application..." -ForegroundColor Yellow
Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Application is starting..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Access the application at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "Default admin login: admin / admin123" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor White
Write-Host ""

python app.py
