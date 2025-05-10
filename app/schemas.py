from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# Schemas para Categoría
class CategoriaBase(BaseModel):
    nombre: str


class CategoriaCreate(CategoriaBase):
    pass


class Categoria(CategoriaBase):
    id: int

    class Config:
        from_attributes = True  # Reemplaza orm_mode = True


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
        from_attributes = True  # Reemplaza orm_mode = True


# Schema para filtros dinámicos
class ProductoFilter(BaseModel):
    nombre: Optional[str] = None
    precio_min: Optional[int] = None
    precio_max: Optional[int] = None
    disponible: Optional[bool] = None
    categoria_id: Optional[int] = None