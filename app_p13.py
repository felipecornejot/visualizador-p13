import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from io import BytesIO
import requests

# --- Paleta de Colores ---
# Definición de colores en formato RGB (0-1) para Matplotlib
color_primario_1_rgb = (14/255, 69/255, 74/255) # 0E454A (Oscuro)
color_primario_2_rgb = (31/255, 255/255, 95/255) # 1FFF5F (Verde vibrante)
color_primario_3_rgb = (255/255, 255/255, 255/255) # FFFFFF (Blanco)

# Colores del logo de Sustrend para complementar
color_sustrend_1_rgb = (0/255, 155/255, 211/255) # 009BD3 (Azul claro)
color_sustrend_2_rgb = (0/255, 140/255, 207/255) # 008CCF (Azul medio)
color_sustrend_3_rgb = (0/255, 54/255, 110/255) # 00366E (Azul oscuro)

# Selección de colores para los gráficos
colors_for_charts = [color_primario_1_rgb, color_primario_2_rgb, color_sustrend_1_rgb, color_sustrend_3_rgb]

# --- Configuración de la página de Streamlit ---
st.set_page_config(layout="wide")

st.title('✨ Visualizador de Impactos - Proyecto P13')
st.subheader('Tratamiento de residuos orgánicos para generar energía y biofertilizante')
st.markdown("""
    Ajusta los parámetros para explorar cómo las proyecciones de impacto ambiental y económico del Proyecto P13
    varían con diferentes escenarios de tratamiento de residuos, generación de energía y producción de biofertilizante.
""")

# --- 1. Datos del Proyecto (Línea Base) ---
# Datos base extraídos de la ficha técnica P13.docx
# Se asumen valores base para los indicadores que se quieren comparar
base_residuos_valorizados = 90 # ton/año - Referencia de la ficha para un escenario base
base_energia_generada = 20000 # kWh/año - Referencia de la ficha
base_biofertilizante_producido = 35 # ton/año - Referencia de la ficha
base_ingresos_totales = 9000000 # CLP/año - Referencia de la ficha (90 ton valorizadas * 0.9 tasa de valorización * (precio energía + precio biofertilizante asumido))
base_agroquimicos_evitados = base_biofertilizante_producido * 0.1 # 10% de sustitución sobre el biofertilizante base

# --- 2. Widgets Interactivos para Parámetros (Streamlit) ---
st.sidebar.header('Parámetros de Simulación')

residuos_tratados = st.sidebar.slider(
    'Residuos Tratados (ton/año):',
    min_value=80,
    max_value=200, # Increased max for more flexibility
    value=90,
    step=5,
    help="Cantidad de residuos orgánicos tratados anualmente."
)

tasa_valorizacion = st.sidebar.slider(
    'Tasa de Valorización (%):',
    min_value=0.70,
    max_value=1.00,
    value=0.90,
    step=0.01,
    format='%.1f%%',
    help="Porcentaje de los residuos tratados que son valorizados (convertidos en biogás o biofertilizante)."
)

energia_generada_kWh = st.sidebar.slider(
    'Energía Generada (kWh/año):',
    min_value=15000,
    max_value=50000, # Increased max for more flexibility
    value=20000,
    step=1000,
    help="Cantidad de energía generada en kWh por año a partir del biogás."
)

biofertilizante_ton = st.sidebar.slider(
    'Producción Biofertilizante (ton/año):',
    min_value=30,
    max_value=80, # Increased max for more flexibility
    value=35,
    step=1,
    help="Cantidad de biofertilizante producido anualmente."
)

porcentaje_materiales_reciclados = st.sidebar.slider(
    'Porcentaje Materiales Reciclados Usados (%):',
    min_value=0.1,
    max_value=0.5,
    value=0.3,
    step=0.01,
    format='%.1f%%',
    help="Porcentaje de materiales reciclados utilizados en el proceso o construcción del módulo."
)

precio_energia = st.sidebar.slider(
    'Precio Energía (CLP/kWh):',
    min_value=100,
    max_value=300,
    value=150,
    step=10,
    help="Precio de venta de la energía generada por kWh."
)

precio_biofertilizante = st.sidebar.slider(
    'Precio Biofertilizante (CLP/ton):',
    min_value=100000,
    max_value=500000, # Increased max for more flexibility
    value=200000,
    step=10000,
    help="Precio de venta del biofertilizante por tonelada."
)

# --- 3. Cálculos de Indicadores ---
residuos_valorizados = residuos_tratados * tasa_valorizacion
agroquimicos_ev = biofertilizante_ton * 0.1 # Suponemos 10% de tasa de sustitución según ficha
ingresos_energia = energia_generada_kWh * precio_energia
ingresos_biofertilizante = biofertilizante_ton * precio_biofertilizante
ingresos_totales = ingresos_energia + ingresos_biofertilizante
personas_capacitadas = 30 # Valor fijo según la ficha
alianzas_colaborativas = 4 # Valor fijo según la ficha

st.header('Resultados Proyectados Anuales:')

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="♻️ **Residuos Valorizados**", value=f"{residuos_valorizados:.2f} ton/año")
    st.caption("Cantidad de residuos orgánicos transformados en productos útiles.")
with col2:
    st.metric(label="🌾 **Agroquímicos Sintéticos Evitados**", value=f"{agroquimicos_ev:.2f} ton/año")
    st.caption("Reducción del uso de fertilizantes químicos convencionales.")
with col3:
    st.metric(label="⚡ **Ingresos por Energía**", value=f"CLP {ingresos_energia:,.0f}")
    st.caption("Ingresos generados por la venta de energía (biogás).")

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(label="💰 **Ingresos por Biofertilizante**", value=f"CLP {ingresos_biofertilizante:,.0f}")
    st.caption("Ingresos generados por la venta de biofertilizante.")
with col5:
    st.metric(label="📈 **Ingresos Totales del Proyecto**", value=f"CLP {ingresos_totales:,.0f}")
    st.caption("Suma de ingresos por energía y biofertilizante.")
with col6:
    st.metric(label="🧑‍🏫 **Personas Capacitadas**", value=f"{personas_capacitadas} personas")
    st.caption("Número de personas que reciben formación o entrenamiento.")

st.markdown("---")

st.header('📊 Análisis Gráfico de Impactos')

# --- Visualización (Gráficos 2D con Matplotlib) ---
labels = ['Línea Base', 'Proyección']
bar_width = 0.6
x = np.arange(len(labels))

# Creamos una figura con 3 subplots (2D)
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(20, 7), facecolor=color_primario_3_rgb)
fig.patch.set_facecolor(color_primario_3_rgb)

# --- Gráfico 1: Residuos Valorizados (ton/año) ---
residuos_values = [base_residuos_valorizados, residuos_valorizados]
bars1 = ax1.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax1.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[3])
ax1.set_title('Residuos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax1.yaxis.set_tick_params(colors=colors_for_charts[0])
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='x', length=0)
max_residuos_val = max(residuos_values)
ax1.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1)) # Asegura al menos 1 ton si es muy bajo
for bar in bars1:
    yval = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 2: Energía Generada (kWh/año) ---
energia_values = [base_energia_generada, energia_generada_kWh]
bars2 = ax2.bar(x, energia_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax2.set_ylabel('kWh/año', fontsize=12, color=colors_for_charts[0])
ax2.set_title('Energía Generada', fontsize=14, color=colors_for_charts[3], pad=20)
ax2.set_xticks(x)
ax2.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax2.yaxis.set_tick_params(colors=colors_for_charts[0])
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(axis='x', length=0)
max_energia_val = max(energia_values)
ax2.set_ylim(bottom=0, top=max(max_energia_val * 1.15, 1000)) # 15% de margen superior o mínimo 1000 kWh
for bar in bars2:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

# --- Gráfico 3: Ingresos Totales (CLP/año) ---
ingresos_values = [base_ingresos_totales, ingresos_totales]
bars3 = ax3.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax3.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax3.set_title('Ingresos Totales', fontsize=14, color=colors_for_charts[3], pad=20)
ax3.set_xticks(x)
ax3.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax3.yaxis.set_tick_params(colors=colors_for_charts[0])
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.tick_params(axis='x', length=0)
max_ingresos_val = max(ingresos_values)
ax3.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000000)) # 15% de margen superior o mínimo 1 millón CLP
for bar in bars3:
    yval = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])

plt.tight_layout(rect=[0, 0.05, 1, 0.95])
st.pyplot(fig)

# --- Funcionalidad de descarga de cada gráfico ---
st.markdown("---")
st.subheader("Descargar Gráficos Individualmente")

# Función auxiliar para generar el botón de descarga
def download_button(fig, filename_prefix, key):
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=300)
    st.download_button(
        label=f"Descargar {filename_prefix}.png",
        data=buf.getvalue(),
        file_name=f"{filename_prefix}.png",
        mime="image/png",
        key=key
    )

# Crear figuras individuales para cada gráfico para poder descargarlas
# Figura 1: Residuos Valorizados
fig_residuos, ax_residuos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_residuos.bar(x, residuos_values, width=bar_width, color=[colors_for_charts[0], colors_for_charts[1]])
ax_residuos.set_ylabel('Toneladas/año', fontsize=12, color=colors_for_charts[3])
ax_residuos.set_title('Residuos Valorizados', fontsize=14, color=colors_for_charts[3], pad=20)
ax_residuos.set_xticks(x)
ax_residuos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_residuos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_residuos.spines['top'].set_visible(False)
ax_residuos.spines['right'].set_visible(False)
ax_residuos.tick_params(axis='x', length=0)
ax_residuos.set_ylim(bottom=0, top=max(max_residuos_val * 1.15, 1))
for bar in ax_residuos.patches:
    yval = bar.get_height()
    ax_residuos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.2f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_residuos, "Residuos_Valorizados", "download_residuos")
plt.close(fig_residuos)

# Figura 2: Energía Generada
fig_energia, ax_energia = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_energia.bar(x, energia_values, width=bar_width, color=[colors_for_charts[2], colors_for_charts[3]])
ax_energia.set_ylabel('kWh/año', fontsize=12, color=colors_for_charts[0])
ax_energia.set_title('Energía Generada', fontsize=14, color=colors_for_charts[3], pad=20)
ax_energia.set_xticks(x)
ax_energia.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_energia.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_energia.spines['top'].set_visible(False)
ax_energia.spines['right'].set_visible(False)
ax_energia.tick_params(axis='x', length=0)
ax_energia.set_ylim(bottom=0, top=max(max_energia_val * 1.15, 1000))
for bar in ax_energia.patches:
    yval = bar.get_height()
    ax_energia.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"{yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_energia, "Energia_Generada", "download_energia")
plt.close(fig_energia)

# Figura 3: Ingresos Totales
fig_ingresos, ax_ingresos = plt.subplots(figsize=(8, 6), facecolor=color_primario_3_rgb)
ax_ingresos.bar(x, ingresos_values, width=bar_width, color=[colors_for_charts[1], colors_for_charts[0]])
ax_ingresos.set_ylabel('CLP/año', fontsize=12, color=colors_for_charts[3])
ax_ingresos.set_title('Ingresos Totales', fontsize=14, color=colors_for_charts[3], pad=20)
ax_ingresos.set_xticks(x)
ax_ingresos.set_xticklabels(labels, rotation=15, color=colors_for_charts[0])
ax_ingresos.yaxis.set_tick_params(colors=colors_for_charts[0])
ax_ingresos.spines['top'].set_visible(False)
ax_ingresos.spines['right'].set_visible(False)
ax_ingresos.tick_params(axis='x', length=0)
ax_ingresos.set_ylim(bottom=0, top=max(max_ingresos_val * 1.15, 1000000))
for bar in ax_ingresos.patches:
    yval = bar.get_height()
    ax_ingresos.text(bar.get_x() + bar.get_width()/2, yval + 0.05 * yval, f"CLP {yval:,.0f}", ha='center', va='bottom', color=colors_for_charts[0])
plt.tight_layout()
download_button(fig_ingresos, "Ingresos_Totales", "download_ingresos")
plt.close(fig_ingresos)

st.markdown("---")
st.markdown("### Información Adicional:")
st.markdown(f"- **Estado de Avance y Recomendaciones:** El Proyecto P13 se encuentra en una etapa avanzada de desarrollo tecnológico, con un módulo de digestión anaeróbica estandarizado ya diseñado y fabricado, el cual está siendo validado en contextos agroindustriales y municipales a escala piloto y precomercial. La tecnología ha demostrado su capacidad para tratar residuos orgánicos de diversa naturaleza, generando biogás y un biofertilizante con potencial agrícola comprobado. Asimismo, el modelo de negocio se encuentra en fase de escalamiento, con primeras ventas en curso y alianzas estratégicas en exploración con municipios, productores agrícolas y empresas generadoras de residuos.")

st.markdown("---")
# Texto de atribución centrado
st.markdown("<div style='text-align: center;'>Visualizador Creado por el equipo Sustrend SpA en el marco del Proyecto TT GREEN Foods</div>", unsafe_allow_html=True)

# Aumentar el espaciado antes de los logos
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# --- Mostrar Logos ---
col_logos_left, col_logos_center, col_logos_right = st.columns([1, 2, 1])

with col_logos_center:
    sustrend_logo_url = "https://drive.google.com/uc?id=1vx_znPU2VfdkzeDtl91dlpw_p9mmu4dd"
    ttgreenfoods_logo_url = "https://drive.google.com/uc?id=1uIQZQywjuQJz6Eokkj6dNSpBroJ8tQf8"

    try:
        sustrend_response = requests.get(sustrend_logo_url)
        sustrend_response.raise_for_status()
        sustrend_image = Image.open(BytesIO(sustrend_response.content))

        ttgreenfoods_response = requests.get(ttgreenfoods_logo_url)
        ttgreenfoods_response.raise_for_status()
        ttgreenfoods_image = Image.open(BytesIO(ttgreenfoods_response.content))

        st.image([sustrend_image, ttgreenfoods_image], width=100)
    except requests.exceptions.RequestException as e:
        st.error(f"Error al cargar los logos desde las URLs. Por favor, verifica los enlaces: {e}")
    except Exception as e:
        st.error(f"Error inesperado al procesar las imágenes de los logos: {e}")

st.markdown("<div style='text-align: center; font-size: small; color: gray;'>Viña del Mar, Valparaíso, Chile</div>", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='text-align: center; font-size: smaller; color: gray;'>Versión del Visualizador: 1.0</div>", unsafe_allow_html=True) # Versión inicial para P13
st.sidebar.markdown(f"<div style='text-align: center; font-size: x-small; color: lightgray;'>Desarrollado con Streamlit</div>", unsafe_allow_html=True)
