@echo off

echo Stopping and removing containers...
docker compose down

echo.
echo Building and starting containers in detached mode...
docker compose up -d --build

echo.
echo Showing live logs (Press Ctrl+C to stop)...
docker compose logs -f

pause
