
DATOS DEL PROYECTO:
Materia: Programación Avanzada en Ciencia de datos
Profesor: JUAN CARLOS CIFUENTES DURAN
Trabajo realizado por: Irala Matias Jose
Año: 02/10/2025
---------------------------------------------------------------------------------------------------
# 🚗 Trabajo Práctico N°2 - Autos  

Este repositorio contiene un **dashboard interactivo** para explorar un dataset de autos.  
El objetivo es practicar el ciclo completo de trabajo con datos:  
1. Obtención desde una fuente pública.  
2. Almacenamiento en base de datos (SQLite).  
3. Construcción de un dashboard interactivo con visualizaciones dinámicas.  
---------------------------------------------------------------------------------------------------

## 📊 Dataset  

- **Archivo:** `car_sales_data.csv`  
- **Fuente:** [Kaggle - Vehicle Stats](https://www.kaggle.com/datasets/rukenmissonnier/vehiclestats)  

### Columnas principales
| Columna                | Descripción                          |
|-------------------------|--------------------------------------|
| `manufacturer`         | Marca del auto (Ford, Toyota, VW…)   |
| `model`                | Modelo                               |
| `engine_size`          | Cilindrada del motor (L)             |
| `fuel_type`            | Tipo de combustible (Petrol, Diesel…)|
| `year_of_manufacture`  | Año de fabricación                   |
| `mileage`              | Kilometraje                          |
| `price`                | Precio del vehículo ($)              |

---

## 🗄️ Base de Datos  

- **Motor:** SQLite  
- **Archivo:** `autos.db`  
- **Tabla:** `car_sales`  

📌 **Para crear y cargar la base de datos:**  

```bash
python Scripts/cargar_datos.py
📈 Dashboard Interactivo

Script principal: tp_auto.py (Flask)

Funcionalidades

✅ Filtros: Marca, Combustible, Año, Cilindrada y Precio
✅ Validaciones de rangos (ejemplo: no permitir año mínimo > año máximo)
✅ Gráficos interactivos con Plotly:

Scatter: Precio vs Kilometraje

Histograma de Precios

Boxplot de Precios por Marca
✅ Tabla resumen ordenable por cualquier columna
✅ Descripciones debajo de cada gráfico para interpretación
---------------------------------------------------------------------------------------------------
🚀 Ejecución

Instalar dependencias:

pip install flask pandas plotly

#EXISTE UN ARCHIVO LLAMADO NOTEBOOK\INSTALACIONES CON LOS PASOS A SEGUIR PERO LOS PASOS LOGICOS SON ESTOS. SI NO GENERA NINGUN PROBLEMA
Ejecutar la aplicación:

python notebook/tp_auto.py


Abrir en el navegador:

http://127.0.0.1:5000/
---------------------------------------------------------------------------------------------------
📂 Estructura del Repositorio
/trabajo_practico_n2_autos
│
├─ data
│  └─ car_sales_data.csv     # Dataset original
├─ autos.db                  # Base de datos SQLite
├─ Scripts
│  └─ cargar_datos.py        # Script para crear y cargar la base
├─ get-pip.py                # Forzador de instalacion
├─ tp2_autos                 # Archivos del entorno
├─ notebook
│  ├─ instalaciones          # PASOS A SEGUIR PARA LA INSTALACION DEL ENTORNO Y DEPENDENCIAS
│  └─ tp_auto.py             # Dashboard interactivo (Flask)
└─ README.md                 # Este archivo

