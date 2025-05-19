@echo off
echo Activating virtual environment...

if not exist venv\Scripts\activate (
    echo Virtual environment not found!
    echo Run reset_venv.bat first to create it.
    pause
    exit /b
)

call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment!
    pause
    exit /b
)

echo Virtual environment activated successfully.
echo.
echo Available commands:
echo - Run Flask server: python run.py
echo - Exit: type 'exit' or close the window
echo.

cmd /k