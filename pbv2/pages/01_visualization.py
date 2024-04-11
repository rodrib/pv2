import pandas as pd
import numpy as np
import streamlit as st

# Crear un DataFrame con 15 filas y columnas 'posicion' y 'Impacto'
np.random.seed(0)  # Fijar la semilla para reproducibilidad
df_posicion = pd.DataFrame({
    'posicion': np.random.randint(1, 21, size=15),  # Generar números aleatorios entre 1 y 20
    'Impacto': np.random.choice(['P', 'PP', 'VUS', 'PB', 'B'], size=15)  # Seleccionar aleatoriamente de los valores dados
})

# Mostrar el DataFrame
st.write(df_posicion)


import streamlit as st



# Función para aplicar emojis según el impacto
def aplicar_emoji(impacto):
    if impacto in ['P', 'PP']:
        return '🔴'
    elif impacto == 'VUS':
        return '🟡'
    elif impacto in ['PB', 'B']:
        return '🟢'
    else:
        return ''

# Ordenar el DataFrame por la columna 'posicion'
df_posicion = df_posicion.sort_values(by='posicion')

# Crear la representación visual ordenada
visualizacion = ' '.join([aplicar_emoji(impacto) + '[' + str(pos) + ']' for pos, impacto in zip(df_posicion['posicion'], df_posicion['Impacto'])])
st.write(visualizacion)
