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
    
    def __init__(self, root):
        self.root = root
        self.root.title("🏋️ GymForTheMoment - Sistema de Gestión")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Colores personalizados
        self.style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        self.style.configure('Subtitle.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Header.TLabel', font=('Helvetica', 10, 'bold'))
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        self.db.connect()
        self.db.create_tables()
        
        # Crear interfaz
        self.crear_interfaz()
        
        # Cargar datos iniciales
        self.cargar_clientes()
        self.cargar_aparatos()
        
    def crear_interfaz(self):
        """Crea la interfaz principal con pestañas"""
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = ttk.Label(
            self.main_frame, 
            text="🏋️ GymForTheMoment - Sistema de Gestión",
            style='Title.TLabel'
        )
        titulo.pack(pady=(0, 10))
        
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
        
        self.notebook.add(self.tab_clientes, text="👥 Clientes")
        self.notebook.add(self.tab_aparatos, text="🏃 Aparatos")
        self.notebook.add(self.tab_reservas, text="📅 Reservas")
        self.notebook.add(self.tab_ocupacion, text="📊 Ocupación")
        self.notebook.add(self.tab_pagos, text="💰 Pagos")
        self.notebook.add(self.tab_morosos, text="⚠️ Morosos")
        
        # Configurar cada pestaña
        self.configurar_tab_clientes()
        self.configurar_tab_aparatos()
        self.configurar_tab_reservas()
        self.configurar_tab_ocupacion()
        self.configurar_tab_pagos()
        self.configurar_tab_morosos()
        
        # Barra de estado
        self.status_var = tk.StringVar(value="Listo")
        self.status_bar = ttk.Label(
            self.main_frame, 
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(fill=tk.X, pady=(10, 0))
    
    # ==================== PESTAÑA CLIENTES ====================
    
    def configurar_tab_clientes(self):
        """Configura la pestaña de gestión de clientes"""
        
        # Frame izquierdo: Lista de clientes
        frame_lista = ttk.LabelFrame(self.tab_clientes, text="Lista de Clientes", padding="5")
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Treeview para clientes
        columns = ('ID', 'Nombre', 'Apellidos', 'DNI', 'Teléfono', 'Email')
        self.tree_clientes = ttk.Treeview(frame_lista, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.tree_clientes.heading(col, text=col)
            self.tree_clientes.column(col, width=100)
        
        self.tree_clientes.column('ID', width=50)
        self.tree_clientes.column('Nombre', width=100)
        self.tree_clientes.column('Apellidos', width=150)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_clientes.yview)
        self.tree_clientes.configure(yscrollcommand=scrollbar.set)
        
        self.tree_clientes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Frame derecho: Formulario
        frame_form = ttk.LabelFrame(self.tab_clientes, text="Datos del Cliente", padding="10")
        frame_form.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        
        # Campos del formulario
        ttk.Label(frame_form, text="Nombre:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.entry_nombre = ttk.Entry(frame_form, width=25)
        self.entry_nombre.grid(row=0, column=1, pady=2)
        
        ttk.Label(frame_form, text="Apellidos:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.entry_apellidos = ttk.Entry(frame_form, width=25)
        self.entry_apellidos.grid(row=1, column=1, pady=2)
        
        ttk.Label(frame_form, text="DNI:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_dni = ttk.Entry(frame_form, width=25)
        self.entry_dni.grid(row=2, column=1, pady=2)
        
        ttk.Label(frame_form, text="Teléfono:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.entry_telefono = ttk.Entry(frame_form, width=25)
        self.entry_telefono.grid(row=3, column=1, pady=2)
        
        ttk.Label(frame_form, text="Email:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.entry_email = ttk.Entry(frame_form, width=25)
        self.entry_email.grid(row=4, column=1, pady=2)
        
        # Botones
        frame_botones = ttk.Frame(frame_form)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="➕ Nuevo", command=self.nuevo_cliente).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="💾 Guardar", command=self.guardar_cliente).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️ Eliminar", command=self.eliminar_cliente).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Refrescar", command=self.cargar_clientes).pack(side=tk.LEFT, padx=2)
        
        # Evento de selección
        self.tree_clientes.bind('<<TreeviewSelect>>', self.seleccionar_cliente)
        
        # Variable para ID seleccionado
        self.cliente_seleccionado_id = None
    
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
                cliente['email'] or ''
            ))
        
        self.status_var.set(f"Se cargaron {len(clientes)} clientes")
    
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
    
    def nuevo_cliente(self):
        """Limpia el formulario para un nuevo cliente"""
        self.cliente_seleccionado_id = None
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellidos.delete(0, tk.END)
        self.entry_dni.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_nombre.focus()
    
    def guardar_cliente(self):
        """Guarda o actualiza un cliente"""
        nombre = self.entry_nombre.get().strip()
        apellidos = self.entry_apellidos.get().strip()
        dni = self.entry_dni.get().strip().upper()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        
        # Validaciones
        if not nombre or not apellidos or not dni:
            messagebox.showerror("Error", "Nombre, apellidos y DNI son obligatorios")
            return
        
        if not validar_email(email):
            messagebox.showerror("Error", "El formato del email no es válido")
            return
        
        try:
            if self.cliente_seleccionado_id:
                # Actualizar
                if self.db.actualizar_cliente(
                    self.cliente_seleccionado_id, nombre, apellidos, dni, telefono, email
                ):
                    messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
                    self.cargar_clientes()
                else:
                    messagebox.showerror("Error", "No se pudo actualizar el cliente")
            else:
                # Insertar nuevo
                id_nuevo = self.db.insertar_cliente(nombre, apellidos, dni, telefono, email)
                if id_nuevo:
                    messagebox.showinfo("Éxito", f"Cliente creado con ID: {id_nuevo}")
                    self.cargar_clientes()
                    self.nuevo_cliente()
                else:
                    messagebox.showerror("Error", "No se pudo crear el cliente. ¿El DNI ya existe?")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def eliminar_cliente(self):
        """Elimina el cliente seleccionado"""
        if not self.cliente_seleccionado_id:
            messagebox.showwarning("Aviso", "Seleccione un cliente para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este cliente?"):
            if self.db.eliminar_cliente(self.cliente_seleccionado_id):
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.cargar_clientes()
                self.nuevo_cliente()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el cliente")
    
    # ==================== PESTAÑA APARATOS ====================
    
    def configurar_tab_aparatos(self):
        """Configura la pestaña de gestión de aparatos"""
        
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
        self.combo_tipo = ttk.Combobox(frame_form, width=22, values=['Cardio', 'Musculación', 'Funcional', 'Otro'])
        self.combo_tipo.grid(row=1, column=1, pady=2)
        
        ttk.Label(frame_form, text="Descripción:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.entry_aparato_desc = ttk.Entry(frame_form, width=25)
        self.entry_aparato_desc.grid(row=2, column=1, pady=2)
        
        # Botones
        frame_botones = ttk.Frame(frame_form)
        frame_botones.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(frame_botones, text="➕ Nuevo", command=self.nuevo_aparato).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="💾 Guardar", command=self.guardar_aparato).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🗑️ Eliminar", command=self.eliminar_aparato).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame_botones, text="🔄 Refrescar", command=self.cargar_aparatos).pack(side=tk.LEFT, padx=2)
        
        self.tree_aparatos.bind('<<TreeviewSelect>>', self.seleccionar_aparato)
        self.aparato_seleccionado_id = None
    
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
        frame_nueva = ttk.LabelFrame(self.tab_reservas, text="Nueva Reserva", padding="10")
        frame_nueva.pack(fill=tk.X, pady=(0, 10))
        
        # Cliente
        ttk.Label(frame_nueva, text="Cliente:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.combo_reserva_cliente = ttk.Combobox(frame_nueva, width=30, state='readonly')
        self.combo_reserva_cliente.grid(row=0, column=1, padx=5)
        
        # Aparato
        ttk.Label(frame_nueva, text="Aparato:").grid(row=0, column=2, sticky=tk.W, padx=5)
        self.combo_reserva_aparato = ttk.Combobox(frame_nueva, width=25, state='readonly')
        self.combo_reserva_aparato.grid(row=0, column=3, padx=5)
        
        # Día
        ttk.Label(frame_nueva, text="Día:").grid(row=0, column=4, sticky=tk.W, padx=5)
        self.combo_reserva_dia = ttk.Combobox(frame_nueva, width=12, state='readonly')
        self.combo_reserva_dia['values'] = list(DIAS_SEMANA.values())
        self.combo_reserva_dia.grid(row=0, column=5, padx=5)
        
        # Hora
        ttk.Label(frame_nueva, text="Hora:").grid(row=0, column=6, sticky=tk.W, padx=5)
        self.combo_reserva_hora = ttk.Combobox(frame_nueva, width=12, state='readonly')
        franjas = generar_franjas_horarias()
        self.combo_reserva_hora['values'] = [f[0] for f in franjas]
        self.combo_reserva_hora.grid(row=0, column=7, padx=5)
        
        # Botón reservar
        ttk.Button(frame_nueva, text="📅 Reservar", command=self.realizar_reserva).grid(row=0, column=8, padx=10)
        
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
        
        ttk.Button(frame_filtro, text="🗑️ Cancelar Reserva", command=self.cancelar_reserva).pack(side=tk.RIGHT, padx=5)
        
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
    
    def realizar_reserva(self):
        """Realiza una nueva reserva"""
        cliente_sel = self.combo_reserva_cliente.get()
        aparato_sel = self.combo_reserva_aparato.get()
        dia_sel = self.combo_reserva_dia.get()
        hora_sel = self.combo_reserva_hora.get()
        
        if not all([cliente_sel, aparato_sel, dia_sel, hora_sel]):
            messagebox.showerror("Error", "Complete todos los campos")
            return
        
        # Extraer IDs
        id_cliente = int(cliente_sel.split(' - ')[0])
        id_aparato = int(aparato_sel.split(' - ')[0])
        dia_num = [k for k, v in DIAS_SEMANA.items() if v == dia_sel][0]
        
        # Verificar disponibilidad
        if not self.db.verificar_disponibilidad(id_aparato, dia_num, hora_sel):
            messagebox.showerror("Error", "El aparato ya está reservado en ese horario")
            return
        
        # Realizar reserva
        id_reserva = self.db.insertar_reserva(id_cliente, id_aparato, dia_num, hora_sel)
        if id_reserva:
            messagebox.showinfo("Éxito", f"Reserva creada correctamente (ID: {id_reserva})")
            self.cargar_reservas()
            # Limpiar selección
            self.combo_reserva_cliente.set('')
            self.combo_reserva_aparato.set('')
            self.combo_reserva_dia.set('')
            self.combo_reserva_hora.set('')
        else:
            messagebox.showerror("Error", "No se pudo crear la reserva")
    
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
        
        # Frame superior: Selector de día
        frame_selector = ttk.Frame(self.tab_ocupacion)
        frame_selector.pack(fill=tk.X, pady=10)
        
        ttk.Label(frame_selector, text="Seleccione día de la semana:", 
                  style='Subtitle.TLabel').pack(side=tk.LEFT, padx=10)
        
        self.combo_ocupacion_dia = ttk.Combobox(frame_selector, width=15, state='readonly')
        self.combo_ocupacion_dia['values'] = list(DIAS_SEMANA.values())
        self.combo_ocupacion_dia.pack(side=tk.LEFT, padx=10)
        
        ttk.Button(frame_selector, text="📊 Ver Ocupación", 
                   command=self.mostrar_ocupacion).pack(side=tk.LEFT, padx=10)
        
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
        
        # Tags para colores
        self.tree_ocupacion.tag_configure('ocupado', background='#ffcccc')
        self.tree_ocupacion.tag_configure('libre', background='#ccffcc')
        
        scrollbar = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_ocupacion.yview)
        self.tree_ocupacion.configure(yscrollcommand=scrollbar.set)
        
        self.tree_ocupacion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def mostrar_ocupacion(self):
        """Muestra la ocupación de aparatos para el día seleccionado"""
        dia_sel = self.combo_ocupacion_dia.get()
        
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
        
        for aparato in ocupacion:
            for franja in aparato['franjas']:
                total_franjas += 1
                estado = "🔴 OCUPADO" if franja['ocupado'] else "🟢 LIBRE"
                cliente = franja['cliente'] or "-"
                tag = 'ocupado' if franja['ocupado'] else 'libre'
                
                if franja['ocupado']:
                    franjas_ocupadas += 1
                
                self.tree_ocupacion.insert('', tk.END, values=(
                    aparato['aparato_nombre'],
                    aparato['aparato_tipo'],
                    franja['hora'],
                    estado,
                    cliente
                ), tags=(tag,))
        
        porcentaje = (franjas_ocupadas / total_franjas * 100) if total_franjas > 0 else 0
        self.status_var.set(f"Ocupación del {dia_sel}: {franjas_ocupadas}/{total_franjas} franjas ocupadas ({porcentaje:.1f}%)")
    
    # ==================== PESTAÑA PAGOS ====================
    
    def configurar_tab_pagos(self):
        """Configura la pestaña de gestión de pagos"""
        
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
        
        ttk.Button(frame_generar, text="📝 Generar Recibos", 
                   command=self.generar_recibos).grid(row=0, column=5, padx=10)
        
        # Frame medio: Registrar pago
        frame_pago = ttk.LabelFrame(self.tab_pagos, text="Recibos Pendientes", padding="5")
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
        
        ttk.Button(frame_btn_pago, text="✅ Registrar Pago", 
                   command=self.registrar_pago).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn_pago, text="🔄 Actualizar Lista", 
                   command=self.cargar_recibos_pendientes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_btn_pago, text="📋 Ver Clientes Pagados", 
                   command=self.ver_clientes_pagados).pack(side=tk.RIGHT, padx=5)
        
        # Cargar recibos
        self.cargar_recibos_pendientes()
    
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
        """Carga los recibos pendientes en el treeview"""
        for item in self.tree_recibos.get_children():
            self.tree_recibos.delete(item)
        
        recibos = self.db.obtener_recibos_pendientes()
        
        for recibo in recibos:
            mes_nombre = MESES.get(recibo['mes'], str(recibo['mes']))
            self.tree_recibos.insert('', tk.END, values=(
                recibo['id_recibo'],
                f"{recibo['nombre']} {recibo['apellidos']}",
                recibo['dni'],
                mes_nombre,
                recibo['anio'],
                formatear_moneda(recibo['importe']),
                "⏳ Pendiente"
            ))
        
        self.status_var.set(f"{len(recibos)} recibos pendientes de pago")
    
    def registrar_pago(self):
        """Registra el pago del recibo seleccionado"""
        selection = self.tree_recibos.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Seleccione un recibo para registrar el pago")
            return
        
        item = self.tree_recibos.item(selection[0])
        id_recibo = item['values'][0]
        cliente = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"¿Registrar pago del recibo de {cliente}?"):
            if self.db.registrar_pago(id_recibo):
                messagebox.showinfo("Éxito", "Pago registrado correctamente")
                self.cargar_recibos_pendientes()
    
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
        
        ttk.Label(ventana, text="✅ Clientes al Corriente de Pago", 
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
        ttk.Label(self.tab_morosos, text="⚠️ Lista de Clientes Morosos",
                  style='Title.TLabel').pack(pady=10)
        
        # Botón actualizar
        ttk.Button(self.tab_morosos, text="🔄 Actualizar Lista",
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
        
        # Tag para resaltar
        self.tree_morosos.tag_configure('moroso', background='#ffcccc')
        
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
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            self.db.disconnect()
            self.root.destroy()


def main():
    """Función principal"""
    root = tk.Tk()
    app = GymApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
