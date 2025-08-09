# check_importance.py

import joblib
import pandas as pd

# Daftar fitur yang sama persis seperti saat latihan
features = [
    'distance_km',
    'passenger_count',
    'hour_sin', 'hour_cos',
    'day_sin', 'day_cos'
]

print("Memuat model yang sudah dilatih...")

try:
    # Ganti nama file jika Anda menyimpannya dengan nama lain
    model = joblib.load('model_terbaik_final.joblib')
    
    # Cek apakah model punya atribut feature_importances_
    # (Model tree-based seperti RandomForest dan XGBoost punya ini)
    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        
        # Buat DataFrame untuk menampilkan hasilnya dengan rapi
        importance_df = pd.DataFrame({
            'Fitur': features,
            'Tingkat Kepentingan': importances
        })
        
        # Urutkan dari yang paling penting
        importance_df = importance_df.sort_values(by='Tingkat Kepentingan', ascending=False)
        
        print("\n--- Tingkat Kepentingan Fitur Menurut Model ---")
        print(importance_df)
        
    else:
        print(f"\nModel Anda (tipe: {type(model).__name__}) tidak memiliki atribut 'feature_importances_'.")
        print("Atribut ini biasanya ada pada model seperti RandomForest atau XGBoost.")

except FileNotFoundError:
    print("ERROR: File 'model_terbaik_final.joblib' tidak ditemukan.")
except Exception as e:
    print(f"Terjadi error: {e}")