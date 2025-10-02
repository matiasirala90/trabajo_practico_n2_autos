# trabajo_practico_n2_autos

Este repositorio contiene un dashboard interactivo para explorar un dataset de autos, utilizando filtros, gráficos y tabla resumen. El propósito es practicar el ciclo completo de trabajo con datos: obtención, almacenamiento en base de datos y visualización interactiva.

---

# Dashboard de Autos - Trabajo Práctico

Este repositorio contiene un dashboard interactivo para explorar un dataset de autos utilizando filtros, gráficos y tabla resumen.

---

## Dataset

- **Archivo:** `car_sales_data.csv`
- **Fuente:** [Kaggle - Vehicle Stats](https://www.kaggle.com/datasets/rukenmissonnier/vehiclestats)
- **Columnas principales:**
  - `manufacturer` → Marca del auto
  - `model` → Modelo
  - `engine_size` → Cilindrada del motor (L)
  - `fuel_type` → Tipo de combustible
  - `year_of_manufacture` → Año de fabricación
  - `mileage` → Kilometraje
  - `price` → Precio ($)

---

## Base de Datos

- **Motor:** SQLite
- **Archivo:** `autos.db`
- **Tabla:** `car_sales`

**Crear y cargar la base:**

```bash
python cargar_datos.py
Dashboard Interactivo

Script: tp_autos.py (Flask)

Funcionalidades:

Filtros: Marca, Combustible, Año, Cilindrada, Precio

Validaciones de rangos

Gráficos Plotly:

Scatter: Precio vs Kilometraje

Histograma de Precios

Boxplot por Marca

Tabla resumen ordenable por columna

Descripciones debajo de cada gráfico para interpretación

Ejecutar:
pip install flask pandas plotly
python app.py
http://127.0.0.1:5000/

Estructura del Repositorio
/trabajo_practico_n2_autos
│
├─ data
│  └─car_sales_data.csv       # Dataset original
├─ autos.db                 # Base de datos SQLite
├─ Scripts
│  └─cargar_datos.py          # Script para crear y cargar la base
├─ notebook
│  └─tp_auto.py                   # Dashboard interactivo
└─ README.md                # Este archivo
