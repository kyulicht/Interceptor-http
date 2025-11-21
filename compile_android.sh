#!/bin/bash
# Script para compilar la aplicación para Android

echo "================================================"
echo "Compilador de HTTPS Interceptor para Android"
echo "================================================"
echo ""

# Verificar que buildozer esté instalado
if ! command -v buildozer &> /dev/null; then
    echo "❌ Buildozer no está instalado."
    echo "Por favor, ejecuta primero: ./install_dependencies.sh"
    exit 1
fi

# Limpiar compilación anterior si existe
if [ -d ".buildozer" ]; then
    echo "🧹 Limpiando compilación anterior..."
    buildozer android clean
fi

echo ""
echo "🔨 Compilando para Android ARM (arm64-v8a y armeabi-v7a)..."
echo "⏳ Esto puede tomar varios minutos (especialmente la primera vez)..."
echo ""

# Compilar
buildozer -v android debug

# Verificar si la compilación fue exitosa
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Compilación exitosa!"
    echo ""
    echo "📱 El APK se encuentra en:"
    ls -lh bin/*.apk 2>/dev/null
    echo ""
    echo "Para instalar en tu dispositivo Android:"
    echo "  1. Conecta tu dispositivo por USB con depuración USB activada"
    echo "  2. Ejecuta: adb install bin/*.apk"
    echo "  3. O ejecuta: buildozer android deploy run"
    echo ""
else
    echo ""
    echo "❌ Error durante la compilación"
    echo "Revisa los logs arriba para más detalles"
    echo ""
    echo "Soluciones comunes:"
    echo "  - Ejecuta: buildozer android clean"
    echo "  - Verifica que todas las dependencias estén instaladas"
    echo "  - Revisa el archivo buildozer.spec"
    exit 1
fi
