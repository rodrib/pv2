import streamlit as st
import requests



# Título y descripción de la aplicación Streamlit
st.title("Cálculo de Correlación")
st.write("Ingrese los datos para calcular la correlación entre EDAD y DX1:")

# Recopila los datos de entrada del usuario
edad = st.number_input("Ingrese la edad:", step=1, value=0)
dx1 = st.number_input("Ingrese el valor DX1:", step=1, value=0)


# Botón para calcular la correlación
if st.button("Calcular Correlación"):
    # Realizar solicitud HTTP GET al servidor FastAPI con los datos ingresados por el usuario
    url = "https://backpv3test.onrender.com/api/correlacion"
    params = {"EDAD": edad, "DX1": dx1}
    response = requests.get(url, params=params)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        resultado_correlacion = response.json()
        st.write("Correlación calculada:", resultado_correlacion["correlacion"])
    else:
        st.error("Error al calcular la correlación. Inténtalo de nuevo más tarde.")


