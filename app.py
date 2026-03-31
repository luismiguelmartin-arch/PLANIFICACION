import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Visualizador de Excel", layout="wide")

st.title("📊 Mi Tablero de Datos")
st.markdown("Esta aplicación carga datos directamente desde un archivo Excel en GitHub.")

# Función para cargar datos
@st.cache_data # Esto hace que la app sea rápida al no recargar el Excel en cada clic
def load_data(file_path):
    df = pd.read_excel(file_path)
    return df

# Nombre de tu archivo (asegúrate de que esté en la misma carpeta)
FILE_NAME = 'tu_archivo.xlsx' 

try:
    data = load_data(FILE_NAME)

    # Sidebar para filtros sencillos
    st.sidebar.header("Filtros")
    columna_filtro = st.sidebar.selectbox("Selecciona una columna para explorar:", data.columns)
    
    # Mostrar métricas básicas
    col1, col2 = st.columns(2)
    col1.metric("Total de Filas", data.shape[0])
    col2.metric("Total de Columnas", data.shape[1])

    # Mostrar la tabla interactiva
    st.subheader("Vista Previa de los Datos")
    st.dataframe(data, use_container_width=True)

    # Gráfico automático (opcional)
    if st.checkbox("Mostrar gráfico de barras"):
        st.subheader("Análisis Visual")
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        if numeric_cols:
            st.bar_chart(data[numeric_cols[0]])
        else:
            st.warning("No hay columnas numéricas para graficar.")

except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.info("Asegúrate de que el archivo Excel esté en la raíz del repositorio.")
