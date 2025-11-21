#!/bin/bash
# Script para instalar todas las dependencias necesarias en Linux

echo "================================================"
echo "Instalador de dependencias para HTTPS Interceptor"
echo "================================================"
echo ""

# Verificar que se esté ejecutando en Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Este script solo funciona en Linux"
    exit 1
fi

echo "📦 Actualizando sistema..."
sudo apt update

echo ""
echo "📦 Instalando dependencias del sistema..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    git \
    build-essential \
    ccache \
    libncurses5:i386 \
    libstdc++6:i386 \
    libgtk2.0-0:i386 \
    libpangox-1.0-0:i386 \
    libpangoxft-1.0-0:i386 \
    libidn11:i386 \
    openjdk-11-jdk \
    unzip \
    zlib1g-dev \
    zlib1g:i386 \
    libssl-dev \
    libffi-dev \
    autoconf \
    libtool \
    pkg-config

echo ""
echo "🐍 Actualizando pip..."
pip3 install --upgrade pip

echo ""
echo "📦 Instalando Python build tools..."
pip3 install --upgrade wheel setuptools

echo ""
echo "📦 Instalando Cython..."
pip3 install --upgrade cython==0.29.36

echo ""
echo "📦 Instalando Buildozer..."
pip3 install --upgrade buildozer

echo ""
echo "📦 Instalando dependencias de Python..."
pip3 install -r requirements.txt

echo ""
echo "✅ Instalación completada!"
echo ""
echo "Para compilar la aplicación, ejecuta:"
echo "  buildozer android debug"
echo ""
echo "Para compilar y desplegar directamente:"
echo "  buildozer android debug deploy run"
echo ""
