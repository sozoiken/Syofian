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
st.set_page_config(
    page_title="Prediksi Tarif Uber NYC",
    page_icon="🚕",
    layout="wide"
)

# --- Fungsi dan Pemuatan Model ---
@st.cache_resource
def load_model_and_scaler():
    try:
        model = joblib.load('model_terbaik_final.joblib')
        scaler = joblib.load('scaler.joblib')
        return model, scaler
    except FileNotFoundError:
        return None, None

@st.cache_resource
def get_geocoder():
    return Nominatim(user_agent="uber_fare_predictor")

model, scaler = load_model_and_scaler()
geolocator = get_geocoder()

def predict_fare(pickup_datetime, distance_km, passenger_count):
    hour, day_of_week = pickup_datetime.hour, pickup_datetime.weekday()
    hour_sin, hour_cos = np.sin(2 * np.pi * hour / 24.0), np.cos(2 * np.pi * hour / 24.0)
    day_sin, day_cos = np.sin(2 * np.pi * day_of_week / 7.0), np.cos(2 * np.pi * day_of_week / 7.0)

    features_dict = {
        'distance_km': [distance_km], 'passenger_count': [passenger_count],
        'hour_sin': [hour_sin], 'hour_cos': [hour_cos],
        'day_sin': [day_sin], 'day_cos': [day_cos]
    }
    input_df = pd.DataFrame(features_dict)
    input_scaled = scaler.transform(input_df)
    prediction = model.predict(input_scaled)
    return prediction[0]

# --- Antarmuka Pengguna (UI) ---
st.title("🚕 Prediksi Tarif Uber di New York City")
st.markdown("Pilih lokasi penjemputan dan tujuan dari daftar di bawah untuk mendapatkan estimasi tarif.")

if model is None or scaler is None:
    st.error("File model atau scaler tidak ditemukan. Harap pastikan file tersebut ada di direktori yang sama.")
else:
    # --- [ BAGIAN YANG DIPERBARUI ] ---
    # Daftar lokasi populer di NYC untuk dropdown
    popular_locations = [
        "JFK Airport, NY",
        "LaGuardia Airport, NY",
        "Times Square, Manhattan, NY",
        "Central Park, NY",
        "Empire State Building, NY",
        "Grand Central Terminal, NY",
        "Penn Station, NY",
        "Statue of Liberty, NY",
        "Brooklyn Bridge, NY",
        "Wall Street, NY",
        "SoHo, Manhattan, NY",
        "Greenwich Village, NY"
    ]

    # --- Formulir Input ---
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        with col1:
            # Ganti st.text_input menjadi st.selectbox
            pickup_location_str = st.selectbox("Pilih Lokasi Penjemputan:", options=popular_locations, index=2) # Default ke Times Square
            pickup_date = st.date_input("Tanggal Penjemputan", datetime.now())
            passengers = st.number_input("Jumlah Penumpang", min_value=1, max_value=6, value=1, step=1)

        with col2:
            # Ganti st.text_input menjadi st.selectbox
            dropoff_location_str = st.selectbox("Pilih Lokasi Tujuan:", options=popular_locations, index=0) # Default ke JFK Airport
            pickup_time = st.time_input("Waktu Penjemputan", datetime.now().time())

        submit_button = st.form_submit_button(label='Prediksi Tarif dan Tampilkan Peta')
    # --- [ AKHIR BAGIAN PEMBARUAN ] ---

    if submit_button:
        if pickup_location_str == dropoff_location_str:
            st.warning("Lokasi penjemputan dan tujuan tidak boleh sama.")
        else:
            with st.spinner("Mencari lokasi dan menghitung tarif..."):
                try:
                    pickup_location = geolocator.geocode(pickup_location_str)
                    dropoff_location = geolocator.geocode(dropoff_location_str)

                    if pickup_location and dropoff_location:
                        nyc_bounds = ((-75, -73), (40, 42))
                        is_pickup_valid = nyc_bounds[0][0] <= pickup_location.longitude <= nyc_bounds[0][1] and \
                                          nyc_bounds[1][0] <= pickup_location.latitude <= nyc_bounds[1][1]
                        is_dropoff_valid = nyc_bounds[0][0] <= dropoff_location.longitude <= nyc_bounds[0][1] and \
                                           nyc_bounds[1][0] <= dropoff_location.latitude <= nyc_bounds[1][1]

                        if is_pickup_valid and is_dropoff_valid:
                            st.info(f"Lokasi Penjemputan ditemukan: {pickup_location.address}\n"
                                    f"Lokasi Tujuan ditemukan: {dropoff_location.address}")
                            pickup_coords = (pickup_location.latitude, pickup_location.longitude)
                            dropoff_coords = (dropoff_location.latitude, dropoff_location.longitude)
                            distance = haversine(pickup_coords, dropoff_coords)
                            pickup_datetime = datetime.combine(pickup_date, pickup_time)
                            prediction = predict_fare(pickup_datetime, distance, passengers)
                            
                            st.success(f"**Estimasi Jarak: {distance:.2f} km**")
                            st.success(f"**Estimasi Tarif: ${prediction:.2f}**")

                            m = folium.Map(location=pickup_coords, zoom_start=13)
                            folium.Marker(pickup_coords, popup="Penjemputan", icon=folium.Icon(color='green')).add_to(m)
                            folium.Marker(dropoff_coords, popup="Tujuan", icon=folium.Icon(color='red')).add_to(m)
                            folium.PolyLine([pickup_coords, dropoff_coords], color="blue", weight=2.5, opacity=1).add_to(m)
                            
                            st.markdown("### Peta Rute Perjalanan")
                            folium_static(m, width=800)
                            st.snow()
                        else:
                            st.error("Satu atau kedua lokasi berada di luar jangkauan data (area New York City).")
                    else:
                        st.error("Gagal menemukan satu atau kedua lokasi.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan: {e}")

st.markdown("---")
st.markdown("Dibuat untuk Proyek UAS MPML 2025.")