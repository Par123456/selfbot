#!/bin/bash

# Enhanced Telegram Self-Bot Installation Script for cp.springhost.ru
# Python 3.13.1 Compatible

echo "🚀 Installing Enhanced Telegram Self-Bot with 50+ Features..."
echo "📋 Compatible with Python 3.13.1 and cp.springhost.ru servers"

# Update system packages
echo "📦 Updating system packages..."
apt-get update -y
apt-get upgrade -y

# Install Python 3.13.1 if not available
echo "🐍 Checking Python version..."
python3 --version

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get install -y \
    python3-pip \
    python3-dev \
    python3-venv \
    build-essential \
    libssl-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python3-tk \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1-dev \
    pkg-config \
    libcairo2-dev \
    libgirepository1.0-dev \
    ffmpeg \
    libavcodec-extra \
    portaudio19-dev \
    flac \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    festival \
    festvox-kallpc16k \
    sqlite3 \
    libsqlite3-dev \
    redis-server \
    git \
    curl \
    wget \
    unzip \
    htop \
    screen \
    tmux

# Create virtual environment
echo "🌐 Creating virtual environment..."
python3 -m venv selfbot_env
source selfbot_env/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install Python packages with error handling
echo "📚 Installing Python packages..."

# Core packages first
pip install --no-cache-dir telethon==1.36.0
pip install --no-cache-dir asyncio
pip install --no-cache-dir pytz==2024.1
pip install --no-cache-dir colorama==0.4.6
pip install --no-cache-dir requests==2.32.3

# Image processing packages
pip install --no-cache-dir Pillow==10.4.0
pip install --no-cache-dir qrcode==7.4.2
pip install --no-cache-dir opencv-python==4.10.0.84

# Audio/Video packages
pip install --no-cache-dir gTTS==2.5.1
pip install --no-cache-dir pyttsx3==2.90
pip install --no-cache-dir SpeechRecognition==3.10.4
pip install --no-cache-dir pygame==2.6.0
pip install --no-cache-dir pydub==0.25.1
pip install --no-cache-dir moviepy==1.0.3

# Data analysis packages
pip install --no-cache-dir pandas==2.2.2
pip install --no-cache-dir numpy==2.1.1
pip install --no-cache-dir matplotlib==3.9.2
pip install --no-cache-dir seaborn==0.13.2
pip install --no-cache-dir scikit-learn==1.5.1

# Text processing packages
pip install --no-cache-dir textblob==0.18.0
pip install --no-cache-dir nltk==3.9.1
pip install --no-cache-dir wordcloud==1.9.3
pip install --no-cache-dir googletrans==4.0.0rc1

# System and network packages
pip install --no-cache-dir psutil==6.0.0
pip install --no-cache-dir aiohttp==3.10.5
pip install --no-cache-dir aiofiles==24.1.0
pip install --no-cache-dir speedtest-cli==2.1.3
pip install --no-cache-dir geo
