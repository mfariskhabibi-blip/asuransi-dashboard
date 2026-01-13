import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder

# --- CONFIG DASHBOARD ---
st.set_page_config(page_title="Telco Churn Analytics", layout="wide")

# --- LOAD DATA & MODEL ---
@st.cache_data
def load_data():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

df = load_data()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigasi")
menu = st.sidebar.radio("Pilih Halaman:", ["Dashboard Analytics", "Prediksi Pelanggan"])

# --- HALAMAN 1: DASHBOARD ANALYTICS ---
if menu == "Dashboard Analytics":
    st.title("📊 Telco Customer Churn Dashboard")
    st.markdown("Analisis pola pelanggan berdasarkan dataset KDD.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Distribusi Churn")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='Churn', palette='viridis', ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Kontrak vs Churn")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='Contract', hue='Churn', palette='magma', ax=ax)
        st.pyplot(fig)

    st.divider()

    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Masa Berlangganan (Tenure)")
        fig, ax = plt.subplots()
        sns.kdeplot(data=df, x='tenure', hue='Churn', fill=True, ax=ax)
        st.pyplot(fig)

    with col4:
        st.subheader("Metode Pembayaran")
        fig, ax = plt.subplots()
        sns.countplot(data=df, x='PaymentMethod', hue='Churn', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

# --- HALAMAN 2: PREDIKSI PELANGGAN ---
elif menu == "Prediksi Pelanggan":
    st.title("🔮 Prediksi Risiko Churn")
    st.markdown("Masukkan data pelanggan untuk melihat probabilitas mereka berhenti berlangganan.")

    with st.form("churn_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            tenure = st.slider("Tenure (Bulan)", 0, 72, 12)
            monthly = st.number_input("Monthly Charges ($)", value=50.0)
        with c2:
            contract = st.selectbox("Tipe Kontrak", ['Month-to-month', 'One year', 'Two year'])
            internet = st.selectbox("Layanan Internet", ['DSL', 'Fiber optic', 'No'])
        with c3:
            payment = st.selectbox("Metode Bayar", ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
            tech_support = st.selectbox("Tech Support", ['No', 'Yes', 'No internet service'])

        submit = st.form_submit_button("Analisis Risiko")

    if submit:
        # Sederhananya kita asumsikan model sudah dilatih (dummy logic untuk simulasi app)
        # Di aplikasi nyata, Anda load model .pkl di sini
        risk_score = 0.0
        if contract == 'Month-to-month': risk_score += 0.4
        if internet == 'Fiber optic': risk_score += 0.2
        if tenure < 12: risk_score += 0.3
        
        st.divider()
        if risk_score > 0.5:
            st.error(f"### HASIL: RISIKO TINGGI ({(risk_score*100):.1f}%)")
            st.info("💡 Rekomendasi: Segera tawarkan perpanjangan kontrak dengan diskon khusus.")
        else:
            st.success(f"### HASIL: RISIKO RENDAH ({(risk_score*100):.1f}%)")
            st.info("💡 Rekomendasi: Pertahankan kualitas layanan saat ini.")