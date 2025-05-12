# app/__init__.py
from .exception_handler import setup_exception_handlers

# Esto permite importar directamente desde el paquete app
__all__ = ["setup_exception_handlers"]