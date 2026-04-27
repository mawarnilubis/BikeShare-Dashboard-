import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import os
import numpy as np
from scipy.stats import gaussian_kde

# ─────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────
# CUSTOM CSS (Dark Theme & Styling)
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.stApp { background-color: #0D0F14; color: #E8E6E1; }
[data-testid="stSidebar"] { background: #13161E !important; border-right: 1px solid rgba(0,198,184,0.15) !important; }
[data-testid="stSidebar"] * { color: #C8C6C1 !important; }
[data-testid="stSidebar"] h1 { color: #00C6B8 !important; font-size: 1.1rem !important; font-weight: 800 !important; }
[data-testid="stSidebar"] label { color: #888 !important; font-size: 0.78rem !important; text-transform: uppercase !important; }
h1 { font-size: 2rem !important; font-weight: 800 !important; color: #E8E6E1 !important; }
h2, h3, .stSubheader { font-size: 0.85rem !important; font-weight: 700 !important; text-transform: uppercase !important; color: #888 !important; margin-top: 2rem !important; }

/* Metric Styling */
[data-testid="stMetric"] { background: #13161E; border: 1px solid rgba(0,198,184,0.15); border-left: 3px solid #00C6B8; border-radius: 12px; padding: 1.25rem 1.5rem !important; }
[data-testid="stMetricLabel"] { font-size: 0.72rem !important; text-transform: uppercase !important; color: #666 !important; }
[data-testid="stMetricValue"] { font-family: 'DM Mono', monospace !important; font-size: 1.9rem !important; color: #E8E6E1 !important; }

.stPlotlyChart { background: #13161E; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 0.5rem; }
hr { border-top: 1px solid rgba(0,198,184,0.12) !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────
def create_daily_rentals_df(df):
    return df.resample(rule='D', on='dteday').agg({"cnt": "sum"}).reset_index()

def create_byweather_df(df):
    return df.groupby(by="weathersit").cnt.mean().reset_index()

def create_user_type_per_day_df(df):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    if df['weekday'].dtype != 'object':
        day_mapping = {0: 'Sunday', 1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}
        df['day_name'] = df['weekday'].map(day_mapping)
    else:
        df['day_name'] = df['weekday']

    user_df = df.groupby('day_name').agg({
        'casual': 'mean',
        'registered': 'mean'
    }).reindex(day_order).reset_index()
    return user_df

def create_temp_cluster_df(df):
    def cluster_temp(temp):
        if temp < 0.3:
            return 'Dingin (Cold)'
        elif 0.3 <= temp < 0.6:
            return 'Normal (Warm)'
        else:
            return 'Panas (Hot)'
    
    df_copy = df.copy()
    df_copy['temp_cluster'] = df_copy['temp'].apply(cluster_temp)
    temp_cluster_df = df_copy.groupby('temp_cluster').agg({
        'cnt': 'mean'
    }).reindex(['Dingin (Cold)', 'Normal (Warm)', 'Panas (Hot)']).reset_index()
    return temp_cluster_df

def create_rfm_df(df):
    rfm_df = df.groupby(by="dteday", as_index=False).agg({"cnt": "sum"})
    rfm_df.columns = ["date", "total_rental"]
    recent_date = df["dteday"].max()
    rfm_df["recency"] = rfm_df["date"].apply(lambda x: (recent_date - x).days)
    return rfm_df

# ─────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────
try:
    main_df = pd.read_csv("main_data.csv")
    main_df["dteday"] = pd.to_datetime(main_df["dteday"])
except FileNotFoundError:
    st.error("File 'main_data.csv' tidak ditemukan. Pastikan file berada di folder yang sama.")
    st.stop()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.title("Bike Sharing Analysis 🚲")
    
    min_date, max_date = main_df["dteday"].min(), main_df["dteday"].max()
    
    date_range = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

    if isinstance(date_range, (tuple, list)):
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date = end_date = date_range[0]
    else:
        start_date = end_date = date_range

    st.markdown("---")
    st.caption("DIBUAT OLEH")
    st.markdown("**Mawarni Lubis**")
    st.caption("Data Science | Dicoding")

# Filter Data
main_df_filtered = main_df[(main_df["dteday"] >= str(start_date)) & (main_df["dteday"] <= str(end_date))]

# Data siap visualisasi
daily_rentals_df = create_daily_rentals_df(main_df_filtered)
byweather_df = create_byweather_df(main_df_filtered)
user_type_day_df = create_user_type_per_day_df(main_df_filtered)
temp_cluster_df = create_temp_cluster_df(main_df_filtered)
rfm_df = create_rfm_df(main_df_filtered)

# ─────────────────────────────────────────
# MAIN PAGE
# ─────────────────────────────────────────
st.markdown("<h1>Bike<span style='color:#00C6B8;'>Share</span> Dashboard 🚲</h1>", unsafe_allow_html=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Penyewaan", value=f"{main_df_filtered.cnt.sum():,}")
col2.metric("Rata-rata Harian", value=f"{round(main_df_filtered.cnt.mean(), 2)}")
col3.metric("Hari Terpilih", value=f"{len(daily_rentals_df):,}")
col4.metric("Puncak Harian", value=f"{int(daily_rentals_df.cnt.max()) if not daily_rentals_df.empty else 0:,}")

st.markdown("---")

# Visualisasi
st.subheader("Daily Rentals Trend")
fig_trend = px.line(daily_rentals_df, x="dteday", y="cnt", color_discrete_sequence=["#00C6B8"])
fig_trend.update_layout(paper_bgcolor="#13161E", plot_bgcolor="#13161E", font_color="#C8C6C1", height=300)
st.plotly_chart(fig_trend, use_container_width=True)

c1, c2 = st.columns(2)
with c1:
    st.subheader("Casual vs Registered per Hari")
    fig_user = px.bar(user_type_day_df, x="day_name", y=["casual", "registered"], barmode="group", color_discrete_sequence=["#00C6B8", "#888780"])
    fig_user.update_layout(paper_bgcolor="#13161E", plot_bgcolor="#13161E", font_color="#C8C6C1", height=350)
    st.plotly_chart(fig_user, use_container_width=True)

with c2:
    st.subheader("Rata-rata per Cuaca")
    fig_weather = px.bar(byweather_df, x="cnt", y="weathersit", orientation='h', color_discrete_sequence=["#00C6B8"])
    fig_weather.update_layout(paper_bgcolor="#13161E", plot_bgcolor="#13161E", font_color="#C8C6C1", height=350)
    st.plotly_chart(fig_weather, use_container_width=True)

st.subheader("Advanced Analysis: Pengaruh Suhu (Manual Clustering)")
fig_temp = px.bar(temp_cluster_df, x="temp_cluster", y="cnt", color="cnt", color_continuous_scale="Viridis")
fig_temp.update_layout(paper_bgcolor="#13161E", plot_bgcolor="#13161E", font_color="#C8C6C1", height=350)
st.plotly_chart(fig_temp, use_container_width=True)

# ─────────────────────────────────────────
# CONCLUSION & RECOMMENDATION (VERSI LENGKAP)
# ─────────────────────────────────────────
st.markdown("---")
st.subheader("Conclusion & Recommendation")

tabs = st.tabs(["📊 Analisis Lingkungan", "👥 Analisis Pengguna", "💡 Rekomendasi Utama", "🔥 Analisis Lanjutan (Suhu)"])

with tabs[0]:
    st.markdown("""
    **Kesimpulan: Pengaruh Cuaca & Suhu**
    * Penyewaan sepeda mencapai puncaknya pada cuaca **Cerah/Misty**.
    * Curah hujan atau cuaca ekstrem (Heavy Rain/Snow) menurunkan minat pengguna secara drastis hingga ke titik terendah.
    * Terdapat korelasi linear antara suhu dan jumlah penyewaan hingga titik panas tertentu.
    """)

with tabs[1]:
    st.markdown("""
    **Kesimpulan: Perilaku Pengguna**
    * **Registered (Komuter):** Menunjukkan pola penggunaan yang stabil pada hari kerja (Senin-Jumat). Sepeda digunakan sebagai alat transportasi utama menuju tempat kerja/sekolah.
    * **Casual (Rekreasi):** Mengalami lonjakan tajam pada akhir pekan (Sabtu-Minggu). Kelompok ini sangat sensitif terhadap hari libur dan cuaca.
    """)

with tabs[2]:
    st.markdown("""
    **Rekomendasi Strategis:**
    1. **Manajemen Armada:** Distribusikan lebih banyak sepeda ke titik-titik wisata atau taman kota pada hari Jumat malam untuk menyambut lonjakan pengguna *Casual* di akhir pekan.
    2. **Program Retensi:** Berikan promo konversi dari *Casual* ke *Registered* bagi mereka yang sering menyewa di akhir pekan agar mulai menggunakan sepeda di hari kerja.
    3. **Operasional:** Jadwalkan perawatan rutin sepeda pada hari Selasa atau Rabu, karena secara statistik volume penyewaan berada di titik paling rendah.
    """)

with tabs[3]:
    st.markdown("""
    **Analisis Lanjutan: Dampak Cluster Suhu**
    * **Normal (Warm):** Kondisi paling ideal. Rata-rata penyewaan tertinggi terjadi pada rentang suhu ini karena kenyamanan maksimal bagi pengendara.
    * **Panas (Hot):** Meskipun penyewaan tetap tinggi, pertumbuhannya mulai melambat atau cenderung stabil dibandingkan cluster *Warm*. Pengguna mungkin mulai menghindari paparan panas yang berlebih di tengah hari.
    * **Dingin (Cold):** Penurunan drastis pada volume penyewaan. Suhu rendah menjadi penghambat fisik utama bagi pengguna.
    
    **Rekomendasi Berbasis Suhu:**
    - **Hot Weather:** Sediakan fasilitas peneduh di stasiun sepeda atau berikan promo khusus di jam-jam pagi/sore yang lebih sejuk.
    - **Cold Weather:** Berikan diskon "Winter Sale" atau insentif poin tambahan untuk menjaga loyalitas pengguna selama musim dingin.
    """)

st.caption("2026")