# Sistema de Gestión de Minimercado - Backend
Este proyecto corresponde a la **Tarea T02.03** y sirve como base para la **Tarea T02.04**, la cual consiste en la implementación de pruebas unitarias y el análisis de cobertura del código.

El sistema fue desarrollado con **FastAPI**, **SQLAlchemy** y **SQLite**. Su estructura está organizada en modelos, repositorios, servicios y controladores para mantener el código ordenado, facilitar su mantenimiento y permitir la implementación de pruebas automáticas.

## Integrantes

- Edgar Mauricio Carrera
- Ariel Argudo
**Grupo 2**

---

# Objetivo de la Tarea T02.04
Implementar pruebas unitarias al backend del Sistema de Gestión de Minimercado utilizando frameworks de Testing para verificar el correcto funcionamiento de los servicios desarrollados y medir la cobertura del código.

## Objetivos específicos

- Crear pruebas automáticas utilizando frameworks de Testing.
- Verificar el correcto funcionamiento de los servicios del sistema.
- Obtener una cobertura mínima del **60%** en los métodos del proyecto.

---

# Frameworks utilizados para las pruebas
De acuerdo con los requerimientos de la asignatura, para Python se utilizan los siguientes frameworks:

- **Doctest**
- **Unittest**
- **Pytest**
- **Coverage.py**
- **Mockito** (cuando sea necesario para simulación de dependencias)

---

# Funcionalidades
El sistema permite realizar las siguientes acciones:

- Inicio de sesión de usuarios.
- Control de acceso mediante roles de administrador y cajero.
- Registro y administración de usuarios.
- Registro de categorías.
- Registro, consulta, modificación y eliminación de productos.
- Control del stock disponible.
- Consulta de productos con bajo inventario.
- Registro y administración de proveedores.
- Registro de ventas.
- Descuento automático de productos del inventario.
- Anulación de ventas.
- Devolución de productos al inventario cuando una venta es anulada.
- Generación de facturas.
- Registro de órdenes de compra.
- Recepción de mercadería.
- Aumento automático del stock al recibir productos.
- Registro de movimientos de inventario.
- Consulta de reportes de ventas.

---

# Estructura del proyecto

```
app/
├── controllers/
├── core/
├── models/
├── repositories/
├── schemas/
├── services/
├── main.py
└── seed.py

tests/
├── test_auth.py
├── test_producto.py
├── test_usuario.py
└── ...
```

## Descripción de las carpetas
**controllers:** contiene los endpoints de la aplicación.

**core:** contiene la configuración, seguridad y conexión con la base de datos.

**models:** contiene las entidades y tablas del sistema.

**repositories:** contiene el acceso a los datos.

**schemas:** contiene la validación de la información.

**services:** contiene las reglas de negocio.

**tests:** contiene las pruebas unitarias implementadas con Pytest.

**main.py:** archivo principal de la aplicación.

**seed.py:** crea los datos iniciales del sistema.

---

# Requisitos
Para ejecutar el proyecto se necesita:

- Python 3.10 o superior.
- Git.
- Visual Studio Code.
- Conexión a Internet para instalar dependencias.

---

# Instalación
Clonar el repositorio

```
git clone https://github.com/mauricio12356/SGM-Backend-FastAPI.git
```
Ingresar al proyecto

```
cd SGM-Backend-FastAPI
```
Crear entorno virtual

```
python -m venv .venv
```
Activar entorno virtual (Windows)

```
.venv\Scripts\activate
```
Instalar dependencias

```
pip install -r requirements.txt
```
Crear datos iniciales

```
python -m app.seed
```
Ejecutar la aplicación

```
uvicorn app.main:app --reload
```

---

# Acceso al sistema
Swagger

```
http://127.0.0.1:8000/docs
```
OpenAPI

```
http://127.0.0.1:8000/openapi.json
```
Estado del sistema

```
http://127.0.0.1:8000/health
```

---

# Usuario inicial
Correo

```
admin@sgm.local
```
Contraseña

```
Admin123*
```
Estas credenciales se utilizan únicamente para fines académicos.

---

# Pruebas mediante Swagger

1. Abrir Swagger.
2. Ejecutar el servicio **POST /api/v1/auth/login**.
3. Ingresar las credenciales.
4. Copiar el token generado.
5. Presionar **Authorize**.
6. Escribir **Bearer** seguido del token.
7. Crear categorías.
8. Registrar productos.
9. Registrar proveedores.
10. Registrar ventas.
11. Consultar inventario y reportes.

---

# Pruebas automáticas
Las pruebas unitarias fueron implementadas utilizando **Pytest**.

Ejecutar todas las pruebas:

```
pytest -q
```
Ejecutar una prueba específica:

```
pytest tests/test_usuario.py
```

---

# Cobertura del código
Para verificar la cobertura del proyecto se utiliza **Coverage.py**.

Ejecutar la cobertura:

```
coverage run -m pytest
```
Generar el reporte:

```
coverage report -m
```
Generar reporte HTML:

```
coverage html
```
Abrir el reporte:

```
htmlcov/index.html
```
La cobertura mínima requerida para la tarea es del **60%** de los métodos implementados.

---

# Repositorio
Código fuente:

[https://github.com/mauricio12356/SGM-Backend-FastAPI](https://github.com/mauricio12356/SGM-Backend-FastAPI)

---

# Entregables de la Tarea T02.04

- Archivo PDF denominado **T02_04_GrupoXX_Apellido1Nombre1.pdf**.
- Aplicación almacenada en un repositorio de código.
- Implementación de pruebas unitarias.
- Evidencia del análisis de cobertura del código.
- La entrega en el AVAC debe realizarse de manera individual, aunque el desarrollo sea en grupo.

---

# Conclusión
El desarrollo de este proyecto permitió aplicar conocimientos relacionados con el desarrollo de servicios web utilizando FastAPI, la organización del código mediante una arquitectura por capas y la implementación de pruebas unitarias para garantizar la calidad del software.

La incorporación de Pytest y Coverage.py permitió validar el comportamiento de los servicios y medir la cobertura del código, asegurando el cumplimiento de los requerimientos establecidos para la Tarea T02.04. Además, Swagger facilita la verificación manual de cada endpoint y complementa el proceso de pruebas automáticas.
