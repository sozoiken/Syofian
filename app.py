# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from geopy.geocoders import Nominatim
import folium
from streamlit_folium import folium_static
from haversine import haversine

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Prediktor Tarif Uber", page_icon="🚕", layout="centered")
# GANTI seluruh blok sidebar Anda dengan ini di SETIAP file .py

# --- Elemen Sidebar ---
# 1. Video diletakkan di bagian paling atas
st.sidebar.video("https://www.youtube.com/watch?v=J_Wk9aAkcno",autoplay=True, loop=True)

# 2. Garis pemisah untuk merapikan
st.sidebar.divider() 

# 3. Logo dan judul diletakkan di bawah video
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/cc/Uber_logo_2018.png", use_container_width=True)
st.sidebar.title("Navigasi Proyek")

# --- Fungsi dan Pemuatan Aset ---
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('model_terbaik_final.joblib')
        scaler = joblib.load('scaler.joblib')
        geolocator = Nominatim(user_agent="uber_fare_predictor_app")
        return model, scaler, geolocator
    except FileNotFoundError:
        return None, None, None

def load_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "<p>Error: File komponen HTML tidak ditemukan.</p>"

model, scaler, geolocator = load_assets()

# --- Tampilan Utama ---
st.title("🚕 Prediktor Tarif Uber NYC")
st.markdown("Selamat datang! Dapatkan estimasi biaya perjalanan Anda di New York City.")

video_html = load_html_file("components/video_component.html")
st.markdown(video_html, unsafe_allow_html=True)

st.markdown("Gunakan **sidebar di kiri** untuk melihat panduan pengguna dan informasi lainnya.")
st.divider()

if model is None or scaler is None:
    st.error("Gagal memuat model. Pastikan file `.joblib` ada di repository.")
else:
    popular_locations = ["Times Square, NY", "JFK Airport, NY", "LaGuardia Airport, NY", "Central Park, NY", "Empire State Building, NY", "Grand Central Terminal, NY", "Penn Station, NY", "Brooklyn Bridge, NY"]
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            pickup_location_str = st.selectbox("Lokasi Penjemputan:", options=popular_locations, index=0)
            pickup_date = st.date_input("Tanggal", datetime.now())
        with col2:
            dropoff_location_str = st.selectbox("Lokasi Tujuan:", options=popular_locations, index=1)
            pickup_time = st.time_input("Waktu", datetime.now().time())
        passengers = st.number_input("Jumlah Penumpang", min_value=1, max_value=6, value=1, step=1)
        submit_button = st.form_submit_button(label='Dapatkan Estimasi Tarif')

    if submit_button:
        if pickup_location_str == dropoff_location_str:
            st.warning("Lokasi penjemputan dan tujuan tidak boleh sama.")
        else:
            with st.spinner("Mencari lokasi dan menghitung..."):
                try:
                    pickup_location = geolocator.geocode(pickup_location_str)
                    dropoff_location = geolocator.geocode(dropoff_location_str)
                    if pickup_location and dropoff_location:
                        pickup_coords = (pickup_location.latitude, pickup_location.longitude)
                        dropoff_coords = (dropoff_location.latitude, dropoff_location.longitude)
                        distance = haversine(pickup_coords, dropoff_coords)
                        pickup_datetime = datetime.combine(pickup_date, pickup_time)
                        
                        hour, day_of_week = pickup_datetime.hour, pickup_datetime.weekday()
                        hour_sin, hour_cos = np.sin(2*np.pi*hour/24), np.cos(2*np.pi*hour/24)
                        day_sin, day_cos = np.sin(2*np.pi*day_of_week/7), np.cos(2*np.pi*day_of_week/7)
                        features = pd.DataFrame([{'distance_km': distance, 'passenger_count': passengers, 'hour_sin': hour_sin, 'hour_cos': hour_cos, 'day_sin': day_sin, 'day_cos': day_cos}])
                        scaled_features = scaler.transform(features)
                        prediction = model.predict(scaled_features)[0]

                        st.success(f"**Estimasi Tarif: ${prediction:.2f}** | **Estimasi Jarak: {distance:.2f} km**")
                        m = folium.Map(location=pickup_coords, zoom_start=13)
                        folium.Marker(pickup_coords, popup="Penjemputan", icon=folium.Icon(color='green')).add_to(m)
                        folium.Marker(dropoff_coords, popup="Tujuan", icon=folium.Icon(color='red')).add_to(m)
                        folium_static(m, height=350)
                        # --- EFEK SALJU TETAP DI SINI ---
                        st.snow()
                        # --- AKHIR EFEK SALJU ---
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")
