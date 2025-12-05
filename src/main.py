import sys
import os

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
