import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Asuransi - Muhammad Faris Khabibi",
    page_icon="🏥",
    layout="wide"
)

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("Navigasi")
st.sidebar.write("Pengembang: **Muhammad Faris Khabibi**")
page = st.sidebar.radio("Pilih Halaman:", ["🔮 Prediksi Biaya", "📊 Visualisasi Insight", "📄 Data Mentah"])

# --- LOAD DATA MENTAH (Simulasi Dataset medical-charges.csv) ---
@st.cache_data
def load_data():
    # Data ini sesuai dengan sampel dataset asuransi yang Anda gunakan di notebook
    data = {
        'age': [19, 18, 28, 33, 32, 31, 46, 37, 37, 60],
        'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'female'],
        'bmi': [27.9, 33.77, 33.0, 22.7, 28.8, 25.7, 33.4, 27.7, 29.8, 25.8],
        'children': [0, 1, 3, 0, 0, 0, 1, 3, 2, 0],
        'smoker': ['yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no'],
        'region': ['southwest', 'southeast', 'southeast', 'northwest', 'northwest', 'southeast', 'southeast', 'northwest', 'northeast', 'northwest'],
        'charges': [16884.92, 1725.55, 4449.46, 21984.47, 3866.85, 3756.62, 8240.58, 7281.50, 6406.41, 28923.13]
    }
    return pd.DataFrame(data)

df = load_data()

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.markdown("Hitung estimasi tagihan medis secara instan berdasarkan profil nasabah.")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Profil")
        usia = st.number_input("Usia (Tahun)", 18, 100, 25)
        bmi = st.number_input("BMI (Indeks Massa Tubuh)", 10.0, 60.0, 24.5)
        perokok = st.selectbox("Status Merokok", ("Ya", "Tidak"))
        
        smoker_val = 1 if perokok == "Ya" else 0
        # Formula Linear Regression sesuai koefisien notebook Anda
        estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
        estimasi = max(0, estimasi)

        if st.button("Hitung Estimasi"):
            st.session_state.hasil = estimasi

    with col2:
        st.subheader("Hasil Prediksi")
        if 'hasil' in st.session_state:
            st.metric(label="Estimasi Tagihan Medis", value=f"${st.session_state.hasil:,.2f}")
            if perokok == "Ya":
                st.error("⚠️ Risiko Tinggi: Status perokok mendominasi kenaikan biaya.")
            else:
                st.success("✅ Risiko Rendah: Status non-perokok menjaga biaya tetap stabil.")

# --- HALAMAN 2: VISUALISASI ---
elif page == "📊 Visualisasi Insight":
    st.title("📊 Analisis Visual KDD")
    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("Dampak Merokok")
        data_plot = pd.DataFrame({'Status': ['Bukan Perokok', 'Perokok'], 'Rata-rata Biaya ($)': [8434, 32050]})
        fig1, ax1 = plt.subplots()
        sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=data_plot, palette=['#3498db', '#e74c3c'], ax=ax1)
        st.pyplot(fig1)

    with row1_col2:
        st.subheader("Korelasi Variabel")
        # Nilai korelasi persis dari notebook Anda (0.299 dan 0.198)
        korelasi = pd.DataFrame({'age': [1.0, 0.11, 0.30], 'bmi': [0.11, 1.0, 0.20], 'charges': [0.30, 0.20, 1.0]}, index=['age', 'bmi', 'charges'])
        fig2, ax2 = plt.subplots()
        sns.heatmap(korelasi, annot=True, cmap='Blues', ax=ax2)
        st.pyplot(fig2)

# --- HALAMAN 3: DATA MENTAH ---
elif page == "📄 Data Mentah":
    st.title("📄 Dataset Asuransi")
    st.markdown("Berikut adalah sampel data mentah yang digunakan untuk melatih model prediksi.")
    st.divider()
    
    # Menampilkan tabel data mentah
    st.dataframe(df, use_container_width=True)
    
    # Tombol Download Data
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Dataset (CSV)", data=csv, file_name='medical_charges_sample.csv', mime='text/csv')
    
    st.subheader("Statistik Deskriptif")
    st.write(df.describe())

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2024 Muhammad Faris Khabibi")