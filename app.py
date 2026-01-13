import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman (Harus paling atas)
st.set_page_config(
    page_title="Dashboard Asuransi - Faris Khabibi",
    page_icon="🏥",
    layout="wide"
)

# 2. Fungsi Load Data (Dibuat sesederhana mungkin untuk menghindari TokenError)
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('medical-charges.csv')
        return data
    except Exception as e:
        st.error(f"Gagal memuat file CSV: {e}")
        return pd.DataFrame()

df = load_data()

# --- SIDEBAR ---
st.sidebar.title("Navigasi")
st.sidebar.write("Pengembang: **Muhammad Faris Khabibi**")
menu = ["🔮 Prediksi Biaya", "📊 Visualisasi Insight", "📄 Data Mentah"]
page = st.sidebar.radio("Pilih Halaman:", menu)

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Profil")
        usia = st.number_input("Usia", 18, 100, 25)
        bmi = st.number_input("BMI", 10.0, 50.0, 25.0)
        perokok = st.selectbox("Perokok?", ["Tidak", "Ya"])
        
        smoker_val = 1 if perokok == "Ya" else 0
        # Rumus Linear Regression
        estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
        estimasi = max(0, estimasi)

        if st.button("Hitung Sekarang"):
            st.session_state.hasil_prediksi = estimasi

    with col2:
        st.subheader("Hasil Analisis")
        if 'hasil_prediksi' in st.session_state:
            st.metric("Estimasi Tagihan", f"${st.session_state.hasil_prediksi:,.2f}")
            if perokok == "Ya":
                st.error("Status perokok sangat mempengaruhi biaya.")
            else:
                st.success("Profil risiko rendah.")

# --- HALAMAN 2: VISUALISASI ---
elif page == "📊 Visualisasi Insight":
    st.title("📊 Visualisasi Pengetahuan")
    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("Dampak Merokok")
            fig1, ax1 = plt.subplots()
            sns.barplot(x='smoker', y='charges', data=df, ax=ax1)
            st.pyplot(fig1)
        with c2:
            st.subheader("Korelasi Data")
            fig2, ax2 = plt.subplots()
            # Hanya kolom numerik untuk heatmap
            df_numeric = df.select_dtypes(include=['float64', 'int64'])
            sns.heatmap(df_numeric.corr(), annot=True, cmap='coolwarm', ax=ax2)
            st.pyplot(fig2)
    else:
        st.warning("Data tidak tersedia untuk visualisasi.")

# --- HALAMAN 3: DATA MENTAH ---
else:
    st.title("📄 Data Mentah")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        st.download_button("Download Data", df.to_csv(index=False), "data.csv")
    else:
        st.error("File medical-charges.csv tidak ditemukan.")