# Sistema de Gestión de Minimercado - Backend

Este proyecto corresponde a la Tarea T02.03 y consiste en el desarrollo del backend de un sistema de gestión para un minimercado.

El sistema fue desarrollado con FastAPI, SQLAlchemy y SQLite. Su estructura está organizada en modelos, repositorios, servicios y controladores para mantener el código ordenado y facilitar su funcionamiento.

## Integrantes

* Edgar Mauricio Carrera
* Ariel Argudo
* Grupo 2

## Funcionalidades

El sistema permite realizar las siguientes acciones:

* Inicio de sesión de usuarios.
* Control de acceso mediante roles de administrador y cajero.
* Registro y administración de usuarios.
* Registro de categorías.
* Registro, consulta, modificación y eliminación de productos.
* Control del stock disponible.
* Consulta de productos con bajo inventario.
* Registro y administración de proveedores.
* Registro de ventas.
* Descuento automático de productos del inventario.
* Anulación de ventas.
* Devolución de productos al inventario cuando una venta es anulada.
* Generación de facturas.
* Registro de órdenes de compra.
* Recepción de mercadería.
* Aumento automático del stock al recibir productos.
* Registro de movimientos de inventario.
* Consulta de reportes de ventas.

## Estructura del proyecto

```text
app/
├── controllers/
├── core/
├── models/
├── repositories/
├── schemas/
├── services/
├── main.py
└── seed.py
```

### Descripción de las carpetas

* `controllers`: contiene los endpoints de la aplicación.
* `core`: contiene la configuración, seguridad y conexión con la base de datos.
* `models`: contiene las entidades y tablas del sistema.
* `repositories`: contiene las consultas y acceso a los datos.
* `schemas`: contiene la validación de la información.
* `services`: contiene las reglas de negocio.
* `main.py`: archivo principal de la aplicación.
* `seed.py`: archivo utilizado para crear los datos iniciales.

## Requisitos

Para ejecutar el proyecto se necesita:

* Python 3.10 o superior.
* Git.
* Visual Studio Code.
* Conexión a internet para instalar las dependencias.

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/mauricio12356/SGM-Backend-FastAPI.git
```

Ingresar a la carpeta del proyecto:

```bash
cd SGM-Backend-FastAPI
```

Crear el entorno virtual:

```bash
python -m venv .venv
```

Activar el entorno virtual en Windows:

```bash
.venv\Scripts\activate
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

Crear los datos iniciales:

```bash
python -m app.seed
```

Ejecutar la aplicación:

```bash
uvicorn app.main:app --reload
```

## Acceso al sistema

Después de ejecutar el proyecto, se puede ingresar desde el navegador a las siguientes direcciones:

* Swagger: `http://127.0.0.1:8000/docs`
* OpenAPI: `http://127.0.0.1:8000/openapi.json`
* Estado del sistema: `http://127.0.0.1:8000/health`

## Usuario inicial

Para realizar las pruebas se puede utilizar el siguiente usuario:

```text
Correo: admin@sgm.local
Contraseña: Admin123*
```

Estas credenciales se utilizan únicamente para las pruebas académicas del sistema.

## Prueba mediante Swagger

Para probar el funcionamiento del sistema:

1. Abrir `http://127.0.0.1:8000/docs`.
2. Buscar el servicio `POST /api/v1/auth/login`.
3. Ingresar el correo y la contraseña.
4. Copiar el token generado.
5. Presionar el botón `Authorize`.
6. Escribir `Bearer`, dejar un espacio y pegar el token.
7. Crear una categoría.
8. Registrar un producto.
9. Registrar un proveedor.
10. Realizar una venta.
11. Consultar el inventario y los reportes.

## Pruebas automáticas

Para ejecutar las pruebas del sistema se utiliza:

```bash
pytest -q
```

Si las pruebas se ejecutan correctamente, la terminal mostrará los casos aprobados.

## Repositorio

El código fuente del proyecto se encuentra disponible en:

```text
https://github.com/mauricio12356/SGM-Backend-FastAPI
```

## Conclusión

El desarrollo de este sistema permitió aplicar conocimientos relacionados con la creación de servicios web, bases de datos, organización de código y control de versiones.

La aplicación permite gestionar productos, ventas, proveedores e inventario dentro de un minimercado. Además, Swagger facilita la revisión y prueba de cada servicio directamente desde el navegador.


