# -*- coding: utf-8 -*-
"""
GymForTheMoment - Utilidades
Funciones auxiliares para la aplicación
"""

from datetime import datetime

# Días de la semana
DIAS_SEMANA = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes"
}

# Meses del año
MESES = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}

# Mensualidad fija
MENSUALIDAD = 50.00


def obtener_nombre_dia(dia_numero: int) -> str:
    """Convierte número de día a nombre"""
    return DIAS_SEMANA.get(dia_numero, "Desconocido")


def obtener_nombre_mes(mes_numero: int) -> str:
    """Convierte número de mes a nombre"""
    return MESES.get(mes_numero, "Desconocido")


def generar_franjas_horarias() -> list:
    """
    Genera todas las franjas horarias de 30 minutos para un día de 24 horas.
    
    Returns:
        Lista de tuplas (hora_str, hora_display)
    """
    franjas = []
    for hora in range(24):
        for minuto in [0, 30]:
            hora_str = f"{hora:02d}:{minuto:02d}"
            if minuto == 0:
                hora_display = f"{hora:02d}:00 - {hora:02d}:30"
            else:
                siguiente_hora = (hora + 1) % 24
                hora_display = f"{hora:02d}:30 - {siguiente_hora:02d}:00"
            franjas.append((hora_str, hora_display))
    return franjas


def validar_dni(dni: str) -> bool:
    """
    Valida el formato de un DNI español.
    
    Args:
        dni: DNI a validar
        
    Returns:
        True si el formato es válido
    """
    if not dni:
        return False
    
    dni = dni.upper().strip()
    
    # DNI: 8 dígitos + 1 letra
    if len(dni) == 9:
        numeros = dni[:8]
        letra = dni[8]
        if numeros.isdigit() and letra.isalpha():
            letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
            letra_correcta = letras_validas[int(numeros) % 23]
            return letra == letra_correcta
    
    # NIE: X/Y/Z + 7 dígitos + 1 letra
    if len(dni) == 9 and dni[0] in 'XYZ':
        primer_digito = {'X': '0', 'Y': '1', 'Z': '2'}[dni[0]]
        numeros = primer_digito + dni[1:8]
        letra = dni[8]
        if numeros.isdigit() and letra.isalpha():
            letras_validas = "TRWAGMYFPDXBNJZSQVHLCKE"
            letra_correcta = letras_validas[int(numeros) % 23]
            return letra == letra_correcta
    
    return False


def validar_email(email: str) -> bool:
    """
    Valida el formato de un email de forma básica.
    
    Args:
        email: Email a validar
        
    Returns:
        True si el formato parece válido
    """
    if not email:
        return True  # Email es opcional
    
    email = email.strip()
    
    if '@' not in email:
        return False
    
    partes = email.split('@')
    if len(partes) != 2:
        return False
    
    usuario, dominio = partes
    if not usuario or not dominio:
        return False
    
    if '.' not in dominio:
        return False
    
    return True


def formatear_moneda(cantidad: float) -> str:
    """Formatea una cantidad como moneda"""
    return f"{cantidad:.2f} €"


def obtener_anio_actual() -> int:
    """Devuelve el año actual"""
    return datetime.now().year


def obtener_mes_actual() -> int:
    """Devuelve el mes actual"""
    return datetime.now().month
