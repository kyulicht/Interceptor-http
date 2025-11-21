#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para ejecutar la aplicación en escritorio
Para testing antes de compilar para Android
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(__file__))

# Importar y ejecutar la aplicación
from main import HTTPSInterceptorApp

if __name__ == '__main__':
    print("=" * 60)
    print("HTTPS Interceptor - Modo de Prueba de Escritorio")
    print("=" * 60)
    print("")
    print("Esta es una versión de prueba para escritorio.")
    print("Para Android, compila con: buildozer android debug")
    print("")
    print("Iniciando aplicación...")
    print("")
    
    try:
        app = HTTPSInterceptorApp()
        app.run()
    except KeyboardInterrupt:
        print("\nAplicación cerrada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
