import streamlit as st
import requests

st.title("Búsqueda en ClinVar")

# Solicitar al usuario que ingrese el nombre del gen y la región variante
gene_name = st.text_input("Ingrese el nombre del gen (gene_name):")
variant_region = st.text_input("Ingrese la región variante (variant_region):")

# Verificar si se ingresaron valores y realizar la búsqueda si es así
if gene_name and variant_region:
    st.write(f"Realizando búsqueda en ClinVar para {gene_name} - {variant_region}...")
    response = requests.get(f"https://backpv3.onrender.com/api/clinvar_search?gene_name={gene_name}&variant_region={variant_region}")
    if response.status_code == 200:
        resultados = response.json()
        st.write("Resultados:")
        st.write(resultados)
    else:
        st.write("Error al realizar la búsqueda.")
