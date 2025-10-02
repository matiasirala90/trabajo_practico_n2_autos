import pandas as pd
import sqlite3

# Conectar a la base SQLite (se crea si no existe)
conn = sqlite3.connect("car_sales.db")
cursor = conn.cursor()

# Crear la tabla
cursor.execute("""
CREATE TABLE IF NOT EXISTS car_sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT,
    model TEXT,
    engine_size REAL,
    fuel_type TEXT,
    year_of_manufacture INTEGER,
    mileage INTEGER,
    price INTEGER
);
""")

# Cargar el CSV
df = pd.read_csv("data/car_sales_data.csv")

# Insertar datos en la tabla
df.to_sql("car_sales", conn, if_exists="append", index=False)

conn.commit()
conn.close()

print("Datos cargados exitosamente en car_sales.db")