import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman (Menggunakan layout wide agar grafik terlihat jelas)
st.set_page_config(
    page_title="Analisis Biaya Asuransi",
    page_icon="🏥",
    layout="wide"
)

# 2. Judul dan Deskripsi
st.title("🏥 Dashboard Analisis & Prediksi Biaya Asuransi")
st.markdown("""
Dashboard ini menyajikan **Knowledge Presentation** dari hasil KDD. 
Sistem ini memprediksi biaya medis sekaligus menampilkan pola data yang ditemukan.
""")

st.divider()

# 3. Sidebar untuk Input Pengguna
st.sidebar.header("⚙️ Input Profil Nasabah")
usia = st.sidebar.slider("Usia (Tahun)", 18, 100, 25)
bmi = st.sidebar.slider("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# 4. Logika Prediksi (Berdasarkan Model di Google Colab)
smoker_val = 1 if perokok == "Ya" else 0
# Rumus Linear Regression hasil Data Mining
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
estimasi = max(0, estimasi) # Memastikan hasil tidak negatif

# 5. Tampilan Dashboard (Membagi menjadi 2 Kolom)
col_grafik, col_hasil = st.columns([1.5, 1])

with col_grafik:
    st.subheader("📊 Insight: Dampak Merokok")
    # Menyiapkan data insight untuk grafik
    data_insight = {
        'Status': ['Bukan Perokok', 'Perokok'],
        'Rata-rata Biaya ($)': [8434, 32050]
    }
    df_plot = pd.DataFrame(data_insight)
    
    # Membuat Grafik Batang
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=df_plot, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title("Perbandingan Rata-rata Biaya Medis (Hasil Mining)")
    
    # Menampilkan grafik ke Streamlit
    st.pyplot(fig)
    st.caption("Pengetahuan: Perokok terbukti memiliki beban biaya medis 4x lipat lebih tinggi.")

with col_hasil:
    st.subheader("🔮 Estimasi Hasil")
    st.write("Prediksi tagihan berdasarkan profil input:")
    
    # Menampilkan Metric Utama
    st.metric(label="Total Estimasi Tagihan", value=f"${estimasi:,.2f}")
    
    # Status Risiko
    if perokok == "Ya":
        st.error(f"⚠️ Profil Risiko Tinggi (Perokok)")
        st.caption("Faktor gaya hidup meningkatkan premi secara signifikan.")
    else:
        st.success(f"✅ Profil Risiko Rendah (Bukan Perokok)")
        st.caption("Biaya tetap rendah berkat pola hidup sehat.")

# 6. Informasi Metodologi KDD
st.divider()
with st.expander("🔍 Detail Metodologi (KDD Cycle)"):
    st.write("""
    * **Data Cleaning**: Menghilangkan outlier dan data duplikat.
    * **Transformation**: Mapping variabel kategori 'smoker' menjadi data biner (0/1).
    * **Data Mining**: Menerapkan algoritma Linear Regression untuk menemukan pola korelasi.
    * **Knowledge Presentation**: Visualisasi dashboard ini sebagai alat bantu pengambilan keputusan.
    """)

st.info("Catatan: Gunakan hasil ini sebagai referensi simulasi biaya medis berdasarkan model statistik.")