"""
==========================================================
Archivo: main.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez

Descripción:
    Punto de entrada principal del sistema de observabilidad.
    Ejecuta el entrenamiento, monitorea el modelo, genera
    alertas y muestra el runbook correspondiente.

    Gestión de Proyectos de Inteligencia Artificial
==========================================================
"""

# ==========================================================
# Importación de módulos
# ==========================================================

import pandas as pd
from src.train import run_training
from src.monitor import ModelMonitor
from src.runbooks import get_runbook
from src.drift import DriftDetector


# ==========================================================
# Programa principal
# ==========================================================

def main() -> None:
    """
    Ejecuta el flujo completo del sistema.
    """

    print("\n==========================================")
    print(" SISTEMA DE OBSERVABILIDAD PARA MODELOS IA")
    print("==========================================\n")

    # Entrenamiento
    metrics = run_training()

    # Monitoreo
    monitor = ModelMonitor()
    alerts = monitor.monitor(metrics)

    # Detección de Data Drift
    reference_data = pd.read_csv("data/breast_cancer.csv")
    current_data = reference_data.copy()

    drift_detector = DriftDetector()
    drift_result = drift_detector.detect_drift(
        reference_data,
        current_data
    )

    # Mostrar resultados
    print("\nMétricas del modelo")
    print("----------------------------")

    for metric, value in metrics.items():
        print(f"{metric:<12}: {value:.4f}")

    print("\nEstado del Data Drift")
    print("----------------------------")
    print(f"Estado             : {drift_result['status']}")
    print(
    f"Drift detectado    : "
    f"{'Sí' if drift_result['drift_detected'] else 'No'}"
    )
    print(
    f"Variables evaluadas: "
    f"{drift_result['variables_evaluadas']}"
  )

    print("\nAlertas")
    print("----------------------------")

    for alert in alerts:

        print(f"\nNivel    : {alert['level']}")
        print(f"Métrica  : {alert['metric']}")
        print(f"Valor    : {alert['value']:.4f}")
        print(f"Mensaje  : {alert['message']}")

        print("\nRunbook recomendado:")

        for step in get_runbook(alert["level"]):
            print(f"  • {step}")


# ==========================================================
# Punto de entrada
# ==========================================================

if __name__ == "__main__":
    main()