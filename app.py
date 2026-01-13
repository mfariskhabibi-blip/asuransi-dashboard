import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Analisis & Prediksi Biaya Asuransi",
    page_icon="🏥",
    layout="wide"
)

# 2. Judul Utama
st.title("🏥 Dashboard Analisis & Prediksi Biaya Asuransi")
st.markdown("""
Dashboard ini menyajikan hasil **Knowledge Discovery in Databases (KDD)** untuk memahami faktor risiko yang memengaruhi biaya medis nasabah.
""")

# 3. Sidebar untuk Input Prediksi
st.sidebar.header("Input Profil Nasabah")
usia = st.sidebar.slider("Usia (Tahun)", 18, 100, 25)
bmi = st.sidebar.slider("Indeks Massa Tubuh (BMI)", 10.0, 60.0, 24.0)
perokok = st.sidebar.selectbox("Status Merokok", ("Ya", "Tidak"))

# Logika Prediksi Sederhana
smoker_val = 1 if perokok == "Ya" else 0
estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
estimasi = max(0, estimasi)

# 4. Layout Utama (Dua Kolom)
col_grafik, col_prediksi = st.columns([1.5, 1])

with col_grafik:
    st.subheader("📊 Insight Data: Dampak Merokok")
    
    # Data simulasi berdasarkan temuan riset (KDD Insight)
    data_insight = {
        'Status': ['Bukan Perokok', 'Perokok'],
        'Rata-rata Biaya ($)': [8434, 32050]
    }
    df_insight = pd.DataFrame(data_insight)

    # Membuat Grafik Seaborn
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x='Status', y='Rata-rata Biaya ($)', data=df_insight, palette=['#3498db', '#e74c3c'], ax=ax)
    ax.set_title("Perbandingan Rata-rata Biaya Medis")
    ax.set_ylabel("Biaya dalam USD ($)")
    
    # Menampilkan grafik di Streamlit
    st.pyplot(fig)
    st.write("**Insight:** Perokok memiliki risiko biaya medis 4x lebih tinggi dibandingkan bukan perokok.")

with col_prediksi:
    st.subheader("🔮 Estimasi Biaya")
    st.write("Berdasarkan input profil nasabah:")
    
    # Menampilkan hasil estimasi dalam kotak metric
    st.metric(label="Total Estimasi Tagihan", value=f"${estimasi:,.2f}")
    
    # Pesan Rekomendasi
    if perokok == "Ya":
        st.error(f"Profil: Perokok, Usia {usia}, BMI {bmi}")
        st.warning("Gaya hidup merokok meningkatkan premi asuransi secara signifikan.")
    else:
        st.success(f"Profil: Bukan Perokok, Usia {usia}, BMI {bmi}")
        st.info("Premi asuransi Anda berada pada kategori risiko rendah.")

# 5. Tabel Korelasi & Metodologi
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Hubungan Faktor Risiko")
    data_korelasi = {
        'Faktor': ['Status Merokok', 'Usia', 'BMI'],
        'Kekuatan Korelasi': ['Sangat Kuat (0.78)', 'Sedang (0.30)', 'Lemah (0.20)']
    }
    st.table(pd.DataFrame(data_korelasi))

with c2:
    st.subheader("📜 Metodologi KDD")
    st.markdown("""
    1. **Data Cleaning:** Pembersihan data duplikat/kosong.
    2. **Transformation:** Normalisasi data kategori.
    3. **Data Mining:** Pemodelan menggunakan Linear Regression.
    4. **Knowledge:** Merokok adalah faktor biaya nomor satu.
    """)

st.caption("Aplikasi ini dibuat untuk tujuan simulasi edukasi berbasis data.")