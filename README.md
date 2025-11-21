# HTTPS Interceptor para Android

Aplicación Python para Android ARM que intercepta y modifica peticiones HTTPS con interfaz gráfica.

## Características

✅ **Interfaz Gráfica Intuitiva** - Diseñada con Kivy para Android
✅ **Interceptación de Peticiones** - Captura peticiones HTTP/HTTPS en tiempo real
✅ **Modificación de Headers** - Edita headers, content-type y datos
✅ **Reenvío de Peticiones** - Modifica y reenvía peticiones capturadas
✅ **Activación/Desactivación** - Control con switch para activar el interceptor
✅ **Lista de Peticiones** - Visualiza todas las peticiones capturadas
✅ **Soporte ARM** - Compilado específicamente para Android ARM (arm64-v8a y armeabi-v7a)

## Requisitos

### Para compilar:
- Linux (Ubuntu/Debian recomendado)
- Python 3.8+
- Buildozer
- Android SDK y NDK
- Dependencias de Kivy

### En Android:
- Android 5.0 (API 21) o superior
- Permisos de Internet

## Instalación y Compilación

### 1. Instalar dependencias en tu sistema Linux:

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias de Python
sudo apt install -y python3 python3-pip python3-venv git

# Instalar dependencias de Buildozer
sudo apt install -y build-essential ccache libncurses5:i386 libstdc++6:i386 \
    libgtk2.0-0:i386 libpangox-1.0-0:i386 libpangoxft-1.0-0:i386 libidn11:i386 \
    python3-pip openjdk-11-jdk unzip zlib1g-dev zlib1g:i386 libssl-dev \
    libffi-dev autoconf libtool pkg-config

# Instalar Cython y Buildozer
pip3 install --upgrade pip
pip3 install --upgrade cython
pip3 install --upgrade buildozer
```

### 2. Compilar la aplicación:

```bash
# Navegar al directorio del proyecto
cd https_interceptor

# Compilar para Android
buildozer android debug

# O para release firmado:
# buildozer android release
```

La compilación tomará tiempo (especialmente la primera vez). El APK se generará en:
`bin/httpsinterceptor-1.0-arm64-v8a-debug.apk`

### 3. Instalar en Android:

```bash
# Conectar tu dispositivo Android por USB (con depuración USB activada)
buildozer android deploy run

# O manualmente:
adb install bin/httpsinterceptor-1.0-arm64-v8a-debug.apk
```

## Uso de la Aplicación

### 1. Iniciar el Interceptor

1. Abre la aplicación en tu Android
2. Activa el switch "Activar" en la parte superior
3. El estado cambiará a "Activo (Puerto: 8080)"

### 2. Configurar el Proxy en tu Dispositivo

Para interceptar peticiones de otras aplicaciones:

1. Ve a **Configuración → Wi-Fi**
2. Mantén presionada tu red Wi-Fi actual
3. Selecciona **Modificar red**
4. Marca **Opciones avanzadas**
5. En **Proxy**, selecciona **Manual**
6. Configura:
   - **Nombre del host**: 127.0.0.1 (o la IP local del dispositivo)
   - **Puerto**: 8080
7. Guarda los cambios

### 3. Capturar Peticiones

1. Usa cualquier aplicación que haga peticiones HTTP/HTTPS
2. Las peticiones aparecerán en la lista de "Peticiones Capturadas"
3. Toca una petición para cargarla en el editor

### 4. Modificar y Reenviar

1. Selecciona una petición de la lista
2. Modifica los campos según necesites:
   - **URL**: Cambia el endpoint
   - **Método**: GET, POST, PUT, DELETE, etc.
   - **Headers**: JSON con los headers (ej: `{"Authorization": "Bearer token"}`)
   - **Data/Body**: Contenido del body de la petición
3. Presiona **"Reenviar Petición"**
4. La respuesta se mostrará en un popup

### 5. Ejemplos de Modificación

#### Ejemplo 1: Modificar Headers
```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer mi_token_secreto",
  "User-Agent": "MiApp/1.0",
  "X-Custom-Header": "valor"
}
```

#### Ejemplo 2: Modificar Body (POST/PUT)
```json
{
  "username": "usuario",
  "password": "contraseña",
  "remember": true
}
```

#### Ejemplo 3: Cambiar URL
```
Capturada: https://api.example.com/v1/users
Modificada: https://api.example.com/v2/users
```

## Estructura del Proyecto

```
https_interceptor/
├── main.py              # Aplicación principal con UI Kivy
├── proxy_advanced.py    # Módulo de proxy HTTPS avanzado
├── buildozer.spec       # Configuración de compilación
├── README.md           # Este archivo
└── requirements.txt    # Dependencias Python
```

## Funciones Principales

### Clase HTTPSInterceptorApp

- `toggle_interceptor()` - Activa/desactiva el interceptor
- `start_interceptor()` - Inicia el servidor proxy
- `stop_interceptor()` - Detiene el servidor proxy
- `handle_client()` - Maneja conexiones de clientes
- `select_request()` - Carga una petición para editar
- `resend_request()` - Reenvía la petición modificada
- `clear_requests()` - Limpia la lista de peticiones

## Limitaciones y Notas

⚠️ **Seguridad SSL/TLS**: La interceptación de HTTPS real requiere certificados SSL dinámicos. Esta versión básica captura metadatos pero no puede descifrar tráfico SSL sin configuración adicional de certificados.

⚠️ **Uso Educativo**: Esta herramienta es para propósitos educativos y de testing. No la uses para interceptar tráfico de aplicaciones sin permiso.

⚠️ **Root**: Para interceptar tráfico SSL de aplicaciones del sistema, tu dispositivo necesitará root y certificados de CA instalados.

⚠️ **Rendimiento**: El proxy puede afectar la velocidad de conexión.

## Mejoras Futuras

- [ ] Generación dinámica de certificados SSL para interceptación completa
- [ ] Exportar peticiones capturadas a archivo
- [ ] Filtros de peticiones por dominio/método
- [ ] Respuestas automáticas (mock server)
- [ ] Historial de peticiones persistente
- [ ] Análisis de tráfico y estadísticas
- [ ] Integración con mitmproxy

## Solución de Problemas

### El interceptor no captura peticiones HTTPS

**Solución**: Las peticiones HTTPS están cifradas. Para interceptarlas completamente necesitas:
1. Instalar certificados de CA personalizados
2. Usar herramientas como mitmproxy
3. Tener acceso root en el dispositivo

### El APK no se instala

**Solución**: 
- Habilita "Instalar desde fuentes desconocidas" en Android
- Verifica que el APK sea para tu arquitectura ARM

### Error de compilación con Buildozer

**Solución**:
```bash
# Limpiar compilación anterior
buildozer android clean

# Volver a compilar
buildozer android debug
```

## Recursos Adicionales

- [Documentación de Kivy](https://kivy.org/doc/stable/)
- [Documentación de Buildozer](https://buildozer.readthedocs.io/)
- [mitmproxy](https://mitmproxy.org/) - Para interceptación avanzada

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request en GitHub.

## Autor

Desarrollado para propósitos educativos y de testing.

---

**Disclaimer**: Esta herramienta debe usarse solo en redes y aplicaciones donde tengas permiso explícito para interceptar tráfico. El autor no se hace responsable del uso indebido de esta herramienta.
