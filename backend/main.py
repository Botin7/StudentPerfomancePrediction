from pathlib import Path
import shutil
import traceback

import pandas as pd
import numpy as np

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException,
    Query
)

from fastapi.responses import (
    FileResponse,
    JSONResponse
)

from fastapi.middleware.cors import CORSMiddleware

from services.predict_service import predict_uploaded

from services.analytics_service import (
    load_model,
    evaluate_model,
    compare_models
)


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Student Performance Prediction API"
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

TEMPLATE_PATH = (
    BASE_DIR
    / "data"
    / "StudentPerformance.csv"
)

UPLOADS_DIR = BASE_DIR / "uploads"


# =========================================================
# LOAD TEST DATA
# =========================================================

def load_test_data():

    test_path = (
        BASE_DIR
        / "data"
        / "StudentPerformance.csv"
    )

    if not test_path.exists():

        test_path = (
            BASE_DIR
            / "test_data.csv"
        )

    if not test_path.exists():

        test_path = (
            UPLOADS_DIR
            / "latest.csv"
        )

    if not test_path.exists():

        raise HTTPException(
            status_code=404,
            detail="No evaluation dataset found."
        )

    df = pd.read_csv(test_path)

    if "Grade" not in df.columns:

        raise HTTPException(
            status_code=400,
            detail="Dataset missing required target column 'Grade'."
        )

    X_test = df.drop(
        columns=[
            "Grade",
            "Student_ID"
        ],
        errors="ignore"
    )

    y_test = df["Grade"]

    return X_test, y_test


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def read_root():

    return {
        "message": "Backend running"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# =========================================================
# DOWNLOAD TEMPLATE
# =========================================================

@app.get("/template")
def get_template():

    if not TEMPLATE_PATH.exists():

        return JSONResponse(
            {
                "error": "Template not found"
            },
            status_code=404
        )

    return FileResponse(
        str(TEMPLATE_PATH),
        media_type="text/csv",
        filename=TEMPLATE_PATH.name
    )


# =========================================================
# UPLOAD CSV
# =========================================================

@app.post("/upload")
async def upload_csv(
    file: UploadFile = File(...)
):

    UPLOADS_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    if not file.filename.lower().endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed."
        )

    dest = (
        UPLOADS_DIR
        / file.filename
    )

    latest = (
        UPLOADS_DIR
        / "latest.csv"
    )

    with open(
        dest,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    shutil.copy2(
        dest,
        latest
    )

    return {
        "status": "ok",
        "filename": file.filename
    }


# =========================================================
# PREDICT
# =========================================================

@app.post("/predict")
async def predict(
    model_name: str = Query(
        "random_forest"
    )
):

    latest_csv = (
        UPLOADS_DIR
        / "latest.csv"
    )

    if not latest_csv.exists():

        raise HTTPException(
            status_code=400,
            detail="No CSV file uploaded yet."
        )

    try:

        df = pd.read_csv(
            latest_csv
        )

        predictions = predict_uploaded(
            model_name,
            df
        )

        return {
            "status": "success",
            "model": model_name,
            "predictions": predictions.tolist()
        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


# =========================================================
# METRICS
# =========================================================

@app.get("/metrics")
def get_metrics(
    algorithm: str = Query(
        "random_forest"
    )
):

    try:

        X_test, y_test = load_test_data()

        results = evaluate_model(
            algorithm,
            X_test,
            y_test
        )

        metrics = {
            "accuracy": results["accuracy"],
            "precision": results["precision"],
            "recall": results["recall"],
            "f1_score": results["f1_score"]
        }

        return {
            "status": "success",
            "algorithm": algorithm,
            "metrics": metrics
        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Metrics failed: {str(e)}"
        )


# =========================================================
# SUMMARY
# =========================================================

@app.get("/summary")
def get_summary(
    algorithm: str = Query(
        "random_forest"
    )
):

    try:

        X_test, y_test = load_test_data()

        return {
            "status": "success",
            "algorithm": algorithm,
            "students": int(len(y_test)),
            "features": int(len(X_test.columns))
        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Summary failed: {str(e)}"
        )


# =========================================================
# CHARTS
# =========================================================

@app.get("/charts")
def get_charts(
    algorithm: str = Query("random_forest")
):
    try:
        test_path = BASE_DIR / "data" / "StudentPerformance.csv"

        if not test_path.exists():
            test_path = UPLOADS_DIR / "latest.csv"

        if not test_path.exists():
            raise HTTPException(
                status_code=400,
                detail="No dataset available."
            )

        df = pd.read_csv(test_path)

        model = load_model(algorithm)

        X = df.drop(
            columns=["Grade", "Student_ID"],
            errors="ignore"
        )

        predictions = model.predict(X)

        grade_counts = pd.Series(
            predictions
        ).value_counts().to_dict()

        return {
            "status": "success",
            "algorithm": algorithm,
            "grades": grade_counts
        }

    except Exception as e:
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Chart generation failed: {str(e)}"
        )

# =========================================================
# COMPARE MODELS
# =========================================================

@app.get("/compare")
def compare_models_endpoint():

    try:

        X_test, y_test = load_test_data()

        results = compare_models(
            X_test,
            y_test
        )

        return {
            "status": "success",
            "results": results
        }

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Model comparison failed: {str(e)}"
        )


# =========================================================
# AT-RISK STUDENTS
# =========================================================

@app.get("/at_risk")
def get_at_risk(
    algorithm: str = Query("random_forest"),
    threshold: float = Query(50)
):
    try:
        # -----------------------------------------
        # Find dataset
        # -----------------------------------------
        test_path = BASE_DIR / "data" / "StudentPerformance.csv"

        if not test_path.exists():
            test_path = BASE_DIR / "test_data.csv"

        if not test_path.exists():
            test_path = UPLOADS_DIR / "latest.csv"

        if not test_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Student dataset not found."
            )

        df = pd.read_csv(test_path)

        if df.empty:
            return {
                "status": "success",
                "algorithm": algorithm,
                "threshold": threshold,
                "total_students": 0,
                "at_risk_count": 0,
                "at_risk_percentage": 0,
                "students": []
            }

        # -----------------------------------------
        # Load model
        # -----------------------------------------
        model = load_model(algorithm)

        # -----------------------------------------
        # Prepare features
        # -----------------------------------------
        X_test = df.drop(
            columns=["Grade", "Student_ID"],
            errors="ignore"
        )

        # -----------------------------------------
        # Predict
        # -----------------------------------------
        y_pred = model.predict(X_test)

        # -----------------------------------------
        # Build result
        # -----------------------------------------
        result = df.copy()

        result["predicted_grade"] = y_pred

        students = []

        for index, row in result.iterrows():

            predicted = row["predicted_grade"]

            actual = row["Grade"] if "Grade" in row else None

            risk_reasons = []

            # -------------------------------------
            # Numeric prediction
            # -------------------------------------
            try:

                predicted_numeric = float(predicted)

                if predicted_numeric < threshold:

                    risk_reasons.append(
                        f"Predicted grade below {threshold}"
                    )

            except (ValueError, TypeError):

                # ---------------------------------
                # Categorical prediction
                # ---------------------------------
                if str(predicted).upper() in ["D", "F"]:

                    risk_reasons.append(
                        "Predicted grade is D or F"
                    )

            # -------------------------------------
            # Absences
            # -------------------------------------
            if "absences" in row:

                try:

                    absences = float(
                        row["absences"]
                    )

                    if absences > 10:

                        risk_reasons.append(
                            "High number of absences"
                        )

                except (ValueError, TypeError):
                    pass

            # -------------------------------------
            # Previous failures
            # -------------------------------------
            if "failures" in row:

                try:

                    failures = float(
                        row["failures"]
                    )

                    if failures > 0:

                        risk_reasons.append(
                            "Previous class failures"
                        )

                except (ValueError, TypeError):
                    pass

            # -------------------------------------
            # Add student if at risk
            # -------------------------------------
            if risk_reasons:

                student_id = row.get(
                    "Student_ID",
                    index + 1
                )

                students.append({
                    "Student_ID": str(student_id),

                    "Predicted_Grade":
                        predicted.item()
                        if hasattr(predicted, "item")
                        else predicted,

                    "Actual_Grade":
                        actual.item()
                        if hasattr(actual, "item")
                        else actual,

                    "risk_reasons":
                        risk_reasons
                })

        # -----------------------------------------
        # Percentage
        # -----------------------------------------
        total_students = len(result)

        at_risk_count = len(students)

        percentage = (
            round(
                (at_risk_count / total_students) * 100,
                1
            )
            if total_students > 0
            else 0
        )

        # -----------------------------------------
        # Response
        # -----------------------------------------
        return {
            "status": "success",
            "algorithm": algorithm,
            "threshold": threshold,

            "total_students":
                total_students,

            "at_risk_count":
                at_risk_count,

            "at_risk_percentage":
                percentage,

            "students":
                students
        }

    except HTTPException:
        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"At-risk analysis failed: {str(e)}"
        )


# =========================================================
# STUDENT LOOKUP
# =========================================================

@app.get("/student")
def get_student(
    student_id: str = Query(...),
    algorithm: str = Query("random_forest")
):
    try:
        # -----------------------------------------
        # Find dataset
        # -----------------------------------------

        test_path = BASE_DIR / "data" / "StudentPerformance.csv"

        if not test_path.exists():
            test_path = BASE_DIR / "test_data.csv"

        if not test_path.exists():
            test_path = UPLOADS_DIR / "latest.csv"

        if not test_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Student dataset not found."
            )

        df = pd.read_csv(test_path)

        # -----------------------------------------
        # Check Student_ID column
        # -----------------------------------------

        if "Student_ID" not in df.columns:
            raise HTTPException(
                status_code=400,
                detail="Dataset does not contain Student_ID column."
            )

        # -----------------------------------------
        # Find student
        # -----------------------------------------

        student = df[
            df["Student_ID"].astype(str) == str(student_id)
        ]

        if student.empty:
            raise HTTPException(
                status_code=404,
                detail=f"Student ID '{student_id}' not found in Dataset."
            )

        # -----------------------------------------
        # Load selected model
        # -----------------------------------------

        model = load_model(algorithm)

        # -----------------------------------------
        # Prepare student features
        # -----------------------------------------

        X_student = student.drop(
            columns=["Student_ID", "Grade"],
            errors="ignore"
        )

        # -----------------------------------------
        # Predict
        # -----------------------------------------

        prediction = model.predict(X_student)[0]

        # -----------------------------------------
        # Actual grade
        # -----------------------------------------

        actual_grade = None

        if "Grade" in student.columns:
            actual_grade = student.iloc[0]["Grade"]

        # -----------------------------------------
        # Risk reasons
        # -----------------------------------------

        risk_reasons = []

        # If prediction is numeric
        try:

            numeric_prediction = float(prediction)

            if numeric_prediction < 50:
                risk_reasons.append(
                    "Predicted grade is below 50"
                )

        except (ValueError, TypeError):

            # If prediction is categorical
            if str(prediction).upper() in ["D", "F"]:
                risk_reasons.append(
                    "Predicted grade indicates academic risk"
                )

        # Check absences
        if "absences" in student.columns:

            try:

                absences = float(
                    student.iloc[0]["absences"]
                )

                if absences > 10:
                    risk_reasons.append(
                        "High number of absences"
                    )

            except (ValueError, TypeError):
                pass

        # Check failures
        if "failures" in student.columns:

            try:

                failures = float(
                    student.iloc[0]["failures"]
                )

                if failures > 0:
                    risk_reasons.append(
                        "Previous class failures"
                    )

            except (ValueError, TypeError):
                pass

        if not risk_reasons:
            risk_reasons.append(
                "No major risk factors detected"
            )

        # -----------------------------------------
        # Return result
        # -----------------------------------------

        return {
            "status": "success",
            "algorithm": algorithm,
            "Student_ID": str(student_id),
            "Predicted_Grade": prediction.item()
                if hasattr(prediction, "item")
                else prediction,
            "Grade": actual_grade.item()
                if hasattr(actual_grade, "item")
                else actual_grade,
            "risk_reasons": risk_reasons
        }

    except HTTPException:
        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Student lookup failed: {str(e)}"
        )


# =========================================================
# FEATURE IMPORTANCE
# =========================================================

@app.get("/feature_importance")
def get_feature_importance(
    algorithm: str = Query(
        "random_forest"
    )
):

    try:

        model = load_model(
            algorithm
        )

        # =====================================
        # GET CLASSIFIER
        # =====================================

        if hasattr(
            model,
            "named_steps"
        ):

            classifier = model.named_steps.get(
                "classifier"
            )

            preprocessor = model.named_steps.get(
                "preprocessor"
            )

        else:

            classifier = model
            preprocessor = None


        # =====================================
        # TREE MODELS
        # =====================================

        if hasattr(
            classifier,
            "feature_importances_"
        ):

            importances = (
                classifier
                .feature_importances_
            )

        else:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Feature importance is "
                    "only available for "
                    "tree-based models."
                )
            )


        # =====================================
        # FEATURE NAMES
        # =====================================

        if preprocessor is not None:

            try:

                feature_names = (
                    preprocessor
                    .get_feature_names_out()
                )

            except Exception:

                feature_names = [
                    f"feature_{i}"
                    for i in range(
                        len(importances)
                    )
                ]

        else:

            feature_names = [
                f"feature_{i}"
                for i in range(
                    len(importances)
                )
            ]


        # =====================================
        # CREATE RESULT
        # =====================================

        features = []

        for name, importance in zip(
            feature_names,
            importances
        ):

            features.append(
                {
                    "feature": str(name),
                    "importance": float(
                        importance
                    )
                }
            )


        # Highest first
        features.sort(
            key=lambda x: x["importance"],
            reverse=True
        )

        return {
            "status": "success",
            "algorithm": algorithm,
            "features": features
        }

    except HTTPException:
        raise

    except Exception as e:

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Feature importance failed: {str(e)}"
        )


# =========================================================
# STARTUP MESSAGE
# =========================================================

@app.on_event("startup")
async def startup_event():

    print(
        "\n===================================="
    )

    print(
        "Student Performance API Started"
    )

    print(
        "===================================="
    )
@app.get("/download")
def download_result():

    latest_csv = UPLOADS_DIR / "latest.csv"

    if not latest_csv.exists():

        raise HTTPException(
            status_code=404,
            detail="No prediction result available."
        )

    return FileResponse(
        str(latest_csv),
        media_type="text/csv",
        filename="prediction_result.csv"
    )

