# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from . import models, database
from .config import settings
from .routers import auth, usuarios, categorias, productos
from .exception_handler import setup_exception_handlers

# Inicialización de la base de datos
models.Base.metadata.create_all(bind=database.engine)
descripcion_api = """
**ADVERTENCIA:** Todos los usuarios registrados tienen el rol de administrador (is_admin = True) por defecto.
Si necesitas crear un usuario normal, debes modificar la lógica de creación de usuarios para establecer `usuario.is_admin = False`.
Esto generalmente se haría dentro del router o la función encargada de la autenticación y creación de usuarios.
"""

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.2.1",  # Aquí especificas la versión de tu API
    description=descripcion_api,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar manejadores de excepciones
setup_exception_handlers(app)

# Incluir routers
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(categorias.router)
app.include_router(productos.router)

# Página de bienvenida en la ruta principal
@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>FastAPI con SQL Server</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                    background-color: #f5f5f5;
                }
                .container {
                    background-color: white;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 2rem;
                    max-width: 800px;
                    width: 90%;
                }
                h1 {
                    color: #333;
                    margin-bottom: 1rem;
                }
                p {
                    color: #666;
                    line-height: 1.6;
                }
                .buttons {
                    margin-top: 2rem;
                    display: flex;
                    gap: 1rem;
                }
                .button {
                    display: inline-block;
                    background-color: #4361ee;
                    color: white;
                    padding: 0.7rem 1.5rem;
                    text-decoration: none;
                    border-radius: 4px;
                    font-weight: bold;
                    transition: background-color 0.3s;
                }
                .button:hover {
                    background-color: #3a56d4;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>¡Bienvenido a tu API con FastAPI y SQL Server!</h1>
                <p>Esta API proporciona endpoints para gestionar categorías y productos. Usa esta interfaz para crear, leer, actualizar y eliminar registros en la base de datos.</p>
                <div class="buttons">
                    <a href="/docs" class="button">Documentación Swagger</a>
                    <a href="/redoc" class="button">Documentación ReDoc</a>
                </div>
            </div>
        </body>
    </html>
    """
    return html_content

# Si se ejecuta directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)