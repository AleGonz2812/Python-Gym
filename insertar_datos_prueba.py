# -*- coding: utf-8 -*-
"""
Script para insertar datos de prueba en la base de datos
Ejecutar solo cuando sea necesario para pruebas
"""

import sys
import os

# Añadir src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from database.db_manager import DatabaseManager


def main():
    print("=" * 60)
    print("  Inserción de Datos de Prueba - GymForTheMoment")
    print("=" * 60)
    print()
    
    respuesta = input("¿Desea insertar datos de prueba? (s/n): ")
    
    if respuesta.lower() != 's':
        print("Operación cancelada")
        return
    
    db = DatabaseManager()
    db.connect()
    db.create_tables()
    
    try:
        db.insertar_datos_prueba()
        print("\n✓ Datos de prueba insertados correctamente")
        print("\nSe agregaron:")
        print("  - 5 clientes de ejemplo")
        print("  - 7 aparatos de ejemplo")
        print("  - Varias reservas de ejemplo")
        print("\nPuede iniciar sesión con:")
        print("  Email: admin@gymforthemoment.com")
        print("  Contraseña: admin123")
    except Exception as e:
        print(f"\n✗ Error al insertar datos: {str(e)}")
    finally:
        db.disconnect()


if __name__ == "__main__":
    main()
