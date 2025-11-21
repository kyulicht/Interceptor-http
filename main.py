#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interceptor HTTPS para Android
Aplicación que intercepta y modifica peticiones HTTPS
"""

import os
import json
import threading
from datetime import datetime

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

# Configuración de la ventana
Window.clearcolor = (0.1, 0.1, 0.1, 1)


class RequestItem:
    """Clase para almacenar información de una petición"""
    def __init__(self, url, method, headers, data):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data
        self.timestamp = datetime.now().strftime("%H:%M:%S")


class HTTPSInterceptorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interceptor_active = False
        self.proxy_thread = None
        self.captured_requests = []
        self.selected_request = None
        
    def build(self):
        """Construir la interfaz de usuario"""
        self.title = "HTTPS Interceptor"
        
        # Layout principal
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header con botón de activación
        header_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        self.status_label = Label(
            text='Estado: Inactivo',
            size_hint_x=0.7,
            color=(1, 0.5, 0, 1)
        )
        header_layout.add_widget(self.status_label)
        
        # Switch de activación
        switch_layout = BoxLayout(size_hint_x=0.3)
        switch_label = Label(text='Activar', size_hint_x=0.5)
        self.activate_switch = Switch(active=False, size_hint_x=0.5)
        self.activate_switch.bind(active=self.toggle_interceptor)
        switch_layout.add_widget(switch_label)
        switch_layout.add_widget(self.activate_switch)
        header_layout.add_widget(switch_layout)
        
        main_layout.add_widget(header_layout)
        
        # Lista de peticiones capturadas
        request_label = Label(
            text='Peticiones Capturadas:',
            size_hint_y=0.05,
            color=(0.8, 0.8, 1, 1)
        )
        main_layout.add_widget(request_label)
        
        # ScrollView para la lista de peticiones
        scroll = ScrollView(size_hint_y=0.3)
        self.request_list = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=5
        )
        self.request_list.bind(minimum_height=self.request_list.setter('height'))
        scroll.add_widget(self.request_list)
        main_layout.add_widget(scroll)
        
        # Sección de edición de petición
        edit_label = Label(
            text='Editar Petición Seleccionada:',
            size_hint_y=0.05,
            color=(0.8, 1, 0.8, 1)
        )
        main_layout.add_widget(edit_label)
        
        # URL
        url_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        url_layout.add_widget(Label(text='URL:', size_hint_x=0.2))
        self.url_input = TextInput(
            multiline=False,
            size_hint_x=0.8,
            hint_text='https://example.com/api'
        )
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Method
        method_layout = BoxLayout(size_hint_y=0.08, spacing=5)
        method_layout.add_widget(Label(text='Método:', size_hint_x=0.2))
        self.method_input = TextInput(
            multiline=False,
            size_hint_x=0.8,
            hint_text='GET, POST, PUT, DELETE...'
        )
        method_layout.add_widget(self.method_input)
        main_layout.add_widget(method_layout)
        
        # Headers
        headers_label = Label(text='Headers (JSON):', size_hint_y=0.05)
        main_layout.add_widget(headers_label)
        
        self.headers_input = TextInput(
            multiline=True,
            size_hint_y=0.15,
            hint_text='{"Content-Type": "application/json", "Authorization": "Bearer token"}'
        )
        main_layout.add_widget(self.headers_input)
        
        # Data/Body
        data_label = Label(text='Data/Body:', size_hint_y=0.05)
        main_layout.add_widget(data_label)
        
        self.data_input = TextInput(
            multiline=True,
            size_hint_y=0.15,
            hint_text='{"key": "value"}'
        )
        main_layout.add_widget(self.data_input)
        
        # Botones de acción
        button_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        
        self.resend_btn = Button(
            text='Reenviar Petición',
            background_color=(0.2, 0.6, 0.2, 1)
        )
        self.resend_btn.bind(on_press=self.resend_request)
        button_layout.add_widget(self.resend_btn)
        
        clear_btn = Button(
            text='Limpiar Lista',
            background_color=(0.6, 0.2, 0.2, 1)
        )
        clear_btn.bind(on_press=self.clear_requests)
        button_layout.add_widget(clear_btn)
        
        main_layout.add_widget(button_layout)
        
        return main_layout
    
    def toggle_interceptor(self, instance, value):
        """Activar/desactivar el interceptor"""
        if value:
            self.start_interceptor()
        else:
            self.stop_interceptor()
    
    def start_interceptor(self):
        """Iniciar el interceptor de peticiones"""
        try:
            self.interceptor_active = True
            self.status_label.text = 'Estado: Activo (Puerto: 8080)'
            self.status_label.color = (0, 1, 0, 1)
            
            # Iniciar el proxy en un hilo separado
            self.proxy_thread = threading.Thread(target=self.run_proxy, daemon=True)
            self.proxy_thread.start()
            
            self.show_popup('Éxito', 'Interceptor iniciado en puerto 8080\nConfigura tu dispositivo para usar este proxy.')
        except Exception as e:
            self.show_popup('Error', f'No se pudo iniciar el interceptor: {str(e)}')
            self.activate_switch.active = False
    
    def stop_interceptor(self):
        """Detener el interceptor"""
        self.interceptor_active = False
        self.status_label.text = 'Estado: Inactivo'
        self.status_label.color = (1, 0.5, 0, 1)
        self.show_popup('Info', 'Interceptor detenido')
    
    def run_proxy(self):
        """Ejecutar el servidor proxy (versión simplificada)"""
        # NOTA: Esta es una implementación simplificada
        # Para producción, se debería usar mitmproxy o similar
        import socket
        
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', 8080))
            server_socket.listen(5)
            server_socket.settimeout(1.0)
            
            while self.interceptor_active:
                try:
                    client_socket, addr = server_socket.accept()
                    threading.Thread(
                        target=self.handle_client,
                        args=(client_socket,),
                        daemon=True
                    ).start()
                except socket.timeout:
                    continue
                except Exception as e:
                    if self.interceptor_active:
                        print(f"Error aceptando conexión: {e}")
                    
            server_socket.close()
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_popup('Error', f'Error en proxy: {str(e)}'))
    
    def handle_client(self, client_socket):
        """Manejar conexión de cliente"""
        try:
            # Recibir datos del cliente
            request_data = client_socket.recv(4096).decode('utf-8', errors='ignore')
            
            if not request_data:
                return
            
            # Parsear la petición
            lines = request_data.split('\r\n')
            if lines:
                request_line = lines[0].split(' ')
                if len(request_line) >= 2:
                    method = request_line[0]
                    url = request_line[1]
                    
                    # Extraer headers
                    headers = {}
                    body = ''
                    header_section = True
                    
                    for i, line in enumerate(lines[1:]):
                        if line == '':
                            header_section = False
                            body = '\r\n'.join(lines[i+2:])
                            break
                        if header_section and ':' in line:
                            key, value = line.split(':', 1)
                            headers[key.strip()] = value.strip()
                    
                    # Guardar la petición capturada
                    request_item = RequestItem(url, method, headers, body)
                    self.captured_requests.append(request_item)
                    
                    # Actualizar UI
                    Clock.schedule_once(lambda dt: self.add_request_to_list(request_item))
            
            # Respuesta simple al cliente
            response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nPetición capturada"
            client_socket.sendall(response.encode())
            
        except Exception as e:
            print(f"Error manejando cliente: {e}")
        finally:
            client_socket.close()
    
    def add_request_to_list(self, request_item):
        """Agregar petición a la lista visual"""
        btn = Button(
            text=f"[{request_item.timestamp}] {request_item.method} {request_item.url[:50]}",
            size_hint_y=None,
            height=40,
            background_color=(0.2, 0.2, 0.3, 1)
        )
        btn.bind(on_press=lambda x: self.select_request(request_item))
        self.request_list.add_widget(btn)
    
    def select_request(self, request_item):
        """Seleccionar una petición para editar"""
        self.selected_request = request_item
        self.url_input.text = request_item.url
        self.method_input.text = request_item.method
        self.headers_input.text = json.dumps(request_item.headers, indent=2)
        self.data_input.text = request_item.data
    
    def resend_request(self, instance):
        """Reenviar la petición modificada"""
        try:
            import requests
            
            url = self.url_input.text
            method = self.method_input.text.upper()
            
            # Parsear headers
            try:
                headers = json.loads(self.headers_input.text) if self.headers_input.text else {}
            except:
                headers = {}
            
            # Parsear data
            data = self.data_input.text
            
            # Realizar la petición
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, data=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, data=data, timeout=10)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, timeout=10)
            else:
                self.show_popup('Error', 'Método HTTP no soportado')
                return
            
            self.show_popup(
                'Respuesta',
                f'Status: {response.status_code}\n\n{response.text[:500]}'
            )
            
        except Exception as e:
            self.show_popup('Error', f'Error enviando petición: {str(e)}')
    
    def clear_requests(self, instance):
        """Limpiar la lista de peticiones"""
        self.captured_requests.clear()
        self.request_list.clear_widgets()
        self.url_input.text = ''
        self.method_input.text = ''
        self.headers_input.text = ''
        self.data_input.text = ''
        self.show_popup('Info', 'Lista limpiada')
    
    def show_popup(self, title, message):
        """Mostrar un popup con mensaje"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        
        btn = Button(text='Cerrar', size_hint_y=0.3)
        content.add_widget(btn)
        
        popup = Popup(
            title=title,
            content=content,
            size_hint=(0.8, 0.5)
        )
        btn.bind(on_press=popup.dismiss)
        popup.open()


if __name__ == '__main__':
    HTTPSInterceptorApp().run()
