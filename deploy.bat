@echo off
echo 🚀 Nusify Deployment Script
echo ==========================

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not initialized. Running git init...
    git init
)

REM Check if remote origin exists
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ❌ No remote origin found.
    echo Please add your GitHub repository as origin:
    echo git remote add origin https://github.com/YOUR_USERNAME/nusify.git
    echo.
    set /p repo_url="Enter your GitHub repository URL: "
    if not "%repo_url%"=="" (
        git remote add origin "%repo_url%"
        echo ✅ Remote origin added: %repo_url%
    ) else (
        echo ❌ No URL provided. Exiting.
        exit /b 1
    )
)

REM Build frontend
echo 📦 Building frontend...
cd frontend
call npm run build
if errorlevel 1 (
    echo ❌ Frontend build failed
    exit /b 1
)
echo ✅ Frontend built successfully
cd ..

REM Add all changes
echo 📝 Staging changes...
git add .

REM Check if there are changes to commit
git diff --cached --quiet
if errorlevel 1 (
    REM Commit changes
    echo 💾 Committing changes...
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"
    set "datestamp=%YYYY%-%MM%-%DD% %HH%:%Min%:%Sec%"
    git commit -m "Deploy: %datestamp%"
    
    REM Push to GitHub
    echo 🚀 Pushing to GitHub...
    git push origin main
    if errorlevel 1 (
        echo ❌ Failed to push to GitHub
        exit /b 1
    )
    echo ✅ Successfully pushed to GitHub!
    echo.
    echo 🌐 Next steps:
    echo 1. Go to your hosting platform (Render, Heroku, Vercel, etc.)
    echo 2. Connect your GitHub repository
    echo 3. Deploy your application
    echo.
    echo 📖 See DEPLOYMENT.md for detailed deployment instructions
) else (
    echo ℹ️  No changes to commit
)

echo.
echo 🎉 Deployment script completed!
pause
