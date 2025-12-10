# -*- coding: utf-8 -*-
"""
GymForTheMoment - Pantalla de Login y Registro
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from utils.helpers import validar_dni, validar_email


class LoginWindow:
    """Ventana de inicio de sesión"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GymForTheMoment - Login")
        self.root.geometry("550x800")
        self.root.resizable(False, False)
        
        # Colores del tema
        self.COLOR_ROJO = '#DC143C'
        self.COLOR_NEGRO = '#1a1a1a'
        self.COLOR_GRIS = '#2d2d2d'
        self.COLOR_GRIS_CLARO = '#505050'
        self.COLOR_AMARILLO = '#FFD700'
        self.COLOR_BLANCO = '#FFFFFF'
        self.COLOR_TEXTO = '#E0E0E0'
        
        self.root.configure(bg=self.COLOR_NEGRO)
        
        # Inicializar BD
        self.db = DatabaseManager()
        self.db.connect()
        self.db.create_tables()
        self.db.crear_admin_inicial()
        
        # Variables
        self.usuario_autenticado = None
        self.mostrar_login = True
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        """Crea la interfaz de login/registro"""
        
        # Frame principal
        self.main_frame = tk.Frame(self.root, bg=self.COLOR_NEGRO)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Logo/Título
        titulo = tk.Label(
            self.main_frame,
            text="GymForTheMoment",
            font=('Arial', 24, 'bold'),
            bg=self.COLOR_NEGRO,
            fg=self.COLOR_ROJO
        )
        titulo.pack(pady=(0, 10))
        
        subtitulo = tk.Label(
            self.main_frame,
            text="Sistema de Gestion de Gimnasio",
            font=('Arial', 11),
            bg=self.COLOR_NEGRO,
            fg=self.COLOR_TEXTO
        )
        subtitulo.pack(pady=(0, 15))
        
        # Frame para el formulario
        self.form_frame = tk.Frame(self.main_frame, bg=self.COLOR_GRIS, relief=tk.FLAT, bd=0)
        self.form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Título del formulario
        self.form_titulo = tk.Label(
            self.form_frame,
            text="INICIAR SESION",
            font=('Arial', 14, 'bold'),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_AMARILLO
        )
        self.form_titulo.pack(pady=(30, 40))
        
        # Campos solo para registro
        self.label_nombre = tk.Label(
            self.form_frame,
            text="Nombre:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.entry_nombre = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            relief=tk.FLAT,
            bd=2
        )
        
        self.label_apellidos = tk.Label(
            self.form_frame,
            text="Apellidos:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.entry_apellidos = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            relief=tk.FLAT,
            bd=2
        )
        
        self.label_dni = tk.Label(
            self.form_frame,
            text="DNI:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.entry_dni = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            relief=tk.FLAT,
            bd=2
        )
        
        self.label_telefono = tk.Label(
            self.form_frame,
            text="Teléfono:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.entry_telefono = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            relief=tk.FLAT,
            bd=2
        )
        
        # Campo email
        self.label_email = tk.Label(
            self.form_frame,
            text="Email:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.label_email.pack(pady=(15, 5))
        
        self.entry_email = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            relief=tk.FLAT,
            bd=2
        )
        self.entry_email.pack(pady=(0, 20), ipadx=5, ipady=8, fill=tk.X, padx=30)
        
        # Campo contraseña
        self.label_password = tk.Label(
            self.form_frame,
            text="Contraseña:",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.label_password.pack(pady=(0, 5))
        
        self.entry_password = tk.Entry(
            self.form_frame,
            font=('Arial', 11),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            insertbackground=self.COLOR_AMARILLO,
            show='*',
            relief=tk.FLAT,
            bd=2
        )
        self.entry_password.pack(pady=(0, 15), ipadx=5, ipady=8, fill=tk.X, padx=30)
        
        # Botón principal
        self.btn_principal = tk.Button(
            self.form_frame,
            text="ENTRAR",
            font=('Arial', 11, 'bold'),
            bg=self.COLOR_ROJO,
            fg=self.COLOR_BLANCO,
            activebackground='#FF1744',
            activeforeground=self.COLOR_BLANCO,
            relief=tk.FLAT,
            bd=0,
            cursor='hand2',
            command=self.login
        )
        self.btn_principal.pack(pady=(25, 20), ipadx=40, ipady=10)
        
        # Separador
        separator = tk.Label(
            self.form_frame,
            text="─" * 30,
            font=('Arial', 8),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_GRIS_CLARO
        )
        separator.pack(pady=(20, 15))
        
        # Frame para texto con enlace
        self.frame_cambiar = tk.Frame(self.form_frame, bg=self.COLOR_GRIS)
        self.frame_cambiar.pack(pady=(5, 30))
        
        # Texto normal
        self.label_texto_cambiar = tk.Label(
            self.frame_cambiar,
            text="¿No tienes cuenta? ",
            font=('Arial', 10),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO
        )
        self.label_texto_cambiar.pack(side=tk.LEFT)
        
        # Enlace clicable
        self.label_link_cambiar = tk.Label(
            self.frame_cambiar,
            text="Regístrate",
            font=('Arial', 10, 'bold', 'underline'),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_AMARILLO,
            cursor='hand2'
        )
        self.label_link_cambiar.pack(side=tk.LEFT)
        self.label_link_cambiar.bind('<Button-1>', lambda e: self.cambiar_modo())
        
        # Efecto hover en el enlace
        self.label_link_cambiar.bind('<Enter>', lambda e: self.label_link_cambiar.config(fg=self.COLOR_ROJO))
        self.label_link_cambiar.bind('<Leave>', lambda e: self.label_link_cambiar.config(fg=self.COLOR_AMARILLO))
        
        # Info de admin
        info_frame = tk.Frame(self.main_frame, bg=self.COLOR_NEGRO)
        info_frame.pack(pady=(10, 0))
        
        tk.Label(
            info_frame,
            text="Admin: admin@gymforthemoment.com / admin123",
            font=('Arial', 8),
            bg=self.COLOR_NEGRO,
            fg=self.COLOR_GRIS_CLARO
        ).pack()
        
        # Bind Enter key
        self.entry_email.bind('<Return>', lambda e: self.entry_password.focus())
        self.entry_password.bind('<Return>', lambda e: self.ejecutar_accion())
    
    def ejecutar_accion(self):
        """Ejecuta login o registro según el modo actual"""
        if self.mostrar_login:
            self.login()
        else:
            self.registro()
    
    def cambiar_modo(self):
        """Cambia entre modo login y registro"""
        self.mostrar_login = not self.mostrar_login
        
        if self.mostrar_login:
            # Modo LOGIN
            self.form_titulo.config(text="INICIAR SESION")
            self.btn_principal.config(text="ENTRAR", command=self.login)
            self.label_texto_cambiar.config(text="¿No tienes cuenta? ")
            self.label_link_cambiar.config(text="Regístrate")
            print("Modo: LOGIN")  # Debug
            self.label_nombre.pack_forget()
            self.entry_nombre.pack_forget()
            self.label_apellidos.pack_forget()
            self.entry_apellidos.pack_forget()
            self.label_dni.pack_forget()
            self.entry_dni.pack_forget()
            self.label_telefono.pack_forget()
            self.entry_telefono.pack_forget()
        else:
            # Modo REGISTRO
            self.form_titulo.config(text="CREAR CUENTA DE CLIENTE")
            self.btn_principal.config(text="REGISTRARSE", command=self.registro)
            self.label_texto_cambiar.config(text="¿Ya tienes cuenta? ")
            self.label_link_cambiar.config(text="Inicia sesión")
            print("Modo: REGISTRO")  # Debug
            
            # Mostrar todos los campos ANTES del email (en orden)
            self.label_nombre.pack(pady=(10, 5), before=self.label_email)
            self.entry_nombre.pack(pady=(0, 5), ipadx=5, ipady=6, fill=tk.X, padx=30, before=self.label_email)
            
            self.label_apellidos.pack(pady=(0, 5), before=self.label_email)
            self.entry_apellidos.pack(pady=(0, 5), ipadx=5, ipady=6, fill=tk.X, padx=30, before=self.label_email)
            
            self.label_dni.pack(pady=(0, 5), before=self.label_email)
            self.entry_dni.pack(pady=(0, 5), ipadx=5, ipady=6, fill=tk.X, padx=30, before=self.label_email)
            
            self.label_telefono.pack(pady=(0, 5), before=self.label_email)
            self.entry_telefono.pack(pady=(0, 5), ipadx=5, ipady=6, fill=tk.X, padx=30, before=self.label_email)
        
        # Limpiar campos
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
    
    def login(self):
        """Procesa el inicio de sesión"""
        print("Ejecutando LOGIN...")  # Debug
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        if not email or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        usuario = self.db.validar_usuario(email, password)
        
        if usuario:
            self.usuario_autenticado = {
                'id': usuario['id_usuario'],
                'nombre': usuario['nombre'],
                'email': usuario['email'],
                'rol': usuario['rol']
            }
            messagebox.showinfo("Éxito", f"Bienvenido {usuario['nombre']}!")
            self.root.destroy()
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos")
    
    def registro(self):
        """Procesa el registro de nuevo usuario y cliente"""
        print("Ejecutando REGISTRO...")  # Debug
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip().upper()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get().strip()
        
        # Validar campos obligatorios
        if not nombre or not apellidos or not dni or not telefono or not email or not password:
            messagebox.showerror("Error", "Completa todos los campos")
            return
        
        # Validar DNI
        if not validar_dni(dni):
            messagebox.showerror("Error", "DNI inválido. Formato: 12345678A")
            return
        
        # Validar email
        if not validar_email(email):
            messagebox.showerror("Error", "Email inválido")
            return
        
        # Validar contraseña
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres")
            return
        
        # Verificar si ya existe el email
        if self.db.existe_usuario(email):
            messagebox.showerror("Error", "Ya existe un usuario con ese email")
            return
        
        # Verificar si ya existe el DNI
        cliente_existente = self.db.obtener_cliente_por_dni(dni)
        if cliente_existente:
            messagebox.showerror("Error", "Ya existe un cliente con ese DNI")
            return
        
        # Crear usuario empleado
        id_usuario = self.db.crear_usuario(nombre, email, password, 'empleado')
        
        if not id_usuario:
            messagebox.showerror("Error", "No se pudo crear el usuario")
            return
        
        # Crear cliente asociado
        id_cliente = self.db.crear_cliente(nombre, apellidos, dni, telefono, email)
        
        if id_cliente:
            messagebox.showinfo("Éxito", 
                              f"Usuario y cliente creados correctamente.\n\n"
                              f"Ya puedes iniciar sesión con tu email:\n{email}")
            self.cambiar_modo()  # Volver a modo login
        else:
            # Si falla la creación del cliente, eliminar el usuario
            messagebox.showerror("Error", "No se pudo crear el cliente. Inténtalo de nuevo.")
    
    def run(self):
        """Ejecuta la ventana de login"""
        self.root.mainloop()
        return self.usuario_autenticado


def mostrar_login():
    """Función para mostrar la ventana de login"""
    login_window = LoginWindow()
    return login_window.run()
