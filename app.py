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

# 2. Header dengan Nama Anda
st.title("🏥 Dashboard Analisis & Prediksi Biaya Asuransi")
st.subheader("Oleh: Muhammad Faris Khabibi")
st.markdown("""
Aplikasi ini merupakan implementasi **Knowledge Presentation** dari siklus KDD. 
Data diolah untuk memprediksi biaya medis dan memberikan wawasan faktor risiko kesehatan.
""")

st.divider()

# 3. Sidebar untuk Input Pengguna (Data Transformation)
st.sidebar.header("⚙️ Input Profil Nasabah")
usia = st.sidebar.slider("Usia (Tahun)", 18, 100, 25)
bmi = st.sidebar.slider("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# 4. Logika Prediksi (Berdasarkan Model di Colab Anda)
# Konversi kategori ke numerik seperti pada proses di Colab 
smoker_val = 1 if perokok == "Ya" else 0
# Rumus Linear Regression berdasarkan tren data 
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
estimasi = max(0, estimasi)

# 5. Tampilan Utama Dashboard (Layout 2 Kolom)
col_grafik, col_hasil = st.columns([1.5, 1])

with col_grafik:
    st.subheader("📊 Grafik Insight: Perbandingan Biaya")
    
    # Data insight berdasarkan perbandingan perokok vs bukan perokok 
    df_plot = pd.DataFrame({
        'Status': ['Bukan Perokok', 'Perokok'],
        'Rata-rata Biaya ($)': [8434, 32050]
    })
    
    # Membuat visualisasi insight menggunakan Seaborn
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=df_plot, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title("Dampak Status Merokok Terhadap Biaya Medis")
    
    st.pyplot(fig)
    st.info("**Insight Utama:** Status merokok adalah faktor paling dominan yang menentukan mahalnya biaya.")

with col_hasil:
    st.subheader("🔮 Estimasi Prediksi")
    st.write("Hasil kalkulasi model untuk profil ini:")
    
    # Menampilkan hasil prediksi dalam box metric
    st.metric(label="Estimasi Tagihan Medis", value=f"${estimasi:,.2f}")
    
    # Status Risiko berdasarkan input
    if perokok == "Ya":
        st.error(f"Status: Perokok (Risiko Tinggi)")
        st.caption("Biaya meningkat tajam akibat risiko kesehatan gaya hidup.")
    else:
        st.success(f"Status: Bukan Perokok (Risiko Rendah)")
        st.caption("Biaya lebih stabil karena risiko medis lebih kecil.")

# 6. Analisis Korelasi (Sesuai Data Colab Anda)
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Evaluasi Pola (Korelasi)")
    st.write("Hubungan faktor terhadap biaya (charges):")
    korelasi_data = {
        'Faktor': ['Usia (Age)', 'BMI', 'Status Merokok'],
        'Kekuatan Korelasi': ['0.299', '0.198', 'Dominan']
    }
    st.table(pd.DataFrame(korelasi_data))

with c2:
    st.subheader("📜 Metodologi KDD")
    st.markdown("""
    * **Data Cleaning**: Menghapus data duplikat.
    * **Transformation**: Mapping 'smoker' ke angka biner (1/0).
    * **Data Mining**: Melatih model *Linear Regression*.
    * **Knowledge Presentation**: Dashboard interaktif oleh **Muhammad Faris Khabibi**.
    """)

st.caption("Aplikasi ini dibuat untuk tujuan simulasi statistik berbasis data medis historis.")