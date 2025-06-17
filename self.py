from telethon import TelegramClient, events, functions, types, utils
import asyncio
import pytz
from datetime import datetime, timedelta
import logging
import random
import os
import sys
import re
import json
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import textwrap
from io import BytesIO
import requests
from gtts import gTTS
import jdatetime
import colorama
from colorama import Fore, Back, Style
import qrcode
import base64
import hashlib
import sqlite3
import threading
import subprocess
import psutil
import socket
import urllib.parse
import math
import statistics
import calendar
import uuid
import zipfile
import shutil
import csv
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
import tempfile
import mimetypes
import platform

# Initialize colorama for cross-platform colored terminal output
colorama.init(autoreset=True)

# ASCII Art Logo
LOGO = f"""
{Fore.CYAN}╔════════════════════════════════════════════╗
{Fore.CYAN}║ {Fore.BLUE}████████╗███████╗██╗     ███████╗██████╗  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}╚══██╔══╝██╔════╝██║     ██╔════╝██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   █████╗  ██║     █████╗  ██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   ██╔══╝  ██║     ██╔══╝  ██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ██║   ███████╗███████╗███████╗██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.BLUE}   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═════╝  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████╗███████╗██╗     ███████╗██████╗  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}██╔════╝██╔════╝██║     ██╔════╝██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████╗█████╗  ██║     █████╗  ██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}╚════██║██╔══╝  ██║     ██╔══╝  ██╔══██╗ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}███████║███████╗███████╗███████╗██████╔╝ {Fore.CYAN}║
{Fore.CYAN}║ {Fore.MAGENTA}╚══════╝╚══════╝╚══════╝╚══════╝╚═════╝  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╗  ██████╗ ████████╗               {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██╔══██╗██╔═══██╗╚══██╔══╝               {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╔╝██║   ██║   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██╔══██╗██║   ██║   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}██████╔╝╚██████╔╝   ██║                  {Fore.CYAN}║
{Fore.CYAN}║ {Fore.YELLOW}╚═════╝  ╚═════╝    ╚═╝                  {Fore.CYAN}║
{Fore.CYAN}╚════════════════════════════════════════════╝
{Fore.GREEN}        Enhanced Version 3.0 (2025) - 50+ Features
"""

# Configuration variables
CONFIG_FILE = "config.json"
LOG_FILE = "selfbot.log"
DATABASE_FILE = "selfbot.db"

# Default configuration settings
default_config = {
    "api_id": 29042268,
    "api_hash": "54a7b377dd4a04a58108639febe2f443",
    "session_name": "anon",
    "log_level": "ERROR",
    "timezone": "Asia/Tehran",
    "auto_backup": True,
    "backup_interval": 60,  # minutes
    "enemy_reply_chance": 100,  # percentage
    "enemy_auto_reply": True,
    "auto_read_messages": False,
    "allowed_users": [],
    "weather_api_key": "",
    "translate_api_key": "",
    "admin_password": "admin123",
    "auto_save_media": True,
    "max_file_size": 50,  # MB
    "enable_analytics": True,
    "auto_update": True,
    "security_mode": False,
    "custom_commands": {},
    "notification_sound": True,
    "dark_mode": True,
    "language": "fa"
}

# Global variables
enemies = set()
current_font = 'normal'
actions = {
    'typing': False,
    'online': False,
    'reaction': False,
    'read': False,
    'auto_reply': False,
    'auto_save': False,
    'ghost_mode': False,
    'anti_spam': False,
    'auto_translate': False,
    'smart_reply': False
}

# Enhanced data structures
spam_words = []
saved_messages = []
reminders = []
time_enabled = True
saved_pics = []
custom_replies = {}
blocked_words = []
last_backup_time = None
running = True
start_time = time.time()
message_stats = defaultdict(int)
user_analytics = defaultdict(dict)
scheduled_tasks = []
custom_commands = {}
chat_filters = {}
auto_responses = {}
user_notes = {}
chat_logs = defaultdict(list)
media_cache = {}
translation_cache = {}
weather_cache = {}
system_stats = {}
security_logs = []
admin_users = set()
banned_users = set()
vip_users = set()
chat_settings = defaultdict(dict)
message_templates = {}
quick_replies = {}
auto_reactions = {}
custom_fonts = {}
theme_settings = {}
notification_settings = {}
backup_schedules = []
plugin_manager = {}
api_keys = {}
webhook_urls = {}
cron_jobs = []
file_manager = {}
database_manager = None

# Command history for undo functionality
command_history = []
MAX_HISTORY = 100

locked_chats = {
    'screenshot': set(),  # Screenshot protection
    'forward': set(),     # Forward protection
    'copy': set(),        # Copy protection
    'delete': set(),      # Auto-delete messages
    'edit': set(),        # Prevent editing
    'join': set(),        # Auto-join protection
    'leave': set(),       # Auto-leave protection
    'invite': set(),      # Invite protection
    'mention': set(),     # Mention protection
    'link': set()         # Link protection
}

# Enhanced font styles
font_styles = {
    'normal': lambda text: text,
    'bold': lambda text: f"**{text}**",
    'italic': lambda text: f"__{text}__",
    'script': lambda text: f"`{text}`",
    'double': lambda text: f"```{text}```",
    'bubble': lambda text: f"||{text}||",
    'square': lambda text: f"```{text}```",
    'strikethrough': lambda text: f"~~{text}~~",
    'underline': lambda text: f"___{text}___",
    'caps': lambda text: text.upper(),
    'lowercase': lambda text: text.lower(),
    'title': lambda text: text.title(),
    'space': lambda text: " ".join(text),
    'reverse': lambda text: text[::-1],
    'zalgo': lambda text: add_zalgo_text(text),
    'leet': lambda text: to_leet_speak(text),
    'morse': lambda text: to_morse_code(text),
    'binary': lambda text: to_binary(text),
    'hex': lambda text: text.encode().hex(),
    'base64': lambda text: base64.b64encode(text.encode()).decode(),
    'rot13': lambda text: text.encode('rot13') if hasattr(text, 'encode') else text,
    'rainbow': lambda text: rainbow_text(text),
    'gradient': lambda text: gradient_text(text),
    'shadow': lambda text: f"🔲{text}🔲"
}

# Insults list - unchanged for compatibility
insults = [
    "کیرم تو کص ننت", "مادرجنده", "کص ننت", "کونی", "جنده", "کیری", "بی ناموس", "حرومزاده", "مادر قحبه", "جاکش",
    "کص ننه", "ننه جنده", "مادر کصده", "خارکصه", "کون گشاد", "ننه کیردزد", "مادر به خطا", "توله سگ", "پدر سگ", "حروم لقمه",
    "ننه الکسیس", "کص ننت میجوشه", "کیرم تو کص مادرت", "مادر جنده ی حرومی", "زنا زاده", "مادر خراب", "کصکش", "ننه سگ پرست",
    "مادرتو گاییدم", "خواهرتو گاییدم", "کیر سگ تو کص ننت", "کص مادرت", "کیر خر تو کص ننت", "کص خواهرت", "کون گشاد",
    "سیکتیر کص ننه", "ننه کیر خور", "خارکصده", "مادر جنده", "ننه خیابونی", "کیرم تو دهنت", "کص لیس", "ساک زن",
    "کیرم تو قبر ننت", "بی غیرت", "کص ننه پولی", "کیرم تو کص زنده و مردت", "مادر به خطا", "لاشی", "عوضی", "آشغال",
    "ننه کص طلا", "کیرم تو کص ننت بالا پایین", "کیر قاطر تو کص ننت", "کص ننت خونه خالی", "کیرم تو کص ننت یه دور", 
    "مادر خراب گشاد", "کیرم تو نسل اولت", "کیرم تو کص ننت محکم", "کیر خر تو کص مادرت", "کیرم تو روح مادر جندت",
    "کص ننت سفید برفی", "کیرم تو کص خارت", "کیر سگ تو کص مادرت", "کص ننه کیر خور", "کیرم تو کص زیر خواب",
    "مادر جنده ولگرد", "کیرم تو دهن مادرت", "کص مادرت گشاد", "کیرم تو لای پای مادرت", "کص ننت خیس",
    "کیرم تو کص مادرت بگردش", "کص ننه پاره", "مادر جنده حرفه ای", "کیرم تو کص و کون ننت", "کص ننه تنگ",
    "کیرم تو حلق مادرت", "ننه جنده مفت خور", "کیرم از پهنا تو کص ننت", "کص مادرت بد بو", "کیرم تو همه کس و کارت",
    "مادر کصده سیاه", "کیرم تو کص گشاد مادرت", "کص ننه ساک زن", "کیرم تو کص خاندانت", "مادر جنده خیابونی",
    "کیرم تو کص ننت یه عمر", "ننه جنده کص خور", "کیرم تو نسل و نژادت", "کص مادرت پاره", "کیرم تو شرف مادرت",
    "مادر جنده فراری", "کیرم تو روح مادرت", "کص ننه جندت", "کیرم تو غیرتت", "کص مادر بدکاره",
    "کیرم تو ننه جندت", "مادر کصده لاشی", "کیرم تو وجود مادرت", "کص ننه بی آبرو", "کیرم تو شعور ننت"
]

# Setup logging
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=LOG_FILE
)
logger = logging.getLogger("TelegramSelfBot")

# Database setup
def init_database():
    """Initialize SQLite database for enhanced features"""
    global database_manager
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        # Create tables for enhanced features
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS message_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                user_id TEXT,
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                message_type TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_analytics (
                user_id TEXT PRIMARY KEY,
                message_count INTEGER DEFAULT 0,
                last_seen DATETIME,
                first_seen DATETIME,
                total_chars INTEGER DEFAULT 0,
                avg_message_length REAL DEFAULT 0,
                most_active_hour INTEGER DEFAULT 0,
                favorite_words TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_settings (
                chat_id TEXT PRIMARY KEY,
                settings TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scheduled_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id TEXT,
                message TEXT,
                schedule_time DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS file_cache (
                file_id TEXT PRIMARY KEY,
                file_path TEXT,
                file_type TEXT,
                file_size INTEGER,
                upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                access_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        database_manager = True
        print_success("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        print_error(f"Database initialization failed: {e}")

# Enhanced utility functions
def add_zalgo_text(text):
    """Add zalgo effect to text"""
    zalgo_chars = ['̀', '́', '̂', '̃', '̄', '̅', '̆', '̇', '̈', '̉', '̊', '̋', '̌', '̍', '̎', '̏']
    result = ""
    for char in text:
        result += char
        for _ in range(random.randint(1, 3)):
            result += random.choice(zalgo_chars)
    return result

def to_leet_speak(text):
    """Convert text to leet speak"""
    leet_map = {
        'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7', 'l': '1', 'g': '9'
    }
    return ''.join(leet_map.get(char.lower(), char) for char in text)

def to_morse_code(text):
    """Convert text to morse code"""
    morse_map = {
        'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
        'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
        'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
        's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
        'y': '-.--', 'z': '--..', ' ': '/'
    }
    return ' '.join(morse_map.get(char.lower(), char) for char in text)

def to_binary(text):
    """Convert text to binary"""
    return ' '.join(format(ord(char), '08b') for char in text)

def rainbow_text(text):
    """Create rainbow colored text"""
    colors = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣']
    result = ""
    for i, char in enumerate(text):
        if char != ' ':
            result += colors[i % len(colors)] + char
        else:
            result += char
    return result

def gradient_text(text):
    """Create gradient text effect"""
    return f"🌈 {text} 🌈"

def generate_qr_code(text):
    """Generate QR code for text"""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(text)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filename = f"qr_{int(time.time())}.png"
        img.save(filename)
        return filename
    except Exception as e:
        logger.error(f"QR code generation failed: {e}")
        return None

def create_meme(top_text, bottom_text, image_path=None):
    """Create meme with text"""
    try:
        if not image_path:
            # Create a default meme background
            img = Image.new('RGB', (500, 500), color='white')
        else:
            img = Image.open(image_path)
        
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        
        # Add top text
        if top_text:
            draw.text((10, 10), top_text, font=font, fill='black')
        
        # Add bottom text
        if bottom_text:
            draw.text((10, img.height - 60), bottom_text, font=font, fill='black')
        
        filename = f"meme_{int(time.time())}.png"
        img.save(filename)
        return filename
    except Exception as e:
        logger.error(f"Meme creation failed: {e}")
        return None

def get_weather(city):
    """Get weather information for a city"""
    try:
        # This is a placeholder - you would need a real weather API
        weather_data = {
            "city": city,
            "temperature": f"{random.randint(15, 35)}°C",
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Snowy"]),
            "humidity": f"{random.randint(30, 80)}%",
            "wind": f"{random.randint(5, 25)} km/h"
        }
        return weather_data
    except Exception as e:
        logger.error(f"Weather fetch failed: {e}")
        return None

def translate_text(text, target_lang='en'):
    """Translate text to target language"""
    try:
        # This is a placeholder - you would need a real translation API
        return f"[Translated to {target_lang}]: {text}"
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        return text

def calculate_expression(expression):
    """Safely calculate mathematical expressions"""
    try:
        # Remove any potentially dangerous characters
        safe_chars = set('0123456789+-*/.() ')
        if not all(c in safe_chars for c in expression):
            return "Invalid expression"
        
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def get_system_info():
    """Get system information"""
    try:
        info = {
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "Processor": platform.processor(),
            "Python Version": platform.python_version(),
            "CPU Count": psutil.cpu_count(),
            "Memory": f"{psutil.virtual_memory().total // (1024**3)} GB",
            "Disk Usage": f"{psutil.disk_usage('/').percent}%",
            "Network": len(psutil.net_if_addrs())
        }
        return info
    except Exception as e:
        logger.error(f"System info failed: {e}")
        return {}

def create_backup_zip():
    """Create a zip backup of all data"""
    try:
        backup_name = f"selfbot_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
        with zipfile.ZipFile(backup_name, 'w') as zipf:
            # Add config files
            if os.path.exists(CONFIG_FILE):
                zipf.write(CONFIG_FILE)
            if os.path.exists("selfbot_backup.json"):
                zipf.write("selfbot_backup.json")
            if os.path.exists(DATABASE_FILE):
                zipf.write(DATABASE_FILE)
            
            # Add saved pictures
            for pic in saved_pics:
                if os.path.exists(pic):
                    zipf.write(pic)
        
        return backup_name
    except Exception as e:
        logger.error(f"Backup zip creation failed: {e}")
        return None

def analyze_chat_activity(chat_id):
    """Analyze chat activity and return statistics"""
    try:
        if chat_id not in chat_logs:
            return "No data available for this chat"
        
        messages = chat_logs[chat_id]
        total_messages = len(messages)
        
        if total_messages == 0:
            return "No messages in this chat"
        
        # Calculate statistics
        word_count = sum(len(msg.split()) for msg in messages)
        avg_words = word_count / total_messages
        
        # Most common words
        all_words = ' '.join(messages).lower().split()
        word_freq = Counter(all_words)
        common_words = word_freq.most_common(5)
        
        stats = f"""
📊 Chat Activity Analysis:
• Total Messages: {total_messages}
• Total Words: {word_count}
• Average Words per Message: {avg_words:.2f}
• Most Common Words: {', '.join([f'{word}({count})' for word, count in common_words])}
        """
        return stats
    except Exception as e:
        logger.error(f"Chat analysis failed: {e}")
        return "Analysis failed"

def create_word_cloud(text):
    """Create word cloud from text"""
    try:
        # This would require wordcloud library
        # For now, return a simple word frequency analysis
        words = text.lower().split()
        word_freq = Counter(words)
        top_words = word_freq.most_common(10)
        
        result = "🔤 Word Frequency:\n"
        for word, count in top_words:
            result += f"• {word}: {count}\n"
        
        return result
    except Exception as e:
        logger.error(f"Word cloud creation failed: {e}")
        return "Word cloud creation failed"

def generate_password(length=12):
    """Generate a secure password"""
    import string
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def hash_text(text, algorithm='sha256'):
    """Hash text using specified algorithm"""
    try:
        if algorithm == 'md5':
            return hashlib.md5(text.encode()).hexdigest()
        elif algorithm == 'sha1':
            return hashlib.sha1(text.encode()).hexdigest()
        elif algorithm == 'sha256':
            return hashlib.sha256(text.encode()).hexdigest()
        else:
            return "Unsupported algorithm"
    except Exception as e:
        return f"Hashing failed: {e}"

def get_file_info(file_path):
    """Get detailed file information"""
    try:
        if not os.path.exists(file_path):
            return "File not found"
        
        stat = os.stat(file_path)
        info = {
            "Size": f"{stat.st_size} bytes",
            "Created": datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            "Modified": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            "Type": mimetypes.guess_type(file_path)[0] or "Unknown"
        }
        return info
    except Exception as e:
        return f"File info failed: {e}"

def create_ascii_art(text):
    """Create ASCII art from text"""
    try:
        # Simple ASCII art generator
        art_chars = {
            'A': ['  ▄▀█  ', ' █▀▀█ ', ' ▀ ▀▀ '],
            'B': [' █▀▀▄ ', ' █▀▀▄ ', ' ▀▀▀  '],
            'C': [' ▄▀█▀▄', ' █   ', ' ▀▄█▄▀'],
            # Add more characters as needed
        }
        
        result = ""
        for char in text.upper():
            if char in art_chars:
                for line in art_chars[char]:
                    result += line + "\n"
            else:
                result += f" {char} \n"
        
        return result
    except Exception as e:
        return f"ASCII art failed: {e}"

def get_crypto_price(symbol):
    """Get cryptocurrency price (placeholder)"""
    try:
        # This would require a real crypto API
        prices = {
            'BTC': f"${random.randint(40000, 70000)}",
            'ETH': f"${random.randint(2000, 4000)}",
            'ADA': f"${random.uniform(0.3, 1.5):.2f}",
            'DOGE': f"${random.uniform(0.05, 0.3):.3f}"
        }
        return prices.get(symbol.upper(), "Symbol not found")
    except Exception as e:
        return f"Price fetch failed: {e}"

def create_poll_data(question, options):
    """Create poll data structure"""
    poll_id = str(uuid.uuid4())
    poll_data = {
        'id': poll_id,
        'question': question,
        'options': options,
        'votes': {option: 0 for option in options},
        'voters': set(),
        'created_at': datetime.now().isoformat()
    }
    return poll_data

def compress_image(image_path, quality=85):
    """Compress image file"""
    try:
        img = Image.open(image_path)
        compressed_path = f"compressed_{int(time.time())}.jpg"
        img.save(compressed_path, "JPEG", quality=quality, optimize=True)
        return compressed_path
    except Exception as e:
        logger.error(f"Image compression failed: {e}")
        return None

def create_collage(image_paths):
    """Create a collage from multiple images"""
    try:
        if len(image_paths) < 2:
            return None
        
        images = [Image.open(path) for path in image_paths[:4]]  # Max 4 images
        
        # Resize images to same size
        size = (200, 200)
        images = [img.resize(size) for img in images]
        
        # Create collage
        if len(images) == 2:
            collage = Image.new('RGB', (400, 200))
            collage.paste(images[0], (0, 0))
            collage.paste(images[1], (200, 0))
        elif len(images) == 3:
            collage = Image.new('RGB', (400, 400))
            collage.paste(images[0], (0, 0))
            collage.paste(images[1], (200, 0))
            collage.paste(images[2], (100, 200))
        else:  # 4 images
            collage = Image.new('RGB', (400, 400))
            collage.paste(images[0], (0, 0))
            collage.paste(images[1], (200, 0))
            collage.paste(images[2], (0, 200))
            collage.paste(images[3], (200, 200))
        
        filename = f"collage_{int(time.time())}.jpg"
        collage.save(filename)
        return filename
    except Exception as e:
        logger.error(f"Collage creation failed: {e}")
        return None

def apply_image_filter(image_path, filter_type):
    """Apply filters to image"""
    try:
        img = Image.open(image_path)
        
        if filter_type == 'blur':
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'sharpen':
            img = img.filter(ImageFilter.SHARPEN)
        elif filter_type == 'emboss':
            img = img.filter(ImageFilter.EMBOSS)
        elif filter_type == 'edge':
            img = img.filter(ImageFilter.FIND_EDGES)
        elif filter_type == 'smooth':
            img = img.filter(ImageFilter.SMOOTH)
        elif filter_type == 'brightness':
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(1.5)
        elif filter_type == 'contrast':
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.5)
        elif filter_type == 'grayscale':
            img = img.convert('L')
        
        filename = f"filtered_{filter_type}_{int(time.time())}.jpg"
        img.save(filename)
        return filename
    except Exception as e:
        logger.error(f"Image filter failed: {e}")
        return None

# Convert numbers to superscript
def to_superscript(num):
    superscripts = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹'
    }
    return ''.join(superscripts.get(n, n) for n in str(num))

# Pretty print functions
def print_header(text):
    """Print a header with decoration"""
    width = len(text) + 4
    print(f"\n{Fore.CYAN}{'═' * width}")
    print(f"{Fore.CYAN}║ {Fore.WHITE}{text} {Fore.CYAN}║")
    print(f"{Fore.CYAN}{'═' * width}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}")

def print_warning(text):
    """Print warning message"""
    print(f"{Fore.YELLOW}⚠️ {text}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.BLUE}ℹ️ {text}")

def print_status(label, status, active=True):
    """Print a status item with colored indicator"""
    status_color = Fore.GREEN if active else Fore.RED
    status_icon = "✅" if active else "❌"
    print(f"{Fore.WHITE}{label}: {status_color}{status_icon} {status}")

def print_loading(text="Loading", cycles=3):
    """Display a loading animation"""
    animations = [".  ", ".. ", "..."]
    for _ in range(cycles):
        for animation in animations:
            sys.stdout.write(f"\r{Fore.YELLOW}{text} {animation}")
            sys.stdout.flush()
            time.sleep(0.3)
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")
    sys.stdout.flush()

def print_progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    """Call in a loop to create terminal progress bar"""
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '░' * (length - filled_length)
    sys.stdout.write(f'\r{Fore.BLUE}{prefix} |{Fore.CYAN}{bar}{Fore.BLUE}| {percent}% {suffix}')
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

# Config management functions
def load_config():
    """Load configuration from file or create default"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                # Update with any missing keys from default config
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            print_error(f"Failed to load config: {e}")
            return default_config
    else:
        save_config(default_config)
        return default_config

def save_config(config):
    """Save configuration to file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)
        return True
    except Exception as e:
        print_error(f"Failed to save config: {e}")
        return False

# Data backup functions
def backup_data():
    """Backup all user data to file"""
    global last_backup_time
    backup_data_dict = {
        "enemies": list(enemies),
        "current_font": current_font,
        "actions": actions,
        "spam_words": spam_words,
        "saved_messages": saved_messages,
        "reminders": reminders,
        "time_enabled": time_enabled,
        "saved_pics": saved_pics,
        "custom_replies": custom_replies,
        "blocked_words": blocked_words,
        "locked_chats": {k: list(v) for k, v in locked_chats.items()},
        "message_stats": dict(message_stats),
        "user_analytics": dict(user_analytics),
        "custom_commands": custom_commands,
        "chat_filters": chat_filters,
        "auto_responses": auto_responses,
        "user_notes": user_notes,
        "message_templates": message_templates,
        "quick_replies": quick_replies,
        "auto_reactions": auto_reactions,
        "admin_users": list(admin_users),
        "banned_users": list(banned_users),
        "vip_users": list(vip_users),
        "backup_timestamp": datetime.now().isoformat()
    }
    
    try:
        with open("selfbot_backup.json", 'w') as f:
            json.dump(backup_data_dict, f, indent=4)
        last_backup_time = datetime.now()
        return True
    except Exception as e:
        logger.error(f"Backup failed: {e}")
        return False

def restore_data():
    """Restore user data from backup file"""
    global enemies, current_font, actions, spam_words, saved_messages, reminders
    global time_enabled, saved_pics, custom_replies, blocked_words, locked_chats
    global message_stats, user_analytics, custom_commands, chat_filters, auto_responses
    global user_notes, message_templates, quick_replies, auto_reactions
    global admin_users, banned_users, vip_users
    
    if not os.path.exists("selfbot_backup.json"):
        return False
    
    try:
        with open("selfbot_backup.json", 'r') as f:
            data = json.load(f)
            
        enemies = set(data.get("enemies", []))
        current_font = data.get("current_font", "normal")
        actions.update(data.get("actions", {}))
        spam_words = data.get("spam_words", [])
        saved_messages = data.get("saved_messages", [])
        reminders = data.get("reminders", [])
        time_enabled = data.get("time_enabled", True)
        saved_pics = data.get("saved_pics", [])
        custom_replies = data.get("custom_replies", {})
        blocked_words = data.get("blocked_words", [])
        
        # Restore locked_chats as sets
        locked_chats_data = data.get("locked_chats", {})
        for key, value in locked_chats_data.items():
            if key in locked_chats:
                locked_chats[key] = set(value)
        
        # Restore enhanced features
        message_stats.update(data.get("message_stats", {}))
        user_analytics.update(data.get("user_analytics", {}))
        custom_commands.update(data.get("custom_commands", {}))
        chat_filters.update(data.get("chat_filters", {}))
        auto_responses.update(data.get("auto_responses", {}))
        user_notes.update(data.get("user_notes", {}))
        message_templates.update(data.get("message_templates", {}))
        quick_replies.update(data.get("quick_replies", {}))
        auto_reactions.update(data.get("auto_reactions", {}))
        admin_users.update(data.get("admin_users", []))
        banned_users.update(data.get("banned_users", []))
        vip_users.update(data.get("vip_users", []))
                
        return True
    except Exception as e:
        logger.error(f"Restore failed: {e}")
        return False

# Enhanced utility functions
async def text_to_voice(text, lang='fa'):
    """Convert text to voice file with progress indicators"""
    print_info("Converting text to voice...")
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"voice_{int(time.time())}.mp3"
        tts.save(filename)
        print_success("Voice file created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to voice: {e}")
        print_error(f"Failed to convert text to voice: {e}")
        return None

async def text_to_image(text, bg_color='white', text_color='black'):
    """Convert text to image with enhanced customization"""
    print_info("Creating image from text...")
    try:
        width = 800
        height = max(400, len(text) // 20 * 50)  # Dynamic height based on text length
        img = Image.new('RGB', (width, height), color=bg_color)
        draw = ImageDraw.Draw(img)
        
        font_size = 40
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            # Fallback to default
            font = ImageFont.load_default()
        
        lines = textwrap.wrap(text, width=30)
        y = 50
        for i, line in enumerate(lines):
            print_progress_bar(i + 1, len(lines), 'Progress:', 'Complete', 20)
            draw.text((50, y), line, font=font, fill=text_color)
            y += font_size + 10
            
        filename = f"text_{int(time.time())}.png"
        img.save(filename)
        print_success("Image created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to image: {e}")
        print_error(f"Failed to convert text to image: {e}")
        return None

async def text_to_gif(text, duration=500, bg_color='white'):
    """Convert text to animated GIF with customization"""
    print_info("Creating GIF from text...")
    try:
        width = 800
        height = 400
        frames = []
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except IOError:
            font = ImageFont.load_default()
        
        for i, color in enumerate(colors):
            print_progress_bar(i + 1, len(colors), 'Creating frames:', 'Complete', 20)
            img = Image.new('RGB', (width, height), color=bg_color)
            draw = ImageDraw.Draw(img)
            draw.text((50, 150), text, font=font, fill=color)
            frames.append(img)
        
        filename = f"text_{int(time.time())}.gif"
        frames[0].save(
            filename,
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=0
        )
        print_success("GIF created successfully")
        return filename
    except Exception as e:
        logger.error(f"Error in text to gif: {e}")
        print_error(f"Failed to convert text to GIF: {e}")
        return None

async def update_time(client):
    """Update the last name with current time"""
    while running:
        try:
            if time_enabled:
                config = load_config()
                now = datetime.now(pytz.timezone(config['timezone']))
                hours = to_superscript(now.strftime('%H'))
                minutes = to_superscript(now.strftime('%M'))
                time_string = f"{hours}:{minutes}"
                await client(functions.account.UpdateProfileRequest(last_name=time_string))
        except Exception as e:
            logger.error(f'Error updating time: {e}')
        await asyncio.sleep(60)

async def auto_online(client):
    """Keep user online automatically"""
    while running and actions['online']:
        try:
            await client(functions.account.UpdateStatusRequest(offline=False))
        except Exception as e:
            logger.error(f'Error updating online status: {e}')
        await asyncio.sleep(30)

async def auto_typing(client, chat):
    """Maintain typing status in chat"""
    while running and actions['typing']:
        try:
            async with client.action(chat, 'typing'):
                await asyncio.sleep(3)
        except Exception as e:
            logger.error(f'Error in typing action: {e}')
            break

async def auto_reaction(event):
    """Add automatic reaction to messages"""
    if actions['reaction']:
        try:
            reactions = ['👍', '❤️', '😂', '😮', '😢', '🔥', '👏']
            await event.message.react(random.choice(reactions))
        except Exception as e:
            logger.error(f'Error adding reaction: {e}')

async def auto_read_messages(event, client):
    """Mark messages as read automatically"""
    if actions['read']:
        try:
            await client.send_read_acknowledge(event.chat_id, event.message)
        except Exception as e:
            logger.error(f'Error marking message as read: {e}')

async def schedule_message(client, chat_id, delay, message):
    """Schedule message sending with countdown"""
    print_info(f"Message scheduled to send in {delay} minutes")
    for i in range(delay):
        remaining = delay - i
        if remaining % 5 == 0 or remaining <= 5:  # Show updates every 5 minutes or in final countdown
            logger.info(f"Scheduled message will send in {remaining} minutes")
        await asyncio.sleep(60)
    
    try:
        await client.send_message(chat_id, message)
        print_success(f"Scheduled message sent: {message[:30]}...")
        return True
    except Exception as e:
        logger.error(f"Failed to send scheduled message: {e}")
        print_error(f"Failed to send scheduled message: {e}")
        return False

async def spam_messages(client, chat_id, count, message):
    """Send multiple messages in sequence with progress indicators"""
    print_info(f"Sending {count} messages...")
    success_count = 0
    
    for i in range(count):
        try:
            await client.send_message(chat_id, message)
            success_count += 1
            print_progress_bar(i + 1, count, 'Sending:', 'Complete', 20)
            await asyncio.sleep(0.5)
        except Exception as e:
            logger.error(f"Error in spam message {i+1}: {e}")
    
    print_success(f"Successfully sent {success_count}/{count} messages")
    return success_count

async def check_reminders(client):
    """Check and send reminders"""
    while running:
        current_time = datetime.now().strftime('%H:%M')
        to_remove = []
        
        for i, (reminder_time, message, chat_id) in enumerate(reminders):
            if reminder_time == current_time:
                try:
                    await client.send_message(chat_id, f"🔔 یادآوری: {message}")
                    to_remove.append(i)
                except Exception as e:
                    logger.error(f"Failed to send reminder: {e}")
        
        # Remove sent reminders
        for i in sorted(to_remove, reverse=True):
            del reminders[i]
            
        await asyncio.sleep(30)  # Check every 30 seconds

async def auto_backup(client):
    """Automatically backup data at intervals"""
    config = load_config()
    if not config['auto_backup']:
        return
        
    interval = config['backup_interval'] * 60  # Convert to seconds
    
    while running:
        await asyncio.sleep(interval)
        if backup_data():
            logger.info("Auto-backup completed successfully")
        else:
            logger.error("Auto-backup failed")

async def handle_anti_delete(event):
    """Save deleted messages for anti-delete feature"""
    chat_id = str(event.chat_id)
    if chat_id in locked_chats['delete'] and event.message:
        try:
            # Save message info before it's deleted
            msg = event.message
            sender = await event.get_sender()
            sender_name = utils.get_display_name(sender) if sender else "Unknown"
            
            saved_text = f"🔴 Deleted message from {sender_name}:\n{msg.text}"
            await event.reply(saved_text)
            return True
        except Exception as e:
            logger.error(f"Error in anti-delete: {e}")
    return False

async def show_help_menu(client, event):
    """Show enhanced help menu with categories"""
    help_text = """
📱 راهنمای ربات سلف بات نسخه 3.0 - 50+ قابلیت:

⚙️ تنظیمات دشمن:
• تنظیم دشمن (ریپلای) - اضافه کردن به لیست دشمن
• حذف دشمن (ریپلای) - حذف از لیست دشمن  
• لیست دشمن - نمایش لیست دشمنان
• insult [on/off] - فعال/غیرفعال کردن پاسخ خودکار به دشمن

🔤 فونت ها:
• bold/italic/script/double/bubble/square/strikethrough/underline on/off
• caps/lowercase/title/space/reverse/zalgo/leet/morse/binary on/off
• hex/base64/rot13/rainbow/gradient/shadow on/off

⚡️ اکشن های خودکار:
• typing/online/reaction/time/read/reply on/off
• ghost/anti_spam/auto_translate/smart_reply on/off

🔒 قفل‌ها:
• screenshot/forward/copy/delete/edit/join/leave/invite/mention/link on/off

🎨 تبدیل‌ها:
• متن به ویس بگو [متن] - تبدیل متن به ویس
• متن به عکس [متن] - تبدیل متن به عکس  
• متن به گیف [متن] - تبدیل متن به گیف
• qr [متن] - ساخت QR کد
• meme [متن بالا] | [متن پایین] - ساخت میم
• ascii [متن] - تبدیل به ASCII Art
• hash [متن] [الگوریتم] - هش کردن متن
• compress pic (ریپلای) - فشرده سازی عکس
• filter [نوع] (ریپلای) - اعمال فیلتر به عکس
• collage - ساخت کولاژ از عکس‌ها

📊 آنالیز و آمار:
• stats - آمار کامل ربات
• chat stats - آمار چت فعلی
• user stats [یوزر] - آمار کاربر
• word cloud - ابر کلمات
• analytics - تحلیل پیشرفته

🛠 ابزارهای کاربردی:
• calc [عبارت] - ماشین حساب
• weather [شهر] - آب و هوا
• translate [متن] [زبان] - ترجمه
• crypto [نماد] - قیمت ارز دیجیتال
• sysinfo - اطلاعات سیستم
• password [طول] - تولید رمز عبور
• ping [آدرس] - پینگ سرور
• ip - نمایش IP
• speed test - تست سرعت اینترنت

💾 مدیریت فایل:
• save pic/video/file - ذخیره فایل
• show files - نمایش فایل‌های ذخیره شده
• file info [نام] - اطلاعات فایل
• backup zip - ساخت فایل پشتیبان
• clean cache - پاک کردن کش

👥 مدیریت کاربران:
• add admin [یوزر] - اضافه کردن ادمین
• ban user [یوزر] - مسدود کردن کاربر
• vip user [یوزر] - اضافه کردن VIP
• user note [یوزر] [یادداشت] - یادداشت کاربر
• user list [نوع] - لیست کاربران

🤖 هوش مصنوعی:
• smart reply on/off - پاسخ هوشمند
• auto learn on/off - یادگیری خودکار
• chat bot [پیام] - چت بات
• sentiment [متن] - تحلیل احساسات

🎮 سرگرمی:
• dice - تاس
• coin - سکه
• random [حداقل] [حداکثر] - عدد تصادفی
• joke - جوک
• quote - نقل قول
• fact - حقیقت جالب
• riddle - معما

⏰ زمان‌بندی:
• schedule [دقیقه] [پیام] - پیام زمان‌دار
• remind [زمان] [پیام] - یادآور
• timer [ثانیه] - تایمر
• alarm [زمان] - زنگ هشدار
• cron [زمان] [دستور] - کرون جاب

🔍 جستجو و فیلتر:
• search [متن] - جستجو در پیام‌ها
• filter add [کلمه] - اضافه کردن فیلتر
• filter remove [کلمه] - حذف فیلتر
• find user [نام] - پیدا کردن کاربر
• history [تعداد] - تاریخچه پیام‌ها

📝 قابلیت های دیگر:
• template add [نام] [متن] - اضافه کردن قالب
• template use [نام] - استفاده از قالب
• quick [نام] [پاسخ] - پاسخ سریع
• macro [نام] [دستورات] - ماکرو
• webhook [url] - وب‌هوک
• api [endpoint] - فراخوانی API
• log [متن] - ثبت لاگ
• export data - صادرات داده‌ها
• import data - وارد کردن داده‌ها
• security mode on/off - حالت امنیتی

🎛 تنظیمات پیشرفته:
• config [کلید] [مقدار] - تنظیمات
• theme [نام] - تغییر تم
• language [کد] - تغییر زبان
• notification on/off - اعلان‌ها
• debug on/off - حالت دیباگ
• performance - عملکرد سیستم
• memory usage - مصرف حافظه
• cleanup - پاکسازی
• reset - بازنشانی
• update - بروزرسانی

📋 دستورات اضافی:
• help [دسته] - راهنمای دسته‌بندی شده
• commands - لیست تمام دستورات
• shortcuts - میانبرها
• examples - نمونه‌ها
• tips - نکات کاربردی
• changelog - تغییرات نسخه
• about - درباره ربات
• contact - تماس با سازنده
• donate - حمایت مالی
• feedback - بازخورد

استفاده: فقط دستور مورد نظر را تایپ کنید!
"""
    try:
        await event.edit(help_text)
    except:
        print(help_text)

async def show_status(client, event):
    """Show enhanced bot status with detailed information"""
    try:
        # Measure ping
        start_ping = time.time()
        await client(functions.PingRequest(ping_id=0))
        end_ping = time.time()
        ping = round((end_ping - start_ping) * 1000, 2)

        # Get time information
        config = load_config()
        tz = pytz.timezone(config['timezone'])
        now = datetime.now(tz)
        
        # Jalali date for Iran
        j_date = jdatetime.datetime.fromgregorian(datetime=now)
        jalali_date = j_date.strftime('%Y/%m/%d')
        local_time = now.strftime('%H:%M:%S')

        # Calculate uptime
        uptime_seconds = int(time.time() - start_time)
        uptime = str(timedelta(seconds=uptime_seconds))

        # Memory usage
        try:
            process = psutil.Process(os.getpid())
            memory_usage = f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
            cpu_usage = f"{process.cpu_percent():.1f}%"
        except ImportError:
            memory_usage = "N/A"
            cpu_usage = "N/A"

        # System info
        system_info = get_system_info()

        status_text = f"""
⚡️ وضعیت ربات سلف بات نسخه 3.0

📊 اطلاعات سیستم:
• پینگ: {ping} ms
• زمان کارکرد: {uptime}
• مصرف حافظه: {memory_usage}
• مصرف CPU: {cpu_usage}
• سیستم عامل: {system_info.get('OS', 'Unknown')}
• آخرین پشتیبان‌گیری: {last_backup_time.strftime('%Y/%m/%d %H:%M') if last_backup_time else 'هیچوقت'}

📅 اطلاعات زمانی:
• تاریخ شمسی: {jalali_date}
• ساعت: {local_time}
• منطقه زمانی: {config['timezone']}

💡 وضعیت قابلیت‌ها:
• تایپینگ: {'✅' if actions['typing'] else '❌'}
• آنلاین: {'✅' if actions['online'] else '❌'} 
• ری‌اکشن: {'✅' if actions['reaction'] else '❌'}
• ساعت: {'✅' if time_enabled else '❌'}
• خواندن خودکار: {'✅' if actions['read'] else '❌'}
• پاسخ خودکار: {'✅' if actions['auto_reply'] else '❌'}
• حالت شبح: {'✅' if actions['ghost_mode'] else '❌'}
• ضد اسپم: {'✅' if actions['anti_spam'] else '❌'}
• ترجمه خودکار: {'✅' if actions['auto_translate'] else '❌'}
• پاسخ هوشمند: {'✅' if actions['smart_reply'] else '❌'}

📌 آمار:
• تعداد دشمنان: {len(enemies)}
• پیام‌های ذخیره شده: {len(saved_messages)}
• یادآوری‌ها: {len(reminders)}
• کلمات مسدود شده: {len(blocked_words)}
• پاسخ‌های خودکار: {len(custom_replies)}
• دستورات سفارشی: {len(custom_commands)}
• قالب‌های پیام: {len(message_templates)}
• پاسخ‌های سریع: {len(quick_replies)}
• کاربران ادمین: {len(admin_users)}
• کاربران مسدود: {len(banned_users)}
• کاربران VIP: {len(vip_users)}

🔒 قفل‌های فعال:
• اسکرین‌شات: {len(locked_chats['screenshot'])}
• فوروارد: {len(locked_chats['forward'])}
• کپی: {len(locked_chats['copy'])}
• ضد حذف: {len(locked_chats['delete'])}
• ضد ویرایش: {len(locked_chats['edit'])}
• ضد عضویت: {len(locked_chats['join'])}
• ضد خروج: {len(locked_chats['leave'])}
• ضد دعوت: {len(locked_chats['invite'])}
• ضد منشن: {len(locked_chats['mention'])}
• ضد لینک: {len(locked_chats['link'])}

💾 حافظه و فایل‌ها:
• عکس‌های ذخیره شده: {len(saved_pics)}
• فایل‌های کش: {len(media_cache)}
• کش ترجمه: {len(translation_cache)}
• کش آب و هوا: {len(weather_cache)}

🔧 تنظیمات فعال:
• پشتیبان‌گیری خودکار: {'✅' if config.get('auto_backup', False) else '❌'}
• ذخیره خودکار رسانه: {'✅' if config.get('auto_save_media', False) else '❌'}
• حالت امنیتی: {'✅' if config.get('security_mode', False) else '❌'}
• آنالیز فعال: {'✅' if config.get('enable_analytics', False) else '❌'}
• بروزرسانی خودکار: {'✅' if config.get('auto_update', False) else '❌'}
• صدای اعلان: {'✅' if config.get('notification_sound', False) else '❌'}
"""
        await event.edit(status_text)
    except Exception as e:
        logger.error(f"Error in status handler: {e}")
        print_error(f"Error showing status: {e}")

async def main():
    """Main function with enhanced UI and error handling"""
    # Print logo and initialize
    print(LOGO)
    print_header("Initializing Enhanced Telegram Self-Bot v3.0")
    
    # Initialize database
    init_database()
    
    # Load configuration
    config = load_config()
    print_info(f"Configuration loaded from {CONFIG_FILE}")
    
    # Setup logging
    log_level = getattr(logging, config['log_level'])
    logging.basicConfig(level=log_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', filename=LOG_FILE)
    
    # Restore data if available
    if os.path.exists("selfbot_backup.json"):
        if restore_data():
            print_success("Data restored from backup")
        else:
            print_warning("Failed to restore data from backup")
    
    # Initialize client with animated progress
    print_loading("Connecting to Telegram")
    client = TelegramClient(config['session_name'], config['api_id'], config['api_hash'])
    
    try:
        # Connect to Telegram
        await client.connect()
        print_success("Connected to Telegram")
        
        # Check authorization
        if not await client.is_user_authorized():
            print_header("Authentication Required")
            print("Please enter your phone number (e.g., +989123456789):")
            phone = input(f"{Fore.GREEN}> ")
            
            try:
                print_loading("Sending verification code")
                await client.send_code_request(phone)
                print_success("Verification code sent")
                
                print("\nPlease enter the verification code:")
                code = input(f"{Fore.GREEN}> ")
                
                print_loading("Verifying code")
                await client.sign_in(phone, code)
                print_success("Verification successful")
                
            except Exception as e:
                if "two-steps verification" in str(e).lower():
                    print_warning("Two-step verification is enabled")
                    print("Please enter your password:")
                    password = input(f"{Fore.GREEN}> ")
                    
                    print_loading("Verifying password")
                    await client.sign_in(password=password)
                    print_success("Password verification successful")
                else:
                    print_error(f"Login error: {str(e)}")
                    return
        
        # Successfully logged in
        me = await client.get_me()
        print_success(f"Logged in as: {me.first_name} {me.last_name or ''} (@{me.username or 'No username'})")
        print_info("Enhanced Self-bot v3.0 is now active! Type 'پنل' in any chat to see 50+ commands.")
        
        # Start background tasks
        asyncio.create_task(update_time(client))
        asyncio.create_task(check_reminders(client))
        asyncio.create_task(auto_backup(client))
        
        # Enhanced Event handlers with 50+ new features
        
        # Original handlers (preserved)
        @client.on(events.NewMessage(pattern=r'^time (on|off)$'))
        async def time_handler(event):
            global time_enabled
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                time_enabled = (status == 'on')
                if not time_enabled:
                    await client(functions.account.UpdateProfileRequest(last_name=''))
                
                command_history.append(('time', not time_enabled))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                await event.edit(f"✅ نمایش ساعت {'فعال' if time_enabled else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in time handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^insult (on|off)$'))
        async def insult_toggle_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                status = event.pattern_match.group(1)
                config = load_config()
                config['enemy_auto_reply'] = (status == 'on')
                save_config(config)
                
                await event.edit(f"✅ پاسخ خودکار به دشمن {'فعال' if config['enemy_auto_reply'] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in insult toggle handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 1: QR Code Generator
        @client.on(events.NewMessage(pattern=r'^qr (.+)$'))
        async def qr_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                await event.edit("⏳ در حال ساخت QR کد...")
                
                qr_file = generate_qr_code(text)
                if qr_file:
                    await event.delete()
                    await client.send_file(event.chat_id, qr_file, caption=f"QR Code for: {text}")
                    os.remove(qr_file)
                else:
                    await event.edit("❌ خطا در ساخت QR کد")
            except Exception as e:
                logger.error(f"Error in QR handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 2: Meme Generator
        @client.on(events.NewMessage(pattern=r'^meme (.+)$'))
        async def meme_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                parts = text.split('|')
                top_text = parts[0].strip() if len(parts) > 0 else ""
                bottom_text = parts[1].strip() if len(parts) > 1 else ""
                
                await event.edit("⏳ در حال ساخت میم...")
                
                meme_file = create_meme(top_text, bottom_text)
                if meme_file:
                    await event.delete()
                    await client.send_file(event.chat_id, meme_file)
                    os.remove(meme_file)
                else:
                    await event.edit("❌ خطا در ساخت میم")
            except Exception as e:
                logger.error(f"Error in meme handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 3: Calculator
        @client.on(events.NewMessage(pattern=r'^calc (.+)$'))
        async def calc_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                expression = event.pattern_match.group(1)
                result = calculate_expression(expression)
                await event.edit(f"🧮 {expression} = {result}")
            except Exception as e:
                logger.error(f"Error in calc handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 4: Weather
        @client.on(events.NewMessage(pattern=r'^weather (.+)$'))
        async def weather_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                city = event.pattern_match.group(1)
                await event.edit(f"⏳ در حال دریافت آب و هوای {city}...")
                
                weather_data = get_weather(city)
                if weather_data:
                    weather_text = f"""
🌤 آب و هوای {weather_data['city']}:
🌡 دما: {weather_data['temperature']}
☁️ وضعیت: {weather_data['condition']}
💧 رطوبت: {weather_data['humidity']}
💨 باد: {weather_data['wind']}
                    """
                    await event.edit(weather_text)
                else:
                    await event.edit("❌ خطا در دریافت آب و هوا")
            except Exception as e:
                logger.error(f"Error in weather handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 5: Translation
        @client.on(events.NewMessage(pattern=r'^translate (.+) (.+)$'))
        async def translate_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                target_lang = event.pattern_match.group(2)
                
                await event.edit("⏳ در حال ترجمه...")
                translated = translate_text(text, target_lang)
                await event.edit(f"🔤 ترجمه:\n{translated}")
            except Exception as e:
                logger.error(f"Error in translate handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 6: System Info
        @client.on(events.NewMessage(pattern='^sysinfo$'))
        async def sysinfo_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال دریافت اطلاعات سیستم...")
                
                info = get_system_info()
                info_text = "💻 اطلاعات سیستم:\n"
                for key, value in info.items():
                    info_text += f"• {key}: {value}\n"
                
                await event.edit(info_text)
            except Exception as e:
                logger.error(f"Error in sysinfo handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 7: Password Generator
        @client.on(events.NewMessage(pattern=r'^password (\d+)$'))
        async def password_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                length = int(event.pattern_match.group(1))
                if length > 50:
                    await event.edit("❌ حداکثر طول رمز عبور 50 کاراکتر است")
                    return
                
                password = generate_password(length)
                await event.edit(f"🔐 رمز عبور تولید شده:\n`{password}`")
            except Exception as e:
                logger.error(f"Error in password handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 8: Hash Generator
        @client.on(events.NewMessage(pattern=r'^hash (.+) (.+)$'))
        async def hash_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                algorithm = event.pattern_match.group(2)
                
                hashed = hash_text(text, algorithm)
                await event.edit(f"🔐 Hash ({algorithm}):\n`{hashed}`")
            except Exception as e:
                logger.error(f"Error in hash handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 9: ASCII Art
        @client.on(events.NewMessage(pattern=r'^ascii (.+)$'))
        async def ascii_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                ascii_art = create_ascii_art(text)
                await event.edit(f"```\n{ascii_art}\n```")
            except Exception as e:
                logger.error(f"Error in ASCII handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 10: Crypto Prices
        @client.on(events.NewMessage(pattern=r'^crypto (.+)$'))
        async def crypto_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                symbol = event.pattern_match.group(1)
                price = get_crypto_price(symbol)
                await event.edit(f"💰 قیمت {symbol.upper()}: {price}")
            except Exception as e:
                logger.error(f"Error in crypto handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 11: Dice Roll
        @client.on(events.NewMessage(pattern='^dice$'))
        async def dice_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                result = random.randint(1, 6)
                dice_emoji = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'][result-1]
                await event.edit(f"🎲 تاس: {dice_emoji} ({result})")
            except Exception as e:
                logger.error(f"Error in dice handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 12: Coin Flip
        @client.on(events.NewMessage(pattern='^coin$'))
        async def coin_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                result = random.choice(['شیر', 'خط'])
                emoji = '🦅' if result == 'شیر' else '🪙'
                await event.edit(f"🪙 سکه: {emoji} {result}")
            except Exception as e:
                logger.error(f"Error in coin handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 13: Random Number
        @client.on(events.NewMessage(pattern=r'^random (\d+) (\d+)$'))
        async def random_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                min_num = int(event.pattern_match.group(1))
                max_num = int(event.pattern_match.group(2))
                
                if min_num > max_num:
                    min_num, max_num = max_num, min_num
                
                result = random.randint(min_num, max_num)
                await event.edit(f"🎲 عدد تصادفی بین {min_num} و {max_num}: {result}")
            except Exception as e:
                logger.error(f"Error in random handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 14: Chat Statistics
        @client.on(events.NewMessage(pattern='^chat stats$'))
        async def chat_stats_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال تحلیل آمار چت...")
                stats = analyze_chat_activity(str(event.chat_id))
                await event.edit(stats)
            except Exception as e:
                logger.error(f"Error in chat stats handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 15: Word Cloud
        @client.on(events.NewMessage(pattern='^word cloud$'))
        async def wordcloud_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if str(event.chat_id) not in chat_logs:
                    await event.edit("❌ داده‌ای برای این چت موجود نیست")
                    return
                
                text = ' '.join(chat_logs[str(event.chat_id)])
                word_cloud = create_word_cloud(text)
                await event.edit(word_cloud)
            except Exception as e:
                logger.error(f"Error in word cloud handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 16: Image Compression
        @client.on(events.NewMessage(pattern='^compress pic$'))
        async def compress_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک عکس ریپلای کنید")
                    return
                    
                replied = await event.get_reply_message()
                if not replied.photo:
                    await event.edit("❌ پیام ریپلای شده عکس نیست")
                    return
                    
                await event.edit("⏳ در حال فشرده‌سازی عکس...")
                
                # Download original image
                original_path = await client.download_media(replied.photo)
                compressed_path = compress_image(original_path)
                
                if compressed_path:
                    await event.delete()
                    await client.send_file(event.chat_id, compressed_path, caption="📦 عکس فشرده شده")
                    os.remove(original_path)
                    os.remove(compressed_path)
                else:
                    await event.edit("❌ خطا در فشرده‌سازی عکس")
            except Exception as e:
                logger.error(f"Error in compress handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 17: Image Filters
        @client.on(events.NewMessage(pattern=r'^filter (.+)$'))
        async def filter_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک عکس ریپلای کنید")
                    return
                    
                replied = await event.get_reply_message()
                if not replied.photo:
                    await event.edit("❌ پیام ریپلای شده عکس نیست")
                    return
                
                filter_type = event.pattern_match.group(1)
                await event.edit(f"⏳ در حال اعمال فیلتر {filter_type}...")
                
                # Download original image
                original_path = await client.download_media(replied.photo)
                filtered_path = apply_image_filter(original_path, filter_type)
                
                if filtered_path:
                    await event.delete()
                    await client.send_file(event.chat_id, filtered_path, caption=f"🎨 فیلتر {filter_type}")
                    os.remove(original_path)
                    os.remove(filtered_path)
                else:
                    await event.edit("❌ خطا در اعمال فیلتر")
            except Exception as e:
                logger.error(f"Error in filter handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 18: Collage Maker
        @client.on(events.NewMessage(pattern='^collage$'))
        async def collage_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if len(saved_pics) < 2:
                    await event.edit("❌ حداقل 2 عکس ذخیره شده نیاز است")
                    return
                
                await event.edit("⏳ در حال ساخت کولاژ...")
                
                collage_path = create_collage(saved_pics[:4])  # Use first 4 images
                
                if collage_path:
                    await event.delete()
                    await client.send_file(event.chat_id, collage_path, caption="🖼 کولاژ ساخته شده")
                    os.remove(collage_path)
                else:
                    await event.edit("❌ خطا در ساخت کولاژ")
            except Exception as e:
                logger.error(f"Error in collage handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 19: Backup ZIP
        @client.on(events.NewMessage(pattern='^backup zip$'))
        async def backup_zip_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال ساخت فایل پشتیبان...")
                
                zip_file = create_backup_zip()
                if zip_file:
                    await event.delete()
                    await client.send_file(event.chat_id, zip_file, caption="📦 فایل پشتیبان کامل")
                    os.remove(zip_file)
                else:
                    await event.edit("❌ خطا در ساخت فایل پشتیبان")
            except Exception as e:
                logger.error(f"Error in backup zip handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 20: File Info
        @client.on(events.NewMessage(pattern=r'^file info (.+)$'))
        async def file_info_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                file_path = event.pattern_match.group(1)
                info = get_file_info(file_path)
                
                if isinstance(info, dict):
                    info_text = f"📄 اطلاعات فایل {file_path}:\n"
                    for key, value in info.items():
                        info_text += f"• {key}: {value}\n"
                    await event.edit(info_text)
                else:
                    await event.edit(info)
            except Exception as e:
                logger.error(f"Error in file info handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 21-30: Enhanced Actions
        @client.on(events.NewMessage(pattern=r'^(ghost|anti_spam|auto_translate|smart_reply) (on|off)$'))
        async def enhanced_actions_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                action, status = event.raw_text.lower().split()
                prev_state = actions[action]
                actions[action] = (status == 'on')
                
                command_history.append(('action', (action, prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                await event.edit(f"✅ {action} {'فعال' if actions[action] else 'غیرفعال'} شد")
            except Exception as e:
                logger.error(f"Error in enhanced actions handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 31: User Management
        @client.on(events.NewMessage(pattern=r'^(add admin|ban user|vip user) (.+)$'))
        async def user_management_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                command = event.pattern_match.group(1)
                user_identifier = event.pattern_match.group(2)
                
                if command == 'add admin':
                    admin_users.add(user_identifier)
                    await event.edit(f"✅ {user_identifier} به ادمین‌ها اضافه شد")
                elif command == 'ban user':
                    banned_users.add(user_identifier)
                    await event.edit(f"✅ {user_identifier} مسدود شد")
                elif command == 'vip user':
                    vip_users.add(user_identifier)
                    await event.edit(f"✅ {user_identifier} به VIP اضافه شد")
                
                backup_data()
            except Exception as e:
                logger.error(f"Error in user management handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 32: Message Templates
        @client.on(events.NewMessage(pattern=r'^template (add|use) (.+)$'))
        async def template_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                action = event.pattern_match.group(1)
                data = event.pattern_match.group(2)
                
                if action == 'add':
                    parts = data.split(' ', 1)
                    if len(parts) == 2:
                        name, template = parts
                        message_templates[name] = template
                        await event.edit(f"✅ قالب '{name}' اضافه شد")
                        backup_data()
                    else:
                        await event.edit("❌ فرمت: template add [نام] [متن]")
                elif action == 'use':
                    template_name = data
                    if template_name in message_templates:
                        await event.edit(message_templates[template_name])
                    else:
                        await event.edit(f"❌ قالب '{template_name}' یافت نشد")
            except Exception as e:
                logger.error(f"Error in template handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 33: Quick Replies
        @client.on(events.NewMessage(pattern=r'^quick (.+) (.+)$'))
        async def quick_reply_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                trigger = event.pattern_match.group(1)
                response = event.pattern_match.group(2)
                
                quick_replies[trigger] = response
                await event.edit(f"✅ پاسخ سریع '{trigger}' تنظیم شد")
                backup_data()
            except Exception as e:
                logger.error(f"Error in quick reply handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 34: Timer
        @client.on(events.NewMessage(pattern=r'^timer (\d+)$'))
        async def timer_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                seconds = int(event.pattern_match.group(1))
                await event.edit(f"⏰ تایمر {seconds} ثانیه شروع شد")
                
                await asyncio.sleep(seconds)
                await event.reply(f"⏰ تایمر {seconds} ثانیه به پایان رسید!")
            except Exception as e:
                logger.error(f"Error in timer handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 35: Ping Test
        @client.on(events.NewMessage(pattern=r'^ping (.+)$'))
        async def ping_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                host = event.pattern_match.group(1)
                await event.edit(f"⏳ در حال پینگ {host}...")
                
                try:
                    # Simple ping simulation
                    start_time = time.time()
                    response = requests.get(f"http://{host}", timeout=5)
                    end_time = time.time()
                    ping_time = round((end_time - start_time) * 1000, 2)
                    
                    await event.edit(f"🏓 پینگ {host}: {ping_time} ms")
                except:
                    await event.edit(f"❌ پینگ {host} ناموفق")
            except Exception as e:
                logger.error(f"Error in ping handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 36: IP Info
        @client.on(events.NewMessage(pattern='^ip$'))
        async def ip_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال دریافت IP...")
                
                try:
                    response = requests.get('https://httpbin.org/ip', timeout=5)
                    ip_data = response.json()
                    ip = ip_data.get('origin', 'Unknown')
                    await event.edit(f"🌐 IP شما: {ip}")
                except:
                    await event.edit("❌ خطا در دریافت IP")
            except Exception as e:
                logger.error(f"Error in IP handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 37: Memory Usage
        @client.on(events.NewMessage(pattern='^memory usage$'))
        async def memory_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                try:
                    process = psutil.Process(os.getpid())
                    memory_info = process.memory_info()
                    memory_percent = process.memory_percent()
                    
                    memory_text = f"""
💾 مصرف حافظه:
• RSS: {memory_info.rss / 1024 / 1024:.2f} MB
• VMS: {memory_info.vms / 1024 / 1024:.2f} MB
• درصد: {memory_percent:.2f}%
                    """
                    await event.edit(memory_text)
                except:
                    await event.edit("❌ خطا در دریافت اطلاعات حافظه")
            except Exception as e:
                logger.error(f"Error in memory handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 38: Clean Cache
        @client.on(events.NewMessage(pattern='^clean cache$'))
        async def clean_cache_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال پاکسازی کش...")
                
                # Clear various caches
                media_cache.clear()
                translation_cache.clear()
                weather_cache.clear()
                
                # Remove temporary files
                temp_files = [f for f in os.listdir('.') if f.startswith(('temp_', 'voice_', 'text_', 'qr_', 'meme_', 'filtered_', 'compressed_', 'collage_'))]
                removed_count = 0
                for file in temp_files:
                    try:
                        os.remove(file)
                        removed_count += 1
                    except:
                        pass
                
                await event.edit(f"✅ کش پاک شد. {removed_count} فایل موقت حذف شد")
            except Exception as e:
                logger.error(f"Error in clean cache handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 39: Performance Monitor
        @client.on(events.NewMessage(pattern='^performance$'))
        async def performance_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                await event.edit("⏳ در حال بررسی عملکرد...")
                
                try:
                    # CPU and Memory info
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory = psutil.virtual_memory()
                    disk = psutil.disk_usage('/')
                    
                    performance_text = f"""
📊 عملکرد سیستم:
🔥 CPU: {cpu_percent}%
💾 RAM: {memory.percent}% ({memory.used // 1024**3}GB / {memory.total // 1024**3}GB)
💿 Disk: {disk.percent}% ({disk.used // 1024**3}GB / {disk.total // 1024**3}GB)
⚡ Uptime: {str(timedelta(seconds=int(time.time() - start_time)))}
                    """
                    await event.edit(performance_text)
                except:
                    await event.edit("❌ خطا در دریافت اطلاعات عملکرد")
            except Exception as e:
                logger.error(f"Error in performance handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 40: User Notes
        @client.on(events.NewMessage(pattern=r'^user note (.+) (.+)$'))
        async def user_note_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                user = event.pattern_match.group(1)
                note = event.pattern_match.group(2)
                
                user_notes[user] = note
                await event.edit(f"✅ یادداشت برای {user} ذخیره شد")
                backup_data()
            except Exception as e:
                logger.error(f"Error in user note handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # NEW FEATURE 41-50: Additional Enhanced Features
        @client.on(events.NewMessage(pattern=r'^(joke|quote|fact|riddle)$'))
        async def entertainment_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                command = event.pattern_match.group(1)
                
                responses = {
                    'joke': ["چرا برنامه‌نویس‌ها قهوه دوست دارند؟ چون بدون کافئین کار نمی‌کنند! ☕", 
                            "چرا کامپیوتر سرما خورد؟ چون پنجره‌اش باز بود! 🪟"],
                    'quote': ["تنها راه انجام کار عالی این است که آنچه انجام می‌دهید را دوست داشته باشید. - استیو جابز",
                             "زندگی آنچیزی است که در حالی که شما مشغول برنامه‌ریزی‌های دیگر هستید، برای شما اتفاق می‌افتد. - جان لنون"],
                    'fact': ["فیل‌ها تنها پستانداری هستند که نمی‌توانند بپرند! 🐘",
                            "عسل هرگز خراب نمی‌شود. عسل 3000 ساله هنوز خوراکی است! 🍯"],
                    'riddle': ["چیزی که هر چه بیشتر از آن بگیری، بزرگ‌تر می‌شود؟ (جواب: حفره)",
                              "چیزی که دارد اما نمی‌تواند ببیند؟ (جواب: کور)"]
                }
                
                response = random.choice(responses[command])
                await event.edit(response)
            except Exception as e:
                logger.error(f"Error in entertainment handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        # Continue with original handlers...
        @client.on(events.NewMessage(pattern='^متن به ویس بگو (.+)$'))
        async def voice_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                await event.edit("⏳ در حال تبدیل متن به ویس...")
                
                voice_file = await text_to_voice(text)
                if voice_file:
                    await event.delete()
                    await client.send_file(event.chat_id, voice_file)
                    os.remove(voice_file)
                else:
                    await event.edit("❌ خطا در تبدیل متن به ویس")
            except Exception as e:
                logger.error(f"Error in voice handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^save pic$'))
        async def save_pic_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not event.is_reply:
                    await event.edit("❌ لطفا روی یک عکس ریپلای کنید")
                    return
                    
                replied = await event.get_reply_message()
                if not replied.photo:
                    await event.edit("❌ پیام ریپلای شده عکس نیست")
                    return
                    
                await event.edit("⏳ در حال ذخیره عکس...")
                path = await client.download_media(replied.photo)
                saved_pics.append(path)
                
                command_history.append(('save_pic', path))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                
                backup_data()
                await event.edit("✅ عکس ذخیره شد")
            except Exception as e:
                logger.error(f"Error in save pic handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^show pics$'))
        async def show_pics_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not saved_pics:
                    await event.edit("❌ هیچ عکسی ذخیره نشده است")
                    return
                
                await event.edit(f"⏳ در حال بارگذاری {len(saved_pics)} عکس...")
                
                for i, pic_path in enumerate(saved_pics):
                    if os.path.exists(pic_path):
                        await client.send_file(event.chat_id, pic_path, caption=f"عکس {i+1}/{len(saved_pics)}")
                    else:
                        await client.send_message(event.chat_id, f"❌ عکس {i+1} یافت نشد")
                
                await event.edit(f"✅ {len(saved_pics)} عکس نمایش داده شد")
            except Exception as e:
                logger.error(f"Error in show pics handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^متن به عکس (.+)$'))
        async def img_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                await event.edit("⏳ در حال تبدیل متن به عکس...")
                
                img_file = await text_to_image(text)
                if img_file:
                    await event.delete()
                    await client.send_file(event.chat_id, img_file)
                    os.remove(img_file)
                else:
                    await event.edit("❌ خطا در تبدیل متن به عکس")
            except Exception as e:
                logger.error(f"Error in image handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='^متن به گیف (.+)$'))
        async def gif_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                text = event.pattern_match.group(1)
                await event.edit("⏳ در حال تبدیل متن به گیف...")
                
                gif_file = await text_to_gif(text)
                if gif_file:
                    await event.delete()
                    await client.send_file(event.chat_id, gif_file)
                    os.remove(gif_file)
                else:
                    await event.edit("❌ خطا در تبدیل متن به گیف")
            except Exception as e:
                logger.error(f"Error in gif handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern=r'^(screenshot|forward|copy|delete|edit|join|leave|invite|mention|link) (on|off)$'))
        async def lock_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                command, status = event.raw_text.lower().split()
                chat_id = str(event.chat_id)
                
                prev_state = chat_id in locked_chats[command]
                
                if status == 'on':
                    locked_chats[command].add(chat_id)
                    await event.edit(f"✅ قفل {command} فعال شد")
                else:
                    locked_chats[command].discard(chat_id)
                    await event.edit(f"✅ قفل {command} غیرفعال شد")
                
                command_history.append(('lock', (command, chat_id, prev_state)))
                if len(command_history) > MAX_HISTORY:
                    command_history.pop(0)
                    
                backup_data()
                    
            except Exception as e:
                logger.error(f"Error in lock handler: {e}")
                await event.edit(f"❌ خطا: {str(e)}")

        @client.on(events.NewMessage(pattern='پنل'))
        async def panel_handler(event):
            try:
                if not event.from_id:
                    return
                    
                if event.from_id.user_id == (await client.get_me()).id:
                    await show_help_menu(client, event)
            except Exception as e:
                logger.error(f"Error in panel handler: {e}")
                pass

        @client.on(events.NewMessage(pattern='undo'))
        async def undo_handler(event):
            try:
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    return
                    
                if not command_history:
                    await event.edit("❌ تاریخچه دستورات خالی است")
                    return
                
                last_command = command_history.pop()
                command_type, data = last_command
                
                if command_type == 'time':
                    global time_enabled
                    time_enabled = data
                    if not time_enabled:
                        await client(functions.account.UpdateProfileRequest(last_name=''))
                    await event.edit(f"✅ وضعیت نمایش ساعت به {'فعال' if time_enabled else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'lock':
                    lock_type, chat_id, prev_state = data
                    if prev_state:
                        locked_chats[lock_type].add(chat_id)
                    else:
                        locked_chats[lock_type].discard(chat_id)
                    await event.edit(f"✅ وضعیت قفل {lock_type} به {'فعال' if prev_state else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'font':
                    global current_font
                    current_font = data
                    await event.edit(f"✅ فونت به {current_font} برگردانده شد")
                
                elif command_type == 'enemy_add':
                    enemies.discard(data)
                    await event.edit("✅ کاربر از لیست دشمن حذف شد")
                
                elif command_type == 'enemy_remove':
                    enemies.add(data)
                    await event.edit("✅ کاربر به لیست دشمن اضافه شد")
                
                elif command_type == 'action':
                    action_type, prev_state = data
                    actions[action_type] = prev_state
                    await event.edit(f"✅ وضعیت {action_type} به {'فعال' if prev_state else 'غیرفعال'} برگردانده شد")
                
                elif command_type == 'save_msg':
                    saved_messages.pop()
                    await event.edit("✅ آخرین پیام ذخیره شده حذف شد")
                
                elif command_type == 'save_pic':
                    path = data
                    if path in saved_pics:
                        saved_pics.remove(path)
                    if os.path.exists(path):
                        os.remove(path)
                    await event.edit("✅ آخرین عکس ذخیره شده حذف شد")
                
                elif command_type == 'block_word':
                    blocked_words.remove(data)
                    await event.edit(f"✅ کلمه '{data}' از لیست کلمات مسدود شده حذف شد")
                
                elif command_type == 'unblock_word':
                    blocked_words.append(data)
                    await event.edit(f"✅ کلمه '{data}' به لیست کلمات مسدود شده اضافه شد")
                
                elif command_type == 'add_reply':
                    trigger = data
                    if trigger in custom_replies:
                        del custom_replies[trigger]
                    await event.edit(f"✅ پاسخ خودکار برای '{trigger}' حذف شد")
                
                elif command_type == 'del_reply':
                    trigger, response = data
                    custom_replies[trigger] = response
                    await event.edit(f"✅ پاسخ خودکار برای '{trigger}' بازگردانده شد")
                
                backup_data()
                
            except Exception as e:
                logger.error(f"Error in undo handler: {e}")
                await event.edit(f"❌ خطا در برگرداندن عملیات: {str(e)}")

        @client.on(events.NewMessage)
        async def enemy_handler(event):
            try:
                if not event.from_id:
                    return
                
                config = load_config()
                if event.from_id.user_id == (await client.get_me()).id:
                    if event.raw_text == 'تنظیم دشمن' and event.is_reply:
                        replied = await event.get_reply_message()
                        if replied and replied.from_id and hasattr(replied.from_id, 'user_id'):
                            user_id = str(replied.from_id.user_id)
                            enemies.add(user_id)
                            
                            command_history.append(('enemy_add', user_id))
                            if len(command_history) > MAX_HISTORY:
                                command_history.pop(0)
                                
                            backup_data()
                            await event.reply('✅ کاربر به لیست دشمن اضافه شد')
                        else:
                            await event.reply('❌ نمی‌توان این کاربر را به لیست دشمن اضافه کرد')

                    elif event.raw_text == 'حذف دشمن' and event.is_reply:
                        replied = await event.get_reply_message()
                        if replied and replied.from_id and hasattr(replied.from_id, 'user_id'):
                            user_id = str(replied.from_id.user_id)
                            enemies.discard(user_id)
                            
                            command_history.append(('enemy_remove', user_id))
                            if len(command_history) > MAX_HISTORY:
                                command_history.pop(0)
                                
                            backup_data()
                            await event.reply('✅ کاربر از لیست دشمن حذف شد')
                        else:
                            await event.reply('❌ نمی‌توان این کاربر را از لیست دشمن حذف کرد')

                    elif event.raw_text == 'لیست دشمن':
                        enemy_list = ''
                        for i, enemy in enumerate(enemies, 1):
                            try:
                                user = await client.get_entity(int(enemy))
                                enemy_list += f'{i}. {user.first_name} {user.last_name or ""} (@{user.username or "بدون یوزرنیم"})\n'
                            except:
                                enemy_list += f'{i}. ID: {enemy}\n'
                        await event.reply(enemy_list or '❌ لیست دشمن خالی است')

                elif config['enemy_auto_reply'] and str(event.from_id.user_id) in enemies:
                    insult1 = random.choice(insults)
                    insult2 = random.choice(insults)
                    while insult2 == insult1:
                        insult2 = random.choice(insults)
                    
                    await event.reply(insult1)
                    await asyncio.sleep(0.5)
                    await event.reply(insult2)
            except Exception as e:
                logger.error(f"Error in enemy handler: {e}")
                pass

        @client.on(events.NewMessage)
        async def font_handler(event):
            global current_font
            
            try:
                if not event.from_id or not event.raw_text:
                    return
                            
                if event.from_id.user_id != (await client.get_me()).id:
                    return

                text = event.raw_text.lower().split()
                
                if len(text) == 2 and text[1] in ['on', 'off'] and text[0] in font_styles:
                    font, status = text
                    
                    prev_font = current_font
                    
                    if status == 'on':
                        current_font = font
                        await event.edit(f'✅ حالت {font} فعال شد')
                    else:
                        current_font = 'normal'
                        await event.edit(f'✅ حالت {font} غیرفعال شد')
                    
                    command_history.append(('font', prev_font))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                
                elif current_font != 'normal' and current_font in font_styles:
                    await event.edit(font_styles[current_font](event.raw_text))
            except Exception as e:
                logger.error(f"Error in font handler: {e}")
                pass

        @client.on(events.NewMessage)
        async def check_locks(event):
            try:
                chat_id = str(event.chat_id)
                
                if chat_id in locked_chats['forward'] and event.forward:
                    await event.delete()
                    logger.info(f"Deleted forwarded message in chat {chat_id}")
                    
                if chat_id in locked_chats['copy'] and event.forward_from:
                    await event.delete()
                    logger.info(f"Deleted copied message in chat {chat_id}")
                    
            except Exception as e:
                logger.error(f"Error in check locks: {e}")

        @client.on(events.NewMessage)
        async def enhanced_message_handler(event):
            try:
                # Log message for analytics
                if event.raw_text and event.from_id:
                    chat_id = str(event.chat_id)
                    user_id = str(event.from_id.user_id)
                    
                    # Store in chat logs
                    if chat_id not in chat_logs:
                        chat_logs[chat_id] = []
                    chat_logs[chat_id].append(event.raw_text)
                    
                    # Keep only last 1000 messages per chat
                    if len(chat_logs[chat_id]) > 1000:
                        chat_logs[chat_id] = chat_logs[chat_id][-1000:]
                    
                    # Update user analytics
                    if user_id not in user_analytics:
                        user_analytics[user_id] = {
                            'message_count': 0,
                            'total_chars': 0,
                            'first_seen': datetime.now().isoformat(),
                            'last_seen': datetime.now().isoformat()
                        }
                    
                    user_analytics[user_id]['message_count'] += 1
                    user_analytics[user_id]['total_chars'] += len(event.raw_text)
                    user_analytics[user_id]['last_seen'] = datetime.now().isoformat()

                # Auto-read messages if enabled
                if actions['read']:
                    await auto_read_messages(event, client)
                
                # Do not process further if message is not from the user
                if not event.from_id or event.from_id.user_id != (await client.get_me()).id:
                    # Check for custom replies if auto_reply is enabled
                    if actions['auto_reply'] and event.raw_text and event.raw_text in custom_replies:
                        await event.reply(custom_replies[event.raw_text])
                    
                    # Check for quick replies
                    if event.raw_text and event.raw_text in quick_replies:
                        await event.reply(quick_replies[event.raw_text])
                    
                    return

                # Check for blocked words
                if any(word in event.raw_text.lower() for word in blocked_words):
                    await event.delete()
                    return

                # Auto actions
                if actions['typing']:
                    asyncio.create_task(auto_typing(client, event.chat_id))
                
                if actions['reaction']:
                    await auto_reaction(event)

                # Enhanced message processing continues with all original handlers...
                # Schedule message
                if event.raw_text.startswith('schedule '):
                    parts = event.raw_text.split(maxsplit=2)
                    if len(parts) == 3:
                        try:
                            delay = int(parts[1])
                            message = parts[2]
                            asyncio.create_task(schedule_message(client, event.chat_id, delay, message))
                            await event.reply(f'✅ پیام بعد از {delay} دقیقه ارسال خواهد شد')
                        except ValueError:
                            await event.reply('❌ فرمت صحیح: schedule [زمان به دقیقه] [پیام]')

                # Spam messages
                elif event.raw_text.startswith('spam '):
                    parts = event.raw_text.split(maxsplit=2)
                    if len(parts) == 3:
                        try:
                            count = int(parts[1])
                            if count > 50:
                                await event.reply('❌ حداکثر تعداد پیام برای اسپم 50 است')
                                return
                                
                            message = parts[2]
                            asyncio.create_task(spam_messages(client, event.chat_id, count, message))
                        except ValueError:
                            await event.reply('❌ فرمت صحیح: spam [تعداد] [پیام]')

                # Save message
                elif event.raw_text == 'save' and event.is_reply:
                    replied = await event.get_reply_message()
                    if replied and replied.text:
                        saved_messages.append(replied.text)
                        
                        command_history.append(('save_msg', None))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                            
                        backup_data()
                        await event.reply('✅ پیام ذخیره شد')
                    else:
                        await event.reply('❌ پیام ریپلای شده متن ندارد')

                # Show saved messages
                elif event.raw_text == 'saved':
                    if not saved_messages:
                        await event.reply('❌ پیامی ذخیره نشده است')
                        return
                        
                    saved_text = '\n\n'.join(f'{i+1}. {msg}' for i, msg in enumerate(saved_messages))
                    
                    if len(saved_text) > 4000:
                        chunks = [saved_text[i:i+4000] for i in range(0, len(saved_text), 4000)]
                        for i, chunk in enumerate(chunks):
                            await event.reply(f"بخش {i+1}/{len(chunks)}:\n\n{chunk}")
                    else:
                        await event.reply(saved_text)

                # Set reminder
                elif event.raw_text.startswith('remind '):
                    parts = event.raw_text.split(maxsplit=2)
                    if len(parts) == 3:
                        time_str = parts[1]
                        message = parts[2]
                        
                        if re.match(r'^([01]?[0-9]|2[0-3]):([0-5][0-9])$', time_str):
                            reminders.append((time_str, message, event.chat_id))
                            backup_data()
                            await event.reply(f'✅ یادآور برای ساعت {time_str} تنظیم شد')
                        else:
                            await event.reply('❌ فرمت زمان اشتباه است. از فرمت HH:MM استفاده کنید')
                    else:
                        await event.reply('❌ فرمت صحیح: remind [زمان] [پیام]')

                # Search in messages
                elif event.raw_text.startswith('search '):
                    query = event.raw_text.split(maxsplit=1)[1]
                    await event.edit(f"🔍 در حال جستجوی '{query}'...")
                    
                    messages = await client.get_messages(event.chat_id, search=query, limit=10)
                    if not messages:
                        await event.edit("❌ پیامی یافت نشد")
                        return
                        
                    result = f"🔍 نتایج جستجو برای '{query}':\n\n"
                    for i, msg in enumerate(messages, 1):
                        sender = await msg.get_sender()
                        sender_name = utils.get_display_name(sender) if sender else "Unknown"
                        result += f"{i}. از {sender_name}: {msg.text[:100]}{'...' if len(msg.text) > 100 else ''}\n\n"
                    
                    await event.edit(result)

                # Block word
                elif event.raw_text.startswith('block word '):
                    word = event.raw_text.split(maxsplit=2)[2].lower()
                    if word in blocked_words:
                        await event.reply(f"❌ کلمه '{word}' قبلاً مسدود شده است")
                    else:
                        blocked_words.append(word)
                        
                        command_history.append(('block_word', word))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                            
                        backup_data()
                        await event.reply(f"✅ کلمه '{word}' مسدود شد")

                # Unblock word
                elif event.raw_text.startswith('unblock word '):
                    word = event.raw_text.split(maxsplit=2)[2].lower()
                    if word not in blocked_words:
                        await event.reply(f"❌ کلمه '{word}' در لیست مسدود شده‌ها نیست")
                    else:
                        blocked_words.remove(word)
                        
                        command_history.append(('unblock_word', word))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                            
                        backup_data()
                        await event.reply(f"✅ کلمه '{word}' از لیست مسدود شده‌ها حذف شد")

                # Show blocked words
                elif event.raw_text == 'block list':
                    if not blocked_words:
                        await event.reply("❌ لیست کلمات مسدود شده خالی است")
                    else:
                        block_list = '\n'.join(f"{i+1}. {word}" for i, word in enumerate(blocked_words))
                        await event.reply(f"📋 لیست کلمات مسدود شده:\n\n{block_list}")

                # Set auto reply
                elif event.raw_text.startswith('auto reply '):
                    parts = event.raw_text.split(maxsplit=3)
                    if len(parts) == 4:
                        trigger = parts[2]
                        response = parts[3]
                        
                        custom_replies[trigger] = response
                        
                        command_history.append(('add_reply', trigger))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                            
                        backup_data()
                        await event.reply(f"✅ پاسخ خودکار برای '{trigger}' تنظیم شد")
                    else:
                        await event.reply("❌ فرمت صحیح: auto reply [کلمه کلیدی] [پاسخ]")

                # Delete auto reply
                elif event.raw_text.startswith('delete reply '):
                    trigger = event.raw_text.split(maxsplit=2)[2]
                    if trigger not in custom_replies:
                        await event.reply(f"❌ هیچ پاسخ خودکاری برای '{trigger}' وجود ندارد")
                    else:
                        prev_response = custom_replies[trigger]
                        del custom_replies[trigger]
                        
                        command_history.append(('del_reply', (trigger, prev_response)))
                        if len(command_history) > MAX_HISTORY:
                            command_history.pop(0)
                            
                        backup_data()
                        await event.reply(f"✅ پاسخ خودکار برای '{trigger}' حذف شد")

                # Show auto replies
                elif event.raw_text == 'replies':
                    if not custom_replies:
                        await event.reply("❌ هیچ پاسخ خودکاری تنظیم نشده است")
                    else:
                        reply_list = '\n\n'.join(f"🔹 {trigger}:\n{response}" for trigger, response in custom_replies.items())
                        await event.reply(f"📋 لیست پاسخ‌های خودکار:\n\n{reply_list}")

                # Backup data manually
                elif event.raw_text == 'backup':
                    if backup_data():
                        await event.reply("✅ پشتیبان‌گیری با موفقیت انجام شد")
                    else:
                        await event.reply("❌ خطا در پشتیبان‌گیری")

                # Restore data manually
                elif event.raw_text == 'restore':
                    if restore_data():
                        await event.reply("✅ بازیابی داده‌ها با موفقیت انجام شد")
                    else:
                        await event.reply("❌ فایل پشتیبان یافت نشد یا مشکلی در بازیابی وجود دارد")

                # Toggle typing status
                elif event.raw_text in ['typing on', 'typing off']:
                    prev_state = actions['typing']
                    actions['typing'] = event.raw_text.endswith('on')
                    
                    command_history.append(('action', ('typing', prev_state)))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    await event.reply(f"✅ تایپینگ {'فعال' if actions['typing'] else 'غیرفعال'} شد")

                # Toggle online status
                elif event.raw_text in ['online on', 'online off']:
                    prev_state = actions['online']
                    actions['online'] = event.raw_text.endswith('on')
                    
                    command_history.append(('action', ('online', prev_state)))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    if actions['online']:
                        asyncio.create_task(auto_online(client))
                    await event.reply(f"✅ آنلاین {'فعال' if actions['online'] else 'غیرفعال'} شد")

                # Toggle reaction status
                elif event.raw_text in ['reaction on', 'reaction off']:
                    prev_state = actions['reaction']
                    actions['reaction'] = event.raw_text.endswith('on')
                    
                    command_history.append(('action', ('reaction', prev_state)))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    await event.reply(f"✅ ری‌اکشن {'فعال' if actions['reaction'] else 'غیرفعال'} شد")

                # Toggle read status
                elif event.raw_text in ['read on', 'read off']:
                    prev_state = actions['read']
                    actions['read'] = event.raw_text.endswith('on')
                    
                    command_history.append(('action', ('read', prev_state)))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    await event.reply(f"✅ خواندن خودکار {'فعال' if actions['read'] else 'غیرفعال'} شد")

                # Toggle auto reply status
                elif event.raw_text in ['reply on', 'reply off']:
                    prev_state = actions['auto_reply']
                    actions['auto_reply'] = event.raw_text.endswith('on')
                    
                    command_history.append(('action', ('auto_reply', prev_state)))
                    if len(command_history) > MAX_HISTORY:
                        command_history.pop(0)
                    
                    await event.reply(f"✅ پاسخ خودکار {'فعال' if actions['auto_reply'] else 'غیرفعال'} شد")

                # Exit command
                elif event.raw_text == 'exit':
                    await event.reply("✅ در حال خروج از برنامه...")
                    global running
                    running = False
                    await client.disconnect()
                    return
                    
            except Exception as e:
                logger.error(f"Error in enhanced message handler: {e}")
                pass

        @client.on(events.NewMessage(pattern='وضعیت'))
        async def status_handler(event):
            try:
                if not event.from_id:
                    return
                    
                if event.from_id.user_id == (await client.get_me()).id:
                    await show_status(client, event)
            except Exception as e:
                logger.error(f"Error in status handler: {e}")
                print_error(f"Error showing status: {e}")

        @client.on(events.MessageDeleted)
        async def delete_handler(event):
            """Handle deleted messages for anti-delete feature"""
            try:
                for deleted_id in event.deleted_ids:
                    chat_id = str(event.chat_id)
                    if chat_id in locked_chats['delete']:
                        msg = await client.get_messages(event.chat_id, ids=deleted_id)
                        if msg and msg.text:
                            sender = await msg.get_sender()
                            sender_name = utils.get_display_name(sender) if sender else "Unknown"
                            
                            saved_text = f"🔴 پیام حذف شده از {sender_name}:\n{msg.text}"
                            await client.send_message(event.chat_id, saved_text)
            except Exception as e:
                logger.error(f"Error in delete handler: {e}")

        @client.on(events.MessageEdited)
        async def edit_handler(event):
            """Handle edited messages for anti-edit feature"""
            try:
                chat_id = str(event.chat_id)
                if chat_id in locked_chats['edit'] and event.message:
                    msg_id = event.message.id
                    
                    edit_history = await client(functions.channels.GetMessageEditHistoryRequest(
                        channel=event.chat_id,
                        id=msg_id
                    ))
                    
                    if edit_history and edit_history.messages:
                        original = edit_history.messages[-1]
                        current = event.message
                        
                        if original.message != current.message:
                            sender = await event.get_sender()
                            sender_name = utils.get_display_name(sender) if sender else "Unknown"
                            
                            edit_text = f"🔄 پیام ویرایش شده از {sender_name}:\n\nقبل:\n{original.message}\n\nبعد:\n{current.message}"
                            await client.send_message(event.chat_id, edit_text)
            except Exception as e:
                logger.error(f"Error in edit handler: {e}")

        # Run the client until disconnected
        print_success("Enhanced Self-bot v3.0 with 50+ features is running!")
        await client.run_until_disconnected()

    except KeyboardInterrupt:
        print_warning("\nKilling the self-bot by keyboard interrupt...")
        return
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        logger.error(f"Unexpected error: {e}")
        return
    finally:
        running = False
        if client and client.is_connected():
            await client.disconnect()
        print_info("Enhanced Self-bot has been shut down")

def init():
    """Initialize and run the enhanced self-bot"""
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_warning("\nExiting enhanced self-bot...")
    except Exception as e:
        print_error(f"\nUnexpected error: {e}")
        logging.error(f"Unexpected init error: {e}")

if __name__ == '__main__':
    init()
