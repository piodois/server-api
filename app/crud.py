from sqlalchemy.orm import Session
from . import models, schemas
from typing import Dict, Any, List, Optional
from sqlalchemy import and_


# Operaciones CRUD para Categorías
def crear_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(nombre=categoria.nombre)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


def obtener_categoria(db: Session, categoria_id: int):
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()


def obtener_categorias(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).offset(skip).limit(limit).all()


def actualizar_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaCreate):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria:
        db_categoria.nombre = categoria.nombre
        db.commit()
        db.refresh(db_categoria)
    return db_categoria


def eliminar_categoria(db: Session, categoria_id: int):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria:
        db.delete(db_categoria)
        db.commit()
    return db_categoria


# Operaciones CRUD para Productos
def crear_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def obtener_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()


def obtener_productos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Producto).offset(skip).limit(limit).all()


def actualizar_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        update_data = producto.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_producto, key, value)
        db.commit()
        db.refresh(db_producto)
    return db_producto


def eliminar_producto(db: Session, producto_id: int):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto:
        db.delete(db_producto)
        db.commit()
    return db_producto


# Función para filtrado dinámico de productos
def filtrar_productos(db: Session, filtros: Optional[Dict[str, Any]] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Producto)

    if filtros:
        condiciones = []

        if filtros.get("nombre"):
            condiciones.append(models.Producto.nombre.like(f"%{filtros['nombre']}%"))

        if filtros.get("precio_min") is not None:
            condiciones.append(models.Producto.precio >= filtros["precio_min"])

        if filtros.get("precio_max") is not None:
            condiciones.append(models.Producto.precio <= filtros["precio_max"])

        if filtros.get("disponible") is not None:
            condiciones.append(models.Producto.disponible == filtros["disponible"])

        if filtros.get("categoria_id") is not None:
            condiciones.append(models.Producto.categoria_id == filtros["categoria_id"])

        if condiciones:
            query = query.filter(and_(*condiciones))

    return query.offset(skip).limit(limit).all()