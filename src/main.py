#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║                    🏋️ GymForTheMoment                            ║
║              Sistema de Gestión de Gimnasio                      ║
╠══════════════════════════════════════════════════════════════════╣
║  Autor: Estudiante                                               ║
║  Versión: 1.0                                                    ║
║  Python: 3.8+                                                    ║
╚══════════════════════════════════════════════════════════════════╝

Aplicación para la gestión de un gimnasio que incluye:
- Gestión de clientes
- Gestión de aparatos de entrenamiento
- Reservas de sesiones de 30 minutos
- Control de pagos mensuales
- Listado de ocupación de aparatos por día
- Control de clientes morosos
"""

import sys
import os

# Asegurar que el directorio src está en el path
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from gui.app import main


if __name__ == "__main__":
    print("=" * 60)
    print("🏋️  GymForTheMoment - Sistema de Gestión de Gimnasio")
    print("=" * 60)
    print("\nIniciando aplicación...")
    print("Horario: 24 horas, Lunes a Viernes")
    print("Sesiones: 30 minutos por aparato")
    print("\n")
    
    main()
