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
page = st.sidebar.radio("Pilih Halaman:", ["🔮 Prediksi Biaya", "📊 Visualisasi Insight"])

# --- DATA UNTUK VISUALISASI (Berdasarkan Temuan Notebook Anda) ---
# Data rata-rata biaya
data_biaya = pd.DataFrame({
    'Status': ['Bukan Perokok', 'Perokok'],
    'Rata-rata Biaya ($)': [8434, 32050]
})

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.markdown("Gunakan form ini untuk mendapatkan estimasi tagihan medis berdasarkan profil nasabah.")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Profil")
        usia = st.number_input("Usia (Tahun)", 18, 100, 25)
        bmi = st.number_input("BMI (Indeks Massa Tubuh)", 10.0, 60.0, 24.5)
        perokok = st.selectbox("Status Merokok", ("Ya", "Tidak"))
        
        # Logika Prediksi Sederhana (Koefisien Linear Regression dari Notebook)
        smoker_val = 1 if perokok == "Ya" else 0
        # Formula: intercept + (coef_age * age) + (coef_bmi * bmi) + (coef_smoker * smoker)
        estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
        estimasi = max(0, estimasi)

        if st.button("Hitung Estimasi"):
            st.session_state.hasil = estimasi

    with col2:
        st.subheader("Hasil Analisis")
        if 'hasil' in st.session_state:
            st.metric(label="Estimasi Tagihan Medis", value=f"${st.session_state.hasil:,.2f}")
            
            if perokok == "Ya":
                st.error("⚠️ Peringatan: Status perokok meningkatkan biaya medis secara drastis.")
            else:
                st.success("✅ Info: Status bukan perokok membantu menjaga biaya tetap rendah.")
            
            st.write(f"Berdasarkan model, profil nasabah usia {usia} dengan BMI {bmi} diprediksi memiliki beban tagihan di atas.")

# --- HALAMAN 2: VISUALISASI ---
elif page == "📊 Visualisasi Insight":
    st.title("📊 Seluruh Visualisasi Insight Data")
    st.markdown("Halaman ini menyajikan temuan dari tahap **Data Mining** dan **Pattern Evaluation**.")
    st.divider()

    # Layout baris pertama: 2 Grafik
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        st.subheader("1. Distribusi Biaya Berdasarkan Status")
        fig1, ax1 = plt.subplots()
        sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=data_biaya, palette=['#3498db', '#e74c3c'], ax=ax1)
        ax1.set_ylabel("Rata-rata Tagihan ($)")
        st.pyplot(fig1)
        st.caption("Insight: Perokok memiliki rata-rata tagihan jauh lebih tinggi (>$30k) dibanding non-perokok.")

    with row1_col2:
        st.subheader("2. Korelasi Variabel (Heatmap)")
        # Data korelasi dari output notebook Anda
        korelasi_matriks = pd.DataFrame({
            'age': [1.00, 0.11, 0.30],
            'bmi': [0.11, 1.00, 0.20],
            'charges': [0.30, 0.20, 1.00]
        }, index=['age', 'bmi', 'charges'])
        
        fig2, ax2 = plt.subplots()
        sns.heatmap(korelasi_matriks, annot=True, cmap='coolwarm', ax=ax2)
        st.pyplot(fig2)
        st.caption("Insight: Usia (0.30) memiliki korelasi lebih kuat terhadap biaya dibanding BMI (0.20).")

    st.divider()

    # Layout baris kedua: 1 Grafik Besar & Tabel
    row2_col1, row2_col2 = st.columns([1.5, 1])

    with row2_col1:
        st.subheader("3. Tren Usia vs Biaya Medis")
        # Simulasi data scatter plot dari notebook
        st.markdown("*Grafik ini menunjukkan kecenderungan kenaikan biaya seiring bertambahnya usia.*")
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        # Data dummy yang merepresentasikan tren linear di notebook Anda
        usia_sampel = [20, 30, 40, 50, 60]
        biaya_sampel = [12000, 15000, 18000, 22000, 26000]
        sns.lineplot(x=usia_sampel, y=biaya_sampel, marker='o', ax=ax3, color='#2ecc71')
        ax3.set_xlabel("Usia")
        ax3.set_ylabel("Estimasi Biaya ($)")
        st.pyplot(fig3)

    with row2_col2:
        st.subheader("📋 Ringkasan Statistik KDD")
        st.write("Hasil evaluasi pola:")
        st.table(pd.DataFrame({
            'Metrik': ['Korelasi Usia', 'Korelasi BMI', 'Faktor Dominan'],
            'Nilai': ['0.299008', '0.198341', 'Smoker']
        }))
        st.info("Pengetahuan: Merokok adalah 'Key Feature' dalam prediksi biaya asuransi kesehatan.")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2024 Muhammad Faris Khabibi | KDD Project")