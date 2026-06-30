# Trazabilidad con la Tarea T02.01

| Requerimiento SRS | Implementación |
|---|---|
| Registrar usuarios y perfiles | `/api/v1/users`, roles ADMIN/CASHIER |
| Registrar productos y categorías | `/api/v1/products`, `/api/v1/categories` |
| Controlar stock | Venta, recepción de orden y movimientos automáticos |
| Registrar ventas | `/api/v1/sales` |
| Generar facturas y tickets | Entidad Invoice devuelta con cada venta |
| Registrar proveedores | `/api/v1/suppliers` |
| Registrar clientes | Datos fiscales del cliente en cada factura |
| Reportes de ventas e inventario | `/api/v1/reports/*` y `/products/low-stock` |
| Arqueos/cierres de caja | Resumen acumulado de ventas como base para cierre |

## Requerimientos no funcionales

- Interfaz de servicios sencilla mediante Swagger.
- Contraseñas con PBKDF2 y endpoints protegidos por token.
- Base de datos relacional con transacciones.
- Separación de responsabilidades por capas.
- Pruebas automáticas del flujo principal.
