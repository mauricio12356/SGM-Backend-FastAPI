# Ejemplos de uso de la API

## Iniciar sesión

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@sgm.local","password":"Admin123*"}'
```

## Crear categoría

```bash
curl -X POST http://127.0.0.1:8000/api/v1/categories \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Abarrotes","description":"Productos básicos"}'
```

## Crear venta

```bash
curl -X POST http://127.0.0.1:8000/api/v1/sales \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"payment_method":"CASH","details":[{"product_id":1,"quantity":2}]}'
```
