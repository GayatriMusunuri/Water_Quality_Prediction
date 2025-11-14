import pandas as pd
import joblib
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# ==============================
# Load Model & Columns
# ==============================
model = joblib.load("pollution_model.pkl")
model_cols = joblib.load("model_columns.pkl")

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Water Pollutants Predictor",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Custom CSS Styling
# ==============================
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        color: #1E90FF;
        font-size: 40px;
        font-weight: bold;
    }
    .subtitle {
        text-align: center;
        font-size: 20px;
        color: #444444;
    }
    .pollutant-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        text-align: center;
        margin: 10px;
    }
    .pollutant-value {
        font-size: 22px;
        font-weight: bold;
        color: #1E90FF;
    }
    .step {
        font-size: 16px;
        margin: 8px 0;
    }
    .active-step {
        color: #1E90FF;
        font-weight: bold;
    }
    .done-step {
        color: green;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==============================
# Sidebar Navigation
# ==============================
pages = ["🏠 Home", "📝 Input Data", "📊 Prediction Results", "📈 Visualizations", "🎉 End"]

# Initialize session state
if "step" not in st.session_state:
    st.session_state["step"] = 0

# Current page
page = pages[st.session_state["step"]]

# Progress indicator
current_step = st.session_state["step"] + 1
progress = int((current_step / len(pages)) * 100)

st.sidebar.title("📌 Navigation")
st.sidebar.markdown("### 🚦 Progress")
st.sidebar.progress(progress)

for i, p in enumerate(pages, start=1):
    if i < current_step:
        st.sidebar.markdown(f"<div class='step done-step'>✔ Step {i}: {p}</div>", unsafe_allow_html=True)
    elif i == current_step:
        st.sidebar.markdown(f"<div class='step active-step'>➡ Step {i}: {p}</div>", unsafe_allow_html=True)
    else:
        st.sidebar.markdown(f"<div class='step'>Step {i}: {p}</div>", unsafe_allow_html=True)

# ==============================
# Navigation Helpers
# ==============================
def next_step():
    if st.session_state["step"] < len(pages) - 1:
        st.session_state["step"] += 1

def prev_step():
    if st.session_state["step"] > 0:
        st.session_state["step"] -= 1

def restart():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state["step"] = 0

# ==============================
# Home Page
# ==============================
if page == "🏠 Home":
    st.markdown("<div class='main-title'>💧 Water Pollutants Predictor</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Predict pollutant levels based on Year & Station ID</div>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2913/2913465.png", width=200)
    st.write(
        """
        Welcome to the *Water Pollutants Predictor* 🌍  
        Use this app to:
        - Enter *Year & Station ID*  
        - Get predicted levels of key pollutants  
        - View results in *cards, bar chart & radar chart*  
        """
    )

    st.button("➡ Next", on_click=next_step)

# ==============================
# Input Page
# ==============================
elif page == "📝 Input Data":
    st.header("📝 Enter Input Parameters")
    year_input = st.number_input("Enter Year", min_value=2000, max_value=2100, value=2022)
    station_id = st.text_input("Enter Station ID", value="1")

    if st.button("🚀 Run Prediction"):
        if not station_id:
            st.warning("⚠ Please enter a valid Station ID.")
        else:
            st.session_state["year_input"] = year_input
            st.session_state["station_id"] = station_id
            st.session_state["predicted"] = True
            st.success("✅ Inputs saved! Now go to Prediction Results.")

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅ Back", on_click=prev_step)
    with col2:
        st.button("➡ Next", on_click=next_step)

# ==============================
# Prediction Page
# ==============================
elif page == "📊 Prediction Results":
    st.header("📊 Predicted Pollutant Levels")

    if "predicted" not in st.session_state or not st.session_state["predicted"]:
        st.info("ℹ Please enter input data first in the *Input Data* page.")
    else:
        year_input = st.session_state["year_input"]
        station_id = st.session_state["station_id"]

        input_df = pd.DataFrame({"year": [year_input], "id": [station_id]})
        input_encoded = pd.get_dummies(input_df, columns=["id"])
        for col in model_cols:
            if col not in input_encoded.columns:
                input_encoded[col] = 0
        input_encoded = input_encoded[model_cols]

        predicted_pollutants = model.predict(input_encoded)[0]
        pollutants = ["O2", "NO3", "NO2", "SO4", "PO4", "CL"]

        st.success(f"✅ Prediction Successful for Station *{station_id}* in Year *{year_input}*")

        cols = st.columns(3)
        for idx, (p, val) in enumerate(zip(pollutants, predicted_pollutants)):
            with cols[idx % 3]:
                st.markdown(
                    f"""
                    <div class='pollutant-card'>
                        <h4>{p}</h4>
                        <div class='pollutant-value'>{val:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.session_state["pollutants"] = pollutants
        st.session_state["values"] = predicted_pollutants

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅ Back", on_click=prev_step)
    with col2:
        st.button("➡ Next", on_click=next_step)

# ==============================
# Visualization Page
# ==============================
elif page == "📈 Visualizations":
    st.header("📈 Pollutant Visualizations")

    if "pollutants" not in st.session_state:
        st.info("ℹ Please generate predictions first in the *Prediction Results* page.")
    else:
        pollutants = st.session_state["pollutants"]
        values = st.session_state["values"]

        df_vis = pd.DataFrame({"Pollutant": pollutants, "Value": values})

        tab1, tab2 = st.tabs(["📉 Bar Chart", "🕸 Radar Chart"])

        with tab1:
            fig_bar = px.bar(
                df_vis, x="Pollutant", y="Value", color="Pollutant",
                text="Value", title="Predicted Pollutant Levels", template="plotly_white"
            )
            fig_bar.update_traces(texttemplate='%{text:.2f}', textposition="outside")
            fig_bar.update_layout(yaxis_title="Concentration (mg/L)", xaxis_title="Pollutants")
            st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=df_vis["Value"], theta=df_vis["Pollutant"],
                fill="toself", name="Pollutant Levels"
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, max(df_vis["Value"]) * 1.2])),
                showlegend=False,
                title="Radar View of Pollutant Levels"
            )
            st.plotly_chart(fig_radar, use_container_width=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.button("⬅ Back", on_click=prev_step)
    with col2:
        st.button("➡ Next", on_click=next_step)

# ==============================
# End Page
# ==============================
elif page == "🎉 End":
    st.markdown("<div class='main-title'>🎉 Thank You!</div>", unsafe_allow_html=True)
    st.success("✅ You have completed the Water Pollutants Prediction workflow.")

    st.balloons()
    st.snow()

    st.write(
        """
        🔄 Would you like to start again?  
        Click *Restart* to go back to the Home page.
        """
    )

    st.button("🔄 Restart", on_click=restart)

# ==============================
# Footer
# ==============================
st.markdown("---")
st.markdown("<p style='text-align: center; color: grey;'>Made with ❤ using Streamlit</p>", unsafe_allow_html=True)