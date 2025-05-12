# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import schemas, database, auth, crud
from ..config import settings

router = APIRouter(
    prefix=f"{settings.API_V1_STR}/auth",
    tags=["autenticación"]
)

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(database.get_db)
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/registro", response_model=schemas.Usuario, status_code=201)
def registrar_usuario(
        usuario: schemas.UsuarioCreate,
        db: Session = Depends(database.get_db)
):
    # Para el registro de usuarios normales, no administradores
    usuario.is_admin = True

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