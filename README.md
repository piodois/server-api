# API FastAPI con SQL Server y Autenticación JWT

Este proyecto es una demostración de una API REST desarrollada con FastAPI que utiliza SQL Server como base de datos y JWT para la autenticación de usuarios.

## Características

- Autenticación de usuarios mediante JWT (JSON Web Tokens)
- Sistema de roles (admin/usuario)
- CRUD completo para entidades (Productos, Categorías, Usuarios)
- Conexión a SQL Server con SQLAlchemy
- Documentación automática con Swagger UI
- Filtrado dinámico de productos
- Seguridad y validación de datos con Pydantic
- Estructurado siguiendo las mejores prácticas

## Requisitos

- Python 3.8+
- SQL Server
- Driver ODBC 17 para SQL Server

## Instalación

1. Clonar el repositorio:
```bash
git clone <repo-url>
cd <repo-directory>