@echo off
REM BookClick - Script de Lancement Rapide pour Windows
REM Usage: Double-cliquer sur start.bat

echo.
echo ========================================
echo   BookClick - Demarrage
echo ========================================
echo.

REM Activer l'environnement virtuel
echo [1/3] Activation de l'environnement virtuel...
call venv\Scripts\activate

REM Vérifier les migrations
echo [2/3] Verification des migrations...
python manage.py migrate --check >nul 2>&1 || python manage.py migrate

REM Collecter les fichiers statiques
echo [3/3] Collection des fichiers statiques...
python manage.py collectstatic --noinput --clear >nul 2>&1

echo.
echo ========================================
echo   BookClick est pret!
echo ========================================
echo.
echo Acces:
echo   - Local:   http://localhost:8000
echo   - Admin:   http://localhost:8000/admin
echo   - API:     http://localhost:8000/api
echo.
echo Comptes de test:
echo   - Admin:   admin@university.edu / admin123
echo   - Teacher: john.doe@university.edu / teacher123
echo   - Student: alice.johnson@university.edu / student123
echo.
echo Pour arreter: Ctrl + C
echo ========================================
echo.

REM Lancer le serveur
python manage.py runserver

pause
