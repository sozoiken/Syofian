# pages/1_💡_Panduan_Pengguna.py
import streamlit as st
# GANTI seluruh blok sidebar Anda dengan ini di SETIAP file .py

# --- Elemen Sidebar ---
# 1. Video diletakkan di bagian paling atas
st.sidebar.video("https://www.youtube.com/watch?v=J_Wk9aAkcno",autoplay=True, loop=True)

# 2. Garis pemisah untuk merapikan
st.sidebar.divider() 

# 3. Logo dan judul diletakkan di bawah video
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png", use_container_width=True)
st.sidebar.title("Navigasi Proyek")

st.set_page_config(page_title="Panduan Pengguna", page_icon="💡")
st.title("💡 Panduan Pengguna")
st.info("Tujuan utama aplikasi ini adalah untuk memberikan **estimasi biaya perjalanan** menggunakan layanan Uber di area New York City berdasarkan data historis.")

st.header("Cara Menggunakan Halaman Utama")
st.markdown("""
Aplikasi ini sangat mudah digunakan. Ikuti langkah-langkah berikut di halaman **'Prediktor Tarif'**:

1.  **Pilih Lokasi:** Gunakan menu dropdown untuk memilih lokasi penjemputan dan tujuan Anda dari daftar tempat-tempat populer di NYC.
2.  **Atur Detail Perjalanan:** Pilih tanggal, waktu penjemputan, dan jumlah penumpang.
3.  **Dapatkan Estimasi:** Klik tombol **'Dapatkan Estimasi Tarif'**.

Aplikasi akan menampilkan estimasi tarif, perkiraan jarak, dan peta rute perjalanan Anda.
""")
# Ganti dengan kode ini:
import folium
from streamlit_folium import folium_static

st.header("Area Jangkauan Prediksi")
st.markdown("Model ini dioptimalkan untuk perjalanan di dalam area utama New York City dan sekitarnya.")

# Buat peta yang berpusat di NYC
m = folium.Map(location=[40.7128, -74.0060], zoom_start=11)

# Tampilkan peta di aplikasi
folium_static(m, height=300)
