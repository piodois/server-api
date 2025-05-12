from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


# Schemas para Usuario
class UsuarioBase(BaseModel):
    email: EmailStr
    username: str
    is_active: bool = True
    is_admin: bool = False


class UsuarioCreate(UsuarioBase):
    password: str


class Usuario(UsuarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class UsuarioInDB(Usuario):
    hashed_password: str


# Schemas para autenticación
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True


# Schemas para Producto
class ProductoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: int = Field(..., gt=0)
    disponible: bool = True
    categoria_id: int


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[int] = Field(None, gt=0)
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None


class Producto(ProductoBase):
    id: int
    fecha_creacion: datetime
    categoria: Categoria

    class Config:
        from_attributes = True


# Schema para filtros dinámicos
class ProductoFilter(BaseModel):
    nombre: Optional[str] = None
    precio_min: Optional[int] = None
    precio_max: Optional[int] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None