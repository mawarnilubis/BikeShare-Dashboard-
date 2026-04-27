# Bike Sharing Analysis Dashboard

Dashboard ini merupakan proyek akhir analisis data untuk mengeksplorasi tren penyewaan sepeda menggunakan Bike Sharing Dataset. Proyek ini mencakup seluruh siklus analisis data, mulai dari *Data Wrangling*, *Exploratory Data Analysis* (EDA), hingga visualisasi interaktif menggunakan Streamlit.

## Deskripsi Proyek
Analisis ini bertujuan untuk memberikan wawasan strategis mengenai faktor-faktor yang memengaruhi jumlah penyewaan sepeda harian. Fokus utama proyek ini adalah:
- **Analisis Lingkungan:** Dampak cuaca dan suhu terhadap volume penyewaan.
- **Analisis Perilaku:** Perbedaan pola antara pengguna *Casual* dan *Registered*.
- **Analisis Lanjutan:** Pengelompokan manual (*Manual Clustering*) berdasarkan suhu untuk strategi operasional.

## Struktur Direktori
submission
├── dashboard
│   ├── dashboard.py      
│   └── main_data.csv      
├── data
│   ├── day.csv          
│   └── hour.csv          
├── notebook.ipynb         
├── requirements.txt      
└── README.md             

## Setup Environment
1. Membuat Virtual Environment (Disarankan)
Bash
# Untuk Windows
python -m venv venv
.\venv\Scripts\activate

# Untuk Mac/Linux
python -m venv venv
source venv/bin/activate
2. Instalasi Library
Install semua dependensi dengan menjalankan perintah berikut:

Bash
pip install -r requirements.txt
Pastikan library scipy terinstall karena diperlukan untuk analisis statistik tingkat lanjut.

## Cara Menjalankan Dashboard
Pastikan Anda berada di direktori dashboard/ atau folder utama tempat file berada.

Jalankan perintah berikut di terminal/command prompt:

Bash
streamlit run dashboard.py
Dashboard akan terbuka secara otomatis di browser Anda pada alamat http://localhost:8501.

⚠️ Catatan Penting
Jika muncul error pada bagian Advanced Analysis, pastikan sudah menginstall:
pip install scipy

## Pertanyaan Bisnis & Insight Utama
1. Bagaimana pengaruh kondisi lingkungan terhadap penyewaan?
Cuaca: Penyewaan mencapai angka tertinggi pada cuaca Cerah/Misty (rata-rata ~4.876 unit). Sebaliknya, cuaca ekstrem menurunkan minat pengguna secara drastis.

Suhu: Terdapat korelasi positif yang kuat (0.63). Semakin hangat suhu (dalam batas wajar), semakin tinggi permintaan penyewaan sepeda.

2. Apa perbedaan pola pengguna Casual vs Registered?
Registered (Komuter): Menunjukkan pola stabil pada hari kerja (Senin-Jumat). Puncak penggunaan terjadi pada jam berangkat dan pulang kantor, menandakan sepeda digunakan sebagai transportasi utama.

Casual (Rekreasi): Mengalami lonjakan signifikan pada akhir pekan (Sabtu-Minggu), yang mengindikasikan penggunaan untuk tujuan wisata atau rekreasi.

3. Analisis Lanjutan: Cluster Suhu (Hot, Warm, Cold)
Normal (Warm): Kondisi suhu paling optimal di mana jumlah penyewaan berada di titik tertinggi.

Panas (Hot): Penyewaan tetap tinggi namun mulai mengalami perlambatan/stagnasi akibat faktor kenyamanan udara.

Dingin (Cold): Penurunan drastis pada volume penyewaan; suhu rendah menjadi hambatan utama aktivitas luar ruangan.

Kesimpulan & Rekomendasi
Optimasi Stok: Menambah unit sepeda di area rekreasi saat akhir pekan untuk melayani pengguna Casual.

Maintenance: Melakukan perawatan rutin pada hari Selasa atau Rabu karena secara statistik memiliki volume penyewaan terendah.

Strategi Marketing: Memberikan promo khusus atau insentif pada saat cluster suhu dingin untuk menjaga stabilitas jumlah penyewaan.