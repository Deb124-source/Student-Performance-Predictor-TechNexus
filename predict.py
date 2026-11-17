"""Load the trained model and predict pass/fail probabilities."""
from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent
bundle = joblib.load(ROOT / "models" / "student_performance_model.pkl")
model = bundle["model"]
features = bundle["features"]

# Edit these example values for the student you want to assess.
student = pd.DataFrame([{
    "attendance_pct": 85,
    "study_hours_per_week": 8,
    "previous_grade_pct": 68,
    "assignment_completion_pct": 80,
    "internal_assessment_pct": 72
}])[features]

probabilities = model.predict_proba(student)[0]
predicted_class = int(model.predict(student)[0])
labels = bundle.get("class_labels", {0: "Fail", 1: "Pass"})

print("Prediction:", labels[predicted_class])
print(f"Fail probability: {probabilities[0] * 100:.2f}%")
print(f"Pass probability: {probabilities[1] * 100:.2f}%")
