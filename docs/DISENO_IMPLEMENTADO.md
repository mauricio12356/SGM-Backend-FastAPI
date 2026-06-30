# Trazabilidad con la Tarea T02.02

El backend aplica una arquitectura en capas:

1. **Modelos:** entidades persistentes del dominio.
2. **Repositorios:** consultas y operaciones de base de datos.
3. **Servicios:** reglas de negocio, cálculos y transacciones.
4. **Controladores:** endpoints HTTP documentados con OpenAPI/Swagger.

## Entidades implementadas

Usuario, Token, Categoría, Producto, Proveedor, Venta, DetalleVenta, Factura, OrdenCompra, DetalleOrden y MovimientoInventario.

## Flujos principales

- **Registrar venta:** valida stock, calcula subtotal/IVA/total, guarda detalles, descuenta inventario, registra movimientos y genera factura.
- **Recibir mercadería:** valida orden pendiente, incrementa stock, actualiza precio de compra y registra movimientos.
- **Anular venta:** restituye stock y genera movimientos de reversión.

## Estados

- Venta: `COMPLETED`, `CANCELLED`.
- Orden de compra: `PENDING`, `RECEIVED`.
- Producto: estado activo y condición dinámica de stock disponible/bajo/sin stock.
