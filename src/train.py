"""
==========================================================
Módulo: train.py
Proyecto: FASE 3 - Actividad 8
Autor: Jonathan Bernal Sánchez
Descripción:
    Entrena un modelo de Machine Learning utilizando el
    dataset Breast Cancer Wisconsin. Además registra los
    parámetros, métricas y el modelo entrenado en MLflow.

    Gestión de Proyectos de Inteligencia Artificial

==========================================================
"""

# ==========================================================
# Importación de librerías
# ==========================================================

import pandas as pd
import mlflow
import mlflow.sklearn
import joblib


from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)

# ==========================================================
# Configuración de rutas
# ==========================================================

DATASET_PATH = "data/breast_cancer.csv"

# ==========================================================
# Carga del dataset
# ==========================================================

def load_data(dataset_path: str) -> pd.DataFrame:
    """
    Carga el dataset desde un archivo CSV.

    Args:
        dataset_path: Ruta del archivo CSV.

    Returns:
        DataFrame con los datos cargados.
    """
    data = pd.read_csv(dataset_path)
    return data

# ==========================================================
# Preparación de los datos
# ==========================================================

def prepare_data(data: pd.DataFrame):
    """
    Separa las variables predictoras y la variable objetivo,
    además divide el dataset en entrenamiento y prueba.

    Args:
        data: DataFrame con el dataset completo.

    Returns:
        X_train, X_test, y_train, y_test
    """


    X = data.drop(columns=["id", "diagnosis", "Unnamed: 32"])
    y = data["diagnosis"].map({"M": 1, "B": 0})


    return train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

# ==========================================================
# Entrenamiento del modelo
# ==========================================================

def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series
) -> RandomForestClassifier:
    """
    Entrena un modelo Random Forest con los datos de entrenamiento.

    Args:
        X_train: Variables predictoras de entrenamiento.
        y_train: Variable objetivo de entrenamiento.

    Returns:
        Modelo Random Forest entrenado.
    """

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

# Guardar el modelo entrenado
    joblib.dump(model, "models/random_forest_model.pkl")

    return model

# ==========================================================
# Evaluación del modelo
# ==========================================================

def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series
) -> dict:
    """
    Evalúa el modelo con el conjunto de prueba.

    Args:
        model: Modelo entrenado.
        X_test: Variables predictoras de prueba.
        y_test: Variable objetivo de prueba.

    Returns:
        Diccionario con las métricas de evaluación.
    """

    predictions = model.predict(X_test)

    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "precision": precision_score(y_test, predictions),
        "recall": recall_score(y_test, predictions),
        "f1_score": f1_score(y_test, predictions)
    }

    return metrics

# ==========================================================
# Registro del experimento en MLflow
# ==========================================================

def log_experiment(
    model: RandomForestClassifier,
    metrics: dict
) -> None:
    """
    Registra en MLflow los parámetros, métricas y el modelo entrenado.

    Args:
        model: Modelo Random Forest entrenado.
        metrics: Diccionario con las métricas de evaluación.
    """

    mlflow.set_experiment("Breast_Cancer_Monitoring")

    with mlflow.start_run():
        mlflow.log_param("model_type", "RandomForestClassifier")
        mlflow.log_param("n_estimators", model.n_estimators)
        mlflow.log_param("random_state", model.random_state)
        mlflow.log_param("class_weight", model.class_weight)

        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(
            sk_model=model,
            name="random_forest_model"
        )

# ==========================================================
# Flujo principal de entrenamiento
# ==========================================================

def run_training() -> dict:
    """
    Ejecuta el flujo completo de entrenamiento del modelo.

    Returns:
        Diccionario con las métricas obtenidas.
    """

    data = load_data(DATASET_PATH)

    X_train, X_test, y_train, y_test = prepare_data(data)

    model = train_model(X_train, y_train)

    metrics = evaluate_model(model, X_test, y_test)

    log_experiment(model, metrics)

    return metrics

# ==========================================================
# Punto de entrada
# ==========================================================

if __name__ == "__main__":

    metrics = run_training()

    print("\nEntrenamiento finalizado correctamente.\n")

    print("Métricas obtenidas:")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.4f}")

