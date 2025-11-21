#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo avanzado de proxy HTTPS con soporte para certificados SSL
Este módulo proporciona interceptación más robusta de peticiones HTTPS
"""

import socket
import ssl
import threading
from urllib.parse import urlparse
import re


class HTTPSProxyHandler:
    """Manejador avanzado de proxy HTTPS"""
    
    def __init__(self, callback=None):
        """
        Inicializar el manejador
        
        Args:
            callback: Función a llamar cuando se capture una petición
                     callback(method, url, headers, body)
        """
        self.callback = callback
        self.running = False
        
    def start(self, host='0.0.0.0', port=8080):
        """Iniciar el servidor proxy"""
        self.running = True
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen(10)
        self.server_socket.settimeout(1.0)
        
        print(f"Proxy HTTPS iniciado en {host}:{port}")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"Error aceptando conexión: {e}")
                    
    def stop(self):
        """Detener el servidor proxy"""
        self.running = False
        if hasattr(self, 'server_socket'):
            self.server_socket.close()
            
    def handle_client(self, client_socket, address):
        """Manejar conexión de cliente"""
        try:
            # Recibir la petición inicial
            request = client_socket.recv(8192).decode('utf-8', errors='ignore')
            
            if not request:
                return
                
            # Parsear la primera línea
            first_line = request.split('\n')[0]
            
            # Detectar si es CONNECT (para HTTPS)
            if first_line.startswith('CONNECT'):
                self.handle_https_connect(client_socket, request, first_line)
            else:
                self.handle_http_request(client_socket, request, first_line)
                
        except Exception as e:
            print(f"Error manejando cliente {address}: {e}")
        finally:
            client_socket.close()
            
    def handle_https_connect(self, client_socket, request, first_line):
        """Manejar petición CONNECT para HTTPS"""
        try:
            # Extraer host y puerto
            url = first_line.split(' ')[1]
            host_port = url.split(':')
            host = host_port[0]
            port = int(host_port[1]) if len(host_port) > 1 else 443
            
            # Establecer conexión con el servidor destino
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((host, port))
            
            # Responder al cliente que la conexión está establecida
            client_socket.sendall(b'HTTP/1.1 200 Connection Established\r\n\r\n')
            
            # Aquí capturamos la petición HTTPS
            # En producción, necesitarías generar certificados SSL dinámicamente
            # para poder inspeccionar el tráfico SSL/TLS
            
            # Recibir datos del cliente
            client_data = client_socket.recv(8192)
            
            # Intentar parsear (si es texto plano o después de descifrar)
            try:
                request_text = client_data.decode('utf-8', errors='ignore')
                self.parse_and_callback(request_text, host)
            except:
                pass
            
            # Reenviar al servidor
            server_socket.sendall(client_data)
            
            # Recibir respuesta
            server_response = server_socket.recv(8192)
            client_socket.sendall(server_response)
            
            server_socket.close()
            
        except Exception as e:
            print(f"Error en HTTPS CONNECT: {e}")
            
    def handle_http_request(self, client_socket, request, first_line):
        """Manejar petición HTTP normal"""
        try:
            # Parsear la petición
            method, url, version = first_line.split(' ')
            
            # Parsear headers y body
            headers_dict, body = self.parse_request(request)
            
            # Llamar al callback si existe
            if self.callback:
                self.callback(method, url, headers_dict, body)
            
            # Extraer host del URL o headers
            parsed_url = urlparse(url)
            host = parsed_url.netloc or headers_dict.get('Host', '')
            path = parsed_url.path or '/'
            
            if not host:
                return
                
            # Conectar con el servidor destino
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((host, 80))
            
            # Reconstruir y enviar la petición
            new_request = f"{method} {path} {version}\r\n"
            for key, value in headers_dict.items():
                new_request += f"{key}: {value}\r\n"
            new_request += "\r\n"
            if body:
                new_request += body
                
            server_socket.sendall(new_request.encode())
            
            # Recibir y reenviar la respuesta
            response = b''
            while True:
                chunk = server_socket.recv(4096)
                if not chunk:
                    break
                response += chunk
                client_socket.sendall(chunk)
                
            server_socket.close()
            
        except Exception as e:
            print(f"Error en HTTP request: {e}")
            
    def parse_request(self, request):
        """Parsear una petición HTTP"""
        lines = request.split('\r\n')
        headers_dict = {}
        body = ''
        
        # Encontrar el final de los headers
        header_end = -1
        for i, line in enumerate(lines[1:], 1):
            if line == '':
                header_end = i
                break
            if ':' in line:
                key, value = line.split(':', 1)
                headers_dict[key.strip()] = value.strip()
                
        # Extraer el body si existe
        if header_end > 0 and len(lines) > header_end:
            body = '\r\n'.join(lines[header_end+1:])
            
        return headers_dict, body
        
    def parse_and_callback(self, request_text, host):
        """Parsear petición y llamar al callback"""
        try:
            lines = request_text.split('\r\n')
            if lines:
                first_line = lines[0]
                parts = first_line.split(' ')
                if len(parts) >= 2:
                    method = parts[0]
                    path = parts[1]
                    url = f"https://{host}{path}"
                    
                    headers_dict, body = self.parse_request(request_text)
                    
                    if self.callback:
                        self.callback(method, url, headers_dict, body)
        except Exception as e:
            print(f"Error parseando petición: {e}")


# Ejemplo de uso
if __name__ == '__main__':
    def on_request_captured(method, url, headers, body):
        print(f"\n=== Petición Capturada ===")
        print(f"Método: {method}")
        print(f"URL: {url}")
        print(f"Headers: {headers}")
        print(f"Body: {body[:200]}")
        print("=" * 40)
        
    proxy = HTTPSProxyHandler(callback=on_request_captured)
    
    try:
        proxy.start(host='0.0.0.0', port=8080)
    except KeyboardInterrupt:
        print("\nDeteniendo proxy...")
        proxy.stop()
