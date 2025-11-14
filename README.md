# 💧 Water Quality Prediction

An **intelligent Machine Learning + Streamlit web application** designed to predict key water pollutants — **O₂, NO₃, NO₂, SO₄, PO₄, Cl⁻** — using **Year** and **Station ID**.  
This project enables **fast, interactive, and user-friendly water quality analysis**.

---

## 🌍 Problem Statement

Water pollution poses a serious threat to the environment and public health. Traditional water testing methods are often **slow and expensive**.  
This project uses **Machine Learning** to predict water quality parameters efficiently, making testing **faster, more cost-effective, and easily accessible**.

---

## ✨ Features

- ✅ Predicts six major water pollutant levels using ML  
- ✅ Fully interactive **Streamlit web app**  
- ✅ Dark blue neon-themed UI with smooth animations  
- ✅ Visualizations: **Bar & Pie charts** for better insights  
- ✅ Built-in navigation: Home, Predict, Data Explorer, About  
- ✅ Dataset preview and exploration capabilities  

---

## 🛠️ Tech Stack

- **Python** – Programming language  
- **Pandas & NumPy** – Data processing and manipulation  
- **Scikit-learn** – Random Forest Regressor for prediction  
- **Joblib** – Model serialization and saving  
- **Plotly** – Interactive visualizations (Bar & Pie charts)  
- **Streamlit** – Deployment and UI development  

---

## 🧩 Methodology

1. **Data Collection:** Imported from `DataSet.csv`  
2. **Preprocessing:** Cleaning data and encoding categorical features  
3. **Model Training:** Trained **Random Forest Regressor** on the dataset  
4. **Model Saving:** Saved model (`pollution_model.pkl`) and columns (`model_columns.pkl`)  
5. **Deployment:** Integrated model into Streamlit app with prediction & visualization functionality  

---

## 🚀 Getting Started

1. **Clone the repository:**

```bash
git clone https://github.com/GayatriMusunuri/Water_Quality_Prediction.git
cd Water_Quality_Prediction '''
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
streamlit run app.py
```

4. Open in Browser:
- Local: http://localhost:8501/
- Network: As displayed in terminal

## 📊 Results
- Predicts six pollutant levels accurately for each input
- Fast and reliable predictions
- Good performance achieved using Random Forest Regressor
- Provides visual insights via Bar & Pie Charts

## 🌐 Live Demo
Check out the live app here:
http://localhost:8501/

## 👩‍💻 Author
https://github.com/GayatriMusunuri

✨ Empowering smarter and cleaner water monitoring with AI! 🌊💧
