from pathlib import Path
import joblib

from services.metrics_service import compute_metrics


# =====================================================
# BASE DIRECTORY
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# LOAD MODEL
# =====================================================

def load_model(name: str):

    model_path = BASE_DIR / "models"

    if name == "random_forest":

        return joblib.load(
            model_path / "random_forest.pkl"
        )

    elif name == "logistic_regression":

        return joblib.load(
            model_path / "logistic_regression.pkl"
        )

    elif name == "decision_tree":

        return joblib.load(
            model_path / "decision_tree.pkl"
        )

    elif name == "svm":

        return joblib.load(
            model_path / "svm.pkl"
        )

    else:

        raise ValueError(
            f"Unknown model name: {name}"
        )


# =====================================================
# EVALUATE MODEL
# =====================================================

def evaluate_model(
    model_name: str,
    X_test,
    y_test
):

    model = load_model(
        model_name
    )

    y_pred = model.predict(
        X_test
    )

    metrics = compute_metrics(
        y_test,
        y_pred
    )

    return {
        "model": model_name,
        **metrics
    }


# =====================================================
# COMPARE ALL MODELS
# =====================================================

def compare_models(
    X_test,
    y_test
):

    models = [
        "random_forest",
        "logistic_regression",
        "decision_tree",
        "svm"
    ]

    results = {}

    for model_name in models:

        results[model_name] = evaluate_model(
            model_name,
            X_test,
            y_test
        )

    return results


# =====================================================
# PREDICT UPLOADED DATA
# =====================================================

def predict_uploaded(
    model_name: str,
    df
):

    model = load_model(
        model_name
    )

    # Remove target column
    if "Grade" in df.columns:

        df = df.drop(
            columns=["Grade"]
        )

    # Remove ID
    if "Student_ID" in df.columns:

        df = df.drop(
            columns=["Student_ID"]
        )

    predictions = model.predict(
        df
    )

    return predictions