# -*- coding: utf-8 -*-
"""
GymForTheMoment - Interfaz Gráfica Principal
Aplicación de gestión de gimnasio con interfaz Tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import sys
import os

# Añadir el directorio padre al path para imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_manager import DatabaseManager
from utils.helpers import (
    DIAS_SEMANA, MESES, MENSUALIDAD,
    obtener_nombre_dia, obtener_nombre_mes,
    generar_franjas_horarias, validar_dni, validar_email,
    formatear_moneda, obtener_anio_actual, obtener_mes_actual
)


class GymApp:
    """Aplicación principal de gestión del gimnasio"""
    
    def __init__(self, root, usuario):
        self.root = root
        self.usuario = usuario  # Guardar info del usuario autenticado
        self.cerro_sesion = False  # Flag para saber si cerró sesión o salió
        self.root.title("GymForTheMoment - Sistema de Gestion")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Colores del tema: Rojo, Negro, Gris, Amarillo
        self.COLOR_ROJO = '#DC143C'      # Crimson red
        self.COLOR_NEGRO = '#1a1a1a'     # Negro
        self.COLOR_GRIS = '#2d2d2d'      # Gris oscuro
        self.COLOR_GRIS_CLARO = '#505050' # Gris medio
        self.COLOR_AMARILLO = '#FFD700'  # Dorado
        self.COLOR_BLANCO = '#FFFFFF'
        self.COLOR_TEXTO = '#E0E0E0'     # Texto claro
        
        # Configurar colores de fondo
        self.root.configure(bg=self.COLOR_NEGRO)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilo general
        self.style.configure('.',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_TEXTO,
                           borderwidth=0,
                           relief='flat')
        
        # Frames
        self.style.configure('TFrame',
                           background=self.COLOR_NEGRO)
        
        self.style.configure('TLabelframe',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_AMARILLO,
                           borderwidth=2,
                           relief='solid')
        
        self.style.configure('TLabelframe.Label',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_AMARILLO,
                           font=('Arial', 10, 'bold'))
        
        # Labels
        self.style.configure('TLabel',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_TEXTO,
                           font=('Arial', 9))
        
        self.style.configure('Title.TLabel',
                           background=self.COLOR_NEGRO,
                           foreground=self.COLOR_ROJO,
                           font=('Arial', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_AMARILLO,
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('Header.TLabel',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_AMARILLO,
                           font=('Arial', 10, 'bold'))
        
        # Botones - rectangulares con bordes definidos
        self.style.configure('TButton',
                           background=self.COLOR_ROJO,
                           foreground=self.COLOR_BLANCO,
                           borderwidth=0,
                           relief='flat',
                           font=('Arial', 9, 'bold'),
                           padding=(10, 5))
        
        self.style.map('TButton',
                      background=[('active', '#FF1744'), ('pressed', '#B71C1C')],
                      foreground=[('active', self.COLOR_BLANCO)])
        
        # Notebook (pestañas)
        self.style.configure('TNotebook',
                           background=self.COLOR_NEGRO,
                           borderwidth=0)
        
        self.style.configure('TNotebook.Tab',
                           background=self.COLOR_GRIS,
                           foreground=self.COLOR_TEXTO,
                           padding=[20, 8],
                           borderwidth=0,
                           font=('Arial', 10, 'bold'))
        
        self.style.map('TNotebook.Tab',
                      background=[('selected', self.COLOR_ROJO)],
                      foreground=[('selected', self.COLOR_BLANCO)])
        
        # Entry
        self.style.configure('TEntry',
                           fieldbackground=self.COLOR_GRIS_CLARO,
                           foreground=self.COLOR_BLANCO,
                           borderwidth=1,
                           relief='solid',
                           insertcolor=self.COLOR_AMARILLO)
        
        # Combobox - Configuración mejorada para visibilidad
        self.style.configure('TCombobox',
                           fieldbackground='white',
                           background='white',
                           foreground='black',
                           selectbackground=self.COLOR_ROJO,
                           selectforeground='white',
                           borderwidth=1,
                           arrowcolor=self.COLOR_ROJO)
        
        self.style.map('TCombobox',
                      fieldbackground=[('readonly', 'white'), ('disabled', self.COLOR_GRIS_CLARO)],
                      foreground=[('readonly', 'black'), ('disabled', '#666666')],
                      background=[('readonly', 'white'), ('active', self.COLOR_ROJO)],
                      selectbackground=[('readonly', self.COLOR_ROJO)])
        
        # Treeview
        self.style.configure('Treeview',
                           background=self.COLOR_GRIS_CLARO,
                           foreground=self.COLOR_BLANCO,
                           fieldbackground=self.COLOR_GRIS_CLARO,
                           borderwidth=0,
                           relief='flat',
                           font=('Arial', 9))
        
        self.style.configure('Treeview.Heading',
                           background=self.COLOR_ROJO,
                           foreground=self.COLOR_BLANCO,
                           borderwidth=0,
                           relief='flat',
                           font=('Arial', 9, 'bold'))
        
        self.style.map('Treeview',
                      background=[('selected', self.COLOR_ROJO)],
                      foreground=[('selected', self.COLOR_BLANCO)])
        
        self.style.map('Treeview.Heading',
                      background=[('active', '#FF1744')])
        
        # Scrollbar
        self.style.configure('Vertical.TScrollbar',
                           background=self.COLOR_GRIS,
                           troughcolor=self.COLOR_NEGRO,
                           borderwidth=0,
                           arrowcolor=self.COLOR_AMARILLO)
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        self.db.connect()
        self.db.create_tables()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        if self.usuario['rol'] == 'admin':
            self.cargar_clientes()
        self.cargar_aparatos()
        
    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas"""
        
        # Crear menú
        menubar = tk.Menu(self.root, bg=self.COLOR_GRIS, fg=self.COLOR_TEXTO,
                         activebackground=self.COLOR_ROJO, activeforeground=self.COLOR_BLANCO)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        menu_archivo = tk.Menu(menubar, tearoff=0, bg=self.COLOR_GRIS, fg=self.COLOR_TEXTO,
                              activebackground=self.COLOR_ROJO, activeforeground=self.COLOR_BLANCO)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)
        menu_archivo.add_command(label="Salir", command=self.on_closing)
        
        # Menú Ayuda
        menu_ayuda = tk.Menu(menubar, tearoff=0, bg=self.COLOR_GRIS, fg=self.COLOR_TEXTO,
                            activebackground=self.COLOR_ROJO, activeforeground=self.COLOR_BLANCO)
        menubar.add_cascade(label="Ayuda", menu=menu_ayuda)
        menu_ayuda.add_command(label="Acerca de", command=self.mostrar_acerca_de)
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame superior para título y botón cerrar sesión
        frame_header = ttk.Frame(self.main_frame)
        frame_header.pack(fill=tk.X, pady=(0, 10))
        
        # Título
        titulo = ttk.Label(
            frame_header, 
            text="GymForTheMoment - Sistema de Gestion",
            style='Title.TLabel'
        )
        titulo.pack(side=tk.LEFT)
        
        # Botón cerrar sesión (en la esquina superior derecha)
        btn_cerrar_sesion = tk.Button(
            frame_header,
            text="Cerrar Sesion",
            font=('Arial', 10, 'bold'),
            bg=self.COLOR_ROJO,
            fg=self.COLOR_BLANCO,
            activebackground='#FF1744',
            command=self.cerrar_sesion,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=8
        )
        btn_cerrar_sesion.pack(side=tk.RIGHT)
        
        # Notebook (pestañas)
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Crear pestañas
        self.tab_clientes = ttk.Frame(self.notebook, padding="10")
        self.tab_aparatos = ttk.Frame(self.notebook, padding="10")
        self.tab_reservas = ttk.Frame(self.notebook, padding="10")
        self.tab_ocupacion = ttk.Frame(self.notebook, padding="10")
        self.tab_pagos = ttk.Frame(self.notebook, padding="10")
        self.tab_morosos = ttk.Frame(self.notebook, padding="10")
        
        # Solo mostrar tab Clientes si es admin
        if self.usuario['rol'] == 'admin':
            self.notebook.add(self.tab_clientes, text="Clientes")
        
        self.notebook.add(self.tab_aparatos, text="Aparatos")
        self.notebook.add(self.tab_reservas, text="Reservas")
        self.notebook.add(self.tab_ocupacion, text="Ocupacion")
        self.notebook.add(self.tab_pagos, text="Pagos")
        self.notebook.add(self.tab_morosos, text="Morosos")
        
        # Barra de estado (crear antes de configurar pestañas)
        self.status_var = tk.StringVar(value=f"Usuario: {self.usuario['nombre']} ({self.usuario['rol']}) | Listo")
        
        # Configurar cada pestaña
        if self.usuario['rol'] == 'admin':
            self.configurar_tab_clientes()
        self.configurar_tab_aparatos()
        self.configurar_tab_reservas()
        self.configurar_tab_ocupacion()
        self.configurar_tab_pagos()
        self.configurar_tab_morosos()
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    # ==================== PESTAÑA CLIENTES ====================
    
    def configurar_tab_clientes(self):
        """Configura la pestaña de gestión de clientes (solo admin - solo eliminar)"""
        
        # Título informativo
        info_label = tk.Label(
            self.tab_clientes,
            text="Gestión de Clientes - Solo Administrador",
            font=('Arial', 12, 'bold'),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_AMARILLO
        )
        info_label.pack(pady=(0, 10))
        
        info_text = tk.Label(
            self.tab_clientes,
            text="Los clientes se crean automáticamente al registrarse.\nAquí solo puedes eliminarlos si es necesario.",
            font=('Arial', 9),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO,
            justify=tk.CENTER
        )
        info_text.pack(pady=(0, 15))
        
        # Frame para la lista
        frame_lista = ttk.LabelFrame(self.tab_clientes, text="Lista de Clientes Registrados", padding="10")
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
        # Treeview para clientes
        columns = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Email', 'Fecha Alta')
        self.tree_clientes = ttk.Treeview(frame_lista, columns=columns, show='headings', height=20)
        
        self.tree_clientes.heading('ID', text='ID')
        self.tree_clientes.heading('Nombre', text='Nombre')
        self.tree_clientes.heading('Apellidos', text='Apellidos')
        self.tree_clientes.heading('DNI', text='DNI')
        self.tree_clientes.heading('Teléfono', text='Teléfono')
        self.tree_clientes.heading('Email', text='Email')
        self.tree_clientes.heading('Fecha Alta', text='Fecha Alta')
        
        self.tree_clientes.column('ID', width=50, anchor=tk.CENTER)
        self.tree_clientes.column('Nombre', width=120)
        self.tree_clientes.column('Apellidos', width=150)
        self.tree_clientes.column('DNI', width=100, anchor=tk.CENTER)
        self.tree_clientes.column('Teléfono', width=110, anchor=tk.CENTER)
        self.tree_clientes.column('Email', width=200)
        self.tree_clientes.column('Fecha Alta', width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame para botones
        frame_botones = ttk.Frame(self.tab_clientes)
        frame_botones.pack(pady=10)
        
        btn_eliminar = tk.Button(
            frame_botones,
            text="ELIMINAR CLIENTE SELECCIONADO",
            font=('Arial', 10, 'bold'),
            bg=self.COLOR_ROJO,
            fg=self.COLOR_BLANCO,
            activebackground='#FF1744',
            command=self.eliminar_cliente,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0
        )
        btn_eliminar.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        
        btn_refrescar = tk.Button(
            frame_botones,
            text="REFRESCAR",
            font=('Arial', 10),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            activebackground=self.COLOR_GRIS,
            command=self.cargar_clientes,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0
        )
        btn_refrescar.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
        
        # Variable para ID seleccionado
        self.cliente_seleccionado_id = None
        self.tree_clientes.bind('<<TreeviewSelect>>', self.seleccionar_cliente_simple)
    
    def seleccionar_cliente_simple(self, event):
        """Maneja la selección de un cliente"""
        selection = self.tree_clientes.selection()
        if selection:
            item = self.tree_clientes.item(selection[0])
            values = item['values']
            self.cliente_seleccionado_id = values[0]
    
    def cargar_clientes(self):
        """Carga los clientes en el treeview"""
        # Limpiar treeview
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        
        # Obtener clientes
        clientes = self.db.obtener_clientes()
        
        for cliente in clientes:
            self.tree_clientes.insert('', tk.END, values=(
                cliente['id_cliente'],
                cliente['nombre'],
                cliente['apellidos'],
                cliente['dni'],
                cliente['telefono'] or '',
                cliente['email'] or '',
                cliente['fecha_alta'][:10] if cliente['fecha_alta'] else ''
            ))
        
        self.status_var.set(f"Usuario: {self.usuario['nombre']} ({self.usuario['rol']}) | {len(clientes)} clientes registrados")
    
    def seleccionar_cliente(self, event):
        """Maneja la selección de un cliente en el treeview"""
        selection = self.tree_clientes.selection()
        if selection:
            item = self.tree_clientes.item(selection[0])
            values = item['values']
            
            self.cliente_seleccionado_id = values[0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_apellidos.delete(0, tk.END)
            self.entry_apellidos.insert(0, values[2])
            self.entry_dni.delete(0, tk.END)
            self.entry_dni.insert(0, values[3])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, values[4])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, values[5])
    
    
    def eliminar_cliente(self):
        """Elimina el cliente seleccionado (solo admin)"""
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Aviso", "Seleccione un cliente de la lista para eliminar")
            return
        
        # Obtener info del cliente
        selection = self.tree_clientes.selection()
        if not selection:
            return
            
        item = self.tree_clientes.item(selection[0])
        values = item['values']
        nombre_completo = f"{values[1]} {values[2]}"
        
        if messagebox.askyesno("Confirmar Eliminación", 
                              f"¿Está seguro de eliminar al cliente?\n\n"
                              f"Nombre: {nombre_completo}\n"
                              f"DNI: {values[3]}\n\n"
                              f"Esta acción no se puede deshacer."):
            if self.db.eliminar_cliente(self.cliente_seleccionado_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cliente_seleccionado_id = None
                self.cargar_clientes()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente.\n"
                                   "Puede tener reservas o pagos asociados.")
    
    # ==================== PESTAÑA APARATOS ====================
    
    def configurar_tab_aparatos(self):
        """Configura la pestaña de gestión de aparatos"""
        
        if self.usuario['rol'] == 'admin':
            # MODO ADMIN: Con formulario de edición
            # Frame izquierdo: Lista
            frame_lista = ttk.LabelFrame(self.tab_aparatos, text="Lista de Aparatos", padding="5")
            frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            
            columns = ('ID', 'Nombre', 'Tipo', 'Descripción')
            self.tree_aparatos = ttk.Treeview(frame_lista, columns=columns, show='headings', height=15)
            
            for col in columns:
                self.tree_aparatos.heading(col, text=col)
            
            self.tree_aparatos.column('ID', width=50)
            self.tree_aparatos.column('Nombre', width=150)
            self.tree_aparatos.column('Tipo', width=100)
            self.tree_aparatos.column('Descripción', width=200)
            
            scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_aparatos.yview)
            self.tree_aparatos.configure(yscrollcommand=scrollbar.set)
            
            self.tree_aparatos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Frame derecho: Formulario
            frame_form = ttk.LabelFrame(self.tab_aparatos, text="Datos del Aparato", padding="10")
            frame_form.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
            
            ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
            self.entry_aparato_nombre = ttk.Entry(frame_form, width=25)
            self.entry_aparato_nombre.grid(row=0, column=1, pady=2)
            
            ttk.Label(frame_form, text="Tipo:").grid(row=1, column=0, sticky=tk.W, pady=2)
            self.combo_tipo = ttk.Combobox(frame_form, width=22, values=['Cardio', 'Musculación', 'Funcional'])
            self.combo_tipo.grid(row=1, column=1, pady=2)
            
            ttk.Label(frame_form, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=2)
            self.entry_aparato_desc = ttk.Entry(frame_form, width=25)
            self.entry_aparato_desc.grid(row=2, column=1, pady=2)
            
            # Botones
            frame_botones = ttk.Frame(frame_form)
            frame_botones.grid(row=3, column=0, columnspan=2, pady=10)
            
            ttk.Button(frame_botones, text="+ Nuevo", command=self.nuevo_aparato).pack(side=tk.LEFT, padx=2)
            ttk.Button(frame_botones, text="Guardar", command=self.guardar_aparato).pack(side=tk.LEFT, padx=2)
            ttk.Button(frame_botones, text="Eliminar", command=self.eliminar_aparato).pack(side=tk.LEFT, padx=2)
            ttk.Button(frame_botones, text="Refrescar", command=self.cargar_aparatos).pack(side=tk.LEFT, padx=2)
            
            self.tree_aparatos.bind('<<TreeviewSelect>>', self.seleccionar_aparato)
            self.aparato_seleccionado_id = None
        else:
            # MODO EMPLEADO: Solo lista de consulta
            info_label = tk.Label(
                self.tab_aparatos,
                text="Aparatos Disponibles",
                font=('Arial', 12, 'bold'),
                bg=self.COLOR_GRIS,
                fg=self.COLOR_AMARILLO
            )
            info_label.pack(pady=(0, 10))
            
            frame_lista = ttk.LabelFrame(self.tab_aparatos, text="Lista de Aparatos del Gimnasio", padding="10")
            frame_lista.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
            
            columns = ('ID', 'Nombre', 'Tipo', 'Descripción')
            self.tree_aparatos = ttk.Treeview(frame_lista, columns=columns, show='headings', height=25)
            
            self.tree_aparatos.heading('ID', text='ID')
            self.tree_aparatos.heading('Nombre', text='Nombre')
            self.tree_aparatos.heading('Tipo', text='Tipo')
            self.tree_aparatos.heading('Descripción', text='Descripción')
            
            self.tree_aparatos.column('ID', width=60, anchor=tk.CENTER)
            self.tree_aparatos.column('Nombre', width=200)
            self.tree_aparatos.column('Tipo', width=150)
            self.tree_aparatos.column('Descripción', width=400)
            
            scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_aparatos.yview)
            self.tree_aparatos.configure(yscrollcommand=scrollbar.set)
            
            self.tree_aparatos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Botón refrescar
            btn_refrescar = tk.Button(
                self.tab_aparatos,
                text="REFRESCAR",
                font=('Arial', 10),
                bg=self.COLOR_GRIS_CLARO,
                fg=self.COLOR_BLANCO,
                activebackground=self.COLOR_GRIS,
                command=self.cargar_aparatos,
                cursor='hand2',
                relief=tk.FLAT,
                bd=0
            )
            btn_refrescar.pack(pady=10, ipadx=15, ipady=8)
    
    def cargar_aparatos(self):
        """Carga los aparatos en el treeview"""
        for item in self.tree_aparatos.get_children():
            self.tree_aparatos.delete(item)
        
        aparatos = self.db.obtener_aparatos()
        
        for aparato in aparatos:
            self.tree_aparatos.insert('', tk.END, values=(
                aparato['id_aparato'],
                aparato['nombre'],
                aparato['tipo'],
                aparato['descripcion'] or ''
            ))
        
        self.status_var.set(f"Se cargaron {len(aparatos)} aparatos")
    
    def seleccionar_aparato(self, event):
        """Maneja la selección de un aparato"""
        selection = self.tree_aparatos.selection()
        if selection:
            item = self.tree_aparatos.item(selection[0])
            values = item['values']
            
            self.aparato_seleccionado_id = values[0]
            self.entry_aparato_nombre.delete(0, tk.END)
            self.entry_aparato_nombre.insert(0, values[1])
            self.combo_tipo.set(values[2])
            self.entry_aparato_desc.delete(0, tk.END)
            self.entry_aparato_desc.insert(0, values[3])
    
    def nuevo_aparato(self):
        """Limpia el formulario para un nuevo aparato"""
        self.aparato_seleccionado_id = None
        self.entry_aparato_nombre.delete(0, tk.END)
        self.combo_tipo.set('')
        self.entry_aparato_desc.delete(0, tk.END)
        self.entry_aparato_nombre.focus()
    
    def guardar_aparato(self):
        """Guarda o actualiza un aparato"""
        nombre = self.entry_aparato_nombre.get().strip()
        tipo = self.combo_tipo.get().strip()
        descripcion = self.entry_aparato_desc.get().strip()
        
        if not nombre or not tipo:
            messagebox.showerror("Error", "Nombre y tipo son obligatorios")
            return
        
        try:
            if self.aparato_seleccionado_id:
                if self.db.actualizar_aparato(self.aparato_seleccionado_id, nombre, tipo, descripcion):
                    messagebox.showinfo("Éxito", "Aparato actualizado correctamente")
                    self.cargar_aparatos()
            else:
                id_nuevo = self.db.insertar_aparato(nombre, tipo, descripcion)
                if id_nuevo:
                    messagebox.showinfo("Éxito", f"Aparato creado con ID: {id_nuevo}")
                    self.cargar_aparatos()
                    self.nuevo_aparato()
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def eliminar_aparato(self):
        """Elimina el aparato seleccionado"""
        if not self.aparato_seleccionado_id:
            messagebox.showwarning("Aviso", "Seleccione un aparato para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este aparato?"):
            if self.db.eliminar_aparato(self.aparato_seleccionado_id):
                messagebox.showinfo("Éxito", "Aparato eliminado correctamente")
                self.cargar_aparatos()
                self.nuevo_aparato()
    
    # ==================== PESTAÑA RESERVAS ====================
    
    def configurar_tab_reservas(self):
        """Configura la pestaña de reservas"""
        
        # Frame superior: Nueva reserva
        frame_nueva = ttk.LabelFrame(self.tab_reservas, text="Nueva Reserva (puede seleccionar múltiples franjas horarias)", padding="10")
        frame_nueva.pack(fill=tk.X, pady=(0, 10))
        
        # Fila 1: Cliente, Aparato, Día
        frame_fila1 = ttk.Frame(frame_nueva)
        frame_fila1.pack(fill=tk.X, pady=5)
        
        # Cliente
        ttk.Label(frame_fila1, text="Cliente:").pack(side=tk.LEFT, padx=5)
        self.combo_reserva_cliente = ttk.Combobox(frame_fila1, width=35, state='readonly')
        self.combo_reserva_cliente.pack(side=tk.LEFT, padx=5)
        
        # Aparato
        ttk.Label(frame_fila1, text="Aparato:").pack(side=tk.LEFT, padx=15)
        self.combo_reserva_aparato = ttk.Combobox(frame_fila1, width=30, state='readonly')
        self.combo_reserva_aparato.pack(side=tk.LEFT, padx=5)
        
        # Día
        ttk.Label(frame_fila1, text="Día:").pack(side=tk.LEFT, padx=15)
        self.combo_reserva_dia = ttk.Combobox(frame_fila1, width=12, state='readonly')
        self.combo_reserva_dia['values'] = list(DIAS_SEMANA.values())
        self.combo_reserva_dia.pack(side=tk.LEFT, padx=5)
        
        # Fila 2: Hora con Combobox y botón agregar
        frame_fila2 = ttk.Frame(frame_nueva)
        frame_fila2.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_fila2, text="Hora:").pack(side=tk.LEFT, padx=5)
        self.combo_reserva_hora = ttk.Combobox(frame_fila2, width=25, state='readonly')
        franjas = generar_franjas_horarias()
        self.combo_reserva_hora['values'] = [f[0] for f in franjas]
        self.combo_reserva_hora.pack(side=tk.LEFT, padx=5)
        
        # Botón agregar hora
        tk.Button(
            frame_fila2,
            text="+ Agregar",
            font=('Arial', 9, 'bold'),
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_BLANCO,
            activebackground=self.COLOR_GRIS,
            command=self.agregar_hora_reserva,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Botón limpiar horas
        tk.Button(
            frame_fila2,
            text="Limpiar",
            font=('Arial', 9),
            bg=self.COLOR_GRIS,
            fg=self.COLOR_TEXTO,
            activebackground=self.COLOR_GRIS_CLARO,
            command=self.limpiar_horas_reserva,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT, padx=5, ipadx=10, ipady=5)
        
        # Fila 3: Lista de horas seleccionadas
        frame_fila3 = ttk.Frame(frame_nueva)
        frame_fila3.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_fila3, text="Horas seleccionadas:").pack(side=tk.LEFT, padx=5)
        
        # Listbox para mostrar horas agregadas
        self.listbox_horas_seleccionadas = tk.Listbox(
            frame_fila3,
            height=3,
            width=60,
            bg=self.COLOR_GRIS_CLARO,
            fg=self.COLOR_AMARILLO,
            selectbackground=self.COLOR_ROJO,
            selectforeground=self.COLOR_BLANCO,
            font=('Arial', 9)
        )
        self.listbox_horas_seleccionadas.pack(side=tk.LEFT, padx=5)
        
        # Botón reservar
        tk.Button(
            frame_fila3,
            text="RESERVAR",
            font=('Arial', 10, 'bold'),
            bg=self.COLOR_ROJO,
            fg=self.COLOR_BLANCO,
            activebackground='#FF1744',
            command=self.realizar_reserva,
            cursor='hand2',
            relief=tk.FLAT,
            bd=0
        ).pack(side=tk.LEFT, padx=20, ipadx=20, ipady=8)
        
        # Frame inferior: Lista de reservas
        frame_lista = ttk.LabelFrame(self.tab_reservas, text="Reservas Actuales", padding="5")
        frame_lista.pack(fill=tk.BOTH, expand=True)
        
        # Filtro por día
        frame_filtro = ttk.Frame(frame_lista)
        frame_filtro.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_filtro, text="Filtrar por día:").pack(side=tk.LEFT, padx=5)
        self.combo_filtro_dia = ttk.Combobox(frame_filtro, width=15, state='readonly')
        self.combo_filtro_dia['values'] = ['Todos'] + list(DIAS_SEMANA.values())
        self.combo_filtro_dia.set('Todos')
        self.combo_filtro_dia.pack(side=tk.LEFT, padx=5)
        self.combo_filtro_dia.bind('<<ComboboxSelected>>', self.filtrar_reservas)
        
        ttk.Button(frame_filtro, text="Cancelar Reserva", command=self.cancelar_reserva).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        columns = ('ID', 'Cliente', 'Aparato', 'Día', 'Hora Inicio', 'Hora Fin')
        self.tree_reservas = ttk.Treeview(frame_lista, columns=columns, show='headings', height=12)
        
        for col in columns:
            self.tree_reservas.heading(col, text=col)
        
        self.tree_reservas.column('ID', width=50)
        self.tree_reservas.column('Cliente', width=200)
        self.tree_reservas.column('Aparato', width=150)
        self.tree_reservas.column('Día', width=100)
        self.tree_reservas.column('Hora Inicio', width=100)
        self.tree_reservas.column('Hora Fin', width=100)
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_reservas.yview)
        self.tree_reservas.configure(yscrollcommand=scrollbar.set)
        
        self.tree_reservas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar datos en combos
        self.actualizar_combos_reserva()
        self.cargar_reservas()
    
    def actualizar_combos_reserva(self):
        """Actualiza los combobox de la pestaña reservas"""
        # Clientes
        clientes = self.db.obtener_clientes()
        self.combo_reserva_cliente['values'] = [
            f"{c['id_cliente']} - {c['nombre']} {c['apellidos']}" for c in clientes
        ]
        
        # Aparatos
        aparatos = self.db.obtener_aparatos()
        self.combo_reserva_aparato['values'] = [
            f"{a['id_aparato']} - {a['nombre']}" for a in aparatos
        ]
    
    def cargar_reservas(self, dia_filtro=None):
        """Carga las reservas en el treeview"""
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        
        # Obtener todas las reservas de todos los días
        todas_reservas = []
        for dia_num in range(1, 6):
            if dia_filtro and DIAS_SEMANA[dia_num] != dia_filtro:
                continue
            reservas = self.db.obtener_reservas_por_dia(dia_num)
            for r in reservas:
                todas_reservas.append(r)
        
        for reserva in todas_reservas:
            self.tree_reservas.insert('', tk.END, values=(
                reserva['id_reserva'],
                f"{reserva['cliente_nombre']} {reserva['cliente_apellidos']}",
                reserva['aparato_nombre'],
                DIAS_SEMANA.get(reserva['dia_semana'], ''),
                reserva['hora_inicio'],
                reserva['hora_fin']
            ))
        
        self.status_var.set(f"Se cargaron {len(todas_reservas)} reservas")
    
    def filtrar_reservas(self, event=None):
        """Filtra las reservas por día"""
        dia = self.combo_filtro_dia.get()
        if dia == 'Todos':
            self.cargar_reservas()
        else:
            self.cargar_reservas(dia)
    
    def agregar_hora_reserva(self):
        """Agrega una hora a la lista de horas seleccionadas"""
        hora = self.combo_reserva_hora.get()
        
        if not hora:
            messagebox.showwarning("Aviso", "Seleccione una hora primero")
            return
        
        # Verificar que no esté duplicada
        horas_actuales = self.listbox_horas_seleccionadas.get(0, tk.END)
        if hora in horas_actuales:
            messagebox.showwarning("Aviso", "Esta hora ya está en la lista")
            return
        
        # Agregar a la lista
        self.listbox_horas_seleccionadas.insert(tk.END, hora)
        self.combo_reserva_hora.set('')  # Limpiar combobox
    
    def limpiar_horas_reserva(self):
        """Limpia todas las horas seleccionadas"""
        self.listbox_horas_seleccionadas.delete(0, tk.END)
    
    def realizar_reserva(self):
        """Realiza una o múltiples reservas"""
        cliente_sel = self.combo_reserva_cliente.get()
        aparato_sel = self.combo_reserva_aparato.get()
        dia_sel = self.combo_reserva_dia.get()
        
        # Obtener horas de la lista
        num_horas = self.listbox_horas_seleccionadas.size()
        horas_seleccionadas = [self.listbox_horas_seleccionadas.get(i) for i in range(num_horas)]
        
        if not all([cliente_sel, aparato_sel, dia_sel]):
            messagebox.showerror("Error", "Complete cliente, aparato y día")
            return
        
        if not horas_seleccionadas:
            messagebox.showerror("Error", "Agregue al menos una hora con el botón '+ Agregar'")
            return
        
        # Extraer IDs
        id_cliente = int(cliente_sel.split(' - ')[0])
        id_aparato = int(aparato_sel.split(' - ')[0])
        dia_num = [k for k, v in DIAS_SEMANA.items() if v == dia_sel][0]
        
        # Verificar disponibilidad de todas las franjas
        no_disponibles = []
        for hora in horas_seleccionadas:
            if not self.db.verificar_disponibilidad(id_aparato, dia_num, hora):
                no_disponibles.append(hora)
        
        if no_disponibles:
            messagebox.showerror("Error", 
                               f"Las siguientes franjas ya están ocupadas:\n" + 
                               "\n".join(no_disponibles))
            return
        
        # Realizar todas las reservas
        reservas_creadas = 0
        for hora in horas_seleccionadas:
            id_reserva = self.db.insertar_reserva(id_cliente, id_aparato, dia_num, hora)
            if id_reserva:
                reservas_creadas += 1
        
        if reservas_creadas > 0:
            messagebox.showinfo("Éxito", 
                              f"Se crearon {reservas_creadas} reserva(s) correctamente")
            self.cargar_reservas()
            # Limpiar campos
            self.combo_reserva_cliente.set('')
            self.combo_reserva_aparato.set('')
            self.combo_reserva_dia.set('')
            self.combo_reserva_hora.set('')
            self.listbox_horas_seleccionadas.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No se pudo crear ninguna reserva")
    
    def cancelar_reserva(self):
        """Cancela la reserva seleccionada"""
        selection = self.tree_reservas.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Seleccione una reserva para cancelar")
            return
        
        item = self.tree_reservas.item(selection[0])
        id_reserva = item['values'][0]
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de cancelar esta reserva?"):
            if self.db.cancelar_reserva(id_reserva):
                messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
                self.cargar_reservas()
    
    # ==================== PESTAÑA OCUPACIÓN ====================
    
    def configurar_tab_ocupacion(self):
        """Configura la pestaña de ocupación de aparatos"""
        
        # Frame superior: Selectores
        frame_selector = ttk.Frame(self.tab_ocupacion)
        frame_selector.pack(fill=tk.X, pady=10)
        
        # Selector de día
        ttk.Label(frame_selector, text="Dia:", 
                  style='Subtitle.TLabel').pack(side=tk.LEFT, padx=10)
        
        self.combo_ocupacion_dia = ttk.Combobox(frame_selector, width=12, state='readonly')
        self.combo_ocupacion_dia['values'] = list(DIAS_SEMANA.values())
        self.combo_ocupacion_dia.pack(side=tk.LEFT, padx=5)
        
        # Selector de tipo de aparato
        ttk.Label(frame_selector, text="Tipo de Aparato:", 
                  style='Subtitle.TLabel').pack(side=tk.LEFT, padx=20)
        
        self.combo_ocupacion_tipo = ttk.Combobox(frame_selector, width=15, state='readonly')
        self.combo_ocupacion_tipo['values'] = ['Todos', 'Cardio', 'Musculación', 'Funcional']
        self.combo_ocupacion_tipo.set('Todos')
        self.combo_ocupacion_tipo.pack(side=tk.LEFT, padx=5)
        
        # Botón ver ocupación
        ttk.Button(frame_selector, text="Ver Ocupacion", 
                   command=self.mostrar_ocupacion).pack(side=tk.LEFT, padx=20)
        
        # Frame para el listado
        frame_lista = ttk.LabelFrame(self.tab_ocupacion, text="Ocupación de Aparatos", padding="5")
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview para ocupación
        columns = ('Aparato', 'Tipo', 'Hora', 'Estado', 'Cliente')
        self.tree_ocupacion = ttk.Treeview(frame_lista, columns=columns, show='headings', height=20)
        
        self.tree_ocupacion.heading('Aparato', text='Aparato')
        self.tree_ocupacion.heading('Tipo', text='Tipo')
        self.tree_ocupacion.heading('Hora', text='Franja Horaria')
        self.tree_ocupacion.heading('Estado', text='Estado')
        self.tree_ocupacion.heading('Cliente', text='Cliente')
        
        self.tree_ocupacion.column('Aparato', width=150)
        self.tree_ocupacion.column('Tipo', width=100)
        self.tree_ocupacion.column('Hora', width=120)
        self.tree_ocupacion.column('Estado', width=100)
        self.tree_ocupacion.column('Cliente', width=200)
        
        # Tags para colores - tonos oscuros y suaves
        self.tree_ocupacion.tag_configure('ocupado', 
                                         background='#4a2020',  # Rojo muy oscuro
                                         foreground='#ffcccc')  # Texto claro
        self.tree_ocupacion.tag_configure('libre', 
                                         background='#1a3a1a',  # Verde muy oscuro
                                         foreground='#ccffcc')  # Texto claro
        self.tree_ocupacion.tag_configure('separador', 
                                         background=self.COLOR_AMARILLO,  # Amarillo
                                         foreground=self.COLOR_NEGRO,     # Negro
                                         font=('Arial', 9, 'bold'))
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_ocupacion.yview)
        self.tree_ocupacion.configure(yscrollcommand=scrollbar.set)
        
        self.tree_ocupacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def mostrar_ocupacion(self):
        """Muestra la ocupación de aparatos para el día seleccionado"""
        dia_sel = self.combo_ocupacion_dia.get()
        tipo_sel = self.combo_ocupacion_tipo.get()
        
        if not dia_sel:
            messagebox.showwarning("Aviso", "Seleccione un día de la semana")
            return
        
        # Limpiar treeview
        for item in self.tree_ocupacion.get_children():
            self.tree_ocupacion.delete(item)
        
        # Obtener número de día
        dia_num = [k for k, v in DIAS_SEMANA.items() if v == dia_sel][0]
        
        # Obtener ocupación
        ocupacion = self.db.obtener_ocupacion_aparatos_por_dia(dia_num)
        
        total_franjas = 0
        franjas_ocupadas = 0
        aparatos_mostrados = 0
        
        for idx, aparato in enumerate(ocupacion):
            # Filtrar por tipo de aparato si no es "Todos"
            if tipo_sel != 'Todos' and aparato['aparato_tipo'] != tipo_sel:
                continue
            
            aparatos_mostrados += 1
            
            # Añadir fila separadora con nombre del aparato
            self.tree_ocupacion.insert('', tk.END, values=(
                f"═══ {aparato['aparato_nombre']} ═══",
                aparato['aparato_tipo'],
                "═══════",
                "═══════",
                "═══════════════"
            ), tags=('separador',))
            
            for franja in aparato['franjas']:
                total_franjas += 1
                estado = "OCUPADO" if franja['ocupado'] else "LIBRE"
                cliente = franja['cliente'] or "-"
                tag = 'ocupado' if franja['ocupado'] else 'libre'
                
                if franja['ocupado']:
                    franjas_ocupadas += 1
                
                # Mostrar el nombre del aparato solo para referencia visual
                self.tree_ocupacion.insert('', tk.END, values=(
                    "",  # Dejamos vacío para que no se repita
                    "",  # Tipo vacío también
                    franja['hora'],
                    estado,
                    cliente
                ), tags=(tag,))
        
        porcentaje = (franjas_ocupadas / total_franjas * 100) if total_franjas > 0 else 0
        filtro_texto = f" ({tipo_sel})" if tipo_sel != 'Todos' else ""
        self.status_var.set(f"Ocupación del {dia_sel}{filtro_texto}: {franjas_ocupadas}/{total_franjas} franjas - {aparatos_mostrados} aparatos mostrados ({porcentaje:.1f}%)")
    
    # ==================== PESTAÑA PAGOS ====================
    
    def configurar_tab_pagos(self):
        """Configura la pestaña de gestión de pagos"""
        
        if self.usuario['rol'] == 'admin':
            # MODO ADMIN: Gestión completa de pagos
            # Frame superior: Generar recibos
            frame_generar = ttk.LabelFrame(self.tab_pagos, text="Generar Recibos del Mes", padding="10")
            frame_generar.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(frame_generar, text="Mes:").grid(row=0, column=0, padx=5)
            self.combo_pago_mes = ttk.Combobox(frame_generar, width=15, state='readonly')
            self.combo_pago_mes['values'] = list(MESES.values())
            self.combo_pago_mes.set(MESES[obtener_mes_actual()])
            self.combo_pago_mes.grid(row=0, column=1, padx=5)
            
            ttk.Label(frame_generar, text="Año:").grid(row=0, column=2, padx=5)
            self.spin_pago_anio = ttk.Spinbox(frame_generar, from_=2020, to=2030, width=10)
            self.spin_pago_anio.set(obtener_anio_actual())
            self.spin_pago_anio.grid(row=0, column=3, padx=5)
            
            ttk.Label(frame_generar, text=f"Importe: {formatear_moneda(MENSUALIDAD)}").grid(row=0, column=4, padx=20)
            
            ttk.Button(frame_generar, text="Generar Recibos", 
                       command=self.generar_recibos).grid(row=0, column=5, padx=10)
            
            # Frame medio: Registrar pago
            frame_pago = ttk.LabelFrame(self.tab_pagos, text="Todos los Recibos", padding="5")
            frame_pago.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            
            # Treeview de recibos pendientes
            columns = ('ID', 'Cliente', 'DNI', 'Mes', 'Año', 'Importe', 'Estado')
            self.tree_recibos = ttk.Treeview(frame_pago, columns=columns, show='headings', height=10)
            
            for col in columns:
                self.tree_recibos.heading(col, text=col)
            
            self.tree_recibos.column('ID', width=50)
            self.tree_recibos.column('Cliente', width=200)
            self.tree_recibos.column('DNI', width=100)
            self.tree_recibos.column('Mes', width=100)
            self.tree_recibos.column('Año', width=70)
            self.tree_recibos.column('Importe', width=100)
            self.tree_recibos.column('Estado', width=100)
            
            scrollbar = ttk.Scrollbar(frame_pago, orient=tk.VERTICAL, command=self.tree_recibos.yview)
            self.tree_recibos.configure(yscrollcommand=scrollbar.set)
            
            self.tree_recibos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Botones de pago
            frame_btn_pago = ttk.Frame(self.tab_pagos)
            frame_btn_pago.pack(fill=tk.X)
            
            ttk.Button(frame_btn_pago, text="Registrar Pago", 
                       command=self.registrar_pago).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_btn_pago, text="Actualizar Lista", 
                       command=self.cargar_recibos_pendientes).pack(side=tk.LEFT, padx=5)
            ttk.Button(frame_btn_pago, text="Ver Clientes Pagados", 
                       command=self.ver_clientes_pagados).pack(side=tk.RIGHT, padx=5)
            
            # Cargar recibos
            self.cargar_recibos_pendientes()
        else:
            # MODO EMPLEADO: Solo ver sus propios pagos
            info_label = tk.Label(
                self.tab_pagos,
                text="Mis Pagos",
                font=('Arial', 12, 'bold'),
                bg=self.COLOR_GRIS,
                fg=self.COLOR_AMARILLO
            )
            info_label.pack(pady=(0, 10))
            
            frame_pago = ttk.LabelFrame(self.tab_pagos, text="Historial de Mis Pagos", padding="10")
            frame_pago.pack(fill=tk.BOTH, expand=True, padx=20)
            
            columns = ('ID', 'Mes', 'Año', 'Importe', 'Estado', 'Fecha Pago')
            self.tree_recibos = ttk.Treeview(frame_pago, columns=columns, show='headings', height=20)
            
            self.tree_recibos.heading('ID', text='ID')
            self.tree_recibos.heading('Mes', text='Mes')
            self.tree_recibos.heading('Año', text='Año')
            self.tree_recibos.heading('Importe', text='Importe')
            self.tree_recibos.heading('Estado', text='Estado')
            self.tree_recibos.heading('Fecha Pago', text='Fecha Pago')
            
            self.tree_recibos.column('ID', width=60, anchor=tk.CENTER)
            self.tree_recibos.column('Mes', width=120)
            self.tree_recibos.column('Año', width=80, anchor=tk.CENTER)
            self.tree_recibos.column('Importe', width=100, anchor=tk.CENTER)
            self.tree_recibos.column('Estado', width=150, anchor=tk.CENTER)
            self.tree_recibos.column('Fecha Pago', width=150, anchor=tk.CENTER)
            
            scrollbar = ttk.Scrollbar(frame_pago, orient=tk.VERTICAL, command=self.tree_recibos.yview)
            self.tree_recibos.configure(yscrollcommand=scrollbar.set)
            
            self.tree_recibos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Frame de botones
            frame_botones_empleado = ttk.Frame(self.tab_pagos)
            frame_botones_empleado.pack(pady=10)
            
            # Botón pagar
            btn_pagar = tk.Button(
                frame_botones_empleado,
                text="PAGAR RECIBO",
                font=('Arial', 10, 'bold'),
                bg=self.COLOR_ROJO,
                fg=self.COLOR_BLANCO,
                activebackground='#FF1744',
                command=self.pagar_recibo_empleado,
                cursor='hand2',
                relief=tk.FLAT,
                bd=0
            )
            btn_pagar.pack(side=tk.LEFT, padx=5, ipadx=20, ipady=8)
            
            # Botón refrescar
            btn_refrescar = tk.Button(
                frame_botones_empleado,
                text="ACTUALIZAR",
                font=('Arial', 10),
                bg=self.COLOR_GRIS_CLARO,
                fg=self.COLOR_BLANCO,
                activebackground=self.COLOR_GRIS,
                command=self.cargar_mis_pagos,
                cursor='hand2',
                relief=tk.FLAT,
                bd=0
            )
            btn_refrescar.pack(side=tk.LEFT, padx=5, ipadx=15, ipady=8)
            
            # Cargar pagos del usuario
            self.cargar_mis_pagos()
    
    def generar_recibos(self):
        """Genera los recibos del mes seleccionado"""
        mes_nombre = self.combo_pago_mes.get()
        anio = int(self.spin_pago_anio.get())
        
        # Convertir nombre de mes a número
        mes_num = [k for k, v in MESES.items() if v == mes_nombre][0]
        
        if messagebox.askyesno("Confirmar", 
                              f"¿Generar recibos para {mes_nombre} {anio}?\n"
                              f"Importe: {formatear_moneda(MENSUALIDAD)}"):
            num_recibos = self.db.generar_recibos_mes(mes_num, anio, MENSUALIDAD)
            messagebox.showinfo("Éxito", f"Se generaron {num_recibos} recibos")
            self.cargar_recibos_pendientes()
    
    def cargar_recibos_pendientes(self):
        """Carga todos los recibos en el treeview con colores"""
        for item in self.tree_recibos.get_children():
            self.tree_recibos.delete(item)
        
        # Obtener TODOS los recibos (pagados y pendientes)
        recibos = self.db.obtener_todos_recibos()
        
        pendientes = 0
        pagados = 0
        
        for recibo in recibos:
            mes_nombre = MESES.get(recibo['mes'], str(recibo['mes']))
            estado = "PAGADO" if recibo['pagado'] else "PENDIENTE"
            tag = 'pagado' if recibo['pagado'] else 'pendiente'
            
            if recibo['pagado']:
                pagados += 1
            else:
                pendientes += 1
            
            self.tree_recibos.insert('', tk.END, values=(
                recibo['id_recibo'],
                f"{recibo['nombre']} {recibo['apellidos']}",
                recibo['dni'],
                mes_nombre,
                recibo['anio'],
                formatear_moneda(recibo['importe']),
                estado
            ), tags=(tag,))
        
        # Configurar colores
        self.tree_recibos.tag_configure('pagado', background='#1a4d1a', foreground='#FFFFFF')  # Verde oscuro
        self.tree_recibos.tag_configure('pendiente', background='#4a2020', foreground='#FFFFFF')  # Rojo oscuro
        
        self.status_var.set(f"Usuario: {self.usuario['nombre']} ({self.usuario['rol']}) | {pendientes} pendientes, {pagados} pagados")
    
    def cargar_mis_pagos(self):
        """Carga los pagos del usuario actual (empleado)"""
        for item in self.tree_recibos.get_children():
            self.tree_recibos.delete(item)
        
        # Buscar cliente por email del usuario
        cliente = self.db.obtener_cliente_por_email(self.usuario['email'])
        
        if not cliente:
            self.status_var.set(f"Usuario: {self.usuario['nombre']} ({self.usuario['rol']}) | No se encontró cliente asociado")
            return
        
        # Obtener todos los recibos del cliente
        recibos = self.db.obtener_recibos_por_cliente(cliente['id_cliente'])
        
        for recibo in recibos:
            mes_nombre = MESES.get(recibo['mes'], str(recibo['mes']))
            estado = "PAGADO" if recibo['pagado'] else "PENDIENTE"
            fecha_pago = recibo['fecha_pago'][:10] if recibo['fecha_pago'] else "-"
            
            self.tree_recibos.insert('', tk.END, values=(
                recibo['id_recibo'],
                mes_nombre,
                recibo['anio'],
                formatear_moneda(recibo['importe']),
                estado,
                fecha_pago
            ), tags=('pagado' if recibo['pagado'] else 'pendiente',))
        
        # Colores según estado
        self.tree_recibos.tag_configure('pagado', background='#1a3a1a')
        self.tree_recibos.tag_configure('pendiente', background='#4a2020')
        
        self.status_var.set(f"Usuario: {self.usuario['nombre']} ({self.usuario['rol']}) | {len(recibos)} recibos en total")
    
    def registrar_pago(self):
        """Registra el pago del recibo seleccionado (Admin)"""
        selection = self.tree_recibos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Seleccione un recibo para registrar el pago")
            return
        
        item = self.tree_recibos.item(selection[0])
        id_recibo = item['values'][0]
        cliente = item['values'][1]
        estado = item['values'][6]
        
        if estado == "PAGADO":
            messagebox.showinfo("Información", "Este recibo ya está pagado")
            return
        
        if messagebox.askyesno("Confirmar", f"¿Registrar pago del recibo de {cliente}?"):
            if self.db.registrar_pago(id_recibo):
                messagebox.showinfo("Éxito", "Pago registrado correctamente")
                self.cargar_recibos_pendientes()
                self.cargar_morosos()  # Actualizar lista de morosos
    
    def pagar_recibo_empleado(self):
        """Permite al empleado pagar su propio recibo"""
        selection = self.tree_recibos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Seleccione un recibo para pagar")
            return
        
        item = self.tree_recibos.item(selection[0])
        id_recibo = item['values'][0]
        mes = item['values'][1]
        anio = item['values'][2]
        importe = item['values'][3]
        estado = item['values'][4]
        
        if estado == "PAGADO":
            messagebox.showinfo("Información", "Este recibo ya está pagado")
            return
        
        if messagebox.askyesno("Confirmar Pago", 
                              f"¿Confirmar pago de {importe} correspondiente a {mes} {anio}?\n\n"
                              f"Este pago se registrará inmediatamente."):
            if self.db.registrar_pago(id_recibo):
                messagebox.showinfo("Éxito", "Pago procesado correctamente")
                self.cargar_mis_pagos()  # Recargar lista
    
    def ver_clientes_pagados(self):
        """Muestra los clientes que han pagado"""
        clientes = self.db.obtener_clientes_al_corriente()
        
        if not clientes:
            messagebox.showinfo("Info", "No hay clientes al corriente de pago")
            return
        
        # Crear ventana emergente
        ventana = tk.Toplevel(self.root)
        ventana.title("Clientes al Corriente de Pago")
        ventana.geometry("500x400")
        
        ttk.Label(ventana, text="Clientes al Corriente de Pago", 
                  style='Subtitle.TLabel').pack(pady=10)
        
        # Lista
        listbox = tk.Listbox(ventana, font=('Courier', 10))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for c in clientes:
            listbox.insert(tk.END, f"{c['nombre']} {c['apellidos']} - {c['dni']}")
        
        ttk.Button(ventana, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    # ==================== PESTAÑA MOROSOS ====================
    
    def configurar_tab_morosos(self):
        """Configura la pestaña de clientes morosos"""
        
        # Título
        ttk.Label(self.tab_morosos, text="Lista de Clientes Morosos",
                  style='Title.TLabel').pack(pady=10)
        
        # Botón actualizar
        ttk.Button(self.tab_morosos, text="Actualizar Lista",
                   command=self.cargar_morosos).pack(pady=5)
        
        # Frame lista
        frame_lista = ttk.Frame(self.tab_morosos)
        frame_lista.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Treeview
        columns = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Recibos Pendientes', 'Total Adeudado')
        self.tree_morosos = ttk.Treeview(frame_lista, columns=columns, show='headings', height=15)
        
        self.tree_morosos.heading('ID', text='ID')
        self.tree_morosos.heading('Nombre', text='Nombre')
        self.tree_morosos.heading('Apellidos', text='Apellidos')
        self.tree_morosos.heading('DNI', text='DNI')
        self.tree_morosos.heading('Teléfono', text='Teléfono')
        self.tree_morosos.heading('Recibos Pendientes', text='Recibos Pend.')
        self.tree_morosos.heading('Total Adeudado', text='Total Adeudado')
        
        self.tree_morosos.column('ID', width=50)
        self.tree_morosos.column('Nombre', width=100)
        self.tree_morosos.column('Apellidos', width=150)
        self.tree_morosos.column('DNI', width=100)
        self.tree_morosos.column('Teléfono', width=100)
        self.tree_morosos.column('Recibos Pendientes', width=120)
        self.tree_morosos.column('Total Adeudado', width=120)
        
        # Tag para resaltar - tono oscuro suave
        self.tree_morosos.tag_configure('moroso', 
                                        background='#4a2020',  # Rojo muy oscuro
                                        foreground='#ffcccc')  # Texto claro
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_morosos.yview)
        self.tree_morosos.configure(yscrollcommand=scrollbar.set)
        
        self.tree_morosos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Resumen
        self.label_resumen_morosos = ttk.Label(self.tab_morosos, text="", style='Header.TLabel')
        self.label_resumen_morosos.pack(pady=10)
        
        # Cargar datos
        self.cargar_morosos()
    
    def cargar_morosos(self):
        """Carga la lista de clientes morosos"""
        for item in self.tree_morosos.get_children():
            self.tree_morosos.delete(item)
        
        morosos = self.db.obtener_clientes_morosos()
        
        total_adeudado = 0
        for m in morosos:
            self.tree_morosos.insert('', tk.END, values=(
                m['id_cliente'],
                m['nombre'],
                m['apellidos'],
                m['dni'],
                m['telefono'] or '-',
                m['num_recibos_pendientes'],
                formatear_moneda(m['total_adeudado'])
            ), tags=('moroso',))
            total_adeudado += m['total_adeudado']
        
        self.label_resumen_morosos.config(
            text=f"Total morosos: {len(morosos)} | Total adeudado: {formatear_moneda(total_adeudado)}"
        )
        self.status_var.set(f"Se encontraron {len(morosos)} clientes morosos")
    
    # ==================== UTILIDADES ====================
    
    def mostrar_acerca_de(self):
        """Muestra información sobre la aplicación"""
        ventana = tk.Toplevel(self.root)
        ventana.title("Acerca de")
        ventana.geometry("400x350")
        ventana.resizable(False, False)
        ventana.configure(bg=self.COLOR_NEGRO)
        
        # Contenido
        frame = ttk.Frame(ventana, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="GymForTheMoment", 
                  style='Title.TLabel').pack(pady=10)
        
        ttk.Label(frame, text="Sistema de Gestion de Gimnasio",
                  style='Subtitle.TLabel').pack(pady=5)
        
        ttk.Label(frame, text=f"\nVersion: 1.0\n",
                  font=('Arial', 10)).pack()
        
        # Mostrar usuario actual
        ttk.Label(frame, text=f"Usuario: {self.usuario['nombre']}",
                  font=('Arial', 9, 'bold')).pack()
        ttk.Label(frame, text=f"Rol: {self.usuario['rol'].capitalize()}",
                  font=('Arial', 9)).pack(pady=(0, 10))
        
        info_text = """
        Funcionalidades:
        • Gestion de clientes
        • Gestion de aparatos
        • Reservas de sesiones (30 min)
        • Control de ocupacion por dia
        • Gestion de pagos mensuales
        • Control de clientes morosos
        
        Horario: 24 horas
        Dias: Lunes a Viernes
        """
        
        ttk.Label(frame, text=info_text,
                  font=('Arial', 9), justify=tk.LEFT).pack(pady=10)
        
        ttk.Button(frame, text="Cerrar", command=ventana.destroy).pack(pady=10)
    
    def cerrar_sesion(self):
        """Cierra la sesión actual y vuelve al login"""
        if messagebox.askokcancel("Cerrar Sesión", "¿Desea cerrar sesión?"):
            self.cerro_sesion = True  # Marcar que se cerró sesión
            self.db.disconnect()
            self.root.quit()  # Sale del mainloop
            self.root.destroy()  # Destruye la ventana
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.db.disconnect()
            self.root.destroy()


def main(usuario):
    """Función principal"""
    root = tk.Tk()
    app = GymApp(root, usuario)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    # Si se ejecuta directamente, mostrar error
    print("Error: Debe ejecutar la aplicacion desde main.py")
    print("Use: python src/main.py")
