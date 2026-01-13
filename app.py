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

# --- LOAD DATA MENTAH ---
# Menggunakan data simulasi yang strukturnya persis dengan dataset asuransi Anda
@st.cache_data
def load_data():
    # Contoh data yang merepresentasikan dataset asuransi (age, bmi, smoker, charges)
    data = {
        'age': [19, 18, 28, 33, 32, 31, 46, 37, 37, 60, 25, 62, 23, 56, 27, 19, 52, 23, 56, 30],
        'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'male', 'female', 'male', 'female', 'male'],
        'bmi': [27.9, 33.7, 33.0, 22.7, 28.8, 25.7, 33.4, 27.7, 29.8, 25.8, 26.2, 26.2, 34.4, 39.8, 42.1, 24.6, 30.7, 23.8, 40.3, 35.3],
        'smoker': ['yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes'],
        'charges': [16884.92, 1725.55, 4449.46, 21984.47, 3866.85, 3756.62, 8240.58, 7281.50, 6406.41, 28923.13, 2721.32, 27808.72, 1826.84, 11090.71, 39611.75, 1837.23, 10797.33, 2395.17, 10602.38, 36837.46]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR NAVIGASI ---
st.sidebar.title("Navigasi")
st.sidebar.write("Pengembang: **Muhammad Faris Khabibi**")
page = st.sidebar.radio("Pilih Halaman:", ["🔮 Prediksi Biaya", "📊 Visualisasi Insight", "📄 Data Mentah"])

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.markdown("Hitung estimasi tagihan medis secara instan berdasarkan model Linear Regression.")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Profil")
        usia = st.number_input("Usia (Tahun)", 18, 100, 25)
        bmi = st.number_input("BMI (Indeks Massa Tubuh)", 10.0, 60.0, 24.5)
        perokok = st.selectbox("Status Merokok", ("Ya", "Tidak"))
        
        # Logika Prediksi (Berdasarkan koefisien notebook Anda)
        smoker_val = 1 if perokok == "Ya" else 0
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
    st.title("📊 Seluruh Visualisasi Insight Data")
    st.divider()

    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Rata-rata Biaya: Perokok vs Non-Perokok")
        data_biaya = pd.DataFrame({
            'Status': ['Bukan Perokok', 'Perokok'],
            'Rata-rata Biaya ($)': [8434, 32050]
        })
        fig1, ax1 = plt.subplots()
        sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=data_biaya, palette=['#3498db', '#e74c3c'], ax=ax1)
        st.pyplot(fig1)

    with row1_col2:
        st.subheader("2. Matriks Korelasi (Heatmap)")
        korelasi = pd.DataFrame({
            'age': [1.00, 0.11, 0.30],
            'bmi': [0.11, 1.00, 0.20],
            'charges': [0.30, 0.20, 1.00]
        }, index=['age', 'bmi', 'charges'])
        fig2, ax2 = plt.subplots()
        sns.heatmap(korelasi, annot=True, cmap='coolwarm', ax=ax2)
        st.pyplot(fig2)

    st.divider()
    
    st.subheader("3. Tren Kenaikan Biaya Berdasarkan Usia")
    fig3, ax3 = plt.subplots(figsize=(12, 4))
    # Menggunakan data dari dataset simulasi
    sns.lineplot(data=df.sort_values('age'), x='age', y='charges', marker='o', color='#2ecc71')
    st.pyplot(fig3)

# --- HALAMAN 3: DATA MENTAH ---
elif page == "📄 Data Mentah":
    st.title("📄 Dataset Asuransi Kesehatan")
    st.markdown("Berikut adalah seluruh baris data mentah yang digunakan dalam analisis ini.")
    st.divider()
    
    # Menampilkan Tabel Data Seluruhnya
    st.dataframe(df, use_container_width=True)
    
    # Statistik Deskriptif
    st.subheader("📋 Ringkasan Statistik Dataset")
    st.write(df.describe())
    
    # Tombol Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download Data Mentah (CSV)", data=csv, file_name='data_asuransi_faris.csv', mime='text/csv')

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2024 Muhammad Faris Khabibi | Project KDD")