"""
==========================================================
Módulo: drift.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Detecta posibles cambios (Data Drift) entre los datos
    utilizados para entrenar el modelo y nuevos datos de
    entrada mediante una comparación estadística.

Materia:
    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Importación de librerías
# ==========================================================

import pandas as pd
from scipy.stats import ks_2samp

from src.logger import logger


# ==========================================================
# Detector de Data Drift
# ==========================================================

class DriftDetector:
    """
    Detecta cambios estadísticos entre dos conjuntos de datos.
    """

    def __init__(self, alpha: float = 0.05):
        self.alpha = alpha

    def detect_drift(
        self,
        reference_data: pd.DataFrame,
        current_data: pd.DataFrame
    ) -> dict:
        """
        Evalúa si existe deriva de datos mediante la prueba
        Kolmogorov-Smirnov.

        Args:
            reference_data: Datos utilizados durante el entrenamiento.
            current_data: Datos actuales.

        Returns:
            Diccionario con el resultado de la evaluación.
        """

        drift_detected = False
        evaluated_features = 0

        for column in reference_data.columns:

            if not pd.api.types.is_numeric_dtype(reference_data[column]):
                continue

            statistic, p_value = ks_2samp(
                reference_data[column],
                current_data[column]
            )

            evaluated_features += 1

            if p_value < self.alpha:
                drift_detected = True

                logger.warning(
                    "Data Drift detectado en '%s' (p-value=%.5f)",
                    column,
                    p_value
                )

        if drift_detected:
            status = "WARNING"
            message = "Se detectó posible Data Drift."
        else:
            status = "INFO"
            message = "No se detectó Data Drift."

        logger.info(message)

        return {
            "status": status,
            "drift_detected": drift_detected,
            "variables_evaluadas": evaluated_features
        }


# ==========================================================
# Prueba independiente
# ==========================================================

if __name__ == "__main__":

    reference = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [10, 20, 30, 40, 50]
    })

    current = pd.DataFrame({
        "A": [1, 2, 3, 4, 5],
        "B": [11, 19, 32, 38, 49]
    })

    detector = DriftDetector()

    result = detector.detect_drift(reference, current)

    print(result)

    