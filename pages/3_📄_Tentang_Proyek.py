# pages/3_📄_Tentang_Proyek.py
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
st.set_page_config(page_title="Tentang Proyek", page_icon="📄")

st.title("📄 Tentang Proyek Ini")

# Menampilkan logo Uber langsung dari URL
st.image("https://st3.depositphotos.com/7186692/37747/i/1600/depositphotos_377471254-stock-photo-sao-paulo-brazil-august-2019.jpg", width=150)

st.markdown("""
Aplikasi ini merupakan Proyek Akhir untuk mata kuliah **Modern Prediction and Machine Learning (MPML)**.

**Tujuan Proyek:**
- Menganalisis dataset historis perjalanan Uber di New York City.
- Membangun model machine learning yang akurat untuk memprediksi tarif perjalanan.
- Men-deploy model ke dalam sebuah aplikasi web interaktif menggunakan Streamlit.

**Dataset:**
- Dataset yang digunakan adalah "Uber Fares Dataset" yang tersedia secara publik di platform Kaggle.

**Dibuat oleh:**
- **[Muhammad Syofian]**
- **[23611064]**
- **[Program Studi Statistika / Universitas Islam Indonesia]**
""")