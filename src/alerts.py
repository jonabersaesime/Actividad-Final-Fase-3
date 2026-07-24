"""
==========================================================
Módulo: alerts.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Evalúa las métricas de desempeño del modelo y genera
    alertas de acuerdo con umbrales previamente definidos.

    El módulo clasifica el estado del modelo en tres niveles:

    - INFO: funcionamiento normal.
    - WARNING: degradación moderada.
    - CRITICAL: degradación severa que requiere intervención.

    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Importación de módulos internos
# ==========================================================

from src.logger import logger


# ==========================================================
# Umbrales de monitoreo
# ==========================================================

RECALL_WARNING_THRESHOLD = 0.85
RECALL_CRITICAL_THRESHOLD = 0.75


# ==========================================================
# Evaluación del recall
# ==========================================================

def evaluate_recall_alert(recall_value: float) -> dict:
    """
    Evalúa el valor de recall y determina el nivel de alerta.

    Args:
        recall_value: Valor de recall obtenido por el modelo.
            Debe encontrarse entre 0 y 1.

    Returns:
        Diccionario con el nivel, la métrica, el valor evaluado
        y el mensaje correspondiente.

    Raises:
        TypeError: Si el valor recibido no es numérico.
        ValueError: Si el recall no se encuentra entre 0 y 1.
    """

    if not isinstance(recall_value, (int, float)):
        raise TypeError("El valor de recall debe ser numérico.")

    if not 0 <= recall_value <= 1:
        raise ValueError("El valor de recall debe estar entre 0 y 1.")

    if recall_value < RECALL_CRITICAL_THRESHOLD:
        level = "CRITICAL"
        message = (
            "El recall presenta una degradación crítica. "
            "Se requiere revisar el modelo y ejecutar el runbook."
        )
        logger.critical(
            "Alerta de recall | Nivel: %s | Valor: %.4f",
            level,
            recall_value
        )

    elif recall_value < RECALL_WARNING_THRESHOLD:
        level = "WARNING"
        message = (
            "El recall presenta una degradación moderada. "
            "Se recomienda mantener el modelo bajo observación."
        )
        logger.warning(
            "Alerta de recall | Nivel: %s | Valor: %.4f",
            level,
            recall_value
        )

    else:
        level = "INFO"
        message = "El recall se encuentra dentro del rango normal."
        logger.info(
            "Evaluación de recall | Nivel: %s | Valor: %.4f",
            level,
            recall_value
        )

    return {
        "metric": "recall",
        "value": recall_value,
        "level": level,
        "message": message
    }


# ==========================================================
# Evaluación general de métricas
# ==========================================================

def evaluate_model_alerts(metrics: dict) -> list[dict]:
    """
    Evalúa las métricas recibidas y genera las alertas aplicables.

    En esta primera versión, el recall es la métrica principal
    utilizada para supervisar la capacidad del modelo para
    identificar correctamente los casos positivos.

    Args:
        metrics: Diccionario con las métricas del modelo.

    Returns:
        Lista con los resultados de las alertas generadas.

    Raises:
        TypeError: Si metrics no es un diccionario.
        KeyError: Si el diccionario no contiene la métrica recall.
    """

    if not isinstance(metrics, dict):
        raise TypeError("Las métricas deben proporcionarse en un diccionario.")

    if "recall" not in metrics:
        raise KeyError("No se encontró la métrica 'recall'.")

    recall_alert = evaluate_recall_alert(metrics["recall"])

    return [recall_alert]


# ==========================================================
# Prueba independiente del módulo
# ==========================================================

if __name__ == "__main__":

    test_metrics = {
        "accuracy": 0.9737,
        "precision": 1.0000,
        "recall": 0.9286,
        "f1_score": 0.9630
    }

    alerts = evaluate_model_alerts(test_metrics)

    print("\nEvaluación de alertas finalizada.\n")

    for alert in alerts:
        print(f"Métrica: {alert['metric']}")
        print(f"Valor: {alert['value']:.4f}")
        print(f"Nivel: {alert['level']}")
        print(f"Mensaje: {alert['message']}")