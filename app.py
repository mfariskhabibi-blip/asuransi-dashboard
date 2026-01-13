import streamlit as st
import pandas as pd

st.title("🏥 Dashboard Prediksi Biaya Asuransi")

# Input User
usia = st.sidebar.slider("Usia", 18, 100, 25)
bmi = st.sidebar.slider("BMI", 10.0, 50.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# Logika Prediksi Sederhana (Berdasarkan model yang dilatih)
smoker_val = 1 if perokok == "Ya" else 0
# Rumus prediksi dari koefisien model Linear Regression Anda
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000

st.subheader("Hasil Estimasi Biaya")
st.metric(label="Estimasi Tagihan", value=f"${estimasi:,.2f}")
