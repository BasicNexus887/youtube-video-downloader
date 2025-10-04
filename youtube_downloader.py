import yt_dlp
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import threading
from PIL import Image, ImageTk
import requests
from io import BytesIO
import re
import webbrowser


class StableYouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("900x700")
        self.root.minsize(800, 600)

        # Языковые настройки
        self.current_language = "ru"  # По умолчанию русский
        self.translations = self.get_translations()

        # Переменные темы
        self.dark_mode = True
        self.colors = self.get_dark_theme()

        # Переменные
        self.download_path = os.path.join(os.path.expanduser("~"), "YouTubeDownloads")
        Path(self.download_path).mkdir(exist_ok=True)

        # Создание основного контейнера с прокруткой
        self.create_scrollable_interface()

    def get_translations(self):
        """Словари переводов"""
        return {
            "ru": {
                "title": "🎬 YouTube Video Downloader",
                "subtitle": "Скачивайте видео быстро и просто",
                "donate": "☕ Поддержать разработчика",
                "dark_theme": "🌙 Темная тема",
                "light_theme": "☀️ Светлая тема",
                "language": "🌐 Язык",
                "url_section": " 📥 Ссылка на видео",
                "url_placeholder": "Вставьте ссылку YouTube...",
                "paste": "📋 Вставить",
                "clear": "🧹 Очистить",
                "settings": " ⚙️ Настройки загрузки",
                "format": "Формат:",
                "format_mp4": "MP4 (Видео)",
                "format_mp3": "MP3 (Аудио)",
                "quality": "Качество:",
                "quality_480": "480p",
                "quality_720": "720p HD",
                "quality_best": "Лучшее",
                "folder": "Папка сохранения:",
                "download_btn": "⬇️ Скачать видео",
                "open_folder": "📂 Открыть папку",
                "progress": " 📊 Прогресс загрузки",
                "ready": "Готов к работе",
                "logs": " 📝 Журнал событий",
                "preview": " 👀 Превью видео",
                "preview_text": "Превью появится здесь\nпосле ввода ссылки",
                "video_title": "Название видео",
                "duration": "⏱️ --:--",
                "quality_label": "📊 Качество: --",
                "loading_info": "🔄 Загружаем информацию...",
                "loading_preview": "🔄 Загружаем превью...",
                "ready_download": "✅ Готово к загрузке",
                "clipboard_error": "Неверная YouTube ссылка в буфере",
                "clipboard_access": "Ошибка доступа к буферу",
                "field_cleared": "🧹 Поле ввода очищено",
                "folder_selected": "📁 Папка сохранения:",
                "folder_opened": "📂 Открыта папка с загрузками",
                "folder_not_exists": "Папка не существует",
                "download_started": "🚀 Запускаю загрузку...",
                "download_in_progress": "📥 Начинаю загрузку видео...",
                "download_complete": "✅ Загрузка завершена!",
                "download_success": "✅ Успешно скачано:",
                "download_error": "❌ Ошибка:",
                "error_url": "Введите ссылку на YouTube видео!",
                "error_valid_url": "Введите корректную ссылку на YouTube!",
                "success_title": "Успех",
                "success_message": "Видео скачано!",
                "error_title": "Ошибка",
                "error_message": "Не удалось скачать видео:",
                "thanks_donation": "☕ Спасибо за поддержку! Открываю ссылку для донатов...",
                "preview_unavailable": "Превью недоступно",
                "unknown_duration": "Неизвестно",
                "unknown_quality": "Неизвестно",
                "no_title": "Без названия"
            },
            "en": {
                "title": "🎬 YouTube Video Downloader",
                "subtitle": "Download videos quickly and easily",
                "donate": "☕ Support Developer",
                "dark_theme": "🌙 Dark Theme",
                "light_theme": "☀️ Light Theme",
                "language": "🌐 Language",
                "url_section": " 📥 Video URL",
                "url_placeholder": "Paste YouTube link...",
                "paste": "📋 Paste",
                "clear": "🧹 Clear",
                "settings": " ⚙️ Download Settings",
                "format": "Format:",
                "format_mp4": "MP4 (Video)",
                "format_mp3": "MP3 (Audio)",
                "quality": "Quality:",
                "quality_480": "480p",
                "quality_720": "720p HD",
                "quality_best": "Best",
                "folder": "Save Folder:",
                "download_btn": "⬇️ Download Video",
                "open_folder": "📂 Open Folder",
                "progress": " 📊 Download Progress",
                "ready": "Ready to work",
                "logs": " 📝 Event Log",
                "preview": " 👀 Video Preview",
                "preview_text": "Preview will appear here\nafter entering URL",
                "video_title": "Video Title",
                "duration": "⏱️ --:--",
                "quality_label": "📊 Quality: --",
                "loading_info": "🔄 Loading information...",
                "loading_preview": "🔄 Loading preview...",
                "ready_download": "✅ Ready to download",
                "clipboard_error": "Invalid YouTube link in clipboard",
                "clipboard_access": "Clipboard access error",
                "field_cleared": "🧹 Input field cleared",
                "folder_selected": "📁 Save folder:",
                "folder_opened": "📂 Downloads folder opened",
                "folder_not_exists": "Folder does not exist",
                "download_started": "🚀 Starting download...",
                "download_in_progress": "📥 Starting video download...",
                "download_complete": "✅ Download complete!",
                "download_success": "✅ Successfully downloaded:",
                "download_error": "❌ Error:",
                "error_url": "Enter YouTube video URL!",
                "error_valid_url": "Enter valid YouTube URL!",
                "success_title": "Success",
                "success_message": "Video downloaded!",
                "error_title": "Error",
                "error_message": "Failed to download video:",
                "thanks_donation": "☕ Thank you for support! Opening donation link...",
                "preview_unavailable": "Preview unavailable",
                "unknown_duration": "Unknown",
                "unknown_quality": "Unknown",
                "no_title": "No title"
            }
        }

    def t(self, key):
        """Получение перевода по ключу"""
        return self.translations[self.current_language].get(key, key)

    def get_dark_theme(self):
        """Темная тема"""
        return {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2d2d2d',
            'bg_card': '#3a3a3a',
            'accent': '#ff4757',
            'accent_hover': '#ff6b81',
            'text_primary': '#ffffff',
            'text_secondary': '#b0b0b0',
            'text_muted': '#666666',
            'border': '#555555',
            'success': '#2ed573',
            'warning': '#ffa502',
            'error': '#ff4757'
        }

    def get_light_theme(self):
        """Светлая тема"""
        return {
            'bg_primary': '#f5f5f5',
            'bg_secondary': '#ffffff',
            'bg_card': '#e9ecef',
            'accent': '#007bff',
            'accent_hover': '#0056b3',
            'text_primary': '#212529',
            'text_secondary': '#6c757d',
            'text_muted': '#adb5bd',
            'border': '#dee2e6',
            'success': '#28a745',
            'warning': '#ffc107',
            'error': '#dc3545'
        }

    def create_scrollable_interface(self):
        """Создание интерфейса с прокруткой"""
        # Главный контейнер с прокруткой
        main_container = tk.Frame(self.root, bg=self.colors['bg_primary'])
        main_container.pack(fill='both', expand=True)

        # Создаем canvas и scrollbar
        self.canvas = tk.Canvas(main_container, bg=self.colors['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.colors['bg_primary'])

        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Упаковка элементов прокрутки
        self.canvas.pack(side='left', fill='both', expand=True, padx=15)
        scrollbar.pack(side='right', fill='y')

        # Привязка колесика мыши ко всему canvas
        self.bind_mousewheel(self.canvas)
        self.bind_mousewheel(self.scrollable_frame)

        # Создание интерфейса
        self.create_stable_interface()

    def bind_mousewheel(self, widget):
        """Привязка колесика мыши к виджету и всем его потомкам"""
        widget.bind('<MouseWheel>', self._on_mousewheel)
        for child in widget.winfo_children():
            self.bind_mousewheel(child)

    def _on_mousewheel(self, event):
        """Обработчик колесика мыши"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

    def create_stable_interface(self):
        """Создание стабильного интерфейса без плавающих элементов"""
        # Заголовок с кнопками управления
        self.create_header_with_controls(self.scrollable_frame)

        # Основной контент
        content_frame = tk.Frame(self.scrollable_frame, bg=self.colors['bg_primary'])
        content_frame.pack(fill='both', expand=True, pady=15)

        # Две колонки с фиксированными размерами
        left_column = tk.Frame(content_frame, bg=self.colors['bg_primary'], width=500)
        left_column.pack(side='left', fill='both', expand=True)

        right_column = tk.Frame(content_frame, bg=self.colors['bg_primary'], width=350)
        right_column.pack(side='right', fill='y')
        right_column.pack_propagate(False)

        # Создание стабильных секций
        self.create_url_section(left_column)
        self.create_settings_section(left_column)
        self.create_actions_section(left_column)
        self.create_progress_section(left_column)
        self.create_logs_section(left_column)
        self.create_preview_section(right_column)

    def create_header_with_controls(self, parent):
        """Заголовок с кнопками управления (донат, тема, язык)"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill='x', pady=(0, 20))

        # Верхняя строка - заголовок и кнопки управления
        top_row = tk.Frame(header_frame, bg=self.colors['bg_primary'])
        top_row.pack(fill='x')

        # Заголовок
        self.title_label = tk.Label(top_row,
                                    text=self.t("title"),
                                    font=('Arial', 20, 'bold'),
                                    bg=self.colors['bg_primary'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side='left')

        # Правая часть с кнопками управления
        controls_frame = tk.Frame(top_row, bg=self.colors['bg_primary'])
        controls_frame.pack(side='right')

        # Кнопка переключения языка
        self.language_btn = tk.Button(controls_frame,
                                      text=f"{'RU' if self.current_language == 'ru' else 'EN'}",
                                      command=self.toggle_language,
                                      bg=self.colors['bg_secondary'],
                                      fg=self.colors['text_primary'],
                                      font=('Arial', 9, 'bold'),
                                      relief='solid',
                                      bd=1,
                                      padx=12,
                                      pady=5,
                                      width=4)
        self.language_btn.pack(side='right', padx=(5, 0))

        # Кнопка переключения темы
        self.theme_btn = tk.Button(controls_frame,
                                   text="🌙" if self.dark_mode else "☀️",
                                   command=self.toggle_theme,
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   font=('Arial', 9),
                                   relief='solid',
                                   bd=1,
                                   padx=8,
                                   pady=5,
                                   width=3)
        self.theme_btn.pack(side='right', padx=(5, 0))

        # Кнопка донатов
        self.donation_btn = tk.Button(controls_frame,
                                      text=self.t("donate"),
                                      command=self.open_donation_link,
                                      bg='#FF6B35',
                                      fg='white',
                                      font=('Arial', 9, 'bold'),
                                      relief='solid',
                                      bd=1,
                                      padx=12,
                                      pady=5)
        self.donation_btn.pack(side='right', padx=(5, 0))

        self.subtitle_label = tk.Label(header_frame,
                                       text=self.t("subtitle"),
                                       font=('Arial', 11),
                                       bg=self.colors['bg_primary'],
                                       fg=self.colors['text_secondary'])
        self.subtitle_label.pack(pady=(5, 0))

    def toggle_language(self):
        """Переключение языка"""
        self.current_language = "en" if self.current_language == "ru" else "ru"
        self.update_language()

    def update_language(self):
        """Обновление всех текстов интерфейса"""
        # Обновляем текст кнопок
        self.language_btn.config(text='RU' if self.current_language == 'ru' else 'EN')
        self.theme_btn.config(text="🌙" if self.dark_mode else "☀️")

        # Обновляем заголовок
        self.title_label.config(text=self.t("title"))
        self.subtitle_label.config(text=self.t("subtitle"))
        self.donation_btn.config(text=self.t("donate"))

        # Пересоздаем интерфейс для обновления всех текстов
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_stable_interface()

    def toggle_theme(self):
        """Переключение между темной и светлой темой"""
        self.dark_mode = not self.dark_mode
        self.colors = self.get_dark_theme() if self.dark_mode else self.get_light_theme()

        # Обновляем интерфейс
        self.update_theme()

        # Обновляем текст кнопки темы
        self.theme_btn.config(
            text="🌙" if self.dark_mode else "☀️",
            bg=self.colors['bg_secondary'],
            fg=self.colors['text_primary']
        )

    def update_theme(self):
        """Обновление всех элементов интерфейса под новую тему"""
        # Фон главного окна
        self.root.configure(bg=self.colors['bg_primary'])
        self.canvas.configure(bg=self.colors['bg_primary'])
        self.scrollable_frame.configure(bg=self.colors['bg_primary'])

        # Пересоздаем интерфейс
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_stable_interface()

    def open_donation_link(self):
        """Открытие ссылки для донатов"""
        donation_url = "https://dalink.to/elys_cc"
        webbrowser.open(donation_url)
        self.log_message(self.t("thanks_donation"))

    def create_url_section(self, parent):
        """Секция ввода URL"""
        self.url_frame = tk.LabelFrame(parent,
                                       text=self.t("url_section"),
                                       font=('Arial', 11, 'bold'),
                                       bg=self.colors['bg_primary'],
                                       fg=self.colors['text_primary'],
                                       padx=15,
                                       pady=15)
        self.url_frame.pack(fill='x', pady=10)

        # Поле ввода
        self.url_var = tk.StringVar()
        self.url_entry = tk.Entry(self.url_frame,
                                  textvariable=self.url_var,
                                  bg=self.colors['bg_secondary'],
                                  fg=self.colors['text_primary'],
                                  font=('Arial', 11),
                                  relief='solid',
                                  bd=1)
        self.url_entry.pack(fill='x', pady=10, ipady=8)
        self.url_entry.insert(0, self.t("url_placeholder"))
        self.url_entry.bind('<KeyRelease>', self.on_url_change)

        # Кнопки управления
        btn_frame = tk.Frame(self.url_frame, bg=self.colors['bg_primary'])
        btn_frame.pack(fill='x')

        self.paste_btn = tk.Button(btn_frame,
                                   text=self.t("paste"),
                                   command=self.paste_url,
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   font=('Arial', 9),
                                   relief='solid',
                                   bd=1)
        self.paste_btn.pack(side='left', padx=(0, 10))

        self.clear_btn = tk.Button(btn_frame,
                                   text=self.t("clear"),
                                   command=self.clear_url,
                                   bg=self.colors['bg_secondary'],
                                   fg=self.colors['text_primary'],
                                   font=('Arial', 9),
                                   relief='solid',
                                   bd=1)
        self.clear_btn.pack(side='left')

    def create_settings_section(self, parent):
        """Секция настроек"""
        self.settings_frame = tk.LabelFrame(parent,
                                            text=self.t("settings"),
                                            font=('Arial', 11, 'bold'),
                                            bg=self.colors['bg_primary'],
                                            fg=self.colors['text_primary'],
                                            padx=15,
                                            pady=15)
        self.settings_frame.pack(fill='x', pady=10)

        # Формат
        format_frame = tk.Frame(self.settings_frame, bg=self.colors['bg_primary'])
        format_frame.pack(fill='x', pady=8)

        tk.Label(format_frame,
                 text=self.t("format"),
                 bg=self.colors['bg_primary'],
                 fg=self.colors['text_primary'],
                 font=('Arial', 10)).pack(anchor='w')

        self.format_var = tk.StringVar(value="mp4")
        format_btn_frame = tk.Frame(format_frame, bg=self.colors['bg_primary'])
        format_btn_frame.pack(fill='x', pady=5)

        self.mp4_radio = tk.Radiobutton(format_btn_frame,
                                        text=self.t("format_mp4"),
                                        variable=self.format_var,
                                        value="mp4",
                                        bg=self.colors['bg_primary'],
                                        fg=self.colors['text_primary'],
                                        selectcolor=self.colors['accent'])
        self.mp4_radio.pack(side='left', padx=(0, 15))

        self.mp3_radio = tk.Radiobutton(format_btn_frame,
                                        text=self.t("format_mp3"),
                                        variable=self.format_var,
                                        value="mp3",
                                        bg=self.colors['bg_primary'],
                                        fg=self.colors['text_primary'],
                                        selectcolor=self.colors['accent'])
        self.mp3_radio.pack(side='left')

        # Качество
        quality_frame = tk.Frame(self.settings_frame, bg=self.colors['bg_primary'])
        quality_frame.pack(fill='x', pady=8)

        tk.Label(quality_frame,
                 text=self.t("quality"),
                 bg=self.colors['bg_primary'],
                 fg=self.colors['text_primary'],
                 font=('Arial', 10)).pack(anchor='w')

        self.quality_var = tk.StringVar(value="720p")
        quality_btn_frame = tk.Frame(quality_frame, bg=self.colors['bg_primary'])
        quality_btn_frame.pack(fill='x', pady=5)

        qualities = [
            (self.t("quality_480"), "480p"),
            (self.t("quality_720"), "720p"),
            (self.t("quality_best"), "best")
        ]

        self.quality_radios = []
        for text, value in qualities:
            radio = tk.Radiobutton(quality_btn_frame,
                                   text=text,
                                   variable=self.quality_var,
                                   value=value,
                                   bg=self.colors['bg_primary'],
                                   fg=self.colors['text_primary'],
                                   selectcolor=self.colors['accent'])
            radio.pack(side='left', padx=(0, 15))
            self.quality_radios.append(radio)

        # Папка сохранения
        folder_frame = tk.Frame(self.settings_frame, bg=self.colors['bg_primary'])
        folder_frame.pack(fill='x', pady=8)

        tk.Label(folder_frame,
                 text=self.t("folder"),
                 bg=self.colors['bg_primary'],
                 fg=self.colors['text_primary'],
                 font=('Arial', 10)).pack(anchor='w')

        folder_input_frame = tk.Frame(folder_frame, bg=self.colors['bg_primary'])
        folder_input_frame.pack(fill='x', pady=5)

        self.folder_var = tk.StringVar(value=self.download_path)
        self.folder_entry = tk.Entry(folder_input_frame,
                                     textvariable=self.folder_var,
                                     bg=self.colors['bg_secondary'],
                                     fg=self.colors['text_primary'],
                                     font=('Arial', 9),
                                     relief='solid',
                                     bd=1)
        self.folder_entry.pack(side='left', fill='x', expand=True, ipady=4)

        self.folder_btn = tk.Button(folder_input_frame,
                                    text="📁",
                                    command=self.browse_folder,
                                    bg=self.colors['bg_secondary'],
                                    fg=self.colors['text_primary'],
                                    font=('Arial', 9),
                                    relief='solid',
                                    bd=1,
                                    width=3)
        self.folder_btn.pack(side='right', padx=(5, 0))

    def create_actions_section(self, parent):
        """Секция действий"""
        actions_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        actions_frame.pack(fill='x', pady=10)

        # Основная кнопка загрузки
        self.download_btn = tk.Button(actions_frame,
                                      text=self.t("download_btn"),
                                      command=self.start_download,
                                      bg=self.colors['accent'],
                                      fg='white',
                                      font=('Arial', 12, 'bold'),
                                      relief='solid',
                                      bd=1,
                                      padx=30,
                                      pady=12)
        self.download_btn.pack(side='left', padx=(0, 15))

        # Кнопка открытия папки
        self.open_folder_btn = tk.Button(actions_frame,
                                         text=self.t("open_folder"),
                                         command=self.open_download_folder,
                                         bg=self.colors['bg_secondary'],
                                         fg=self.colors['text_primary'],
                                         font=('Arial', 10),
                                         relief='solid',
                                         bd=1,
                                         padx=20,
                                         pady=10)
        self.open_folder_btn.pack(side='left')

    def create_progress_section(self, parent):
        """Секция прогресса"""
        self.progress_frame = tk.LabelFrame(parent,
                                            text=self.t("progress"),
                                            font=('Arial', 11, 'bold'),
                                            bg=self.colors['bg_primary'],
                                            fg=self.colors['text_primary'],
                                            padx=15,
                                            pady=15)
        self.progress_frame.pack(fill='x', pady=10)

        # Прогресс-бар
        self.progress = ttk.Progressbar(self.progress_frame,
                                        mode='indeterminate',
                                        length=100)
        self.progress.pack(fill='x', pady=10)

        # Статус
        self.status_label = tk.Label(self.progress_frame,
                                     text=self.t("ready"),
                                     bg=self.colors['bg_primary'],
                                     fg=self.colors['text_secondary'],
                                     font=('Arial', 9))
        self.status_label.pack()

    def create_logs_section(self, parent):
        """Секция логов"""
        self.logs_frame = tk.LabelFrame(parent,
                                        text=self.t("logs"),
                                        font=('Arial', 11, 'bold'),
                                        bg=self.colors['bg_primary'],
                                        fg=self.colors['text_primary'],
                                        padx=15,
                                        pady=15)
        self.logs_frame.pack(fill='both', expand=True, pady=10)

        # Текстовое поле с прокруткой
        log_container = tk.Frame(self.logs_frame, bg=self.colors['bg_secondary'])
        log_container.pack(fill='both', expand=True)

        self.log_text = tk.Text(log_container,
                                height=8,
                                bg=self.colors['bg_secondary'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 9),
                                relief='solid',
                                bd=1,
                                wrap='word')

        scrollbar = ttk.Scrollbar(log_container, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

    def create_preview_section(self, parent):
        """Секция превью"""
        self.preview_frame = tk.LabelFrame(parent,
                                           text=self.t("preview"),
                                           font=('Arial', 11, 'bold'),
                                           bg=self.colors['bg_primary'],
                                           fg=self.colors['text_primary'],
                                           padx=15,
                                           pady=15)
        self.preview_frame.pack(fill='both', pady=10)

        # Контейнер для миниатюры
        thumbnail_container = tk.Frame(self.preview_frame,
                                       bg=self.colors['border'],
                                       height=150,
                                       relief='solid',
                                       bd=1)
        thumbnail_container.pack(fill='x', pady=10)
        thumbnail_container.pack_propagate(False)

        self.thumbnail_label = tk.Label(thumbnail_container,
                                        text=self.t("preview_text"),
                                        bg=self.colors['border'],
                                        fg=self.colors['text_muted'],
                                        justify='center',
                                        font=('Arial', 10))
        self.thumbnail_label.pack(expand=True)

        # Информация о видео
        info_frame = tk.Frame(self.preview_frame, bg=self.colors['bg_primary'])
        info_frame.pack(fill='x', pady=5)

        self.video_title = tk.Label(info_frame,
                                    text=self.t("video_title"),
                                    bg=self.colors['bg_primary'],
                                    fg=self.colors['text_primary'],
                                    font=('Arial', 10, 'bold'),
                                    wraplength=320,
                                    justify='center')
        self.video_title.pack(fill='x', pady=(0, 5))

        meta_frame = tk.Frame(info_frame, bg=self.colors['bg_primary'])
        meta_frame.pack(fill='x')

        self.video_duration = tk.Label(meta_frame,
                                       text=self.t("duration"),
                                       bg=self.colors['bg_primary'],
                                       fg=self.colors['text_secondary'],
                                       font=('Arial', 9))
        self.video_duration.pack(side='left')

        self.video_quality = tk.Label(meta_frame,
                                      text=self.t("quality_label"),
                                      bg=self.colors['bg_primary'],
                                      fg=self.colors['text_secondary'],
                                      font=('Arial', 9))
        self.video_quality.pack(side='right')

    def on_url_change(self, event=None):
        """Обработчик изменения URL"""
        url = self.url_var.get().strip()
        if url and url != self.t("url_placeholder") and self.is_valid_youtube_url(url):
            self.status_label.config(text=self.t("loading_info"))
            threading.Thread(target=self.fetch_video_info, args=(url,), daemon=True).start()

    def is_valid_youtube_url(self, url):
        """Проверка валидности YouTube URL"""
        patterns = [
            r'(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+',
            r'(https?://)?(www\.)?youtu\.be/[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/embed/[\w-]+',
            r'(https?://)?(www\.)?youtube\.com/shorts/[\w-]+'
        ]
        return any(re.match(pattern, url) for pattern in patterns)

    def fetch_video_info(self, url):
        """Получение информации о видео"""
        try:
            self.root.after(0, lambda: self.thumbnail_label.config(text=self.t("loading_preview")))

            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

                thumbnail_url = info.get('thumbnail', '')
                title = info.get('title', self.t("no_title"))
                duration = self.format_duration(info.get('duration', 0))
                quality = info.get('format_note', self.t("unknown_quality"))

                if thumbnail_url:
                    response = requests.get(thumbnail_url, timeout=10)
                    image = Image.open(BytesIO(response.content))
                    image.thumbnail((300, 150), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)

                    self.root.after(0, lambda: self.update_preview(photo, title, duration, quality))
                else:
                    self.root.after(0, lambda: self.update_preview(None, title, duration, quality))

        except Exception as e:
            self.root.after(0, lambda: self.show_error(f"{self.t('download_error')} {str(e)}"))

    def update_preview(self, photo, title, duration, quality):
        """Обновление превью"""
        if photo:
            self.thumbnail_label.configure(image=photo, text="")
            self.thumbnail_label.image = photo
        else:
            self.thumbnail_label.config(image='', text=self.t("preview_unavailable"))

        self.video_title.config(text=title)
        self.video_duration.config(text=f"⏱️ {duration}")
        self.video_quality.config(text=f"📊 {quality}")
        self.status_label.config(text=self.t("ready_download"))
        self.log_message(f"✅ {self.t('download_success')} {title}")

    def format_duration(self, seconds):
        """Форматирование длительности"""
        if not seconds:
            return self.t("unknown_duration")

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

    def paste_url(self):
        """Вставка URL из буфера обмена"""
        try:
            clipboard_content = self.root.clipboard_get()
            if self.is_valid_youtube_url(clipboard_content):
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_content)
                self.log_message("📋 " + (
                    "Ссылка вставлена из буфера" if self.current_language == "ru" else "Link pasted from clipboard"))
                self.on_url_change()
            else:
                self.show_warning(self.t("clipboard_error"))
        except:
            self.show_error(self.t("clipboard_access"))

    def clear_url(self):
        """Очистка URL"""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, self.t("url_placeholder"))
        self.thumbnail_label.config(image='', text=self.t("preview_text"))
        self.video_title.config(text=self.t("video_title"))
        self.video_duration.config(text=self.t("duration"))
        self.video_quality.config(text=self.t("quality_label"))
        self.status_label.config(text=self.t("ready"))
        self.log_message(self.t("field_cleared"))

    def browse_folder(self):
        """Выбор папки для сохранения"""
        folder = filedialog.askdirectory(initialdir=self.download_path)
        if folder:
            self.folder_var.set(folder)
            self.download_path = folder
            self.log_message(f"📁 {self.t('folder_selected')} {folder}")

    def open_download_folder(self):
        """Открытие папки с загрузками"""
        if os.path.exists(self.download_path):
            try:
                os.startfile(self.download_path)
                self.log_message(self.t("folder_opened"))
            except:
                import subprocess
                import platform
                system = platform.system()
                if system == "Darwin":
                    subprocess.run(["open", self.download_path])
                elif system == "Linux":
                    subprocess.run(["xdg-open", self.download_path])
        else:
            self.show_warning(self.t("folder_not_exists"))

    def start_download(self):
        """Начало загрузки видео"""
        url = self.url_var.get().strip()

        if not url or url == self.t("url_placeholder"):
            self.show_error(self.t("error_url"))
            return

        if not self.is_valid_youtube_url(url):
            self.show_error(self.t("error_valid_url"))
            return

        self.log_message(self.t("download_started"))
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def download_video(self, url):
        """Процесс загрузки видео"""
        try:
            self.root.after(0, self.on_download_start)

            format_type = self.format_var.get()
            quality = self.quality_var.get()

            ydl_opts = {
                'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
                'retries': 5,
                'fragment_retries': 5,
            }

            if format_type == "mp4":
                if quality == "480p":
                    ydl_opts['format'] = 'best[height<=480]/best[ext=mp4]/best'
                elif quality == "720p":
                    ydl_opts['format'] = 'best[height<=720]/best[ext=mp4]/best'
                else:
                    ydl_opts['format'] = 'best[ext=mp4]/best'
            else:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', self.t("no_title"))

                self.root.after(0, lambda: self.on_download_success(title))

        except Exception as e:
            self.root.after(0, lambda: self.on_download_error(str(e)))

    def on_download_start(self):
        """Действия при начале загрузки"""
        self.download_btn.config(state='disabled')
        self.progress.start()
        self.status_label.config(
            text="🔄 " + ("Идет загрузка..." if self.current_language == "ru" else "Downloading..."))
        self.log_message(self.t("download_in_progress"))

    def on_download_success(self, title):
        """Действия при успешной загрузке"""
        self.download_btn.config(state='normal')
        self.progress.stop()
        self.status_label.config(text=self.t("download_complete"))
        self.log_message(f"✅ {self.t('download_success')} {title}")
        messagebox.showinfo(self.t("success_title"), f"{self.t('success_message')}\n\n{title}")

    def on_download_error(self, error):
        """Действия при ошибке загрузки"""
        self.download_btn.config(state='normal')
        self.progress.stop()
        self.status_label.config(text="❌ " + ("Ошибка загрузки" if self.current_language == "ru" else "Download error"))
        self.log_message(f"❌ {self.t('download_error')} {error}")
        messagebox.showerror(self.t("error_title"), f"{self.t('error_message')}\n{error}")

    def log_message(self, message):
        """Добавление сообщения в лог"""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def show_error(self, message):
        """Показать ошибку"""
        self.log_message(f"❌ {message}")
        self.status_label.config(text="❌ " + ("Ошибка" if self.current_language == "ru" else "Error"))
        messagebox.showerror(self.t("error_title"), message)

    def show_warning(self, message):
        """Показать предупреждение"""
        self.log_message(f"⚠️ {message}")
        messagebox.showwarning("Внимание" if self.current_language == "ru" else "Warning", message)


def main():
    root = tk.Tk()
    app = StableYouTubeDownloader(root)
    root.mainloop()


if __name__ == '__main__':
    main()