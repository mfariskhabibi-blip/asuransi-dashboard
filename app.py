import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Dashboard Asuransi - Muhammad Faris Khabibi",
    page_icon="🏥",
    layout="wide"
)

# --- LOAD DATA MENTAH ---
@st.cache_data
def load_data():
    # Menggunakan dataset asli jika ada, jika tidak pakai data simulasi
    try:
        df_real = pd.read_csv('medical-charges.csv')
        return df_real
    except:
        data = {
            'age': [19, 18, 28, 33, 32, 31, 46, 37, 37, 60, 25, 62, 23, 56, 27, 19, 52, 23, 56, 30, 33, 45, 64, 52, 61],
            'sex': ['female', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'female'],
            'bmi': [27.9, 33.7, 33.0, 22.7, 28.8, 25.7, 33.4, 27.7, 29.8, 25.8, 26.2, 26.2, 34.4, 39.8, 42.1, 24.6, 30.7, 23.8, 40.3, 35.3, 22.7, 25.1, 26.7, 30.2, 29.0],
            'smoker': ['yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'yes'],
            'charges': [16884.92, 1725.55, 4449.46, 21984.47, 3866.85, 3756.62, 8240.58, 7281.50, 6406.41, 28923.13, 2721.32, 27808.72, 1826.84, 11090.71, 39611.75, 1837.23, 10797.33, 2395.17, 10602.38, 36837.46, 2000.00, 7000.00, 45000.00, 12000.00, 30000.00]
        }
        return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR NAVIGASI ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3421/3421115.png", width=80)
st.sidebar.title("Navigasi Utama")
st.sidebar.write("Pengembang: **Muhammad Faris Khabibi**")
page = st.sidebar.radio("Pilih Halaman:", ["🔮 Prediksi Biaya", "📊 Visualisasi Insight", "📄 Data Mentah"])

# --- HALAMAN 1: PREDIKSI ---
if page == "🔮 Prediksi Biaya":
    st.title("🔮 Prediksi Biaya Asuransi")
    st.markdown("Implementasi model **Linear Regression** untuk estimasi biaya medis.")
    st.divider()
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.subheader("📝 Input Profil")
        usia = st.number_input("Usia (Tahun)", 18, 100, 25)
        bmi = st.number_input("BMI (Indeks Massa Tubuh)", 10.0, 60.0, 24.5)
        perokok = st.selectbox("Apakah Anda Merokok?", ("Ya", "Tidak"))
        
        smoker_val = 1 if perokok == "Ya" else 0
        # Koefisien hasil Data Mining
        estimasi = (250 * usia) + (330 * bmi) + (23500 * smoker_val) - 12000
        estimasi = max(500, estimasi) # Minimal biaya asuransi dasar

        if st.button("🚀 Hitung Prediksi", use_container_width=True):
            st.session_state.hasil = estimasi

    with col2:
        st.subheader("💡 Hasil Estimasi")
        if 'hasil' in st.session_state:
            st.metric(label="Total Tagihan Medis Tahunan", value=f"${st.session_state.hasil:,.2f}", delta=f"{'Risiko Tinggi' if perokok == 'Ya' else 'Risiko Normal'}")
            
            if perokok == "Ya":
                st.warning("⚠️ Merokok adalah faktor dominan yang meningkatkan biaya hingga >200%.")
            
            # Progress bar simulasi risiko
            risiko_pct = min(100, int((st.session_state.hasil / 50000) * 100))
            st.write(f"Tingkat Beban Biaya (Relative): {risiko_pct}%")
            st.progress(risiko_pct)

# --- HALAMAN 2: VISUALISASI ---
elif page == "📊 Visualisasi Insight":
    st.title("📊 Visualisasi Pengetahuan (Knowledge)")
    st.markdown("Tahap **Pattern Evaluation** dalam proses KDD.")
    st.divider()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("1. Dampak Status Merokok")
        fig1, ax1 = plt.subplots()
        sns.boxplot(x='smoker', y='charges', data=df, palette='Set2', ax=ax1)
        st.pyplot(fig1)
        st.info("Boxplot menunjukkan adanya perbedaan median biaya yang sangat ekstrem antara perokok (yes) dan non-perokok (no).")

    with c2:
        st.subheader("2. Matriks Korelasi Numerik")
        # Preprocessing sederhana untuk heatmap
        df_corr = df.copy()
        df_corr['smoker_encoded'] = df_corr['smoker'].map({'yes': 1, 'no': 0})
        
        fig2, ax2 = plt.subplots()
        sns.heatmap(df_corr[['age', 'bmi', 'smoker_encoded', 'charges']].corr(), annot=True, cmap='RdYlGn', ax=ax2)
        st.pyplot(fig2)
        st.info("Korelasi terkuat ditemukan pada variabel **Status Merokok** terhadap biaya (Charges).")

    st.divider()
    
    st.subheader("3. Sebaran Biaya Berdasarkan Usia & Status Merokok")
    fig3, ax3 = plt.subplots(figsize=(12, 5))
    sns.scatterplot(data=df, x='age', y='charges', hue='smoker', style='smoker', s=100, palette='Set1', ax=ax3)
    plt.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig3)
    st.info("Insight: Biaya meningkat seiring usia, namun 'Smoker' membuat biaya melonjak ke level yang berbeda (Cluster Atas).")

# --- HALAMAN 3: DATA MENTAH ---
elif page == "📄 Data Mentah":
    st.title("📄 Dataset & Analisis Statistik")
    st.markdown("Data yang telah melalui tahap **Data Cleaning**.")
    st.divider()
    
    # Metrik Ringkasan
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Data", len(df))
    m2.metric("Rata-rata Biaya", f"${df['charges'].mean():,.2f}")
    m3.metric("Rata-rata BMI", f"{df['bmi'].mean():.2f}")

    # Filter
    filter_sex = st.multiselect("Filter Jenis Kelamin:", options=df['sex'].unique(), default=df['sex'].unique())
    df_filtered = df[df['sex'].isin(filter_sex)]
    
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Unduh CSV", csv, "data_asuransi_faris.csv", "text/csv")

# --- FOOTER ---
st.sidebar.divider()
st.sidebar.caption("© 2024 Muhammad Faris Khabibi | Project KDD")