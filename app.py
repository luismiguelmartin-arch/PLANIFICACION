import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(page_title="Planificación Máquinas 2026", layout="wide")

# --- DATOS EMBEBIDOS (Tu Excel convertido a Python) ---
def get_data():
    data = {
        "MAQUINA": ["MÁQUINA 1", "MÁQUINA 2", "MÁQUINA 3", "MÁQUINA 1", "MÁQUINA 2"],
        "CLIENTE": ["Cliente A", "Cliente B", "Cliente C", "Cliente A", "Cliente D"],
        "PEDIDO": ["P001", "P002", "P003", "P004", "P005"],
        "DESCRIPCIÓN": ["Pieza Base", "Carcasa", "Eje central", "Soporte", "Tapa"],
        "FECHA INICIO": ["2026-01-07", "2026-01-08", "2026-01-12", "2026-01-15", "2026-01-20"],
        "FECHA FIN": ["2026-01-10", "2026-01-15", "2026-01-18", "2026-01-22", "2026-01-25"],
        "ESTADO": ["Completado", "En Proceso", "Pendiente", "Pendiente", "En Proceso"]
    }
    df = pd.DataFrame(data)
    # Convertir textos a formato fecha de Python
    df["FECHA INICIO"] = pd.to_datetime(df["FECHA INICIO"])
    df["FECHA FIN"] = pd.to_datetime(df["FECHA FIN"])
    return df

df = get_data()

# --- INTERFAZ DE USUARIO ---
st.title("🗓️ Planificación de Máquinas 2026")
st.markdown("Visualización interactiva de la hoja de ruta de producción.")

# Filtros en la barra lateral
st.sidebar.header("Filtros de Producción")
maquina_sel = st.sidebar.multiselect(
    "Seleccionar Máquina:", 
    options=df["MAQUINA"].unique(), 
    default=df["MAQUINA"].unique()
)

# Aplicar filtros
df_filtrado = df[df["MAQUINA"].isin(maquina_sel)]

# Métricas rápidas
col1, col2, col3 = st.columns(3)
col1.metric("Total Pedidos", len(df_filtrado))
col2.metric("Máquinas Activas", df_filtrado["MAQUINA"].nunique())
col3.metric("Próxima Entrega", df_filtrado["FECHA FIN"].min().strftime('%d-%m-%Y'))

# --- VISUALIZACIÓN ---
tab1, tab2 = st.tabs(["📋 Tabla de Datos", "📊 Diagrama de Gantt"])

with tab1:
    st.subheader("Detalle de la Planificación")
    st.dataframe(df_filtrado, use_container_width=True)

with tab2:
    st.subheader("Línea de Tiempo de Producción")
    if not df_filtrado.empty:
        fig = px.timeline(
            df_filtrado, 
            x_start="FECHA INICIO", 
            x_end="FECHA FIN", 
            y="MAQUINA", 
            color="ESTADO",
            hover_name="PEDIDO",
            text="CLIENTE",
            color_discrete_map={"Completado": "#2ecc71", "En Proceso": "#f1c40f", "Pendiente": "#e74c3c"}
        )
        fig.update_yaxes(autorange="reversed") 
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No hay datos para mostrar el gráfico.")
            st.warning("No hay columnas numéricas para graficar.")

except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.info("Asegúrate de que el archivo Excel esté en la raíz del repositorio.")
