import streamlit as st
from Bio import Entrez
import pandas as pd
import time

def clinvar_search(gene_name, variant_region):
    # Ingresa tu dirección de correo electrónico (requisito de NCBI)
    Entrez.email = "rodribogado50@gmail.com"

    # Lista para almacenar los resultados
    results = []

    try:
        # Realiza la búsqueda en ClinVar
        handle = Entrez.esearch(db="clinvar", term=f"{gene_name}[cgene] AND {variant_region}[cvar]", retmode="xml")
        record = Entrez.read(handle)

        # Obtiene y muestra los resultados de la búsqueda
        for id in record["IdList"]:
            handle = Entrez.esummary(db="clinvar", id=id, retmode="xml")
            summary = Entrez.read(handle, validate=False)  # Deshabilita la validación

            # Obtener información de Accession y Variation Name
            document_summary = summary['DocumentSummarySet']['DocumentSummary']

            # Verificar la estructura y extraer la información
            if isinstance(document_summary, list):
                for entry in document_summary:
                    accession = entry.get("accession_version", "")
                    variation_name = entry.get("title", "")
                    results.append({"Gene": gene_name, "ID": id, "Accession": accession, "Variation Name": variation_name, "gene_name_variant_region": gene_name + '_' + variant_region})

                    # Obtiene la información de clasificación germinativa y enlaces
                    classification = []
                    links = []

                    # Intentar obtener información de 'clinical_significance'
                    try:
                        for classification_info in entry['clinical_significance']['description']:
                            classification.append(classification_info)
                    except KeyError:
                        pass

                    # Si no se encontró información en 'clinical_significance', intentar con 'germline_classification'
                    try:
                        for classification_info in entry['germline_classification']['description']:
                            classification.append(classification_info)
                    except KeyError:
                        pass

                    # Enlaces
                    for link_info in entry['variation_set'][0]['variation_xrefs']:
                        if link_info['db_source'] == 'dbSNP':
                            links.append(f"dbSNP: {link_info['db_id']}")
                        elif link_info['db_source'] == 'Breast Cancer Information Core (BIC) (BRCA1)':
                            links.append(f"BIC: {link_info['db_id']}")
                        elif link_info['db_source'] == 'ClinGen':
                            links.append(f"ClinGen: {link_info['db_id']}")

                    # Agregar al resultado
                    results[-1]['Germline Classification'] = ', '.join(classification)
                    results[-1]['Links'] = ', '.join(links)

            elif isinstance(document_summary, dict):
                accession = document_summary.get("accession_version", "")
                variation_name = document_summary.get("title", "")
                results.append({"Gene": gene_name, "ID": id, "Accession": accession, "Variation Name": variation_name, "gene_name_variant_region": gene_name + '_' + variant_region})

                # Obtiene la información de clasificación germinativa y enlaces
                classification = []
                links = []

                # Intentar obtener información de 'clinical_significance'
                try:
                    for classification_info in document_summary['clinical_significance']['description']:
                        classification.append(classification_info)
                except KeyError:
                    pass

                # Si no se encontró información en 'clinical_significance', intentar con 'germline_classification'
                try:
                    for classification_info in document_summary['germline_classification']['description']:
                        classification.append(classification_info)
                except KeyError:
                    pass

                # Enlaces
                for link_info in document_summary['variation_set'][0]['variation_xrefs']:
                    if link_info['db_source'] == 'dbSNP':
                        links.append(f"dbSNP: {link_info['db_id']}")
                    elif link_info['db_source'] == 'Breast Cancer Information Core (BIC) (BRCA1)':
                        links.append(f"BIC: {link_info['db_id']}")
                    elif link_info['db_source'] == 'ClinGen':
                        links.append(f"ClinGen: {link_info['db_id']}")

                # Agregar al resultado
                results[-1]['Germline Classification'] = ', '.join(classification)
                results[-1]['Links'] = ', '.join(links)

            # Cierra el handle
            handle.close()

            # Agregar un retraso de 1 segundo entre las solicitudes
            time.sleep(1)

    except Exception as e:
        # Imprime cualquier error que ocurra durante la búsqueda
        st.write(f"Error en la búsqueda para {gene_name} - {variant_region}: {e}")

    # Devuelve los resultados
    return results

# Ejemplo de uso en Streamlit
if __name__ == "__main__":
    st.title("Búsqueda en ClinVar")
    
    # Solicitar al usuario que ingrese el gene_name y variant_region
    gene_name = st.text_input("Ingrese el nombre del gen (gene_name):")
    variant_region = st.text_input("Ingrese la región variante (variant_region):")

    # Verificar si se ingresaron valores y ejecutar la búsqueda si es así
    if gene_name and variant_region:
        st.write(f"Realizando búsqueda en ClinVar para {gene_name} - {variant_region}...")
        resultados = clinvar_search(gene_name, variant_region)
        st.write("Resultados:")
        st.write(pd.DataFrame(resultados))

