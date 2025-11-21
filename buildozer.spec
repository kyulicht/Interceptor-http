[app]

# (str) Título de tu aplicación
title = HTTPS Interceptor

# (str) Nombre del paquete
package.name = httpsinterceptor

# (str) Dominio del paquete (necesario para android/ios)
package.domain = org.interceptor

# (str) Directorio de código fuente donde vive el main.py
source.dir = .

# (list) Archivo fuente a incluir (deja vacío para incluir todo el directorio)
source.include_exts = py,png,jpg,kv,atlas,json

# (str) Versión de la aplicación
version = 1.0

# (list) Requisitos de la aplicación
# Formato: módulo o módulo==versión
requirements = python3,kivy==2.2.1,requests,certifi,urllib3

# (str) Permisos de Android
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# (int) Target Android API, debe ser tan alto como tu NDK soporta
android.api = 33

# (int) Mínimo API que tu APK soportará
android.minapi = 21

# (str) Android NDK versión a usar
android.ndk = 25b

# (str) Android SDK versión a usar
android.sdk = 33

# (bool) Usar --private data storage
android.private_storage = True

# (str) Arquitecturas Android a compilar
# Opciones: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (bool) Habilitar AndroidX
android.enable_androidx = True

# (list) Librerías Java/JAR que necesita tu aplicación
# android.add_jars = foo.jar,bar.jar

# (list) Archivos AAR que tu aplicación necesita
# android.add_aars = foo.aar,bar.aar

# (str) Orientación de la aplicación
orientation = portrait

# (bool) Pantalla completa
fullscreen = 0

# (list) Requisitos del sistema operativo
# android.gradle_dependencies = 

# (bool) Copiar librerías en lugar de hacer symlink
android.copy_libs = 1

# (str) Android logcat filters
android.logcat_filters = *:S python:D

# (bool) Copiar bibliotecas en vez de vincularlas
android.skip_update = False

# (str) Icono de la aplicación
# icon.filename = %(source.dir)s/data/icon.png

# (str) Splash screen
# presplash.filename = %(source.dir)s/data/presplash.png

# (str) Modo de adaptación del presplash
# android.presplash_color = #FFFFFF

[buildozer]

# (int) Nivel de log (0 = solo error, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar advertencias de buildozer
warn_on_root = 1

# (str) Directorio de compilación
# build_dir = ./.buildozer

# (str) Directorio de salida de binarios
# bin_dir = ./bin
