import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Prediksi Biaya Asuransi",
    page_icon="🏥",
    layout="wide"
)

# 2. Judul dan Deskripsi
st.title("🏥 Dashboard Analisis & Prediksi Biaya Asuransi")
st.markdown("""
Aplikasi ini menyajikan **Knowledge Presentation** dari hasil KDD menggunakan data biaya medis nasabah. 
Gunakan panel kiri untuk simulasi prediksi biaya secara real-time.
""")

st.divider()

# 3. Sidebar untuk Input Pengguna (Data Transformation)
st.sidebar.header("⚙️ Input Profil Nasabah")
usia = st.sidebar.slider("Usia (Tahun)", 18, 100, 25)
bmi = st.sidebar.slider("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# 4. Logika Prediksi (Data Mining)
# Menggunakan logika pemrosesan biner dari model Anda 
smoker_val = 1 if perokok == "Ya" else 0
# Estimasi biaya berdasarkan tren data medis
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
estimasi = max(0, estimasi)

# 5. Tampilan Utama (Layout 2 Kolom)
col_grafik, col_hasil = st.columns([1.5, 1])

with col_grafik:
    st.subheader("📊 Grafik Insight: Faktor Utama Biaya")
    
    # Data dari hasil analisis statistik Anda 
    # Rata-rata biaya perokok vs non-perokok
    df_plot = pd.DataFrame({
        'Status': ['Bukan Perokok', 'Perokok'],
        'Rata-rata Biaya ($)': [8434, 32050]
    })
    
    # Membuat visualisasi insight
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=df_plot, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title("Perbandingan Biaya Berdasarkan Status Merokok")
    
    st.pyplot(fig)
    st.info("**Insight:** Status merokok adalah faktor paling dominan dalam menentukan mahalnya biaya medis.")

with col_hasil:
    st.subheader("🔮 Estimasi Hasil")
    st.write("Prediksi biaya medis untuk profil ini:")
    
    # Menampilkan hasil prediksi dalam metric
    st.metric(label="Total Estimasi Tagihan", value=f"${estimasi:,.2f}")
    
    # Menampilkan status risiko sesuai temuan 
    if perokok == "Ya":
        st.error(f"Status: Perokok (Risiko Tinggi)")
        st.caption("Biaya melonjak drastis akibat faktor gaya hidup.")
    else:
        st.success(f"Status: Bukan Perokok (Risiko Rendah)")
        st.caption("Biaya medis cenderung jauh lebih ekonomis.")

# 6. Evaluasi Pola & Metodologi (Sesuai File Colab Anda)
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Evaluasi Pola (Pattern Evaluation)")
    # Data korelasi dari file Anda 
    st.write("Kekuatan hubungan faktor terhadap biaya medis:")
    korelasi_data = {
        'Faktor': ['Usia (Age)', 'BMI', 'Status Merokok'],
        'Nilai Korelasi': ['0.299', '0.198', 'Dominan']
    }
    st.table(pd.DataFrame(korelasi_data))

with c2:
    st.subheader("📜 Tahapan KDD")
    st.markdown("""
    * **Data Cleaning**: Pembersihan data duplikat.
    * **Transformation**: Mapping 'smoker' ke angka 1 dan 0.
    * **Data Mining**: Melatih model *Linear Regression*.
    * **Knowledge Presentation**: Dashboard interaktif ini.
    """)

st.caption("Aplikasi ini merupakan hasil simulasi statistik berdasarkan data kesehatan historis.")