# -*- coding: utf-8 -*-
"""
Script para ver todos los usuarios registrados
"""

import sqlite3

def ver_usuarios():
    print("=" * 70)
    print("  USUARIOS REGISTRADOS EN EL SISTEMA")
    print("=" * 70)
    
    conn = sqlite3.connect('gym_database.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id_usuario, nombre, email, password, rol, activo, fecha_creacion
        FROM usuario
        ORDER BY id_usuario
    """)
    
    usuarios = cursor.fetchall()
    
    if not usuarios:
        print("\nNo hay usuarios registrados.")
    else:
        print(f"\nTotal de usuarios: {len(usuarios)}\n")
        for user in usuarios:
            id_usuario, nombre, email, password, rol, activo, fecha = user
            estado = "ACTIVO" if activo else "INACTIVO"
            print(f"ID: {id_usuario}")
            print(f"Nombre: {nombre}")
            print(f"Email: {email}")
            print(f"Contraseña: {password}")
            print(f"Rol: {rol.upper()}")
            print(f"Estado: {estado}")
            print(f"Creado: {fecha}")
            print("-" * 70)
    
    conn.close()

if __name__ == "__main__":
    ver_usuarios()
