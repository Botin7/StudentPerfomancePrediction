import pandas as pd

from services.analytics_service import load_model


def predict_uploaded(
    model_name: str,
    df: pd.DataFrame
):

    model = load_model(
        model_name
    )

    # Remove target
    if "Grade" in df.columns:

        df = df.drop(
            columns=["Grade"]
        )

    # Remove Student ID
    if "Student_ID" in df.columns:

        df = df.drop(
            columns=["Student_ID"]
        )

    predictions = model.predict(
        df
    )

    return predictions