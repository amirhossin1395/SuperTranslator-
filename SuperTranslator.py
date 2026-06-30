#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Super Translator Pro - مترجم متن + مترجم وب‌سایت + تمام زبان‌های دنیا
سازنده: AmirHossein Haji Moradkhani | کرمان، ایران
"""

import sys
import requests
import json
import os
import tempfile
import webbrowser
import re
from io import BytesIO
from datetime import datetime
from urllib.parse import urlparse

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

# ════════════════ تمام زبان‌های دنیا ════════════════
ALL_LANGUAGES = {
    'fa': '🇮🇷 فارسی', 'en': '🇬🇧 English', 'ar': '🇸🇦 العربية', 'fr': '🇫🇷 Français',
    'de': '🇩🇪 Deutsch', 'es': '🇪🇸 Español', 'it': '🇮🇹 Italiano', 'pt': '🇵🇹 Português',
    'ru': '🇷🇺 Русский', 'zh-CN': '🇨🇳 中文简体', 'zh-TW': '🇹🇼 中文繁體', 'ja': '🇯🇵 日本語',
    'ko': '🇰🇷 한국어', 'hi': '🇮🇳 हिन्दी', 'tr': '🇹🇷 Türkçe', 'nl': '🇳🇱 Nederlands',
    'pl': '🇵🇱 Polski', 'sv': '🇸🇪 Svenska', 'no': '🇳🇴 Norsk', 'da': '🇩🇰 Dansk',
    'fi': '🇫🇮 Suomi', 'el': '🇬🇷 Ελληνικά', 'cs': '🇨🇿 Čeština', 'ro': '🇷🇴 Română',
    'hu': '🇭🇺 Magyar', 'th': '🇹🇭 ไทย', 'vi': '🇻🇳 Tiếng Việt', 'id': '🇮🇩 Indonesia',
    'ms': '🇲🇾 Melayu', 'bn': '🇧🇩 বাংলা', 'ur': '🇵🇰 اردو', 'he': '🇮🇱 עברית',
    'uk': '🇺🇦 Українська', 'bg': '🇧🇬 Български', 'sr': '🇷🇸 Српски', 'hr': '🇭🇷 Hrvatski',
    'sk': '🇸🇰 Slovenčina', 'sl': '🇸🇮 Slovenščina', 'lt': '🇱🇹 Lietuvių', 'lv': '🇱🇻 Latviešu',
    'et': '🇪🇪 Eesti', 'sq': '🇦🇱 Shqip', 'mk': '🇲🇰 Македонски', 'hy': '🇦🇲 Հայերեն',
    'ka': '🇬🇪 ქართული', 'az': '🇦🇿 Azərbaycan', 'uz': '🇺🇿 O\'zbek', 'kk': '🇰🇿 Қазақ',
    'af': '🇿🇦 Afrikaans', 'sw': '🇰🇪 Kiswahili', 'am': '🇪🇹 አማርኛ', 'ne': '🇳🇵 नेपाली',
    'si': '🇱🇰 සිංහල', 'my': '🇲🇲 မြန်မာ', 'km': '🇰🇭 ខ្មែរ', 'lo': '🇱🇦 ລາວ',
    'mn': '🇲🇳 Монгол', 'ps': '🇦🇫 پښتو', 'ku': '🏳️ Kurdî', 'sd': '🇵🇰 سنڌي',
    'ta': '🇮🇳 தமிழ்', 'te': '🇮🇳 తెలుగు', 'ml': '🇮🇳 മലയാളം', 'kn': '🇮🇳 ಕನ್ನಡ',
    'gu': '🇮🇳 ગુજરાતી', 'pa': '🇮🇳 ਪੰਜਾਬੀ', 'mr': '🇮🇳 मराठी', 'or': '🇮🇳 ଓଡ଼ିଆ',
    'eo': '🌍 Esperanto', 'la': '🏛️ Latina', 'ga': '🇮🇪 Gaeilge', 'cy': '🏴󠁧󠁢󠁷󠁬󠁳󠁿 Cymraeg',
    'yi': '🇮🇱 ייִדיש', 'ht': '🇭🇹 Kreyòl', 'mg': '🇲🇬 Malagasy', 'so': '🇸🇴 Soomaali',
    'ig': '🇳🇬 Igbo', 'yo': '🇳🇬 Yorùbá', 'ha': '🇳🇬 Hausa', 'zu': '🇿🇦 isiZulu',
}

# ════════════════ رنگ‌های گوگل ════════════════
BLUE = "#1a73e8"
GREEN = "#34a853"
RED = "#ea4335"
YELLOW = "#fbbc04"
WHITE = "#ffffff"
GREY = "#f8f9fa"
BORDER = "#dadce0"
TEXT = "#3c4043"

STYLE = f"""
QMainWindow {{ background: {WHITE}; }}
QWidget {{ font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 14px; color: {TEXT}; }}
QTabWidget::pane {{ border: none; background: {WHITE}; }}
QTabBar::tab {{
    background: {WHITE}; color: {TEXT}; padding: 14px 28px;
    font-size: 15px; font-weight: 500; border-bottom: 3px solid transparent;
}}
QTabBar::tab:selected {{ color: {BLUE}; border-bottom: 3px solid {BLUE}; font-weight: bold; }}
QTabBar::tab:hover {{ background: {GREY}; }}
QPushButton {{
    background: {BLUE}; color: white; border: none; border-radius: 24px;
    padding: 14px 32px; font-size: 16px; font-weight: bold;
}}
QPushButton:hover {{ background: #1557b0; }}
QPushButton:pressed {{ background: #0d47a1; }}
QPushButton#swapBtn {{
    background: {WHITE}; color: {BLUE}; border: 2px solid {BORDER};
    border-radius: 22px; padding: 10px; font-size: 20px; min-width: 48px; min-height: 48px;
}}
QPushButton#swapBtn:hover {{ background: {GREY}; }}
QTextEdit, QPlainTextEdit {{
    border: 2px solid {BORDER}; border-radius: 16px; padding: 20px;
    font-size: 18px; background: white; color: #202124;
}}
QTextEdit:focus, QPlainTextEdit:focus {{ border-color: {BLUE}; }}
QComboBox {{
    padding: 14px 20px; border: 2px solid {BORDER}; border-radius: 10px;
    background: white; font-size: 15px; min-width: 220px;
}}
QComboBox:hover {{ border-color: {BLUE}; }}
QComboBox QAbstractItemView {{
    selection-background-color: {BLUE}; selection-color: white;
    font-size: 14px; min-width: 280px;
}}
QLabel {{ color: {TEXT}; font-size: 15px; font-weight: 500; }}
QLineEdit {{
    border: 2px solid {BORDER}; border-radius: 10px; padding: 14px;
    font-size: 15px; background: white;
}}
QLineEdit:focus {{ border-color: {BLUE}; }}
QScrollBar:vertical {{ width: 8px; background: transparent; }}
QScrollBar::handle:vertical {{ background: {BORDER}; border-radius: 4px; }}
QScrollBar::handle:vertical:hover {{ background: {BLUE}; }}
QProgressBar {{
    border: none; border-radius: 10px; height: 6px; background: {GREY};
    text-align: center; font-size: 11px;
}}
QProgressBar::chunk {{ background: {BLUE}; border-radius: 10px; }}
"""

# ════════════════ توابع ترجمه ════════════════
def translate_text(text, source, target):
    """ترجمه متن با Google Translate API"""
    try:
        if len(text) > 5000:
            parts = [text[i:i+5000] for i in range(0, len(text), 5000)]
            result = []
            for part in parts:
                url = "https://translate.googleapis.com/translate_a/single"
                params = {'client': 'gtx', 'sl': source, 'tl': target, 'dt': 't', 'q': part}
                resp = requests.get(url, params=params, timeout=10)
                data = json.loads(resp.text)
                result.append(''.join([s[0] for s in data[0] if s and s[0]]))
            return ''.join(result)
        else:
            url = "https://translate.googleapis.com/translate_a/single"
            params = {'client': 'gtx', 'sl': source, 'tl': target, 'dt': 't', 'q': text}
            resp = requests.get(url, params=params, timeout=10)
            data = json.loads(resp.text)
            return ''.join([s[0] for s in data[0] if s and s[0]])
    except Exception as e:
        return f"❌ خطا: {str(e)}"

def translate_website(url, target_lang):
    """ترجمه وب‌سایت"""
    try:
        # ساخت URL مترجم گوگل
        translate_url = f"https://translate.google.com/translate?hl={target_lang}&sl=auto&tl={target_lang}&u={url}"
        return translate_url
    except:
        return None

def detect_language(text):
    """تشخیص زبان متن"""
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {'client': 'gtx', 'sl': 'auto', 'tl': 'en', 'dt': 't', 'q': text[:500]}
        resp = requests.get(url, params=params, timeout=5)
        data = json.loads(resp.text)
        detected = data[2] if len(data) > 2 else 'en'
        return detected
    except:
        return 'en'

# ════════════════ پنجره اصلی ════════════════
class SuperTranslatorPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Super Translator Pro - مترجم متن و وب‌سایت")
        self.setGeometry(100, 80, 1300, 850)
        self.setStyleSheet(STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header
        header = QLabel(f'<h1 style="color:{BLUE};padding:20px;">🌍 Super Translator Pro</h1>')
        header.setAlignment(Qt.AlignCenter)
        layout.addWidget(header)

        sub = QLabel('<p style="color:#666;font-size:13px;">ترجمه متن + ترجمه وب‌سایت | ۱۰۰+ زبان زنده دنیا</p>')
        sub.setAlignment(Qt.AlignCenter)
        layout.addWidget(sub)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        layout.addWidget(self.tabs)

        # Add tabs
        self.text_translate_tab()
        self.website_translate_tab()

        self.statusBar().showMessage("✅ آماده | ترجمه متن + وب‌سایت | ۱۰۰+ زبان")

    # ════════════════ تب ترجمه متن ════════════════
    def text_translate_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # Language bars
        lang_frame = QHBoxLayout()
        lang_frame.setSpacing(15)

        from_box = QVBoxLayout()
        from_box.addWidget(QLabel("از:"))
        self.from_lang = QComboBox()
        self.from_lang.addItems(ALL_LANGUAGES.values())
        self.from_lang.setCurrentText('🇬🇧 English')
        from_box.addWidget(self.from_lang)

        swap_btn = QPushButton("⇄")
        swap_btn.setObjectName("swapBtn")
        swap_btn.clicked.connect(self.swap_languages)
        swap_btn.setFixedSize(52, 52)

        to_box = QVBoxLayout()
        to_box.addWidget(QLabel("به:"))
        self.to_lang = QComboBox()
        self.to_lang.addItems(ALL_LANGUAGES.values())
        self.to_lang.setCurrentText('🇮🇷 فارسی')
        to_box.addWidget(self.to_lang)

        lang_frame.addLayout(from_box)
        lang_frame.addWidget(swap_btn, alignment=Qt.AlignCenter)
        lang_frame.addLayout(to_box)
        layout.addLayout(lang_frame)

        # Auto detect
        self.auto_detect_cb = QCheckBox("🔍 تشخیص خودکار زبان")
        self.auto_detect_cb.setChecked(False)
        layout.addWidget(self.auto_detect_cb)

        # Text areas
        text_frame = QHBoxLayout()
        text_frame.setSpacing(15)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("✍️ متن خود را اینجا بنویسید...")
        self.input_text.setMinimumHeight(300)

        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("📝 ترجمه اینجا نمایش داده می‌شود...")
        self.output_text.setMinimumHeight(300)

        text_frame.addWidget(self.input_text)
        text_frame.addWidget(self.output_text)
        layout.addLayout(text_frame)

        # Progress bar
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # Buttons
        btn_frame = QHBoxLayout()
        btn_frame.setSpacing(12)

        translate_btn = QPushButton("🔄 ترجمه کن")
        translate_btn.clicked.connect(self.do_translate)

        auto_btn = QPushButton("⚡ ترجمه همزمان")
        auto_btn.setStyleSheet(f"background: {YELLOW}; color: #333;")
        auto_btn.clicked.connect(self.toggle_auto_translate)
        self.auto_translating = False

        copy_btn = QPushButton("📋 کپی")
        copy_btn.setStyleSheet(f"background: {GREEN};")
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(self.output_text.toPlainText()))

        clear_btn = QPushButton("🗑️ پاک کردن")
        clear_btn.setStyleSheet(f"background: {RED};")
        clear_btn.clicked.connect(lambda: [self.input_text.clear(), self.output_text.clear()])

        speak_btn = QPushButton("🔊 خواندن")
        speak_btn.clicked.connect(self.speak_translation)

        btn_frame.addWidget(translate_btn)
        btn_frame.addWidget(auto_btn)
        btn_frame.addWidget(copy_btn)
        btn_frame.addWidget(clear_btn)
        btn_frame.addWidget(speak_btn)
        layout.addLayout(btn_frame)

        # Character count
        self.char_count = QLabel("📊 کاراکتر: ۰")
        self.char_count.setStyleSheet("color: #666; font-size: 12px;")
        self.input_text.textChanged.connect(self.update_char_count)
        layout.addWidget(self.char_count)

        self.tabs.addTab(tab, "📝 ترجمه متن")

    def update_char_count(self):
        count = len(self.input_text.toPlainText())
        self.char_count.setText(f"📊 کاراکتر: {count:,}")

    def get_lang_code(self, display_text):
        for code, name in ALL_LANGUAGES.items():
            if name == display_text:
                return code
        return 'en'

    def swap_languages(self):
        from_idx = self.from_lang.currentIndex()
        to_idx = self.to_lang.currentIndex()
        self.from_lang.setCurrentIndex(to_idx)
        self.to_lang.setCurrentIndex(from_idx)
        inp = self.input_text.toPlainText()
        out = self.output_text.toPlainText()
        self.input_text.setText(out)
        self.output_text.setText(inp)

    def toggle_auto_translate(self):
        self.auto_translating = not self.auto_translating
        if self.auto_translating:
            self.input_text.textChanged.connect(self.auto_translate)
        else:
            try:
                self.input_text.textChanged.disconnect(self.auto_translate)
            except:
                pass

    def auto_translate(self):
        if self.auto_translating:
            text = self.input_text.toPlainText().strip()
            if len(text) > 3:
                self.do_translate()

    def do_translate(self):
        text = self.input_text.toPlainText().strip()
        if not text:
            self.output_text.clear()
            return

        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        self.statusBar().showMessage("⏳ در حال ترجمه...")
        QApplication.processEvents()

        if self.auto_detect_cb.isChecked():
            source = detect_language(text)
        else:
            source = self.get_lang_code(self.from_lang.currentText())

        target = self.get_lang_code(self.to_lang.currentText())

        result = translate_text(text, source, target)

        self.output_text.setText(result)
        self.progress.setVisible(False)
        self.statusBar().showMessage("✅ ترجمه کامل شد")

    def speak_translation(self):
        text = self.output_text.toPlainText().strip()
        if not text:
            return
        to_code = self.get_lang_code(self.to_lang.currentText())
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&tl={to_code}&client=gtx&q={text[:200]}"
        webbrowser.open(url)

    # ════════════════ تب ترجمه وب‌سایت ════════════════
    def website_translate_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 20, 25, 20)

        # URL input
        url_frame = QHBoxLayout()
        url_frame.addWidget(QLabel("🌐 آدرس وب‌سایت:"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        url_frame.addWidget(self.url_input)
        layout.addLayout(url_frame)

        # Language for website
        lang_frame = QHBoxLayout()
        lang_frame.addWidget(QLabel("🎯 ترجمه به:"))
        self.web_lang = QComboBox()
        self.web_lang.addItems(ALL_LANGUAGES.values())
        self.web_lang.setCurrentText('🇮🇷 فارسی')
        lang_frame.addWidget(self.web_lang)
        lang_frame.addStretch()

        translate_site_btn = QPushButton("🔄 ترجمه وب‌سایت")
        translate_site_btn.clicked.connect(self.translate_website)
        lang_frame.addWidget(translate_site_btn)
        layout.addLayout(lang_frame)

        # Quick URLs
        quick_frame = QHBoxLayout()
        quick_frame.addWidget(QLabel("⚡ سایت‌های پربازدید:"))
        quick_urls = [
            ("Wikipedia", "https://wikipedia.org"),
            ("BBC", "https://bbc.com"),
            ("CNN", "https://cnn.com"),
            ("GitHub", "https://github.com"),
            ("Stack Overflow", "https://stackoverflow.com"),
        ]
        for name, url in quick_urls:
            btn = QPushButton(name)
            btn.setStyleSheet(f"background: {GREY}; color: {BLUE}; border: 1px solid {BORDER}; padding: 8px 16px; font-size: 12px;")
            btn.clicked.connect(lambda checked, u=url: self.url_input.setText(u))
            quick_frame.addWidget(btn)
        quick_frame.addStretch()
        layout.addLayout(quick_frame)

        # Web view
        layout.addWidget(QLabel("👁️ پیش‌نمایش وب‌سایت:"))
        try:
            self.web_view = QWebEngineView()
            self.web_view.setMinimumHeight(400)
            layout.addWidget(self.web_view)
        except:
            self.web_view = None
            no_web = QTextEdit()
            no_web.setReadOnly(True)
            no_web.setPlaceholderText("⚠️ PyQtWebEngine نصب نیست. وب‌سایت در مرورگر باز می‌شود.")
            layout.addWidget(no_web)

        # Open buttons
        btn_frame = QHBoxLayout()
        open_btn = QPushButton("🌐 باز کردن در مرورگر")
        open_btn.clicked.connect(self.open_in_browser)
        translate_open_btn = QPushButton("🔄 ترجمه و باز کردن")
        translate_open_btn.setStyleSheet(f"background: {GREEN};")
        translate_open_btn.clicked.connect(self.translate_and_open)
        btn_frame.addWidget(open_btn)
        btn_frame.addWidget(translate_open_btn)
        layout.addLayout(btn_frame)

        self.tabs.addTab(tab, "🌐 ترجمه وب‌سایت")

    def translate_website(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "هشدار", "لطفاً آدرس وب‌سایت را وارد کنید")
            return

        if not url.startswith('http'):
            url = 'https://' + url

        target = self.get_lang_code(self.web_lang.currentText())
        translated_url = f"https://translate.google.com/translate?hl={target}&sl=auto&tl={target}&u={url}"

        self.url_input.setText(translated_url)

        if self.web_view:
            self.web_view.setUrl(QUrl(translated_url))
        else:
            webbrowser.open(translated_url)

        self.statusBar().showMessage(f"✅ وب‌سایت به {self.web_lang.currentText()} ترجمه شد")

    def open_in_browser(self):
        url = self.url_input.text().strip()
        if not url:
            return
        if not url.startswith('http'):
            url = 'https://' + url
        webbrowser.open(url)

    def translate_and_open(self):
        url = self.url_input.text().strip()
        if not url:
            return
        if not url.startswith('http'):
            url = 'https://' + url
        target = self.get_lang_code(self.web_lang.currentText())
        translated_url = f"https://translate.google.com/translate?hl={target}&sl=auto&tl={target}&u={url}"
        webbrowser.open(translated_url)

# ════════════════ اجرا ════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = SuperTranslatorPro()
    window.show()
    sys.exit(app.exec_())