# app/routers/categorias.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, database, auth, crud

router = APIRouter(
    prefix="/api/v1/categorias",
    tags=["categorías"]
)

@router.post("/", response_model=schemas.Categoria, status_code=201)
def crear_categoria(
        categoria: schemas.CategoriaCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    return crud.crear_categoria(db=db, categoria=categoria)

@router.get("/", response_model=List[schemas.Categoria])
def leer_categorias(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db)
):
    categorias = crud.obtener_categorias(db, skip=skip, limit=limit)
    return categorias

@router.get("/{categoria_id}", response_model=schemas.Categoria)
def leer_categoria(
        categoria_id: int,
        db: Session = Depends(database.get_db)
):
    db_categoria = crud.obtener_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.put("/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(
        categoria_id: int,
        categoria: schemas.CategoriaCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    db_categoria = crud.actualizar_categoria(db, categoria_id=categoria_id, categoria=categoria)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.delete("/{categoria_id}", response_model=schemas.Categoria)
def eliminar_categoria(
        categoria_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    db_categoria = crud.eliminar_categoria(db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria