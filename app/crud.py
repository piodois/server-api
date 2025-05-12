from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import Dict, Any, List, Optional
from sqlalchemy import and_


# Operaciones CRUD para Usuarios
def crear_usuario(db: Session, usuario: schemas.UsuarioCreate):
    hashed_password = auth.get_password_hash(usuario.password)
    db_usuario = models.Usuario(
        email=usuario.email,
        username=usuario.username,
        hashed_password=hashed_password,
        is_active=usuario.is_active,
        is_admin=usuario.is_admin
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def get_usuario_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def get_usuario_by_username(db: Session, username: str):
    return db.query(models.Usuario).filter(models.Usuario.username == username).first()


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).order_by(models.Usuario.id).offset(skip).limit(limit).all()


def actualizar_usuario(db: Session, usuario_id: int, usuario_update: Dict[str, Any]):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario:
        for key, value in usuario_update.items():
            if key == "password":
                setattr(db_usuario, "hashed_password", auth.get_password_hash(value))
            else:
                setattr(db_usuario, key, value)
        db.commit()
        db.refresh(db_usuario)
    return db_usuario


def eliminar_usuario(db: Session, usuario_id: int):
    db_usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if db_usuario:
        db.delete(db_usuario)
        db.commit()
    return db_usuario


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
    # Agregamos un order_by obligatorio para SQL Server
    return db.query(models.Categoria).order_by(models.Categoria.id).offset(skip).limit(limit).all()


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
    # Agregamos un order_by obligatorio para SQL Server
    return db.query(models.Producto).order_by(models.Producto.id).offset(skip).limit(limit).all()


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

    # Agregamos un order_by obligatorio para SQL Server
    return query.order_by(models.Producto.id).offset(skip).limit(limit).all()