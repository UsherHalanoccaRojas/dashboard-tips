import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(
    page_title="Dashboard de Propinas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados para apariencia moderna
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.05rem;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Título y descripción
st.markdown('<div class="main-header">📊 Dashboard de Propinas</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Análisis interactivo de hábitos de consumo y propinas usando Streamlit, Plotly y Seaborn.</div>', unsafe_allow_html=True)

# Carga de datos con caché
@st.cache_data
def load_data():
    df = px.data.tips()
    # Calcular columna de porcentaje de propina
    df["tip_pct"] = (df["tip"] / df["total_bill"]) * 100
    return df

df_raw = load_data()

# Barra lateral - Filtros
st.sidebar.header("🔍 Filtros de Búsqueda")

# 1. Filtro por Día
dias_disponibles = sorted(df_raw["day"].unique().tolist())
dias_seleccionados = st.sidebar.multiselect(
    "Selecciona los días:",
    options=dias_disponibles,
    default=dias_disponibles,
    help="Filtra las transacciones según el día de la semana"
)

# 2. Filtro por Sexo
sexos_disponibles = sorted(df_raw["sex"].unique().tolist())
sexos_seleccionados = st.sidebar.multiselect(
    "Selecciona el sexo:",
    options=sexos_disponibles,
    default=sexos_disponibles,
    help="Filtra por sexo de quien pagó la cuenta"
)

# Filtro adicional: Fumador
fumador_opciones = ["Todos"] + sorted(df_raw["smoker"].unique().tolist())
fumador_seleccionado = st.sidebar.selectbox(
    "Fumador:",
    options=fumador_opciones,
    index=0
)

# Aplicar filtros
df_filtrado = df_raw[
    (df_raw["day"].isin(dias_seleccionados)) &
    (df_raw["sex"].isin(sexos_seleccionados))
]

if fumador_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["smoker"] == fumador_seleccionado]

# Comprobar si hay datos tras filtrar
if df_filtrado.empty:
    st.warning("⚠️ No se encontraron registros con los filtros seleccionados. Por favor ajusta tus criterios.")
else:
    # Métricas Principales (KPIs)
    total_facturado = df_filtrado["total_bill"].sum()
    propina_promedio = df_filtrado["tip"].mean()
    porcentaje_promedio = df_filtrado["tip_pct"].mean()
    num_registros = len(df_filtrado)

    st.markdown("### 📌 Métricas Clave (KPIs)")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric(
            label="Total Facturado",
            value=f"${total_facturado:,.2f}"
        )
    with kpi2:
        st.metric(
            label="Propina Promedio",
            value=f"${propina_promedio:.2f}"
        )
    with kpi3:
        st.metric(
            label="% Propina Promedio",
            value=f"{porcentaje_promedio:.1f}%"
        )
    with kpi4:
        st.metric(
            label="Número de Registros",
            value=f"{num_registros}"
        )

    st.markdown("---")

    # Sección de Gráficos: Plotly & Seaborn
    col_plotly, col_seaborn = st.columns(2)

    with col_plotly:
        st.subheader("📈 Gráfico Interactivo (Plotly)")
        st.caption("Relación entre el Total de la Cuenta y la Propina")
        
        fig_plotly = px.scatter(
            df_filtrado,
            x="total_bill",
            y="tip",
            color="sex",
            size="size",
            hover_data=["day", "time", "smoker"],
            labels={
                "total_bill": "Total de la Cuenta ($)",
                "tip": "Propina ($)",
                "sex": "Sexo",
                "size": "Tamaño de Mesa"
            },
            template="plotly_white",
            color_discrete_map={"Female": "#e74c3c", "Male": "#3498db"}
        )
        fig_plotly.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_plotly, use_container_width=True)

    with col_seaborn:
        st.subheader("📊 Reporte Estadístico (Seaborn)")
        st.caption("Distribución de Propinas por Día y Sexo")

        sns.set_theme(style="whitegrid", palette="muted")
        fig_sns, ax = plt.subplots(figsize=(7, 4.8))
        
        sns.boxplot(
            data=df_filtrado,
            x="day",
            y="tip",
            hue="sex",
            ax=ax,
            palette={"Female": "#e74c3c", "Male": "#3498db"}
        )
        ax.set_title("Distribución de Propinas por Día de la Semana", fontsize=12, pad=12)
        ax.set_xlabel("Día de la Semana", fontsize=10)
        ax.set_ylabel("Propina ($)", fontsize=10)
        ax.legend(title="Sexo", loc="upper right")
        sns.despine(top=True, right=True)
        plt.tight_layout()
        
        st.pyplot(fig_sns)
        plt.close(fig_sns)

    # Detalle de Datos y Descarga
    with st.expander("📋 Ver Dataset Filtrado"):
        st.dataframe(
            df_filtrado.style.format({
                "total_bill": "${:.2f}",
                "tip": "${:.2f}",
                "tip_pct": "{:.1f}%"
            }),
            use_container_width=True
        )
        
        csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar datos filtrados (CSV)",
            data=csv_data,
            file_name="tips_filtrados.csv",
            mime="text/csv"
        )
