import streamlit as st
import requests

# Define la URL del servidor FastAPI
API_URL = "https://backpv2-18.onrender.com/api/prediccion_cluster"

# Título y descripción de la aplicación Streamlit
st.title("Predicción de Cluster")
st.write("Ingrese los datos para predecir el cluster:")

# Recopila los datos de entrada del usuario
RECIDIVA = st.slider("RECIDIVA", min_value=0, max_value=1, step=1)
DX1 = st.slider("DX1", min_value=0, max_value=1, step=1)
EDAD = st.slider("EDAD", min_value=0, max_value=100, step=1)
GRADO1 = st.slider("GRADO1", min_value=1, max_value=3, step=1)
HER21 = st.slider("HER21", min_value=0, max_value=1, step=1)

# Realiza una solicitud HTTP POST al servidor FastAPI con los datos como cuerpo de la solicitud
data = {
    "RECIDIVA": RECIDIVA,
    "DX1": DX1,
    "EDAD": EDAD,
    "GRADO1": GRADO1,
    "HER21": HER21
}
response = requests.post(API_URL, json=data)


# Verifica si la solicitud fue exitosa y muestra los resultados
if response.status_code == 200:
    result = response.json()
    st.write("Cluster predicho:", result["cluster_predicho"])
else:
    st.error("Error al realizar la predicción. Inténtalo de nuevo más tarde.")