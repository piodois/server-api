# API REST con FastAPI, SQL Server y JWT

Este proyecto es una API REST completa desarrollada con FastAPI que utiliza SQL Server como motor de base de datos y autenticación JWT para gestionar usuarios, productos y categorías.

## Características

- ✅ **Autenticación segura** con JWT (JSON Web Tokens)
- 👥 **Sistema de roles** (administrador/usuario)
- 🔄 **CRUD completo** para Productos, Categorías y Usuarios
- 🔍 **Filtrado dinámico** de productos por múltiples parámetros
- 🛡️ **Validación de datos** con Pydantic
- 📝 **Documentación automática** con Swagger UI y ReDoc
- 🧩 **Arquitectura modular** siguiendo las mejores prácticas
- 🔒 **Manejo seguro de contraseñas** con hashing bcrypt
- 🚨 **Control de excepciones** centralizado

## Requisitos previos

- Python 3.8+
- SQL Server
- Driver ODBC 17 para SQL Server

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/piodois/server-api.git
cd server-api
```

2. Crear un entorno virtual e instalar dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Configurar las variables de entorno:
```bash
# Copiar el archivo de ejemplo
cp .env.example .env

# Editar el archivo .env con los datos de conexión a SQL Server
```

## Configuración de la base de datos

La API puede conectarse a SQL Server de dos maneras:

- **Autenticación de Windows** (trusted connection):
```
DB_TRUSTED_CONNECTION=True
DB_HOST=localhost
DB_NAME=nombre_base_datos
```

- **Autenticación con usuario y contraseña**:
```
DB_TRUSTED_CONNECTION=False
DB_HOST=localhost
DB_PORT=1433
DB_NAME=nombre_base_datos
DB_USER=usuario
DB_PASSWORD=contraseña
```

## Ejecución

Para iniciar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://localhost:8000`

## Documentación

La documentación de la API está disponible en:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estructura del proyecto

```
server-api/
├── app/
│   ├── routers/           # Endpoints de la API
│   │   ├── auth.py        # Autenticación y registro
│   │   ├── categorias.py  # Gestión de categorías
│   │   ├── productos.py   # Gestión de productos
│   │   └── usuarios.py    # Gestión de usuarios
│   ├── __init__.py        # Inicialización
│   ├── auth.py            # Lógica de autenticación
│   ├── config.py          # Configuración global
│   ├── crud.py            # Operaciones CRUD
│   ├── database.py        # Conexión a la base de datos
│   ├── exception_handler.py # Manejador de excepciones
│   ├── main.py            # Punto de entrada principal
│   ├── models.py          # Modelos SQLAlchemy
│   └── schemas.py         # Esquemas Pydantic
├── .env                   # Variables de entorno (no incluido en el repo)
├── .env.example           # Ejemplo de variables de entorno
├── README.md              # Documentación
└── requirements.txt       # Dependencias
```

## Endpoints principales

### Autenticación

- `POST /api/v1/auth/login` - Iniciar sesión
- `POST /api/v1/auth/registro` - Registrar nuevo usuario

### Usuarios

- `GET /api/v1/usuarios/me` - Obtener información del usuario actual
- `PUT /api/v1/usuarios/me` - Actualizar información del usuario actual

### Productos

- `GET /api/v1/productos/` - Listar todos los productos
- `POST /api/v1/productos/` - Crear un nuevo producto (admin)
- `GET /api/v1/productos/{producto_id}` - Obtener un producto específico
- `PUT /api/v1/productos/{producto_id}` - Actualizar un producto (admin)
- `DELETE /api/v1/productos/{producto_id}` - Eliminar un producto (admin)
- `GET /api/v1/productos/filtrar/` - Filtrar productos por diversos criterios

### Categorías

- `GET /api/v1/categorias/` - Listar todas las categorías
- `POST /api/v1/categorias/` - Crear una nueva categoría (admin)
- `GET /api/v1/categorias/{categoria_id}` - Obtener una categoría específica
- `PUT /api/v1/categorias/{categoria_id}` - Actualizar una categoría (admin)
- `DELETE /api/v1/categorias/{categoria_id}` - Eliminar una categoría (admin)

## Seguridad

- Las contraseñas se almacenan utilizando hashing bcrypt
- La autenticación se realiza mediante tokens JWT
- Se implementan roles para restringir el acceso a ciertos endpoints
- Las excepciones se manejan centralmente para evitar la divulgación de información sensible

## Contribuir

1. Hacer fork del repositorio
2. Crear una rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Hacer commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`)
4. Hacer push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Notas

⚠️ **Atención**: Por defecto, todos los usuarios registrados tienen el rol de administrador. Para crear usuarios regulares, es necesario modificar la lógica en el router de autenticación.