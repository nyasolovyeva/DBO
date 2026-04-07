@echo off
chcp 65001 > nul
echo ============================================
echo Скрипт сброса миграций, базы данных и запуска сервера
echo ============================================
echo ВНИМАНИЕ! Это действие удалит все данные из базы данных!
echo ============================================
set /p confirm="Вы уверены? (y/n): "
if not "%confirm%"=="y" (
    echo Операция отменена.
    pause
    exit /b
)

echo.
echo ШАГ 1: Удаление файлов миграций...
del /q services\migrations\*.py 2>nul
rmdir /s /q services\migrations\__pycache__ 2>nul
echo Создание папки migrations...
mkdir services\migrations 2>nul
echo. > services\migrations\__init__.py

echo.
echo ШАГ 2: Пересоздание базы данных PostgreSQL...
echo Подключение к PostgreSQL...
set PGPASSWORD=postgres
psql -U postgres -h localhost -p 5432 -c "DROP DATABASE IF EXISTS dbo_banks;"

if %errorlevel% neq 0 (
    echo [ERROR] Failed to drop database. Check PostgreSQL connection.
    pause
    exit /b
)

psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE dbo_banks ENCODING 'UTF8' OWNER postgres;"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create database.
    pause
    exit /b
)

echo.
echo ШАГ 3: Создание миграций...
python manage.py makemigrations services

echo.
echo ШАГ 4: Применение миграций...
python manage.py migrate

echo.
echo ШАГ 5: Создание суперпользователя...
python manage.py createsuperuser

echo.
echo ШАГ 6: Загрузка данных...
python manage.py add_banks_data

echo.
echo ============================================
echo Запуск сервера командой:
python manage.py runserver
echo ============================================
