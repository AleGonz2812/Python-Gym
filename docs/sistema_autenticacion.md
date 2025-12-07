# Sistema de Autenticación

## Descripción

GymForTheMoment implementa un sistema de autenticación de usuarios que controla el acceso a la aplicación mediante credenciales (email y contraseña).

## Características

### 1. Login
- Pantalla de inicio de sesión al arrancar la aplicación
- Validación de email y contraseña
- Mensaje de bienvenida personalizado
- Acceso denegado si las credenciales son incorrectas

### 2. Registro de Usuarios
- Opción de crear nueva cuenta desde la pantalla de login
- Campos requeridos:
  - Nombre completo
  - Email (único en el sistema)
  - Contraseña (mínimo 6 caracteres)
- Rol por defecto: `empleado`
- Validación de email duplicado

### 3. Roles de Usuario

#### Administrador (`admin`)
- Acceso completo al sistema
- Credenciales por defecto:
  - Email: `admin@gymforthemoment.com`
  - Contraseña: `admin123`

#### Empleado (`empleado`)
- Acceso a las funciones operativas
- Creado mediante el formulario de registro

## Tabla de Base de Datos

### usuario

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_usuario | INTEGER | Identificador único (PRIMARY KEY) |
| nombre | TEXT | Nombre completo del usuario |
| email | TEXT | Email único del usuario |
| password | TEXT | Contraseña (almacenada en texto plano*) |
| rol | TEXT | Rol del usuario (admin/empleado) |
| activo | INTEGER | Estado del usuario (1=activo, 0=inactivo) |
| fecha_creacion | TEXT | Fecha y hora de creación |

> ⚠️ **Nota de Seguridad**: En esta versión educativa, las contraseñas se almacenan en texto plano. En un entorno de producción, deberían utilizarse funciones de hash (bcrypt, argon2, etc.).

## Flujo de Uso

```
1. Iniciar aplicación
   ↓
2. Mostrar pantalla de Login
   ↓
3a. ¿Tiene cuenta?
    SÍ → Ingresar email/contraseña → Validar → Acceso a aplicación
    NO → Ir a Registro
          ↓
4. Registro: Ingresar nombre, email, contraseña
   ↓
5. Crear usuario con rol 'empleado'
   ↓
6. Volver a Login
   ↓
7. Ingresar credenciales
   ↓
8. Acceso a aplicación principal
```

## Interfaz de Usuario

### Pantalla de Login
- **Título**: GymForTheMoment
- **Subtítulo**: Sistema de Gestión de Gimnasio
- **Campos**:
  - Email
  - Contraseña (oculta)
- **Botones**:
  - ENTRAR (rojo)
  - ¿No tienes cuenta? Regístrate (amarillo)
- **Info**: Credenciales de admin en gris

### Pantalla de Registro
- **Título**: CREAR CUENTA
- **Campos**:
  - Nombre
  - Email
  - Contraseña (mínimo 6 caracteres)
- **Botones**:
  - REGISTRARSE (rojo)
  - ¿Ya tienes cuenta? Inicia sesión (amarillo)

## Funciones Principales

### En `src/database/db_manager.py`

```python
# Crear nuevo usuario
crear_usuario(nombre, email, password, rol='empleado')

# Validar credenciales de login
validar_usuario(email, password)

# Verificar si existe un email
existe_usuario(email)

# Verificar si existe admin
existe_admin()

# Crear admin inicial (automático)
crear_admin_inicial()
```

### En `src/gui/login.py`

```python
# Mostrar ventana de login y retornar usuario autenticado
mostrar_login()

# Clase principal de la ventana
class LoginWindow:
    def login()          # Procesar inicio de sesión
    def registro()       # Procesar registro
    def cambiar_modo()   # Alternar entre login/registro
```

## Integración con la Aplicación

Una vez autenticado, el usuario se pasa a la aplicación principal:

```python
# En src/main.py
usuario = mostrar_login()

if usuario:
    # usuario = {
    #     'id': 1,
    #     'nombre': 'Admin',
    #     'email': 'admin@gymforthemoment.com',
    #     'rol': 'admin'
    # }
    app = GymApp(root, usuario)
```

El objeto `usuario` se almacena en `GymApp.usuario` y se muestra en:
- Barra de estado: `Usuario: [nombre] ([rol]) | Listo`
- Ventana "Acerca de": Información del usuario actual

## Seguridad

### Implementado
✅ Validación de campos obligatorios  
✅ Validación de longitud mínima de contraseña (6 caracteres)  
✅ Validación de email único  
✅ Creación automática de administrador inicial  
✅ Control de acceso por roles  

### Pendiente (para versión de producción)
⚠️ Hash de contraseñas (bcrypt/argon2)  
⚠️ Tokens de sesión  
⚠️ Límite de intentos de login  
⚠️ Recuperación de contraseña  
⚠️ Cambio de contraseña desde la aplicación  
⚠️ Gestión de usuarios por admin  
⚠️ Logs de acceso  

## Mejoras Futuras

1. **Gestión de usuarios**: Panel de administración para crear/editar/desactivar usuarios
2. **Permisos granulares**: Definir qué puede hacer cada rol en cada módulo
3. **Sesiones**: Mantener sesión activa y cierre de sesión manual
4. **Historial**: Registro de acciones por usuario
5. **Recuperación**: Sistema de recuperación de contraseña por email
6. **Seguridad**: Implementar hashing de contraseñas con bcrypt
