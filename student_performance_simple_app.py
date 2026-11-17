import streamlit as st

st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 Student Performance Prediction")
st.write("Enter the student's academic details to view a simple performance result.")

st.divider()

with st.form("prediction_form"):
    st.subheader("Student Information")

    attendance = st.number_input(
        "Attendance (%)",
        min_value=0.0, max_value=100.0, value=80.0, step=1.0
    )
    study_hours = st.number_input(
        "Study hours per week",
        min_value=0.0, max_value=80.0, value=10.0, step=1.0
    )
    previous_grade = st.number_input(
        "Previous academic grade (%)",
        min_value=0.0, max_value=100.0, value=65.0, step=1.0
    )

    submitted = st.form_submit_button("Predict Performance", use_container_width=True)

if submitted:
    # Simple illustrative rule-based result.
    # This is NOT a prediction from the trained ML model.
    score = (
        attendance * 0.40
        + min(study_hours / 20 * 100, 100) * 0.20
        + previous_grade * 0.40
    )

    st.divider()
    st.subheader("Prediction Result")

    if score >= 50:
        st.success("PASS — Student is likely to pass.")
    else:
        st.error("FAIL — Student may need additional academic support.")

    st.metric("Performance score", f"{score:.1f} / 100")

    if score >= 70:
        st.write("Overall indication: Good performance")
    elif score >= 50:
        st.write("Overall indication: Average performance")
    else:
        st.write("Overall indication: Needs improvement")

    st.caption(
        "Note: This is a simple rule-based demonstration for the frontend. "
        "It does not use the trained Decision Tree or Random Forest model "
        "and should not be used for real academic decisions."
    )
