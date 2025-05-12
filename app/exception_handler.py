from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError
from typing import Union
import traceback


def setup_exception_handlers(app: FastAPI) -> None:
    """Configura los manejadores de excepciones para la aplicación."""

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
        """Maneja excepciones de SQLAlchemy."""
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error de base de datos", "error": str(exc)},
        )

    @app.exception_handler(JWTError)
    async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
        """Maneja excepciones relacionadas con tokens JWT."""
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Error de autenticación", "error": str(exc)},
            headers={"WWW-Authenticate": "Bearer"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        """Maneja excepciones generales no capturadas por otros manejadores."""
        # En producción, no deberías exponer el error completo
        error_details = str(exc)
        if app.debug:
            error_details = f"{str(exc)}\n{traceback.format_exc()}"

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Error interno del servidor", "error": error_details},
        )