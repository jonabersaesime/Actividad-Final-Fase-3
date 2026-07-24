"""
==========================================================
Módulo: monitor.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Supervisa el desempeño del modelo de Machine Learning.
    Recibe las métricas generadas durante el entrenamiento,
    ejecuta las reglas de alerta y registra el estado del
    modelo en el sistema de logs.


    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Importación de módulos internos
# ==========================================================

from src.logger import logger
from src.alerts import evaluate_model_alerts


# ==========================================================
# Monitor del modelo
# ==========================================================

class ModelMonitor:
    """
    Clase responsable de supervisar el desempeño del modelo.
    """

    def __init__(self) -> None:
        logger.info("Monitor de IA inicializado.")

    def monitor(self, metrics: dict) -> list[dict]:
        """
        Ejecuta el monitoreo del modelo.

        Args:
            metrics:
                Diccionario con las métricas del modelo.

        Returns:
            Lista con las alertas generadas.
        """

        logger.info("Iniciando evaluación de métricas.")

        alerts = evaluate_model_alerts(metrics)

        logger.info(
            "Proceso de monitoreo finalizado correctamente."
        )

        return alerts


# ==========================================================
# Prueba independiente
# ==========================================================

if __name__ == "__main__":

    test_metrics = {
        "accuracy": 0.9737,
        "precision": 1.0000,
        "recall": 0.9286,
        "f1_score": 0.9630
    }

    monitor = ModelMonitor()

    alerts = monitor.monitor(test_metrics)

    print("\nResultado del monitoreo\n")

    for alert in alerts:
        print(alert)