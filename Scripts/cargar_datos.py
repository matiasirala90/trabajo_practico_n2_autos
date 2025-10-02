import pandas as pd
import sqlite3

# Cargar CSV
df = pd.read_csv("data\car_sales_data.csv")

# Renombrar columnas
df.rename(columns={
    "Manufacturer": "manufacturer",
    "Model": "model",
    "Engine size": "engine_size",
    "Fuel type": "fuel_type",
    "Year of manufacture": "year_of_manufacture",
    "Mileage": "mileage",
    "Price": "price"
}, inplace=True)

# Conectar a SQLite
conn = sqlite3.connect("autos.db")

# Crear tabla (si no existe)
conn.execute("""
CREATE TABLE IF NOT EXISTS car_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT,
    model TEXT,
    engine_size REAL,
    fuel_type TEXT,
    year_of_manufacture date,
    mileage REAL,
    price REAL
)
""")

# Cargar datos
df.to_sql("car_sales", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Datos cargados correctamente en SQLite.")
