import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(
    page_title="Proactive Asset Health Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for aesthetic warning boxes and clean typography
st.markdown("""
    <style>
    .healthy-box { padding: 25px; border-radius: 12px; background-color: #ecfdf5; border: 2px solid #10b981; color: #065f46; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .faulty-box { padding: 25px; border-radius: 12px; background-color: #fef2f2; border: 2px solid #ef4444; color: #991b1b; text-align: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    .metric-value { font-size: 2rem; font-weight: bold; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """Loads the serialized XGBoost model. Uses caching to prevent reloading on every UI interaction."""
    model_path = "xgboost_model.pkl"
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        return None

model = load_model()

st.title("🏭 Proactive Engine Health Diagnostics")
st.write("Enter real-time telemetry from edge sensors to forecast impending mechanical failures based on our tuned XGBoost classification model.")

if model is None:
    st.error("⚠️ Error: `xgboost_model.pkl` not found. Please run `train.py` first to generate the model artifact before running the dashboard.")
    st.stop()

st.sidebar.header("📡 Live Sensor Telemetry Input")
st.sidebar.write("Adjust the thermodynamic and mechanical parameters below:")

def get_user_input():
    # Ranges based on the EDA distributions from the interim report
    engine_rpm = st.sidebar.slider("Engine RPM", min_value=500, max_value=2500, value=1500, step=10)
    lub_oil_pressure = st.sidebar.slider("Lubricating Oil Pressure (bar)", min_value=0.0, max_value=7.0, value=3.2, step=0.1)
    fuel_pressure = st.sidebar.slider("Fuel Pressure (bar)", min_value=2.0, max_value=10.0, value=6.6, step=0.1)
    coolant_pressure = st.sidebar.slider("Coolant Pressure (bar)", min_value=0.5, max_value=5.0, value=2.4, step=0.1)
    lub_oil_temp = st.sidebar.slider("Lubricating Oil Temp (°C)", min_value=50.0, max_value=130.0, value=76.0, step=0.5)
    coolant_temp = st.sidebar.slider("Coolant Temp (°C)", min_value=50.0, max_value=130.0, value=72.0, step=0.5)
    
    # Store in a dataframe mimicking the training data structure
    features = pd.DataFrame({
        'Engine_RPM': [engine_rpm],
        'Lub_Oil_Pressure': [lub_oil_pressure],
        'Fuel_Pressure': [fuel_pressure],
        'Coolant_Pressure': [coolant_pressure],
        'Lub_Oil_Temperature': [lub_oil_temp],
        'Coolant_Temperature': [coolant_temp]
    })
    return features

input_df = get_user_input()

st.subheader("Current Asset Parameters")
st.dataframe(input_df, use_container_width=True, hide_index=True)

st.write("---")

if st.button("🔍 Run Diagnostic Inference", type="primary", use_container_width=True):
    with st.spinner("Analyzing thermodynamic and mechanical thresholds..."):
        # Run inference
        prediction = model.predict(input_df)
        probability = model.predict_proba(input_df)[0]
        
        st.subheader("Diagnostic Result")
        
        # 0 = Healthy, 1 = Faulty
        if prediction[0] == 0:
            st.markdown(f'''
            <div class="healthy-box">
                <h2>✅ Engine is Healthy</h2>
                <p>Normal Operation Verified</p>
                <div class="metric-value">{(probability[0]*100):.1f}% Confidence</div>
                <p>All mechanical and thermodynamic sensors are operating within safe boundaries. No immediate maintenance is required.</p>
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div class="faulty-box">
                <h2>⚠️ Maintenance Required</h2>
                <p>Fault Signatures Detected</p>
                <div class="metric-value">{(probability[1]*100):.1f}% Failure Probability</div>
                <p><strong>Recommended Action:</strong> Discontinue heavy load. Inspect lubrication and cooling systems immediately.</p>
            </div>
            ''', unsafe_allow_html=True)
            
            st.write("#### 🔎 Potential Diagnostic Focus Areas:")
            col1, col2 = st.columns(2)
            with col1:
                if input_df['Lub_Oil_Temperature'].values[0] > 84:
                    st.warning("🔥 **Thermal Runaway Warning:** Lubricating Oil Temperature is exceptionally high, risking viscosity breakdown.")
                if input_df['Coolant_Temperature'].values[0] > 82:
                    st.warning("🌡️ **Coolant System Alert:** Engine block temperature is exceeding safe operational medians.")
            with col2:
                if input_df['Lub_Oil_Pressure'].values[0] < 2.5 and input_df['Engine_RPM'].values[0] > 1200:
                    st.error("💥 **Friction Danger:** Low oil pressure detected at high RPMs. Immediate risk of bearing seizing.")
                if input_df['Coolant_Pressure'].values[0] < 2.0:
                    st.warning("💧 **Pressure Drop:** Coolant pressure is low. Inspect for closed-loop leaks or head gasket breaches.")
