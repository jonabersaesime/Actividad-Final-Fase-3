"""
==========================================================
Módulo: runbooks.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Contiene los procedimientos recomendados (Runbooks)
    para atender incidentes detectados durante el monitoreo
    del modelo de Machine Learning.

Materia:
    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Runbooks disponibles
# ==========================================================

RUNBOOKS = {

    "INFO": [
        "El modelo opera dentro de los parámetros esperados.",
        "Continuar con el monitoreo periódico.",
        "No se requieren acciones correctivas."
    ],

    "WARNING": [
        "Revisar las métricas recientes del modelo.",
        "Analizar posibles cambios en los datos de entrada.",
        "Programar una revisión del desempeño."
    ],

    "CRITICAL": [
        "Detener el despliegue si el modelo está en producción.",
        "Analizar el origen del problema.",
        "Reentrenar el modelo utilizando datos actualizados.",
        "Validar nuevamente las métricas antes de liberar el modelo."
    ]
}


# ==========================================================
# Obtención del Runbook
# ==========================================================

def get_runbook(level: str) -> list:
    """
    Devuelve el procedimiento recomendado para un nivel
    específico de alerta.

    Args:
        level: Nivel de alerta.

    Returns:
        Lista de acciones recomendadas.
    """

    return RUNBOOKS.get(
        level.upper(),
        ["No existe un procedimiento definido."]
    )


# ==========================================================
# Prueba independiente
# ==========================================================

if __name__ == "__main__":

    for step in get_runbook("WARNING"):
        print(step)

