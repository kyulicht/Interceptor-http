# Tutorial Completo: HTTPS Interceptor para Android

## 📱 ¿Qué hace esta aplicación?

Esta aplicación te permite:
1. **Interceptar** peticiones HTTP/HTTPS que tu dispositivo Android envía
2. **Ver** todos los detalles de las peticiones (URL, método, headers, datos)
3. **Modificar** cualquier aspecto de la petición
4. **Reenviar** la petición modificada para ver cómo responde el servidor

## 🎯 Casos de Uso

- **Testing de APIs**: Prueba diferentes parámetros sin modificar el código
- **Debugging**: Identifica qué datos envían tus aplicaciones
- **Desarrollo**: Simula diferentes escenarios de red
- **Aprendizaje**: Entiende cómo funcionan las peticiones HTTP/HTTPS

## 🛠️ Instalación Paso a Paso

### Opción 1: Compilar desde código (Recomendado)

#### Paso 1: Preparar el entorno Linux

```bash
# En Ubuntu/Debian
cd https_interceptor
./install_dependencies.sh
```

Esto instalará:
- Python 3 y pip
- Android SDK y NDK (automáticamente)
- Buildozer y Kivy
- Todas las dependencias necesarias

#### Paso 2: Compilar para Android

```bash
./compile_android.sh
```

La primera compilación puede tomar **30-60 minutos** porque descarga:
- Android SDK (~500 MB)
- Android NDK (~1 GB)
- Todas las dependencias de Python

Compilaciones posteriores serán mucho más rápidas (5-10 minutos).

#### Paso 3: Instalar en Android

```bash
# Opción A: Instalar automáticamente (con USB)
buildozer android deploy run

# Opción B: Instalar manualmente
adb install bin/httpsinterceptor-1.0-arm64-v8a-debug.apk
```

### Opción 2: Probar en escritorio primero

```bash
# Instalar dependencias de Kivy
pip3 install kivy requests

# Ejecutar en escritorio
python3 test_app.py
```

## 🚀 Guía de Uso Completa

### 1. Primera Ejecución

1. **Abrir la aplicación** en tu Android
2. Verás la pantalla principal con:
   - Switch "Activar" en la parte superior
   - Lista de peticiones capturadas (vacía)
   - Campos de edición (URL, Método, Headers, Data)
   - Botones "Reenviar Petición" y "Limpiar Lista"

### 2. Activar el Interceptor

1. **Toca el switch "Activar"**
2. El estado cambiará a: `Estado: Activo (Puerto: 8080)`
3. Aparecerá un mensaje: "Interceptor iniciado en puerto 8080"

### 3. Configurar el Proxy en Android

Para interceptar tráfico de otras apps:

#### Método 1: Configuración Manual de Proxy WiFi

1. Ve a **Ajustes → WiFi**
2. **Mantén presionada** tu red WiFi actual
3. Selecciona **Modificar red** o **Gestionar ajustes de red**
4. Toca **Opciones avanzadas**
5. En **Proxy**, selecciona **Manual**
6. Configura:
   ```
   Nombre del host del proxy: 127.0.0.1
   Puerto del proxy: 8080
   ```
7. **Guarda** los cambios

#### Método 2: Apps de Proxy (Más fácil)

Instala una app como "Proxy Manager" y configúrala para usar:
- Host: `127.0.0.1`
- Puerto: `8080`

### 4. Capturar Peticiones

1. Con el interceptor activo y el proxy configurado
2. **Abre cualquier aplicación** que use internet (navegador, app de noticias, etc.)
3. Las peticiones aparecerán automáticamente en la lista
4. Cada entrada muestra:
   - **Hora** de captura
   - **Método** HTTP (GET, POST, etc.)
   - **URL** (primeros 50 caracteres)

### 5. Ver Detalles de una Petición

1. **Toca cualquier petición** en la lista
2. Los campos de edición se llenarán automáticamente:
   - **URL**: Dirección completa del endpoint
   - **Método**: GET, POST, PUT, DELETE, etc.
   - **Headers**: JSON con todos los headers
   - **Data/Body**: Contenido enviado (para POST/PUT)

### 6. Modificar una Petición

#### Ejemplo 1: Cambiar la URL

```
Original: https://api.example.com/v1/users
Modificado: https://api.example.com/v2/users
```

#### Ejemplo 2: Agregar/Modificar Headers

```json
{
  "Content-Type": "application/json",
  "Authorization": "Bearer tu_token_aqui",
  "User-Agent": "MiApp/2.0",
  "X-Custom-Header": "valor_personalizado"
}
```

#### Ejemplo 3: Modificar el Body (POST/PUT)

```json
{
  "email": "nuevo@email.com",
  "password": "nueva_contraseña",
  "nombre": "Usuario Modificado"
}
```

#### Ejemplo 4: Cambiar el Método

```
Original: GET
Modificado: POST
```

### 7. Reenviar la Petición

1. Después de modificar los campos deseados
2. Toca el botón **"Reenviar Petición"**
3. La app enviará la petición con tus modificaciones
4. Aparecerá un popup con:
   - **Status Code**: 200, 404, 500, etc.
   - **Respuesta del servidor**: Primeros 500 caracteres

### 8. Gestionar Peticiones

- **Limpiar Lista**: Toca "Limpiar Lista" para eliminar todas las peticiones capturadas
- **Desactivar**: Toca el switch para desactivar el interceptor cuando no lo necesites

## 💡 Ejemplos Prácticos

### Ejemplo 1: Testing de API REST

**Objetivo**: Probar un endpoint de login con diferentes credenciales

1. Captura una petición de login de tu app
2. Modifica el body:
   ```json
   {
     "email": "test@example.com",
     "password": "password123"
   }
   ```
3. Reenvía y ve la respuesta
4. Prueba con otras credenciales sin recompilar la app

### Ejemplo 2: Cambiar User-Agent

**Objetivo**: Ver cómo responde un servidor a diferentes navegadores

1. Captura una petición GET
2. Modifica el header User-Agent:
   ```json
   {
     "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)"
   }
   ```
3. Reenvía y compara respuestas

### Ejemplo 3: Testing de Autenticación

**Objetivo**: Probar con diferentes tokens de autorización

1. Captura una petición autenticada
2. Modifica el header Authorization:
   ```json
   {
     "Authorization": "Bearer token_de_prueba"
   }
   ```
3. Reenvía para ver si el servidor rechaza tokens inválidos

### Ejemplo 4: Modificar Datos de Formulario

**Objetivo**: Enviar datos diferentes a un formulario

1. Captura un POST de formulario
2. Modifica los datos:
   ```json
   {
     "nombre": "Otro Nombre",
     "edad": 25,
     "ciudad": "Madrid"
   }
   ```
3. Reenvía y verifica la respuesta

## 🔧 Solución de Problemas

### Problema 1: No se capturan peticiones

**Causas posibles**:
- El interceptor no está activo
- El proxy no está configurado correctamente
- La app usa HTTPS con certificate pinning

**Soluciones**:
1. Verifica que el switch esté activado (verde)
2. Confirma la configuración del proxy (127.0.0.1:8080)
3. Para apps con certificate pinning, necesitas root

### Problema 2: "Error enviando petición"

**Causas posibles**:
- Headers con formato JSON incorrecto
- URL inválida
- Sin conexión a internet

**Soluciones**:
1. Verifica el formato JSON de headers (usa validador online)
2. Asegúrate de que la URL comience con http:// o https://
3. Comprueba tu conexión a internet

### Problema 3: Solo veo peticiones HTTP, no HTTPS

**Explicación**: HTTPS está cifrado y requiere interceptación SSL

**Soluciones avanzadas**:
1. Instalar certificado CA personalizado (requiere root)
2. Usar mitmproxy con certificados
3. Esta versión captura metadatos, no contenido cifrado

### Problema 4: La aplicación se cierra

**Causas posibles**:
- Falta de permisos
- Error en el código del proxy

**Soluciones**:
1. Reinstala la aplicación
2. Verifica los logs: `adb logcat | grep python`
3. Reporta el error en GitHub

## 📊 Limitaciones Actuales

### Interceptación HTTPS

⚠️ **La interceptación completa de HTTPS requiere**:
- Certificados SSL personalizados instalados
- Acceso root en Android
- Configuración avanzada

**Estado actual**: Captura metadatos de peticiones HTTPS pero no puede descifrar el contenido sin certificados.

### Solución: Integración con mitmproxy

Para interceptación completa:
```bash
# En tu PC con mitmproxy instalado
mitmproxy --mode transparent --showhost

# Configurar Android para usar mitmproxy
# Instalar certificado de mitmproxy en Android
```

### Performance

- El proxy puede hacer más lentas las conexiones
- Muchas peticiones simultáneas pueden saturar la UI
- Recomendado: Desactivar cuando no uses

## 🎓 Conceptos Técnicos

### ¿Cómo funciona?

1. **Proxy Server**: La app crea un servidor proxy en el puerto 8080
2. **Interceptación**: Todo el tráfico pasa por el proxy
3. **Parsing**: Analiza las peticiones HTTP/HTTPS
4. **Storage**: Guarda las peticiones en memoria
5. **Modification**: Permite editar antes de reenviar

### Estructura de una Petición HTTP

```
POST /api/login HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer token123

{"username": "user", "password": "pass"}
```

Componentes:
- **Línea de petición**: Método + URL + Versión
- **Headers**: Metadata de la petición
- **Body**: Datos enviados (POST/PUT)

## 🔐 Consideraciones de Seguridad

### Uso Ético

✅ **Permitido**:
- Testing de tus propias aplicaciones
- Debugging de problemas de red
- Aprendizaje y educación

❌ **NO permitido**:
- Interceptar tráfico de otros usuarios sin permiso
- Capturar credenciales de terceros
- Uso malicioso

### Seguridad de Datos

- Las peticiones capturadas solo se guardan en memoria
- No se persisten al cerrar la app
- No se envían a servidores externos

### Recomendaciones

1. **Desactiva el proxy** cuando no lo uses
2. **No compartas** peticiones con datos sensibles
3. **Usa solo en redes confiables**
4. **No interceptes** apps bancarias sin autorización

## 📚 Recursos Adicionales

### Documentación
- [Kivy Documentation](https://kivy.org/doc/stable/)
- [HTTP Protocol](https://developer.mozilla.org/es/docs/Web/HTTP)
- [mitmproxy](https://mitmproxy.org/)

### Herramientas Relacionadas
- **Charles Proxy**: Interceptor profesional
- **Burp Suite**: Testing de seguridad
- **Postman**: Cliente API con interfaz gráfica

### Comunidad
- [Stack Overflow - Kivy](https://stackoverflow.com/questions/tagged/kivy)
- [Stack Overflow - HTTP](https://stackoverflow.com/questions/tagged/http)

## 🚀 Próximas Mejoras

Funcionalidades planeadas:
- [ ] Soporte completo para HTTPS con certificados
- [ ] Exportar peticiones a formato HAR
- [ ] Filtros avanzados (por dominio, método, status)
- [ ] Mock server (respuestas automáticas)
- [ ] Historial persistente
- [ ] Replay de secuencias de peticiones
- [ ] Estadísticas y gráficos
- [ ] Integración con Postman

## 🤝 Contribuir

¿Quieres mejorar la aplicación?

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -am 'Agrega nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

## 📄 Licencia

MIT License - Uso libre para proyectos educativos y personales.

## ✉️ Soporte

¿Problemas o preguntas?
- Abre un issue en GitHub
- Consulta la documentación
- Revisa ejemplos en el código

---

**¡Disfruta interceptando y aprendiendo! 🎉**
