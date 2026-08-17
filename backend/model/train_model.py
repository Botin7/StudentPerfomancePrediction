import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Added the new classifiers here
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

# =====================================================
# Load Dataset
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "StudentPerformance.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset Loaded Successfully!")
print(df.head())

# =====================================================
# Remove Student_ID
# =====================================================

df = df.drop(columns=["Student_ID"])

# =====================================================
# Features & Target
# =====================================================

X = df.drop("Grade", axis=1)
y = df["Grade"]

# =====================================================
# Detect Data Types
# =====================================================

categorical_features = X.select_dtypes(include=["object", "string"]).columns.tolist()
numerical_features = X.select_dtypes(exclude=["object", "string"]).columns.tolist()

print("\nCategorical Features:")
print(categorical_features)

print("\nNumerical Features:")
print(numerical_features)

# =====================================================
# Preprocessing
# =====================================================

numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ]
)

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numerical_features),
        ("cat", categorical_transformer, categorical_features)
    ]
)

# =====================================================
# Split Dataset
# =====================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================================
# Create Models (Updated with Decision Tree & SVM)
# =====================================================

models = {
    "random_forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    ),
    "logistic_regression": LogisticRegression(
        max_iter=1000
    ),
    "decision_tree": DecisionTreeClassifier(
        random_state=42
    ),
    "svm": SVC(
        kernel="linear", 
        random_state=42
    )
}

# =====================================================
# Create models folder
# =====================================================

MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

# =====================================================
# Train Models
# =====================================================

for model_name, classifier in models.items():

    print("\n" + "=" * 50)
    print(f"Training {model_name}")
    print("=" * 50)

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )
    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )
    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print(f"\nAccuracy : {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall   : {recall:.4f}")
    print(f"F1 Score : {f1:.4f}")

    print("\nClassification Report")
    print(classification_report(y_test, predictions, zero_division=0))

    model_path = MODEL_DIR / f"{model_name}.pkl"

    joblib.dump(pipeline, model_path)

    print(f"\nSaved Model -> {model_path}")

print("\n")
print("=" * 60)
print("Training Completed Successfully!")
print("=" * 60)