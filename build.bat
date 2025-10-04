@echo off
chcp 65001
echo ===============================================
echo    Сборка YouTube Downloader
echo ===============================================

echo Установка зависимостей для сборки...
pip install pyinstaller

echo Очистка предыдущих сборок...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "YouTubeDownloader.spec" del "YouTubeDownloader.spec"

echo Сборка приложения...
pyinstaller --onefile --windowed --name "YouTube Downloader" --icon=icon.ico --hidden-import=yt_dlp --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=requests --add-data="*.py;." --clean --noconfirm youtube_downloader.py

echo ===============================================
if exist "dist\YouTube Downloader.exe" (
    echo ✅ Сборка успешно завершена!
    echo 📁 Файл: dist\YouTube Downloader.exe
) else (
    echo ❌ Ошибка сборки!
)

echo.
pause