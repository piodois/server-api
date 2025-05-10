from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from . import models, schemas, crud, database
from .config import settings

# Inicialización de la base de datos
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
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


# Endpoints para Categorías
@app.post(f"{settings.API_V1_STR}/categorias/", response_model=schemas.Categoria, status_code=201)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(database.get_db)):
    return crud.crear_categoria(db=db, categoria=categoria)


@app.get(f"{settings.API_V1_STR}/categorias/", response_model=List[schemas.Categoria])
def leer_categorias(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    categorias = crud.obtener_categorias(db, skip=skip, limit=limit)
    return categorias


@app.get(f"{settings.API_V1_STR}/categorias/{{categoria_id}}", response_model=schemas.Categoria)
def leer_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    db_categoria = crud.obtener_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


@app.put(f"{settings.API_V1_STR}/categorias/{{categoria_id}}", response_model=schemas.Categoria)
def actualizar_categoria(
        categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(database.get_db)
):
    db_categoria = crud.actualizar_categoria(db, categoria_id=categoria_id, categoria=categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


@app.delete(f"{settings.API_V1_STR}/categorias/{{categoria_id}}", response_model=schemas.Categoria)
def eliminar_categoria(categoria_id: int, db: Session = Depends(database.get_db)):
    db_categoria = crud.eliminar_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


# Endpoints para Productos
@app.post(f"{settings.API_V1_STR}/productos/", response_model=schemas.Producto, status_code=201)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(database.get_db)):
    return crud.crear_producto(db=db, producto=producto)


@app.get(f"{settings.API_V1_STR}/productos/", response_model=List[schemas.Producto])
def leer_productos(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    productos = crud.obtener_productos(db, skip=skip, limit=limit)
    return productos


@app.get(f"{settings.API_V1_STR}/productos/{{producto_id}}", response_model=schemas.Producto)
def leer_producto(producto_id: int, db: Session = Depends(database.get_db)):
    db_producto = crud.obtener_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@app.put(f"{settings.API_V1_STR}/productos/{{producto_id}}", response_model=schemas.Producto)
def actualizar_producto(
        producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(database.get_db)
):
    db_producto = crud.actualizar_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


@app.delete(f"{settings.API_V1_STR}/productos/{{producto_id}}", response_model=schemas.Producto)
def eliminar_producto(producto_id: int, db: Session = Depends(database.get_db)):
    db_producto = crud.eliminar_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto


# Endpoint GET dinámico para filtrar productos
@app.get(f"{settings.API_V1_STR}/productos/filtrar/", response_model=List[schemas.Producto])
def filtrar_productos(
        nombre: Optional[str] = None,
        precio_min: Optional[int] = None,
        precio_max: Optional[int] = None,
        disponible: Optional[bool] = None,
        categoria_id: Optional[int] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db)
):
    filtros = {
        "nombre": nombre,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "disponible": disponible,
        "categoria_id": categoria_id
    }
    # Eliminar valores None para no aplicar esos filtros
    filtros = {k: v for k, v in filtros.items() if v is not None}

    productos = crud.filtrar_productos(db=db, filtros=filtros, skip=skip, limit=limit)
    return productos


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)