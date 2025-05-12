# app/routers/usuarios.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from .. import schemas, database, auth, crud

router = APIRouter(
    prefix="/api/v1/usuarios",
    tags=["usuarios"]
)

@router.post("/", response_model=schemas.Usuario, status_code=201)
def crear_usuario(
        usuario: schemas.UsuarioCreate,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    # Verificar si el email ya existe
    db_user = crud.get_usuario_by_email(db, email=usuario.email)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El correo electrónico ya está registrado"
        )

    # Verificar si el username ya existe
    db_user = crud.get_usuario_by_username(db, username=usuario.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="El nombre de usuario ya está en uso"
        )

    return crud.crear_usuario(db=db, usuario=usuario)

@router.get("/", response_model=List[schemas.Usuario])
def leer_usuarios(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios

@router.get("/me", response_model=schemas.Usuario)
def leer_usuario_propio(
        current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    return current_user

@router.get("/{usuario_id}", response_model=schemas.Usuario)
def leer_usuario(
        usuario_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    db_usuario = crud.get_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.put("/me", response_model=schemas.Usuario)
def actualizar_usuario_propio(
        usuario_update: Dict[str, Any],
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_active_user)
):
    # No permitir cambiar el estado de administrador
    if "is_admin" in usuario_update:
        del usuario_update["is_admin"]

    # Verificar si se está actualizando el email y si ya existe
    if "email" in usuario_update and usuario_update["email"] != current_user.email:
        db_user = crud.get_usuario_by_email(db, email=usuario_update["email"])
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="El correo electrónico ya está registrado"
            )

    # Verificar si se está actualizando el username y si ya existe
    if "username" in usuario_update and usuario_update["username"] != current_user.username:
        db_user = crud.get_usuario_by_username(db, username=usuario_update["username"])
        if db_user:
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya está en uso"
            )

    return crud.actualizar_usuario(db, usuario_id=current_user.id, usuario_update=usuario_update)

@router.put("/{usuario_id}", response_model=schemas.Usuario)
def actualizar_usuario(
        usuario_id: int,
        usuario_update: Dict[str, Any],
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    # Verificar si se está actualizando el email y si ya existe
    if "email" in usuario_update:
        db_user = crud.get_usuario_by_email(db, email=usuario_update["email"])
        if db_user and db_user.id != usuario_id:
            raise HTTPException(
                status_code=400,
                detail="El correo electrónico ya está registrado"
            )

    # Verificar si se está actualizando el username y si ya existe
    if "username" in usuario_update:
        db_user = crud.get_usuario_by_username(db, username=usuario_update["username"])
        if db_user and db_user.id != usuario_id:
            raise HTTPException(
                status_code=400,
                detail="El nombre de usuario ya está en uso"
            )

    db_usuario = crud.actualizar_usuario(db, usuario_id=usuario_id, usuario_update=usuario_update)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@router.delete("/{usuario_id}", response_model=schemas.Usuario)
def eliminar_usuario(
        usuario_id: int,
        db: Session = Depends(database.get_db),
        current_user: schemas.Usuario = Depends(auth.get_current_admin_user)
):
    # No permitir que un administrador se elimine a sí mismo
    if usuario_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="No puedes eliminar tu propio usuario"
        )

    db_usuario = crud.eliminar_usuario(db, usuario_id=usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario