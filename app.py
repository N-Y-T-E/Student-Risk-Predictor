import streamlit as st
import pandas as pd
import joblib

# 1. Load the pre-trained model engine
try:
    model = joblib.load('student_model.pkl')
except:
    model = None

# 2. Page Configuration & Design
st.set_page_config(page_title="Academic Analytics Portal", page_icon="📊", layout="centered")

# --- HIDE ALL STREAMLIT & GITHUB BRANDING (WITHOUT HIDING SIDEBAR CONTROLS) ---
hide_style = """
    <style>
    /* Hide the main menu (three dots) */
    #MainMenu {visibility: hidden !important;}
    
    /* Hide the footer */
    footer {visibility: hidden !important;}
    
    /* Hide the deploy button */
    .stAppDeployButton {display: none !important;}
    
    /* Hide the header colorful line decoration */
    [data-testid="stDecoration"] {display: none !important;}
    
    /* Hide the standard header background but keep the container so the sidebar toggle arrow works */
    [data-testid="stHeader"] {
        background-color: rgba(0,0,0,0) !important;
        background-image: none !important;
    }
    </style>
"""
st.markdown(hide_style, unsafe_allow_html=True)

# JavaScript to catch the stubborn floating badge in the bottom-right corner
from streamlit.components.v1 import html
html("""
<script>
    const hideBadges = () => {
        window.top.document.querySelectorAll('a[href*="streamlit.io"]').forEach(el => {
            el.style.display = 'none';
        });
        window.top.document.querySelectorAll('[data-testid="stStatusWidget"]').forEach(el => {
            el.style.display = 'none';
        });
        window.top.document.querySelectorAll('.viewerBadge').forEach(el => {
            el.style.display = 'none';
        });
    };
    hideBadges();
    setInterval(hideBadges, 500);
</script>
""", height=0)
# -------------------------------------------------------------------------------
    

    hideBadges();
    setInterval(hideBadges, 500);
</script>
""", height=0)
# --------------------------------------------

st.title("🏫 Academic Performance Analytics Portal")
st.markdown("""
This system uses predictive modeling to analyze student performance metrics 
and identify early indicators for academic intervention.
""")
st.markdown("---")

# 3. Sidebar / Input Panel for Student Metrics
st.sidebar.header("📥 Student Data Input Panel")

attendance = st.sidebar.slider("Current Attendance (%)", min_value=0, max_value=100, value=85, step=1)
study_hours = st.sidebar.slider("Weekly Study Hours", min_value=0, max_value=40, value=12, step=1)
mid_term = st.sidebar.slider("Mid-Term Examination Score", min_value=0, max_value=100, value=75, step=1)
internet = st.sidebar.selectbox("Home Internet Access Available?", options=["Yes", "No"])

# 4. Processing the Inputs on Button Click
st.subheader("📋 Evaluation Summary")

if st.button("Run Performance Diagnostic"):
    if model is not None:
        internet_encoded = 1 if internet == "Yes" else 0
        input_data = pd.DataFrame([{
            'Attendance_Pct': attendance,
            'Weekly_Study_Hours': study_hours,
            'Mid_Term_Score': mid_term,
            'Internet_Access': internet_encoded
        }])
        
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        
        st.markdown("### System Diagnosis:")
        if prediction == 1:
            risk_pct = probabilities[1] * 100
            st.error(f"⚠️ **Status:** Critical / Assistance Required")
            st.metric(label="Calculated Risk Factor", value=f"{risk_pct:.1f}%")
            st.warning("**Recommended Action:** Flag for immediate remedial classes and academic consultation.")
        else:
            safety_pct = probabilities[0] * 100
            st.success(f"✅ **Status:** Clear / Satisfactory Performance")
            st.metric(label="Calculated Stability Index", value=f"{safety_pct:.1f}%")
            st.info("**Recommended Action:** Continue standard academic monitoring.")
            
    else:
        st.error("Error: Trained model engine ('student_model.pkl') not found. Please upload the model file.")

st.markdown("---")
st.caption("Internal School Administration Dashboard | Secure Data Node")
