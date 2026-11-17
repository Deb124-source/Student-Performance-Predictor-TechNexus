 # Student Performance Prediction — Education Analytics

 ## Live Website :
 https://student-performance-predictor-technexus.streamlit.app/
 

## What is included
- `models/student_performance_model.pkl` — trained Random Forest/Decision Tree pipeline selected by F1 score.
- `train_model.py` — cleans missing feature values with median imputation, trains both classifiers, compares metrics, and saves the best model.
- `predict.py` — example pass/fail probability prediction.
- `data/student_performance_demo.csv` — reproducible **synthetic demonstration data**.
- `reports/model_metrics.json` and `reports/model_comparison.csv` — evaluation results.


The original brief mentions attendance, study hours and academic records. The model uses:
- `attendance_pct` — attendance percentage
- `study_hours_per_week` — weekly study hours
- `previous_grade_pct` — previous academic grade
- `assignment_completion_pct` — assignment completion percentage
- `internal_assessment_pct` — internal assessment score


## Setup
Python 3.10+ recommended.

```bash
pip install -r requirements.txt
python train_model.py
python predict.py
```

## Use the model in your own Python file
```python
import joblib
import pandas as pd

bundle = joblib.load("models/student_performance_model.pkl")
model = bundle["model"]
features = bundle["features"]

student = pd.DataFrame([{
    "attendance_pct": 85,
    "study_hours_per_week": 8,
    "previous_grade_pct": 68,
    "assignment_completion_pct": 80,
    "internal_assessment_pct": 72
}])[features]

p_fail, p_pass = model.predict_proba(student)[0]
print(f"Fail: {p_fail:.1%}")
print(f"Pass: {p_pass:.1%}")
```

## Model comparison
See `reports/model_metrics.json`. Random Forest and Decision Tree are compared using accuracy, precision, recall and F1 score. The saved model is selected by F1 score on a held-out test split.
