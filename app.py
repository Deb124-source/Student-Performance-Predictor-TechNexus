import streamlit as st
import pandas as pd

st.set_page_config(page_title="EduPredict | Student Analytics", page_icon="🎓", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
.stApp{background:#0b1020;color:#e8edf8}
[data-testid="stSidebar"]{background:#111a2e;border-right:1px solid #273752}
[data-testid="stSidebar"] *{color:#e8edf8}
.hero{background:linear-gradient(120deg,#172b4d,#173c59,#21445a);border:1px solid #31536d;border-radius:22px;padding:28px 30px;margin-bottom:22px}
.eyebrow{color:#7dd3fc;font-size:12px;font-weight:700;letter-spacing:2px;text-transform:uppercase}
.hero h1{font-family:Manrope,sans-serif;color:#f8fbff;font-size:34px;margin:8px 0}
.hero p,.muted{color:#9aabc5;font-size:14px}
.metric{background:#131e33;border:1px solid #273752;border-radius:16px;padding:18px;min-height:108px}
.label{color:#91a4c2;font-size:12px;font-weight:700;letter-spacing:.8px;text-transform:uppercase}
.value{color:#f4f7fc;font-family:Manrope,sans-serif;font-size:29px;font-weight:800;margin-top:8px}
.note{color:#6ee7b7;font-size:12px}
.panel{background:#131e33;border:1px solid #273752;border-radius:16px;padding:20px;margin-bottom:14px}
.pill{display:inline-block;border:1px solid #31516b;background:#142b40;color:#8ed9f8;padding:5px 10px;border-radius:999px;font-size:11px;font-weight:700}
div.stButton>button{background:linear-gradient(90deg,#0ea5e9,#2563eb);color:white;border:0;border-radius:10px;font-weight:700}
footer{visibility:hidden}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🎓 EduPredict")
    st.caption("STUDENT ANALYTICS PLATFORM")
    st.divider()
    page = st.radio("NAVIGATION", ["Overview", "Performance Prediction", "Student Insights", "About"])
    st.divider()
    st.markdown('<span class="pill">FRONTEND PROTOTYPE</span>', unsafe_allow_html=True)
    st.caption("No model or database is connected.")

st.markdown("""
<div class="hero">
<div class="eyebrow">Education analytics · Student success</div>
<h1>Student Performance Dashboard</h1>
<p>Explore academic indicators, review student trends, and preview a pass/fail assessment workflow.</p>
</div>
""", unsafe_allow_html=True)

def metric(label, value, note):
    st.markdown(f'<div class="metric"><div class="label">{label}</div><div class="value">{value}</div><div class="note">{note}</div></div>', unsafe_allow_html=True)

if page == "Overview":
    st.subheader("Academic snapshot")
    cols = st.columns(4)
    for col, vals in zip(cols, [
        ("Students analysed","2,400","Illustrative sample"),
        ("Average attendance","82.4%","Demo indicator"),
        ("Average study time","5.8 hrs","Per week · demo"),
        ("Pass rate","68.1%","Demo distribution")
    ]):
        with col: metric(*vals)
    left, right = st.columns([1.3,1])
    with left:
        st.markdown('<div class="panel"><b>Performance distribution</b><p class="muted">Illustrative grade bands</p></div>', unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"Students":[180,520,740,650,310]},index=["Below 40","40–59","60–74","75–89","90+"]), color="#38bdf8")
    with right:
        st.markdown('<div class="panel"><b>Key performance factors</b><p class="muted">Example indicator scores</p></div>', unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"Score":[82,66,71,76,69]},index=["Attendance","Study hours","Previous grades","Assignments","Internal assessment"]), color="#34d399")
    st.info("All dashboard numbers and charts are sample values, not results from a connected dataset or trained model.")

elif page == "Performance Prediction":
    st.subheader("Student assessment")
    st.markdown('<p class="muted">Enter academic indicators to preview the interface. This frontend-only version does not run machine learning.</p>', unsafe_allow_html=True)
    with st.form("assessment"):
        c1,c2 = st.columns(2)
        with c1:
            attendance = st.slider("Attendance (%)",0,100,85)
            study = st.slider("Study hours per week",0.0,30.0,8.0,0.5)
            previous = st.slider("Previous grade (%)",0,100,68)
        with c2:
            assignment = st.slider("Assignment completion (%)",0,100,80)
            internal = st.slider("Internal assessment (%)",0,100,72)
            student_id = st.text_input("Student reference (optional)",placeholder="e.g. STU-001")
        submitted = st.form_submit_button("Preview assessment",use_container_width=True)
    if submitted:
        st.warning("Demo-only: no trained model is connected. These probability values are placeholders, not a real prediction.")
        a,b = st.columns(2)
        with a:
            metric("Illustrative pass probability","72%","Sample display only")
            st.progress(0.72)
        with b:
            metric("Illustrative fail probability","28%","Sample display only")
            st.progress(0.28)
        st.markdown("**Entered student indicators**")
        st.dataframe(pd.DataFrame({
            "Indicator":["Attendance","Study hours / week","Previous grade","Assignment completion","Internal assessment"],
            "Entered value":[f"{attendance}%",f"{study:.1f} hours",f"{previous}%",f"{assignment}%",f"{internal}%"]
        }),hide_index=True,use_container_width=True)
        if student_id.strip(): st.caption(f"Reference: {student_id.strip()}")

elif page == "Student Insights":
    st.subheader("Student insights")
    st.markdown('<p class="muted">Example records for demonstrating filters, tables, and charts.</p>',unsafe_allow_html=True)
    data = pd.DataFrame({
        "Student ID":["STU-001","STU-002","STU-003","STU-004","STU-005","STU-006"],
        "Attendance":[92,68,85,74,96,59],
        "Study hours":[9.5,3.0,7.0,4.5,11.0,2.5],
        "Previous grade":[88,45,72,61,91,38],
        "Status (demo)":["Pass","At risk","Pass","At risk","Pass","At risk"]
    })
    chosen = st.multiselect("Filter by demo status",["Pass","At risk"],default=["Pass","At risk"])
    filtered = data[data["Status (demo)"].isin(chosen)]
    st.dataframe(filtered,hide_index=True,use_container_width=True)
    st.subheader("Attendance overview")
    st.bar_chart(data.set_index("Student ID")[["Attendance"]],color="#38bdf8")
    st.caption("These records are fictional examples.")

else:
    st.subheader("About this application")
    st.markdown("""
    <div class="panel">
    <h3 style="color:#f3f6fc">Student Performance Prediction</h3>
    <p class="muted">An Education Analytics interface concept for reviewing attendance, study hours, and academic records.</p>
    <span class="pill">FRONTEND ONLY</span><br><br>
    <b>Included screens</b>
    <ul class="muted"><li>Overview dashboard with KPI cards and charts</li><li>Student assessment form</li><li>Illustrative pass/fail probability display</li><li>Student insights table and filters</li></ul>
    <b>Not included</b>
    <ul class="muted"><li>Model loading or prediction logic</li><li>Database, authentication, or API integration</li><li>Real student data or real prediction results</li></ul>
    </div>""",unsafe_allow_html=True)

st.divider()
st.caption("EduPredict · Student Performance Prediction · Frontend prototype only")
