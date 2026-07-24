"""
==========================================================
Módulo: logger.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Configura el sistema de registro de eventos del proyecto.
    Permite almacenar mensajes informativos, advertencias,
    errores y eventos críticos generados por los módulos de
    entrenamiento, monitoreo, alertas y detección de deriva.

    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Importación de librerías
# ==========================================================

import logging
from pathlib import Path

# ==========================================================
# Configuración de rutas
# ==========================================================

LOG_DIRECTORY = Path("logs")
LOG_DIRECTORY.mkdir(exist_ok=True)

LOG_FILE = LOG_DIRECTORY / "monitor.log"

# ==========================================================
# Configuración del logger
# ==========================================================

def setup_logger(name: str = "ml_monitor") -> logging.Logger:
    """
    Configura y devuelve un logger para registrar eventos
    tanto en consola como en un archivo.

    Args:
        name: Nombre asignado al logger.

    Returns:
        Logger configurado.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        file_handler = logging.FileHandler(LOG_FILE)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# ==========================================================
# Punto de acceso al logger
# ==========================================================

logger = setup_logger()


