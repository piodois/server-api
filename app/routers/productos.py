# app/routers/productos.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from .. import schemas, database, auth, crud

router = APIRouter(
    prefix="/api/v1/productos",
    tags=["productos"]
)

@router.post("/", response_model=schemas.Producto, status_code=201)
def crear_producto(
        producto: schemas.ProductoCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    return crud.crear_producto(db=db, producto=producto)

@router.get("/", response_model=List[schemas.Producto])
def leer_productos(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db)
):
    productos = crud.obtener_productos(db, skip=skip, limit=limit)
    return productos

@router.get("/{producto_id}", response_model=schemas.Producto)
def leer_producto(
        producto_id: int,
        db: Session = Depends(database.get_db)
):
    db_producto = crud.obtener_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.put("/{producto_id}", response_model=schemas.Producto)
def actualizar_producto(
        producto_id: int,
        producto: schemas.ProductoUpdate,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    db_producto = crud.actualizar_producto(db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.delete("/{producto_id}", response_model=schemas.Producto)
def eliminar_producto(
    producto_id: int,
    db: Session = Depends(database.get_db),
    current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    db_producto = crud.eliminar_producto(db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto

@router.get("/filtrar/", response_model=List[schemas.Producto])
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