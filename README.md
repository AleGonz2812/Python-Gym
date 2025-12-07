# 🏋️ GymForTheMoment - Sistema de Gestión de Gimnasio

Sistema de gestión para gimnasio desarrollado en Python con interfaz gráfica Tkinter.

## 📋 Descripción

Aplicación informática para llevar el control de la gestión de un gimnasio que opera 24 horas de lunes a viernes. El sistema incluye autenticación de usuarios y control de acceso basado en roles.

## 🎯 Características Principales

- **Autenticación de usuarios** con login y registro
- **Gestión de clientes** (alta, baja, modificación)
- **Gestión de aparatos** de entrenamiento
- **Reserva de aparatos** (sesiones de 30 minutos)
- **Control de ocupación** por día y tipo de aparato
- **Control de pagos** mensuales (50€/mes)
- **Listado de clientes morosos**
- **Interfaz con tema oscuro** (rojo, negro, gris, amarillo)

## 🔐 Sistema de Autenticación

### Credenciales por defecto

Al iniciar la aplicación por primera vez, se crea automáticamente un usuario administrador:

```
Email: admin@gymforthemoment.com
Contraseña: admin123
```

### Registro de nuevos usuarios

Los nuevos usuarios pueden registrarse desde la pantalla de login. Por defecto, todos los usuarios registrados tienen rol de `empleado`.

### Roles disponibles

- **admin**: Acceso completo al sistema
- **empleado**: Acceso a las funciones operativas

## 📁 Estructura del Proyecto

```
Python-Gym/
├── docs/
│   ├── requisitos_funcionales.md
│   ├── diagrama_casos_uso.md
│   └── diagrama_er.md
├── src/
│   ├── main.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── db_manager.py
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── login.py
│   │   └── app.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── insertar_datos_prueba.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 🚀 Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/AleGonz2812/Python-Gym.git
cd Python-Gym
```

2. Instalar dependencias (solo Python 3.8+ con tkinter)
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación
```bash
python src/main.py
```

## 🧪 Datos de Prueba

Para facilitar las pruebas, puedes insertar datos de ejemplo ejecutando:

```bash
python insertar_datos_prueba.py
```

Esto agregará:
- 5 clientes de ejemplo
- 7 aparatos de ejemplo
- Varias reservas de ejemplo

## 💻 Uso

1. **Iniciar sesión** con las credenciales de admin o crear una nueva cuenta
2. **Gestionar clientes**: Alta, baja y modificación de clientes
3. **Gestionar aparatos**: Añadir equipos de entrenamiento
4. **Crear reservas**: Asignar aparatos a clientes por franjas de 30 minutos
5. **Ver ocupación**: Consultar disponibilidad por día y tipo de aparato
6. **Gestionar pagos**: Controlar los pagos mensuales de 50€
7. **Control de morosos**: Identificar clientes con pagos pendientes

## 🎨 Tema Visual

La interfaz utiliza un esquema de colores personalizado:
- **Rojo Crimson** (#DC143C) - Color principal
- **Negro** (#1a1a1a) - Fondo
- **Gris** (#2d2d2d, #505050) - Elementos
- **Amarillo Dorado** (#FFD700) - Acentos

## 📊 Base de Datos

El sistema utiliza SQLite con las siguientes tablas:
- `usuario` - Usuarios del sistema
- `cliente` - Clientes del gimnasio
- `aparato` - Equipos de entrenamiento
- `reserva` - Reservas de aparatos
- `recibo` - Pagos mensuales

## 👤 Autor

Alejandro González - [@AleGonz2812](https://github.com/AleGonz2812)

Proyecto individual para gymforthemoment

## 📄 Licencia

Este proyecto está bajo la Licencia MIT
