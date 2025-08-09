# pages/2_⚙️_Info_Teknologi.py
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
st.set_page_config(page_title="Info Teknologi", page_icon="⚙️")
st.title("⚙️ Info Teknologi di Balik Prediksi")
st.markdown("Aplikasi ini didukung oleh teknologi Machine Learning untuk memberikan hasil yang akurat.")

st.header("Model Machine Learning")
st.write("Prediksi tarif dihasilkan oleh sebuah model **Machine Learning** yang telah dilatih pada puluhan ribu data perjalanan Uber. Model terbaik yang digunakan adalah **Random Forest**, sebuah algoritma yang kuat untuk tugas regresi.")

st.subheader("Tingkat Akurasi")
# Gunakan skor R2 terbaru Anda
r2_score = 0.800
st.metric(label="Akurasi Model (R-squared)", value=f"{r2_score:.1%}")
st.caption("Skor R-squared 80.0% berarti model dapat menjelaskan sekitar 80% dari variasi harga tarif.")

st.subheader("Faktor Penentu Utama")
st.info("Berdasarkan analisis, faktor yang paling signifikan dalam menentukan tarif adalah **jarak perjalanan**. Ini berarti model kami bekerja secara logis, sama seperti cara kerja penetapan harga di dunia nyata.")