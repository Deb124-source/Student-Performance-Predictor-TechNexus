"""
Train and compare Decision Tree and Random Forest models.
Default input: data/student_performance_demo.csv (synthetic demonstration data).
For real use, replace the CSV with properly collected, consented school data
having the same feature columns and a pass column (1=Pass, 0=Fail).
"""
from pathlib import Path
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "student_performance_demo.csv"
FEATURES = [
    "attendance_pct", "study_hours_per_week", "previous_grade_pct",
    "assignment_completion_pct", "internal_assessment_pct"
]
df = pd.read_csv(DATA)
if "pass" not in df.columns:
    raise ValueError("Dataset must contain target column 'pass' (1=Pass, 0=Fail).")
X, y = df[FEATURES], df["pass"].astype(int)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
models = {
    "Decision Tree": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", DecisionTreeClassifier(max_depth=5, min_samples_leaf=8, random_state=42))
    ]),
    "Random Forest": Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("classifier", RandomForestClassifier(
            n_estimators=300, max_depth=10, min_samples_leaf=4,
            class_weight="balanced", random_state=42, n_jobs=-1
        ))
    ])
}
comparison = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    comparison[name] = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred, zero_division=0), 4),
        "recall": round(recall_score(y_test, pred, zero_division=0), 4),
        "f1_score": round(f1_score(y_test, pred, zero_division=0), 4)
    }
best_name = max(comparison, key=lambda k: comparison[k]["f1_score"])
bundle = {
    "model": models[best_name],
    "features": FEATURES,
    "class_labels": {0: "Fail", 1: "Pass"},
    "dataset_note": "Update this field if training on real student records."
}
(ROOT / "models").mkdir(exist_ok=True)
joblib.dump(bundle, ROOT / "models" / "student_performance_model.pkl")
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports" / "model_metrics.json").write_text(json.dumps({
    "best_model_by_f1": best_name, "model_comparison": comparison
}, indent=2))
print("Best model:", best_name)
print(json.dumps(comparison, indent=2))
print("Saved: models/student_performance_model.pkl")
