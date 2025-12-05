# Requisitos Funcionales - GymForTheMoment

## 1. Introducción

Este documento describe los requisitos funcionales del sistema de gestión para el gimnasio "GymForTheMoment".

---

## 2. Requisitos Funcionales

### RF01 - Gestión de Clientes
| ID | RF01 |
|---|---|
| **Nombre** | Gestión de Clientes |
| **Descripción** | El sistema debe permitir dar de alta, modificar, eliminar y consultar clientes del gimnasio |
| **Entradas** | Datos del cliente: nombre, apellidos, DNI, teléfono, email, fecha de alta |
| **Salidas** | Confirmación de operación realizada |
| **Prioridad** | Alta |

### RF02 - Gestión de Aparatos
| ID | RF02 |
|---|---|
| **Nombre** | Gestión de Aparatos de Entrenamiento |
| **Descripción** | El sistema debe permitir dar de alta, modificar, eliminar y consultar los aparatos disponibles |
| **Entradas** | Datos del aparato: nombre, tipo, descripción |
| **Salidas** | Confirmación de operación realizada |
| **Prioridad** | Alta |

### RF03 - Reserva de Sesiones
| ID | RF03 |
|---|---|
| **Nombre** | Reserva de Sesiones de Aparatos |
| **Descripción** | El sistema debe permitir reservar sesiones de 30 minutos en los aparatos para los clientes |
| **Entradas** | Cliente, aparato, día de la semana (lunes-viernes), hora de inicio |
| **Salidas** | Confirmación de reserva o mensaje de error si está ocupado |
| **Prioridad** | Alta |
| **Restricciones** | - Sesiones de 30 minutos exactos<br>- Solo de lunes a viernes<br>- Disponible 24 horas |

### RF04 - Cancelar Reserva
| ID | RF04 |
|---|---|
| **Nombre** | Cancelación de Reservas |
| **Descripción** | El sistema debe permitir cancelar reservas existentes |
| **Entradas** | ID de la reserva a cancelar |
| **Salidas** | Confirmación de cancelación |
| **Prioridad** | Media |

### RF05 - Listado de Ocupación por Día
| ID | RF05 |
|---|---|
| **Nombre** | Consulta de Ocupación de Aparatos |
| **Descripción** | El sistema debe generar un listado de las horas ocupadas de cada aparato para un día específico, indicando qué cliente lo tiene reservado |
| **Entradas** | Día de la semana (lunes a viernes) |
| **Salidas** | Listado con: aparato, hora, estado (libre/ocupado), cliente (si está ocupado) |
| **Prioridad** | Alta |

### RF06 - Gestión de Pagos Mensuales
| ID | RF06 |
|---|---|
| **Nombre** | Control de Mensualidades |
| **Descripción** | El sistema debe permitir registrar el pago de la mensualidad de los clientes |
| **Entradas** | Cliente, mes, año, estado de pago |
| **Salidas** | Confirmación del registro de pago |
| **Prioridad** | Alta |

### RF07 - Generación de Recibos
| ID | RF07 |
|---|---|
| **Nombre** | Generación Masiva de Recibos |
| **Descripción** | El sistema debe poder generar todos los recibos del mes para todos los clientes activos |
| **Entradas** | Mes y año para generar recibos |
| **Salidas** | Lista de recibos generados |
| **Prioridad** | Alta |

### RF08 - Registro de Pago
| ID | RF08 |
|---|---|
| **Nombre** | Marcar Recibo como Pagado |
| **Descripción** | El sistema debe permitir marcar un recibo como pagado |
| **Entradas** | ID del recibo, fecha de pago |
| **Salidas** | Confirmación del pago registrado |
| **Prioridad** | Alta |

### RF09 - Listado de Morosos
| ID | RF09 |
|---|---|
| **Nombre** | Consulta de Clientes Morosos |
| **Descripción** | El sistema debe generar un listado de clientes que tienen recibos pendientes de pago |
| **Entradas** | Ninguna (o filtro por mes/año opcional) |
| **Salidas** | Listado de clientes morosos con: nombre, recibos pendientes, importe total adeudado |
| **Prioridad** | Alta |

### RF10 - Listado de Clientes que han Pagado
| ID | RF10 |
|---|---|
| **Nombre** | Consulta de Clientes al Corriente de Pago |
| **Descripción** | El sistema debe generar un listado de clientes que han pagado sus mensualidades |
| **Entradas** | Mes y año (opcional) |
| **Salidas** | Listado de clientes con pagos al día |
| **Prioridad** | Media |

---

## 3. Requisitos No Funcionales

### RNF01 - Usabilidad
- La interfaz debe ser intuitiva y fácil de usar
- Mensajes de error claros y descriptivos

### RNF02 - Rendimiento
- Las consultas deben ejecutarse en menos de 2 segundos

### RNF03 - Disponibilidad
- El sistema debe estar disponible para uso local

### RNF04 - Mantenibilidad
- Código documentado y estructurado
- Uso de buenas prácticas de programación

### RNF05 - Portabilidad
- Compatible con Windows, Linux y macOS

---

## 4. Reglas de Negocio

| ID | Regla |
|---|---|
| RN01 | El gimnasio opera 24 horas de lunes a viernes |
| RN02 | Cada sesión de aparato dura exactamente 30 minutos |
| RN03 | Aparatos iguales se tratan como distintos (cada uno tiene su propio horario) |
| RN04 | La mensualidad es fija e igual para todos los clientes |
| RN05 | Los recibos se generan una vez al mes |
| RN06 | Un cliente es moroso si tiene al menos un recibo sin pagar |

---

## 5. Actores del Sistema

| Actor | Descripción |
|---|---|
| **Administrador** | Usuario principal que gestiona clientes, aparatos, reservas y pagos |
| **Sistema** | Genera automáticamente recibos y reportes |
