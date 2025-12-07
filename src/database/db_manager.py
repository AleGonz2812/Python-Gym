# -*- coding: utf-8 -*-
"""
GymForTheMoment - Gestor de Base de Datos
Módulo para la gestión de la base de datos SQLite
"""

import sqlite3
from datetime import datetime, date, time, timedelta
from typing import List, Optional, Tuple, Any
import os


class DatabaseManager:
    """Clase para gestionar la conexión y operaciones con la base de datos SQLite"""
    
    def __init__(self, db_path: str = "gym_database.db"):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establece la conexión con la base de datos"""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.cursor = self.connection.cursor()
            # Habilitar claves foráneas
            self.cursor.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return False
    
    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[sqlite3.Cursor]:
        """
        Ejecuta una consulta SQL.
        
        Args:
            query: Consulta SQL a ejecutar
            params: Parámetros de la consulta
            
        Returns:
            Cursor con los resultados o None si hay error
        """
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            return self.cursor
        except sqlite3.Error as e:
            print(f"Error al ejecutar consulta: {e}")
            return None
    
    def create_tables(self):
        """Crea todas las tablas necesarias en la base de datos"""
        
        # Tabla USUARIO (para login)
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS usuario (
                id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                rol VARCHAR(20) DEFAULT 'empleado',
                activo BOOLEAN DEFAULT 1,
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Tabla CLIENTE
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50) NOT NULL,
                apellidos VARCHAR(100) NOT NULL,
                dni VARCHAR(15) NOT NULL UNIQUE,
                telefono VARCHAR(20),
                email VARCHAR(100),
                fecha_alta DATE NOT NULL,
                activo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabla APARATO
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS aparato (
                id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre VARCHAR(50) NOT NULL,
                tipo VARCHAR(50) NOT NULL,
                descripcion TEXT,
                activo BOOLEAN DEFAULT 1
            )
        """)
        
        # Tabla RESERVA
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS reserva (
                id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                id_aparato INTEGER NOT NULL,
                dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 5),
                hora_inicio TIME NOT NULL,
                hora_fin TIME NOT NULL,
                fecha_creacion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
                FOREIGN KEY (id_aparato) REFERENCES aparato(id_aparato) ON DELETE CASCADE,
                UNIQUE (id_aparato, dia_semana, hora_inicio)
            )
        """)
        
        # Tabla RECIBO
        self.execute_query("""
            CREATE TABLE IF NOT EXISTS recibo (
                id_recibo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER NOT NULL,
                mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
                anio INTEGER NOT NULL,
                importe DECIMAL(10,2) NOT NULL,
                pagado BOOLEAN DEFAULT 0,
                fecha_pago DATE,
                fecha_emision DATE NOT NULL DEFAULT CURRENT_DATE,
                FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
                UNIQUE (id_cliente, mes, anio)
            )
        """)
        
        # Crear índices para optimización
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_reserva_dia ON reserva(dia_semana)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_reserva_aparato ON reserva(id_aparato)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_recibo_pagado ON recibo(pagado)")
        self.execute_query("CREATE INDEX IF NOT EXISTS idx_recibo_cliente ON recibo(id_cliente)")
        
        print("Tablas creadas correctamente")
    
    # ==================== OPERACIONES CON USUARIOS ====================
    
    def crear_usuario(self, nombre: str, email: str, password: str, rol: str = 'empleado') -> Optional[int]:
        """
        Crea un nuevo usuario.
        NOTA: En producción, la contraseña debería ser hasheada con bcrypt o similar.
        """
        query = """
            INSERT INTO usuario (nombre, email, password, rol, activo)
            VALUES (?, ?, ?, ?, 1)
        """
        result = self.execute_query(query, (nombre, email, password, rol))
        if result:
            return self.cursor.lastrowid
        return None
    
    def validar_usuario(self, email: str, password: str) -> Optional[sqlite3.Row]:
        """Valida las credenciales de un usuario"""
        query = """
            SELECT * FROM usuario 
            WHERE email = ? AND password = ? AND activo = 1
        """
        self.execute_query(query, (email, password))
        return self.cursor.fetchone()
    
    def existe_usuario(self, email: str) -> bool:
        """Verifica si existe un usuario con ese email"""
        query = "SELECT COUNT(*) FROM usuario WHERE email = ?"
        self.execute_query(query, (email,))
        return self.cursor.fetchone()[0] > 0
    
    def existe_admin(self) -> bool:
        """Verifica si ya existe un administrador"""
        query = "SELECT COUNT(*) FROM usuario WHERE rol = 'admin'"
        self.execute_query(query)
        return self.cursor.fetchone()[0] > 0
    
    def crear_admin_inicial(self):
        """Crea el usuario administrador por defecto si no existe"""
        if not self.existe_admin():
            self.crear_usuario(
                nombre="Administrador",
                email="admin@gymforthemoment.com",
                password="admin123",
                rol="admin"
            )
            print("Usuario administrador creado: admin@gymforthemoment.com / admin123")
    
    # ==================== OPERACIONES CON CLIENTES ====================
    
    def insertar_cliente(self, nombre: str, apellidos: str, dni: str, 
                         telefono: str = None, email: str = None) -> Optional[int]:
        """
        Inserta un nuevo cliente en la base de datos.
        
        Returns:
            ID del cliente insertado o None si hay error
        """
        query = """
            INSERT INTO cliente (nombre, apellidos, dni, telefono, email, fecha_alta, activo)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        fecha_alta = date.today().isoformat()
        result = self.execute_query(query, (nombre, apellidos, dni, telefono, email, fecha_alta))
        if result:
            return self.cursor.lastrowid
        return None
    
    def obtener_clientes(self, solo_activos: bool = True) -> List[sqlite3.Row]:
        """Obtiene todos los clientes"""
        if solo_activos:
            query = "SELECT * FROM cliente WHERE activo = 1 ORDER BY apellidos, nombre"
        else:
            query = "SELECT * FROM cliente ORDER BY apellidos, nombre"
        self.execute_query(query)
        return self.cursor.fetchall()
    
    def obtener_cliente_por_id(self, id_cliente: int) -> Optional[sqlite3.Row]:
        """Obtiene un cliente por su ID"""
        query = "SELECT * FROM cliente WHERE id_cliente = ?"
        self.execute_query(query, (id_cliente,))
        return self.cursor.fetchone()
    
    def actualizar_cliente(self, id_cliente: int, nombre: str, apellidos: str, 
                           dni: str, telefono: str = None, email: str = None) -> bool:
        """Actualiza los datos de un cliente"""
        query = """
            UPDATE cliente 
            SET nombre = ?, apellidos = ?, dni = ?, telefono = ?, email = ?
            WHERE id_cliente = ?
        """
        result = self.execute_query(query, (nombre, apellidos, dni, telefono, email, id_cliente))
        return result is not None
    
    def eliminar_cliente(self, id_cliente: int) -> bool:
        """Elimina un cliente (desactivación lógica)"""
        query = "UPDATE cliente SET activo = 0 WHERE id_cliente = ?"
        result = self.execute_query(query, (id_cliente,))
        return result is not None
    
    def eliminar_cliente_fisico(self, id_cliente: int) -> bool:
        """Elimina un cliente de forma permanente"""
        query = "DELETE FROM cliente WHERE id_cliente = ?"
        result = self.execute_query(query, (id_cliente,))
        return result is not None
    
    # ==================== OPERACIONES CON APARATOS ====================
    
    def insertar_aparato(self, nombre: str, tipo: str, descripcion: str = None) -> Optional[int]:
        """
        Inserta un nuevo aparato en la base de datos.
        
        Returns:
            ID del aparato insertado o None si hay error
        """
        query = """
            INSERT INTO aparato (nombre, tipo, descripcion, activo)
            VALUES (?, ?, ?, 1)
        """
        result = self.execute_query(query, (nombre, tipo, descripcion))
        if result:
            return self.cursor.lastrowid
        return None
    
    def obtener_aparatos(self, solo_activos: bool = True) -> List[sqlite3.Row]:
        """Obtiene todos los aparatos"""
        if solo_activos:
            query = "SELECT * FROM aparato WHERE activo = 1 ORDER BY tipo, nombre"
        else:
            query = "SELECT * FROM aparato ORDER BY tipo, nombre"
        self.execute_query(query)
        return self.cursor.fetchall()
    
    def obtener_aparato_por_id(self, id_aparato: int) -> Optional[sqlite3.Row]:
        """Obtiene un aparato por su ID"""
        query = "SELECT * FROM aparato WHERE id_aparato = ?"
        self.execute_query(query, (id_aparato,))
        return self.cursor.fetchone()
    
    def actualizar_aparato(self, id_aparato: int, nombre: str, tipo: str, 
                           descripcion: str = None) -> bool:
        """Actualiza los datos de un aparato"""
        query = """
            UPDATE aparato 
            SET nombre = ?, tipo = ?, descripcion = ?
            WHERE id_aparato = ?
        """
        result = self.execute_query(query, (nombre, tipo, descripcion, id_aparato))
        return result is not None
    
    def eliminar_aparato(self, id_aparato: int) -> bool:
        """Elimina un aparato (desactivación lógica)"""
        query = "UPDATE aparato SET activo = 0 WHERE id_aparato = ?"
        result = self.execute_query(query, (id_aparato,))
        return result is not None
    
    # ==================== OPERACIONES CON RESERVAS ====================
    
    def insertar_reserva(self, id_cliente: int, id_aparato: int, 
                         dia_semana: int, hora_inicio: str) -> Optional[int]:
        """
        Inserta una nueva reserva.
        
        Args:
            id_cliente: ID del cliente
            id_aparato: ID del aparato
            dia_semana: Día de la semana (1=Lunes, 5=Viernes)
            hora_inicio: Hora de inicio en formato "HH:MM"
            
        Returns:
            ID de la reserva o None si hay error
        """
        # Calcular hora de fin (30 minutos después)
        h, m = map(int, hora_inicio.split(':'))
        hora_inicio_dt = datetime.now().replace(hour=h, minute=m, second=0)
        hora_fin_dt = hora_inicio_dt + timedelta(minutes=30)
        hora_fin = hora_fin_dt.strftime("%H:%M")
        
        query = """
            INSERT INTO reserva (id_cliente, id_aparato, dia_semana, hora_inicio, hora_fin, fecha_creacion)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        fecha_creacion = datetime.now().isoformat()
        result = self.execute_query(query, (id_cliente, id_aparato, dia_semana, 
                                            hora_inicio, hora_fin, fecha_creacion))
        if result:
            return self.cursor.lastrowid
        return None
    
    def verificar_disponibilidad(self, id_aparato: int, dia_semana: int, 
                                  hora_inicio: str) -> bool:
        """Verifica si un aparato está disponible en un horario específico"""
        query = """
            SELECT COUNT(*) FROM reserva 
            WHERE id_aparato = ? AND dia_semana = ? AND hora_inicio = ?
        """
        self.execute_query(query, (id_aparato, dia_semana, hora_inicio))
        count = self.cursor.fetchone()[0]
        return count == 0
    
    def obtener_reservas_por_dia(self, dia_semana: int) -> List[sqlite3.Row]:
        """
        Obtiene todas las reservas de un día específico.
        
        Args:
            dia_semana: Día de la semana (1=Lunes, 5=Viernes)
            
        Returns:
            Lista de reservas con información del cliente y aparato
        """
        query = """
            SELECT r.*, c.nombre as cliente_nombre, c.apellidos as cliente_apellidos,
                   a.nombre as aparato_nombre, a.tipo as aparato_tipo
            FROM reserva r
            JOIN cliente c ON r.id_cliente = c.id_cliente
            JOIN aparato a ON r.id_aparato = a.id_aparato
            WHERE r.dia_semana = ?
            ORDER BY a.nombre, r.hora_inicio
        """
        self.execute_query(query, (dia_semana,))
        return self.cursor.fetchall()
    
    def obtener_ocupacion_aparatos_por_dia(self, dia_semana: int) -> List[dict]:
        """
        Genera un listado de ocupación de todos los aparatos para un día.
        
        Returns:
            Lista con la información de ocupación de cada aparato
        """
        aparatos = self.obtener_aparatos()
        ocupacion = []
        
        for aparato in aparatos:
            # Generar todas las franjas horarias (48 franjas de 30 min en 24h)
            franjas = []
            for hora in range(24):
                for minuto in [0, 30]:
                    hora_str = f"{hora:02d}:{minuto:02d}"
                    
                    # Buscar si hay reserva para esta franja
                    query = """
                        SELECT r.*, c.nombre, c.apellidos
                        FROM reserva r
                        JOIN cliente c ON r.id_cliente = c.id_cliente
                        WHERE r.id_aparato = ? AND r.dia_semana = ? AND r.hora_inicio = ?
                    """
                    self.execute_query(query, (aparato['id_aparato'], dia_semana, hora_str))
                    reserva = self.cursor.fetchone()
                    
                    if reserva:
                        franjas.append({
                            'hora': hora_str,
                            'ocupado': True,
                            'cliente': f"{reserva['nombre']} {reserva['apellidos']}"
                        })
                    else:
                        franjas.append({
                            'hora': hora_str,
                            'ocupado': False,
                            'cliente': None
                        })
            
            ocupacion.append({
                'aparato_id': aparato['id_aparato'],
                'aparato_nombre': aparato['nombre'],
                'aparato_tipo': aparato['tipo'],
                'franjas': franjas
            })
        
        return ocupacion
    
    def cancelar_reserva(self, id_reserva: int) -> bool:
        """Cancela una reserva"""
        query = "DELETE FROM reserva WHERE id_reserva = ?"
        result = self.execute_query(query, (id_reserva,))
        return result is not None
    
    def obtener_reservas_cliente(self, id_cliente: int) -> List[sqlite3.Row]:
        """Obtiene todas las reservas de un cliente"""
        query = """
            SELECT r.*, a.nombre as aparato_nombre, a.tipo as aparato_tipo
            FROM reserva r
            JOIN aparato a ON r.id_aparato = a.id_aparato
            WHERE r.id_cliente = ?
            ORDER BY r.dia_semana, r.hora_inicio
        """
        self.execute_query(query, (id_cliente,))
        return self.cursor.fetchall()
    
    # ==================== OPERACIONES CON RECIBOS ====================
    
    def generar_recibos_mes(self, mes: int, anio: int, importe: float) -> int:
        """
        Genera recibos para todos los clientes activos de un mes.
        
        Returns:
            Número de recibos generados
        """
        clientes = self.obtener_clientes(solo_activos=True)
        recibos_generados = 0
        
        for cliente in clientes:
            # Verificar si ya existe recibo para ese cliente/mes/año
            query = """
                SELECT COUNT(*) FROM recibo 
                WHERE id_cliente = ? AND mes = ? AND anio = ?
            """
            self.execute_query(query, (cliente['id_cliente'], mes, anio))
            if self.cursor.fetchone()[0] == 0:
                # Crear recibo
                query = """
                    INSERT INTO recibo (id_cliente, mes, anio, importe, pagado, fecha_emision)
                    VALUES (?, ?, ?, ?, 0, ?)
                """
                fecha_emision = date.today().isoformat()
                if self.execute_query(query, (cliente['id_cliente'], mes, anio, 
                                              importe, fecha_emision)):
                    recibos_generados += 1
        
        return recibos_generados
    
    def registrar_pago(self, id_recibo: int) -> bool:
        """Marca un recibo como pagado"""
        query = """
            UPDATE recibo 
            SET pagado = 1, fecha_pago = ?
            WHERE id_recibo = ?
        """
        fecha_pago = date.today().isoformat()
        result = self.execute_query(query, (fecha_pago, id_recibo))
        return result is not None
    
    def obtener_recibos_pendientes(self, id_cliente: int = None) -> List[sqlite3.Row]:
        """Obtiene los recibos pendientes de pago"""
        if id_cliente:
            query = """
                SELECT r.*, c.nombre, c.apellidos, c.dni
                FROM recibo r
                JOIN cliente c ON r.id_cliente = c.id_cliente
                WHERE r.pagado = 0 AND r.id_cliente = ?
                ORDER BY r.anio, r.mes
            """
            self.execute_query(query, (id_cliente,))
        else:
            query = """
                SELECT r.*, c.nombre, c.apellidos, c.dni
                FROM recibo r
                JOIN cliente c ON r.id_cliente = c.id_cliente
                WHERE r.pagado = 0
                ORDER BY c.apellidos, c.nombre, r.anio, r.mes
            """
            self.execute_query(query)
        return self.cursor.fetchall()
    
    def obtener_clientes_morosos(self) -> List[dict]:
        """
        Obtiene la lista de clientes morosos con información de deuda.
        
        Returns:
            Lista de diccionarios con información de morosos
        """
        query = """
            SELECT c.id_cliente, c.nombre, c.apellidos, c.dni, c.telefono, c.email,
                   COUNT(r.id_recibo) as num_recibos_pendientes,
                   SUM(r.importe) as total_adeudado
            FROM cliente c
            JOIN recibo r ON c.id_cliente = r.id_cliente
            WHERE r.pagado = 0 AND c.activo = 1
            GROUP BY c.id_cliente
            ORDER BY total_adeudado DESC
        """
        self.execute_query(query)
        rows = self.cursor.fetchall()
        
        morosos = []
        for row in rows:
            morosos.append({
                'id_cliente': row['id_cliente'],
                'nombre': row['nombre'],
                'apellidos': row['apellidos'],
                'dni': row['dni'],
                'telefono': row['telefono'],
                'email': row['email'],
                'num_recibos_pendientes': row['num_recibos_pendientes'],
                'total_adeudado': row['total_adeudado']
            })
        
        return morosos
    
    def obtener_clientes_al_corriente(self, mes: int = None, anio: int = None) -> List[sqlite3.Row]:
        """
        Obtiene los clientes que han pagado sus recibos.
        
        Args:
            mes: Mes específico (opcional)
            anio: Año específico (opcional)
        """
        if mes and anio:
            query = """
                SELECT DISTINCT c.*
                FROM cliente c
                JOIN recibo r ON c.id_cliente = r.id_cliente
                WHERE r.pagado = 1 AND r.mes = ? AND r.anio = ? AND c.activo = 1
                ORDER BY c.apellidos, c.nombre
            """
            self.execute_query(query, (mes, anio))
        else:
            # Clientes sin recibos pendientes
            query = """
                SELECT c.*
                FROM cliente c
                WHERE c.activo = 1 AND c.id_cliente NOT IN (
                    SELECT DISTINCT id_cliente FROM recibo WHERE pagado = 0
                )
                ORDER BY c.apellidos, c.nombre
            """
            self.execute_query(query)
        
        return self.cursor.fetchall()
    
    def obtener_recibos_cliente(self, id_cliente: int) -> List[sqlite3.Row]:
        """Obtiene todos los recibos de un cliente"""
        query = """
            SELECT * FROM recibo 
            WHERE id_cliente = ?
            ORDER BY anio DESC, mes DESC
        """
        self.execute_query(query, (id_cliente,))
        return self.cursor.fetchall()
    
    def obtener_todos_recibos(self, mes: int = None, anio: int = None) -> List[sqlite3.Row]:
        """Obtiene todos los recibos, opcionalmente filtrados por mes y año"""
        if mes and anio:
            query = """
                SELECT r.*, c.nombre, c.apellidos, c.dni
                FROM recibo r
                JOIN cliente c ON r.id_cliente = c.id_cliente
                WHERE r.mes = ? AND r.anio = ?
                ORDER BY c.apellidos, c.nombre
            """
            self.execute_query(query, (mes, anio))
        else:
            query = """
                SELECT r.*, c.nombre, c.apellidos, c.dni
                FROM recibo r
                JOIN cliente c ON r.id_cliente = c.id_cliente
                ORDER BY r.anio DESC, r.mes DESC, c.apellidos, c.nombre
            """
            self.execute_query(query)
        return self.cursor.fetchall()
    
    # ==================== DATOS DE PRUEBA ====================
    
    def insertar_datos_prueba(self):
        """Inserta datos de prueba en la base de datos"""
        
        # Clientes de prueba
        clientes = [
            ("Juan", "García López", "12345678A", "600111222", "juan@email.com"),
            ("María", "Fernández Ruiz", "23456789B", "600222333", "maria@email.com"),
            ("Carlos", "Martínez Sanz", "34567890C", "600333444", "carlos@email.com"),
            ("Ana", "López Pérez", "45678901D", "600444555", "ana@email.com"),
            ("Pedro", "Sánchez Gil", "56789012E", "600555666", "pedro@email.com"),
        ]
        
        for c in clientes:
            self.insertar_cliente(*c)
        
        # Aparatos de prueba
        aparatos = [
            ("Cinta de correr 1", "Cardio", "Cinta de correr profesional"),
            ("Cinta de correr 2", "Cardio", "Cinta de correr profesional"),
            ("Bicicleta estática 1", "Cardio", "Bicicleta estática con monitor"),
            ("Press de banca", "Musculación", "Press de banca con barra olímpica"),
            ("Máquina de poleas", "Musculación", "Máquina multiusos de poleas"),
            ("Elíptica 1", "Cardio", "Máquina elíptica"),
            ("Rack de sentadillas", "Musculación", "Rack para sentadillas y dominadas"),
        ]
        
        for a in aparatos:
            self.insertar_aparato(*a)
        
        # Algunas reservas de prueba
        reservas = [
            (1, 1, 1, "09:00"),  # Juan, Cinta 1, Lunes 9:00
            (1, 1, 1, "09:30"),  # Juan, Cinta 1, Lunes 9:30
            (2, 1, 1, "10:00"),  # María, Cinta 1, Lunes 10:00
            (3, 4, 2, "18:00"),  # Carlos, Press banca, Martes 18:00
            (4, 3, 3, "07:00"),  # Ana, Bici 1, Miércoles 7:00
            (5, 5, 4, "20:00"),  # Pedro, Poleas, Jueves 20:00
        ]
        
        for r in reservas:
            self.insertar_reserva(*r)
        
        print("Datos de prueba insertados correctamente")


# Crear instancia global
db = DatabaseManager()
