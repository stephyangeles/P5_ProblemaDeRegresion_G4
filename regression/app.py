import streamlit as st
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
import os

# Configuración de la página
st.set_page_config(
    page_title="Predictor de Precios de Coches",
    page_icon="🚗",
    layout="centered"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
    }
    .subheader {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .result-card {
        background-color: #E3F2FD;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Cargar modelo CatBoost
@st.cache_resource
def load_model():
    model_path = os.path.join("models", "CatBoostModel.cbm")
    model = CatBoostRegressor()
    model.load_model(model_path)
    return model

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(f"No se pudo cargar el modelo: {str(e)}")
    model_loaded = False

# Diccionario de marca -> modelos
brand_model_map = {
    'MINI': ['Cooper S Base'],
    'Lincoln': ['LS V8'],
    'Chevrolet': ['Silverado 2500 LT'],
    'Genesis': ['G90 5.0 Ultimate'],
    'Mercedes-Benz': ['Metris Base'],
    # Agrega más combinaciones según el dataset
}

# Listas de opciones
brands = list(brand_model_map.keys())
fuel_types = ['Gasoline', 'Diesel', 'Electric', 'Hybrid']
engines = ['Automatic', 'Manual', 'CVT']
yes_no = ['Yes', 'No']

# Título y subtítulo
st.markdown("<h1 class='main-header'>Predicción de Precio de Coches 🚗</h1>", unsafe_allow_html=True)
st.markdown("<p class='subheader'>Introduce las características del vehículo para obtener una estimación de su precio</p>", unsafe_allow_html=True)

# Formulario en una tarjeta
st.markdown("<div class='card'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with st.form("predict_form"):
    with col1:
        brand = st.selectbox("Marca", options=brands)
        model_name = st.selectbox("Modelo", options=brand_model_map[brand])
        model_year = st.number_input("Año del modelo", min_value=1990, max_value=2025, value=2020, step=1)
        mileage = st.number_input("Kilometraje", min_value=0, value=10000)
        fuel_type = st.selectbox("Tipo de combustible", options=fuel_types)
    
    with col2:
        engine = st.selectbox("Transmisión", options=engines)
        engine_L = st.number_input("Tamaño del motor (L)", min_value=0.0, value=2.0, step=0.1)
        horsepower = st.number_input("Caballos de fuerza", min_value=0, value=150)
        accident = st.selectbox("¿Ha tenido accidentes?", options=yes_no)
        clean_title = st.selectbox("¿Tiene título limpio?", options=yes_no)

    submit = st.form_submit_button("Predecir Precio", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if submit and model_loaded:
    try:
        FEATURES = ['milage', 'model_year', 'model', 'brand',
                    'engine', 'engine_L', 'fuel_type',
                    'accident', 'clean_title', 'mileage',
                    'horsepower']

        # Calculamos milage si es necesario
        milage = mileage / (2025 - model_year + 1) if model_year < 2025 else mileage

        input_data = pd.DataFrame([{
            'milage': milage,
            'model_year': model_year,
            'model': model_name,
            'brand': brand,
            'engine': engine,
            'engine_L': engine_L,
            'fuel_type': fuel_type,
            'accident': accident,
            'clean_title': clean_title,
            'mileage': mileage,
            'horsepower': horsepower
        }])[FEATURES]  # Reordenamos columnas

        prediction = model.predict(input_data)[0]
        
        # Mostrar resultado en una tarjeta atractiva
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        st.markdown(f"<h2>💰 Precio estimado: ${prediction:,.2f}</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Mostrar detalles del vehículo
        st.subheader("Resumen del vehículo")
        col1, col2, col3 = st.columns(3)
        col1.metric("Marca", brand)
        col2.metric("Modelo", model_name)
        col3.metric("Año", model_year)
        col1.metric("Kilometraje", f"{mileage:,} km")
        col2.metric("Motor", f"{engine_L}L, {horsepower} HP")
        col3.metric("Transmisión", engine)

    except Exception as e:
        st.error(f"Error al predecir: {str(e)}")