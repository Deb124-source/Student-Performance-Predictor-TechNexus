 # Student Performance Prediction — Education Analytics

## What is included
- `models/student_performance_model.pkl` — trained Random Forest/Decision Tree pipeline selected by F1 score.
- `train_model.py` — cleans missing feature values with median imputation, trains both classifiers, compares metrics, and saves the best model.
- `predict.py` — example pass/fail probability prediction.
- `data/student_performance_demo.csv` — reproducible **synthetic demonstration data**.
- `reports/model_metrics.json` and `reports/model_comparison.csv` — evaluation results.

## Important dataset limitation
No school dataset was supplied with the request. The included model is trained on generated synthetic demonstration records, **not real student records**. The metrics are only a software demonstration and do not establish real-world accuracy. Do not use this model to make decisions about actual students.

The original brief mentions attendance, study hours and academic records. The model uses:
- `attendance_pct` — attendance percentage
- `study_hours_per_week` — weekly study hours
- `previous_grade_pct` — previous academic grade
- `assignment_completion_pct` — assignment completion percentage
- `internal_assessment_pct` — internal assessment score

The original brief does not specify a pass mark or grading scale. This demo defines the target in its synthetic data generator. For a real deployment, define the pass threshold with the school and train/evaluate using that school's historical data.

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

## Training with real academic data
Replace `data/student_performance_demo.csv` with a properly collected dataset containing the five feature columns above and a `pass` target column (1=pass, 0=fail). Keep records anonymized, obtain appropriate permission, and evaluate on a held-out set from the intended student population before relying on predictions. Check for bias and data leakage.

## Model comparison
See `reports/model_metrics.json`. Random Forest and Decision Tree are compared using accuracy, precision, recall and F1 score. The saved model is selected by F1 score on a held-out test split.

## Data source note
The downloadable model here is deliberately self-contained and uses synthetic demo data. A public UCI Student Performance dataset exists, but its columns are not identical to this brief: it records weekly study-time categories and absences, and grade fields; it does not provide a direct attendance percentage or weekly study hours as continuous values. See the UCI repository before adapting the project: https://archive.ics.uci.edu/dataset/320/student+performance
