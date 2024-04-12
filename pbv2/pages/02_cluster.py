import streamlit as st
import requests

# Define la URL del servidor FastAPI
API_URL = "https://backpv2-18.onrender.com/api/prediccion_cluster"

# Título y descripción de la aplicación Streamlit
st.title("Predicción de Cluster")
st.write("Ingrese los datos para predecir el cluster:")

# Campos de entrada para que el usuario ingrese los datos
RECIDIVA = st.slider("RECIDIVA", min_value=0, max_value=1, step=1)
DX1 = st.slider("DX1", min_value=0, max_value=1, step=1)
EDAD = st.slider("EDAD", min_value=0, max_value=100, step=1)
GRADO1 = st.slider("GRADO1", min_value=1, max_value=3, step=1)
HER21 = st.slider("HER21", min_value=0, max_value=1, step=1)

# Botón para hacer la predicción
if st.button("Hacer Predicción"):
    # Realizar solicitud HTTP GET a la API con los datos ingresados por el usuario
    url = "https://backpv2-18.onrender.com/api/prediccion_cluster"
    parametros = {
        "RECIDIVA": RECIDIVA,
        "DX1": DX1,
        "EDAD": EDAD,
        "GRADO1": GRADO1,
        "HER21": HER21
    }
    response = requests.get(url, params=parametros)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        resultado_prediccion = response.json()
        st.write("Cluster predicho:", resultado_prediccion["cluster_predicho"])
    else:
        st.error("Error al hacer la predicción")
