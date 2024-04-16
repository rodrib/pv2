import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import requests
import pandas as pd

# Función para llamar a la API y obtener los datos del DataFrame
def obtener_datos_desde_backend():
    #url = "http://localhost:8000/api/data"  # URL de la API de FastAPI
    url = "https://backpv2-18.onrender.com/api/data"  # URL de la API de FastAPI
    try:
        response = requests.get(url)  # Realizar solicitud GET a la API
        if response.status_code == 200:
            return pd.DataFrame(response.json())  # Convertir los datos JSON en un DataFrame
        else:
            st.error("Error al obtener datos desde el backend. Código de estado: " + str(response.status_code))
            st.write(response.text)
            return None
    except Exception as e:
        st.error("Error al conectarse al backend: " + str(e))
        return None


#df = pd.read_csv("pbv2\df_dumies.csv")
# Llamamos a la función para obtener los datos del DataFrame desde el backend
df = obtener_datos_desde_backend()

# Si se obtienen los datos correctamente, mostrarlos en la aplicación de Streamlit
#if df is not None:
#    st.write(df)
# Título para el costo parcial
st.title('Visualizacion de Datos')


# Si se obtienen los datos correctamente, mostrarlos en la aplicación de Streamlit
if df is not None:
    # Filtrar las columnas que quieres mostrar
    columnas_mostrar = [col for col in df.columns if col not in ['CODIGO', 'PAC']]
    # Mostrar el DataFrame sin las columnas CODIGO y PAC
    st.dataframe(df[columnas_mostrar])


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Definir las columnas permitidas
columnas_permitidas = ['GRUPO', 'ETNIA', 'EDAD', 'DX1', 'nombre-genes', 'ID', 'Germline Classification']

st.title('Graficos de algunas columnas')

# Crear un widget de selección para que el usuario elija la columna
columna_seleccionada = st.selectbox('Selecciona una columna:', columnas_permitidas)

# Verificar si se seleccionó una columna
if columna_seleccionada:
    # Calcular el recuento de valores únicos en la columna seleccionada
    valores_contados = df[columna_seleccionada].value_counts().sort_index()

    # Crear un gráfico de barras ordenado de menor a mayor
    fig, ax = plt.subplots()
    ax.bar(valores_contados.index, valores_contados.values)
    ax.set_xlabel(columna_seleccionada)
    ax.set_ylabel('Count')
    ax.set_title(f'Conteo de valores en la columna {columna_seleccionada}')
    
    # Ajustar la rotación y el tamaño de la fuente de las etiquetas del eje x
    plt.xticks(rotation=90, fontsize=8, ha='right') # 'ha' controla la alineación horizontal de las etiquetas
    
    st.pyplot(fig)

    # Mostrar la tabla de conteo de valores
    st.write(valores_contados)



import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Comparacion de datos')

# Definir las columnas permitidas
columnas_permitidas = ['GRUPO', 'ETNIA', 'EDAD', 'nombre-genes', 'Germline Classification']

# Crear dos widgets de selección para que el usuario elija las dos columnas
columna_agrupacion_1 = st.selectbox('Selecciona la primera columna para agrupar:', columnas_permitidas)
columna_agrupacion_2 = st.selectbox('Selecciona la segunda columna para agrupar:', columnas_permitidas)

# Verificar si se seleccionaron ambas columnas para agrupar
if columna_agrupacion_1 and columna_agrupacion_2:
    # Calcular el recuento de valores agrupados por las dos columnas seleccionadas
    valores_agrupados = df.groupby([columna_agrupacion_1, columna_agrupacion_2]).size().unstack(fill_value=0)

    # Crear un gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(10, 6))
    valores_agrupados.plot(kind='bar', stacked=True, ax=ax)
    ax.set_xlabel(columna_agrupacion_1)
    ax.set_ylabel('Count')
    ax.set_title(f'Conteo de valores agrupados por {columna_agrupacion_1} y {columna_agrupacion_2}')
    plt.xticks(rotation=45, ha='right') # Ajustar la rotación y la alineación de las etiquetas del eje x

    # Mostrar el gráfico
    st.pyplot(fig)

    
    # Mostrar la tabla de conteo de valores
    st.write(valores_agrupados)

st.title('Correlacion')

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



# Filtrar las columnas EDAD y DX1
df_corr = df[['EDAD', 'DX1']]

# Eliminar filas con valores 'sd' en las columnas 'EDAD' y 'DX1'
df_corr = df_corr[(df_corr['EDAD'] != 'sd') & (df_corr['DX1'] != 'sd')]

# Convertir la columna 'EDAD' a valores numéricos
df_corr['EDAD'] = pd.to_numeric(df_corr['EDAD'], errors='coerce')

# Eliminar filas con valores faltantes en EDAD o DX1
df_corr.dropna(subset=['EDAD', 'DX1'], inplace=True)

# Convertir la columna 'DX1' a valores numéricos si es necesario
if df_corr['DX1'].dtype == 'object':
    df_corr['DX1'] = pd.to_numeric(df_corr['DX1'], errors='coerce')

# Eliminar filas con valores faltantes en DX1 después de la conversión
df_corr.dropna(subset=['DX1'], inplace=True)

# Calcular la matriz de correlación
correlation_matrix = df_corr.corr()

# Crear un gráfico de correlación
plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=.5)
plt.title('Correlación entre EDAD y DX1')
plt.xlabel('Variables')
plt.ylabel('Variables')

# Mostrar el gráfico
st.pyplot(plt.gcf())  # Pasar la figura actual a st.pyplot()


st.title('Modelos de IA')

# URL de la API para el modelo de recurrencia del cáncer
url_recidiva = "https://backpv2-18.onrender.com/api/recidiva"

# URL de la API para el modelo de diagnóstico del paciente
url_dx1 = "https://backpv2-18.onrender.com/api/dx1"

# Botón para hacer la predicción de recurrencia del cáncer
if st.button("Predecir Recurrencia del Cáncer"):
    # Realizar solicitud HTTP a la API
    response_recidiva = requests.get(url_recidiva)
    
    # Verificar si la solicitud fue exitosa
    if response_recidiva.status_code == 200:
        data_recidiva = response_recidiva.json()
        st.write("Informe de Recurrencia del Cáncer:")
        st.write(data_recidiva["report"])
        st.write("Precisión:", data_recidiva["accuracy"])
    else:
        st.error("Error al hacer la predicción de recurrencia del cáncer")

# Botón para hacer la predicción del diagnóstico del paciente
if st.button("Predecir Diagnóstico del Paciente"):
    # Realizar solicitud HTTP a la API
    response_dx1 = requests.get(url_dx1)
    
    # Verificar si la solicitud fue exitosa
    if response_dx1.status_code == 200:
        data_dx1 = response_dx1.json()
        st.write("Informe de Diagnóstico del Paciente:")
        st.write(data_dx1["report"])
        st.write("Precisión:", data_dx1["accuracy"])
    else:
        st.error("Error al hacer la predicción del diagnóstico del paciente")


#### Predicciones

# Campos de entrada para que el usuario ingrese la edad y el grado
edad_usuario = st.number_input("Ingrese la edad:", step=1)
grado_usuario = st.number_input("Ingrese el grado:", step=1)

# Botón para hacer la predicción
if st.button("Hacer Predicción"):
    # Realizar solicitud HTTP a la API con los datos ingresados por el usuario
    url = "https://backpv2-18.onrender.com/api/prediccion"
    parametros = {"edad": edad_usuario, "grado": grado_usuario}
    response = requests.get(url, params=parametros)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        resultado_prediccion = response.json()
        st.write("Resultado de la Predicción:")
        st.write(resultado_prediccion)
    else:
        st.error("Error al hacer la predicción")