import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Asuransi Dashboard - Muhammad Faris Khabibi",
    page_icon="🏥",
    layout="wide"
)

# 2. Sidebar Navigasi
st.sidebar.title("Navigasi")
st.sidebar.write("Pengembang: **Muhammad Faris Khabibi**")
page = st.sidebar.radio("Pilih Halaman:", ["🔮 Prediksi Biaya", "📊 Visualisasi Insight"])

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.markdown("Masukkan data profil nasabah untuk mendapatkan estimasi tagihan medis berdasarkan model Linear Regression.")
    
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("Input Data")
        usia = st.number_input("Usia (Tahun)", 18, 100, 25)
        bmi = st.number_input("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
        perokok = st.selectbox("Status Merokok", ("Ya", "Tidak"))
        
        # Logika Prediksi (Berdasarkan bobot model di notebook Anda)
        smoker_val = 1 if perokok == "Ya" else 0
        # Rumus ini merepresentasikan hasil model.fit() pada data charges
        estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
        estimasi = max(0, estimasi)
        
        if st.button("Hitung Estimasi Sekarang"):
            st.session_state.hasil_prediksi = estimasi
        
    with col2:
        st.subheader("Hasil Estimasi")
        if 'hasil_prediksi' in st.session_state:
            st.metric(label="Total Tagihan Medis", value=f"${st.session_state.hasil_prediksi:,.2f}")
            
            if perokok == "Ya":
                st.error("⚠️ Status Perokok Terdeteksi")
                st.write("Status merokok adalah faktor paling dominan yang menentukan mahalnya biaya.")
            else:
                st.success("✅ Status Bukan Perokok")
                st.write("Tagihan lebih rendah dibandingkan kelompok perokok.")

# --- HALAMAN 2: VISUALISASI ---
elif page == "📊 Visualisasi Insight":
    st.title("📊 Visualisasi & Analisis Data")
    st.markdown("Halaman ini menyajikan temuan dari tahap **Data Mining** dan **Pattern Evaluation**.")
    
    st.divider()
    
    # Grafik Insight
    st.subheader("Dampak Merokok terhadap Tagihan")
    data_insight = pd.DataFrame({
        'Status': ['Bukan Perokok', 'Perokok'],
        'Rata-rata Biaya ($)': [8434, 32050]
    })
    
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=data_insight, palette=['#3498db', '#e74c3c'], ax=ax)
    st.pyplot(fig)
    
    # Tabel Korelasi (Berdasarkan output correlation matrix Anda)
    st.subheader("Tabel Korelasi Variabel")
    korelasi_data = {
        'Variabel': ['Usia (Age)', 'BMI', 'Status Merokok'],
        'Nilai Korelasi terhadap Charges': ['0.299008', '0.198341', 'Dominan']
    }
    st.table(pd.DataFrame(korelasi_data))
    st.write("Nilai korelasi menunjukkan seberapa kuat pengaruh variabel terhadap total tagihan.")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.info("""
**Metodologi KDD:**
1. Cleaning (Drop Duplicates)
2. Transformation (Mapping Smoker)
3. Mining (Linear Regression)
4. Presentation (Dashboard)
""")