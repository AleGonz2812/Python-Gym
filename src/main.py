import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

from gui.login import mostrar_login
from gui.app import GymApp
import tkinter as tk


if __name__ == "__main__":
    print("=" * 60)
    print("  GymForTheMoment - Sistema de Gestion de Gimnasio")
    print("=" * 60)
    print("\nIniciando aplicacion...")
    print("Horario: 24 horas, Lunes a Viernes")
    print("Sesiones: 30 minutos por aparato")
    print("\n")
    
    # Mostrar login primero
    usuario = mostrar_login()
    
    if usuario:
        # Si el login fue exitoso, abrir aplicacion principal
        print(f"Usuario autenticado: {usuario['nombre']} ({usuario['rol']})")
        root = tk.Tk()
        app = GymApp(root, usuario)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()
    else:
        print("Login cancelado")
