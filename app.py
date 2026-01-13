import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# --- 1. SETTING HALAMAN (WAJIB DI ATAS) ---
st.set_page_config(page_title="Telco Churn Analytics Pro", layout="wide", page_icon="📡")

# --- 2. CUSTOM CSS (Agar tampilan tidak 'mentah') ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    h1 { color: #1e3d59; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce').fillna(0)
    return df

df = load_data()

# --- 4. PREPROCESSING & MODEL (KDD: Data Mining) ---
@st.cache_resource
def train_pro_model(data):
    df_m = data.copy()
    df_m.drop('customerID', axis=1, inplace=True)
    
    encoders = {}
    for col in df_m.columns:
        if df_m[col].dtype == 'object':
            le = LabelEncoder()
            df_m[col] = le.fit_transform(df_m[col])
            encoders[col] = le
            
    X = df_m.drop('Churn', axis=1)
    y = df_m['Churn']
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    importance = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
    return model, encoders, X.columns, importance

model, encoders, feature_cols, feat_importances = train_pro_model(df)

# --- 5. SIDEBAR NAVIGATION ---
st.sidebar.title("📡 Navigasi Panel")
menu = st.sidebar.radio("Pilih Tampilan:", ["Dashboard Ringkasan", "Sistem Prediksi AI"])

# --- 6. HALAMAN DASHBOARD ---
if menu == "Dashboard Ringkasan":
    st.title("📊 Customer Insight Dashboard")
    
    # Row 1: KPI Metrics
    c1, c2, c3, c4 = st.columns(4)
    churn_rate = (df['Churn'] == 'Yes').mean() * 100
    c1.metric("Total Pelanggan", f"{len(df):,}")
    c2.metric("Churn Rate", f"{churn_rate:.1f}%")
    c3.metric("Avg Monthly Bill", f"${df['MonthlyCharges'].mean():.2f}")
    c4.metric("Total Revenue", f"${df['TotalCharges'].sum()/1e6:.1f}M")

    st.markdown("---")

    # Row 2: Charts (Berdampingan)
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Dampak Kontrak terhadap Churn")
        fig1 = px.histogram(df, x="Contract", color="Churn", barmode="group",
                            color_discrete_map={'Yes':'#EF553B', 'No':'#636EFA'},
                            template="plotly_white")
        st.plotly_chart(fig1, use_container_width=True)

    with col_b:
        st.subheader("Analisis Tenure (Masa Langganan)")
        fig2 = px.box(df, x="Churn", y="tenure", color="Churn",
                      color_discrete_map={'Yes':'#EF553B', 'No':'#636EFA'})
        st.plotly_chart(fig2, use_container_width=True)

    # Row 3: Feature Importance
    st.subheader("Faktor Paling Berpengaruh (Feature Importance)")
    fig3 = px.bar(feat_importances.head(10), orientation='h', 
                  color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig3, use_container_width=True)

# --- 7. HALAMAN PREDIKSI ---
else:
    st.title("🔮 AI Churn Predictor")
    st.write("Gunakan simulator ini untuk mengevaluasi risiko churn pelanggan baru.")

    with st.container():
        st.markdown("### Masukkan Data Pelanggan")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            tenure = st.slider("Tenure (Bulan)", 0, 72, 12)
            contract = st.selectbox("Kontrak", df['Contract'].unique())
            monthly = st.number_input("Tagihan Bulanan ($)", value=65.0)
        
        with col2:
            internet = st.selectbox("Internet Service", df['InternetService'].unique())
            tech = st.selectbox("Tech Support", df['TechSupport'].unique())
            payment = st.selectbox("Metode Bayar", df['PaymentMethod'].unique())

        with col3:
            gender = st.selectbox("Gender", df['gender'].unique())
            multi = st.selectbox("Multiple Lines", df['MultipleLines'].unique())
            paperless = st.selectbox("Paperless Billing", df['PaperlessBilling'].unique())

    if st.button("MULAI ANALISIS PREDIKSI"):
        # Mapping input agar sesuai urutan training
        input_data = {col: 0 for col in feature_cols}
        input_data.update({
            'gender': gender, 'tenure': tenure, 'MonthlyCharges': monthly,
            'Contract': contract, 'InternetService': internet,
            'TechSupport': tech, 'PaymentMethod': payment,
            'PaperlessBilling': paperless, 'MultipleLines': multi,
            'TotalCharges': tenure * monthly
        })
        
        input_df = pd.DataFrame([input_data])

        # Encoding input
        for col, le in encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = le.transform([input_df[col][0]])
                except:
                    input_df[col] = 0

        # Prediksi
        prob = model.predict_proba(input_df[feature_cols])[0][1]
        
        # Display Result
        st.markdown("---")
        res1, res2 = st.columns([1, 2])
        
        with res1:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = prob * 100,
                title = {'text': "Skor Risiko %"},
                gauge = {'bar': {'color': "#EF553B" if prob > 0.5 else "#636EFA"}}))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with res2:
            if prob > 0.5:
                st.error(f"### STATUS: HIGH RISK ({(prob*100):.1f}%)")
                st.write("**Rekomendasi:** Berikan diskon retensi atau hubungi pelanggan segera.")
            else:
                st.success(f"### STATUS: LOW RISK ({(prob*100):.1f}%)")
                st.write("**Rekomendasi:** Pertahankan layanan dan tawarkan program upgrade.")