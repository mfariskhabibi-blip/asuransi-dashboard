import streamlit as st
import pandas as pd

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Prediksi Biaya Asuransi",
    page_icon="🏥",
    layout="centered"
)

# 2. Judul dan Deskripsi
st.title("🏥 Dashboard Prediksi Biaya Asuransi")
st.markdown("""
Aplikasi ini merupakan hasil akhir dari proses **Knowledge Discovery in Databases (KDD)**. 
Gunakan panel di sebelah kiri untuk memasukkan data nasabah dan melihat estimasi biaya medis secara real-time.
""")

st.divider()

# 3. Sidebar untuk Input Pengguna
st.sidebar.header("Input Profil Nasabah")

usia = st.sidebar.slider("Usia (Tahun)", 18, 100, 25)
bmi = st.sidebar.slider("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# 4. Logika Prediksi (Linear Regression)
# Menggunakan koefisien yang ditemukan saat tahap Data Mining di Google Colab
smoker_val = 1 if perokok == "Ya" else 0
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000

# Memastikan hasil prediksi tidak negatif
if estimasi < 0:
    estimasi = 0

# 5. Menampilkan Hasil Prediksi
st.subheader("Hasil Estimasi Biaya")

# Menggunakan kolom untuk tampilan yang lebih rapi
col1, col2 = st.columns([1, 1])

with col1:
    st.metric(label="Total Estimasi Tagihan", value=f"${estimasi:,.2f}")

with col2:
    if perokok == "Ya":
        st.error("⚠️ Status Perokok")
        st.caption("Biaya meningkat signifikan karena faktor gaya hidup.")
    else:
        st.success("✅ Bukan Perokok")
        st.caption("Biaya lebih rendah karena risiko kesehatan lebih kecil.")

# 6. Informasi Tambahan untuk Laporan
st.divider()
with st.expander("Lihat Detail Metodologi (KDD)"):
    st.write("""
    - **Data Cleaning:** Menghapus data kosong dan duplikat.
    - **Transformation:** Mapping 'Smoker' ke angka 1 (Ya) dan 0 (Tidak).
    - **Data Mining:** Menggunakan algoritma Linear Regression.
    - **Knowledge:** Ditemukan bahwa status merokok adalah faktor paling dominan terhadap biaya.
    """)

st.info("Catatan: Angka ini adalah hasil estimasi berdasarkan model statistik dan digunakan untuk tujuan simulasi.")
