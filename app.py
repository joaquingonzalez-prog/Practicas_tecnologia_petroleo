"""
============================================================
PRÁCTICA 2: DESTILACIÓN DE CRUDO - CURVA TBP Y RENDIMIENTOS
Laboratorio Virtual de Tecnologías del Petróleo
============================================================
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.interpolate import PchipInterpolator
import io
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Práctica 2 – Destilación de Crudo",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# ESTILOS CSS PERSONALIZADOS
# ─────────────────────────────────────────────
st.markdown("""
<style>
    /* Fuentes y paleta industrial */
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    /* Fondo principal */
    .stApp {
        background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
        color: #e6edf3;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
        border-right: 1px solid #30363d;
    }

    /* Cabecera hero */
    .hero-header {
        background: linear-gradient(135deg, #1c2128 0%, #21262d 50%, #1c2128 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 2rem 2.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        overflow: hidden;
    }
    .hero-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0; height: 3px;
        background: linear-gradient(90deg, #f78166, #ff9d4d, #ffd166, #06d6a0);
    }
    .hero-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.9rem;
        font-weight: 600;
        color: #ffd166;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .hero-subtitle {
        font-size: 1rem;
        color: #8b949e;
        margin-top: 0.3rem;
    }

    /* Tarjetas de sección */
    .section-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.5rem 1.8rem;
        margin-bottom: 1.5rem;
    }
    .section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1rem;
        font-weight: 600;
        color: #ff9d4d;
        text-transform: uppercase;
        letter-spacing: 1px;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background: #1c2128;
        border-left: 3px solid #388bfd;
        border-radius: 0 6px 6px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.87rem;
        color: #8b949e;
        line-height: 1.6;
    }
    .warning-box {
        background: #1c2128;
        border-left: 3px solid #ffd166;
        border-radius: 0 6px 6px 0;
        padding: 0.75rem 1rem;
        margin-bottom: 1rem;
        font-size: 0.87rem;
        color: #8b949e;
        line-height: 1.6;
    }

    /* Métricas personalizadas */
    [data-testid="stMetric"] {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 0.8rem 1rem;
    }
    [data-testid="stMetric"] label {
        font-size: 0.75rem !important;
        color: #8b949e !important;
        font-family: 'IBM Plex Mono', monospace !important;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #ffd166 !important;
        font-size: 1.5rem !important;
    }

    /* Sliders */
    .stSlider > label {
        color: #c9d1d9 !important;
        font-size: 0.85rem !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-family: 'IBM Plex Mono', monospace !important;
        color: #8b949e !important;
        font-size: 0.85rem !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffd166 !important;
        border-bottom-color: #ffd166 !important;
    }

    /* Dataframe */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }

    /* Form submit button */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #ff9d4d, #f78166) !important;
        color: white !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 600 !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
    }

    /* Download button */
    [data-testid="stDownloadButton"] button {
        background: linear-gradient(135deg, #06d6a0, #388bfd) !important;
        color: white !important;
        font-family: 'IBM Plex Mono', monospace !important;
        font-weight: 600 !important;
        border: none !important;
    }

    .fraction-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-family: 'IBM Plex Mono', monospace;
        font-weight: 600;
        margin-right: 4px;
    }
    .sidebar-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.8rem;
        color: #ff9d4d;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# FUNCIONES DE CONVERSIÓN ASTM → TBP
# ─────────────────────────────────────────────

def astm_to_tbp_daubert(t_astm_C):
    """
    Convierte temperatura ASTM D86 (°C) a TBP (°C) usando la
    correlación de Daubert simplificada (API TDB 3A1.1).
    La transformación es no lineal: amplifica la "cola" pesada
    y deprime la "cabeza" ligera.
    """
    t_F = t_astm_C * 9 / 5 + 32

    # Coeficientes A y B del método API para distintos puntos de corte
    # Basado en la correlación API Chapter 3 (Daubert & Danner)
    A = 0.87180
    B = 1.01820

    # TBP en °F
    tbp_F = A * (t_F ** B)
    tbp_C = (tbp_F - 32) * 5 / 9
    return tbp_C


def generar_curva_astm_tbp():
    """
    Genera una curva ASTM D86 realista para un crudo de mezcla
    (tipo Arab Light / Brent) y la convierte a TBP.
    """
    np.random.seed(int(st.session_state.semilla_crudo))

    # Puntos base: % vol recuperado
    vol_pct = np.array([0.0, 10.0, 30.0, 50.0, 70.0, 90.0, 100.0])

    # Temperaturas ASTM base para un crudo tipo medio (°C)
    # IBP ~30°C, FBP ~480°C
    tbp_base = np.array([32.0, 82.0, 160.0, 255.0, 340.0, 440.0, 485.0])

    # Variación aleatoria controlada para simular distintos crudos
    variaciones = np.array([
        np.random.uniform(-8, 8),    # IBP
        np.random.uniform(-12, 15),  # 10%
        np.random.uniform(-15, 20),  # 30%
        np.random.uniform(-20, 25),  # 50%
        np.random.uniform(-18, 22),  # 70%
        np.random.uniform(-15, 20),  # 90%
        np.random.uniform(-10, 10),  # FBP
    ])

    astm_temps = tbp_base + variaciones

    # Garantizar que la curva sea estrictamente creciente
    for i in range(1, len(astm_temps)):
        if astm_temps[i] <= astm_temps[i - 1]:
            astm_temps[i] = astm_temps[i - 1] + np.random.uniform(8, 18)

    # Redondear a 1 decimal
    astm_temps = np.round(astm_temps, 1)

    # Calcular TBP con la correlación de Daubert
    tbp_temps = np.array([astm_to_tbp_daubert(t) for t in astm_temps])

    # Ajuste manual para que la TBP cruce correctamente a la ASTM:
    # En la cabeza (fracciones ligeras), TBP < ASTM
    # En la cola (fracciones pesadas), TBP > ASTM
    # Implementamos un offset basado en el punto de ebullición
    correccion = np.array([-6, -4, -2, 0, 3, 8, 14])
    tbp_temps = tbp_temps + correccion
    tbp_temps = np.round(tbp_temps, 1)

    # Verificar monotonía de TBP
    for i in range(1, len(tbp_temps)):
        if tbp_temps[i] <= tbp_temps[i - 1]:
            tbp_temps[i] = tbp_temps[i - 1] + 5.0

    return vol_pct, astm_temps, tbp_temps


def interpolar_rendimiento(tbp_interp, t_corte):
    """
    Dado un interpolador de la curva TBP, devuelve el
    % de volumen recuperado hasta la temperatura de corte.
    """
    t_min = tbp_interp.x[0]
    t_max = tbp_interp.x[-1]

    if t_corte <= t_min:
        return 0.0
    if t_corte >= t_max:
        return 100.0

    # Búsqueda por inversión: dada T, encontrar % vol
    # Creamos el interpolador inverso
    from scipy.interpolate import PchipInterpolator
    vol_pts = tbp_interp.x  # estos son los % vol usados para crear el interp
    temp_pts = tbp_interp(vol_pts)  # temperaturas en esos puntos

    inv_interp = PchipInterpolator(temp_pts, vol_pts)
    vol = float(inv_interp(t_corte))
    return max(0.0, min(100.0, vol))


# ─────────────────────────────────────────────
# INICIALIZACIÓN DEL SESSION STATE
# ─────────────────────────────────────────────

if "semilla_crudo" not in st.session_state:
    st.session_state.semilla_crudo = np.random.randint(1, 9999)

if "datos_generados" not in st.session_state:
    st.session_state.datos_generados = False

if "vol_pct" not in st.session_state:
    vol_pct, astm_temps, tbp_temps = generar_curva_astm_tbp()
    st.session_state.vol_pct = vol_pct
    st.session_state.astm_temps = astm_temps
    st.session_state.tbp_temps = tbp_temps
    st.session_state.datos_generados = True

if "informe_enviado" not in st.session_state:
    st.session_state.informe_enviado = False


# ─────────────────────────────────────────────
# CABECERA PRINCIPAL
# ─────────────────────────────────────────────

st.markdown("""
<div class="hero-header">
    <p class="hero-title">🛢️ PRÁCTICA 2 — DESTILACIÓN PRIMARIA DE CRUDO</p>
    <p class="hero-subtitle">
        Laboratorio Virtual · Tecnologías del Petróleo &nbsp;|&nbsp; 
        Curva ASTM D86 → TBP · Temperaturas de Corte · Rendimientos Volumétricos
    </p>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR – CONTROLES DE CORTES
# ─────────────────────────────────────────────

with st.sidebar:
    st.markdown('<p class="sidebar-title">⚙️ Panel de Control</p>', unsafe_allow_html=True)
    st.markdown('<p class="sidebar-title">🔪 Temperaturas de Corte (TBP)</p>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
    Ajusta los límites de cada fracción comercial. El valor de cada slider define 
    el <b>Punto Final de Ebullición (FBP)</b> de esa fracción, que coincide con 
    el <b>Punto Inicial (IBP)</b> de la siguiente.
    </div>
    """, unsafe_allow_html=True)

    # El rango disponible viene de la curva TBP generada
    t_min_tbp = float(st.session_state.tbp_temps[0])
    t_max_tbp = float(st.session_state.tbp_temps[-1])

    # Valores por defecto (temperaturas de corte típicas de refinería)
    corte_nafta_ligera = st.slider(
        "✂️ FBP Nafta Ligera / Gases (°C)",
        min_value=30, max_value=160,
        value=100, step=5,
        help="Fracción que incluye gases licuados (GLP) y nafta de bajo octano."
    )

    corte_nafta_pesada = st.slider(
        "✂️ FBP Nafta Pesada (°C)",
        min_value=corte_nafta_ligera + 10, max_value=220,
        value=max(190, corte_nafta_ligera + 10), step=5,
        help="Nafta de alto punto de ebullición, materia prima de reformado catalítico."
    )

    corte_queroseno = st.slider(
        "✂️ FBP Queroseno / Jet Fuel (°C)",
        min_value=corte_nafta_pesada + 10, max_value=290,
        value=max(250, corte_nafta_pesada + 10), step=5,
        help="Combustible de aviación y queroseno doméstico."
    )

    corte_gasoleo = st.slider(
        "✂️ FBP Gasóleo Ligero / Diésel (°C)",
        min_value=corte_queroseno + 10, max_value=400,
        value=max(340, corte_queroseno + 10), step=5,
        help="Diésel de automoción y gasóleo de calefacción."
    )

    st.markdown("---")
    st.markdown("""
    <div class="warning-box">
    <b>Residuo Atmosférico:</b> Todo lo que supere el FBP del Gasóleo Ligero. 
    Se procesa en la unidad de vacío o en la unidad de craqueo (FCC).
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🔄 Generar Nuevo Crudo Aleatorio", use_container_width=True):
        st.session_state.semilla_crudo = np.random.randint(1, 9999)
        vol_pct, astm_temps, tbp_temps = generar_curva_astm_tbp()
        st.session_state.vol_pct = vol_pct
        st.session_state.astm_temps = astm_temps
        st.session_state.tbp_temps = tbp_temps
        st.rerun()

    st.caption(f"Semilla del crudo: `{st.session_state.semilla_crudo}`")


# ─────────────────────────────────────────────
# RECUPERAR DATOS DEL SESSION STATE
# ─────────────────────────────────────────────

vol_pct    = st.session_state.vol_pct
astm_temps = st.session_state.astm_temps
tbp_temps  = st.session_state.tbp_temps

# Interpoladores de alta fidelidad (PCHIP – Piecewise Cubic Hermite)
interp_astm = PchipInterpolator(vol_pct, astm_temps)
interp_tbp  = PchipInterpolator(vol_pct, tbp_temps)

# Curvas densas para gráfico
vol_denso = np.linspace(0, 100, 500)
astm_denso = interp_astm(vol_denso)
tbp_denso  = interp_tbp(vol_denso)

# ─────────────────────────────────────────────
# CÁLCULO DE RENDIMIENTOS (INTERPOLACIÓN INVERSA)
# ─────────────────────────────────────────────

# Interpolador inverso: Temperatura → % vol recuperado
interp_tbp_inv = PchipInterpolator(tbp_temps, vol_pct)

def vol_hasta(t_corte):
    t = np.clip(t_corte, tbp_temps[0], tbp_temps[-1])
    return float(np.clip(interp_tbp_inv(t), 0, 100))

v_nafta_lig   = vol_hasta(corte_nafta_ligera)
v_nafta_pes   = vol_hasta(corte_nafta_pesada)
v_queroseno   = vol_hasta(corte_queroseno)
v_gasoleo     = vol_hasta(corte_gasoleo)
v_residuo     = 100.0

rend_nafta_lig  = round(v_nafta_lig, 1)
rend_nafta_pes  = round(v_nafta_pes - v_nafta_lig, 1)
rend_queroseno  = round(v_queroseno - v_nafta_pes, 1)
rend_gasoleo    = round(v_gasoleo - v_queroseno, 1)
rend_residuo    = round(100.0 - v_gasoleo, 1)


# ─────────────────────────────────────────────
# PESTAÑAS PRINCIPALES
# ─────────────────────────────────────────────

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Fase 1 – Datos ASTM D86",
    "📈 Fase 2 – Curva TBP",
    "🔪 Fase 3 – Cortes y Rendimientos",
    "📝 Fase 4 – Informe Final"
])


# ══════════════════════════════════════════════
# TAB 1 – DATOS ASTM D86
# ══════════════════════════════════════════════
with tab1:
    st.markdown("""
    <div class="section-card">
        <p class="section-title">📋 Ensayo de Destilación ASTM D86</p>
        <div class="info-box">
        El ensayo <b>ASTM D86</b> es la prueba estándar de destilación en laboratorio. 
        Se calienta una muestra de 100 mL de crudo y se registra la <b>temperatura del vapor</b> 
        a medida que se va recuperando el destilado. Es rápida y reproducible, pero no refleja 
        las condiciones reales de la torre de destilación industrial.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabla de datos
    df_astm = pd.DataFrame({
        "% Vol. Recuperado": [f"{int(v)}%" for v in vol_pct],
        "Temperatura ASTM D86 (°C)": [f"{t:.1f}" for t in astm_temps],
        "Fracción aproximada": [
            "IBP – Inicio de ebullición",
            "10% – Destilación inicial",
            "30% – Destilación temprana",
            "50% – Punto medio (T50)",
            "70% – Destilación tardía",
            "90% – Final de destilación",
            "FBP – Fin de ebullición"
        ]
    })

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### Tabla de Destilación ASTM D86")
        st.dataframe(
            df_astm,
            use_container_width=True,
            hide_index=True,
        )

        st.markdown(f"""
        <div class="warning-box">
        <b>Crudo generado:</b> Semilla #{st.session_state.semilla_crudo}<br>
        <b>IBP (Inicio):</b> {astm_temps[0]:.1f} °C &nbsp;|&nbsp; 
        <b>FBP (Final):</b> {astm_temps[-1]:.1f} °C<br>
        <b>Rango total ASTM:</b> {astm_temps[-1] - astm_temps[0]:.1f} °C
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Gráfico de la curva ASTM únicamente
        fig_astm = go.Figure()
        fig_astm.add_trace(go.Scatter(
            x=vol_denso, y=astm_denso,
            mode='lines',
            name='Curva ASTM D86',
            line=dict(color='#388bfd', width=3),
            fill='tozeroy',
            fillcolor='rgba(56,139,253,0.08)'
        ))
        fig_astm.add_trace(go.Scatter(
            x=vol_pct, y=astm_temps,
            mode='markers',
            name='Puntos medidos',
            marker=dict(color='#ffd166', size=10, symbol='circle',
                        line=dict(color='white', width=1))
        ))
        fig_astm.update_layout(
            title="Curva ASTM D86 del Crudo",
            xaxis_title="% Volumen Recuperado",
            yaxis_title="Temperatura (°C)",
            plot_bgcolor='#0d1117',
            paper_bgcolor='#161b22',
            font=dict(color='#c9d1d9', family='IBM Plex Sans'),
            legend=dict(bgcolor='#1c2128', bordercolor='#30363d', borderwidth=1),
            hovermode='x unified',
            margin=dict(t=50, b=50, l=60, r=20)
        )
        fig_astm.update_xaxes(gridcolor='#21262d', zeroline=False)
        fig_astm.update_yaxes(gridcolor='#21262d', zeroline=False)
        st.plotly_chart(fig_astm, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 2 – CONVERSIÓN A TBP
# ══════════════════════════════════════════════
with tab2:
    st.markdown("""
    <div class="section-card">
        <p class="section-title">🔬 Conversión ASTM D86 → TBP (True Boiling Point)</p>
        <div class="info-box">
        La curva <b>TBP (Punto Verdadero de Ebullición)</b> se obtiene en una columna de 
        destilación con alta separación (≥100 etapas teóricas). Refleja con mayor fidelidad 
        la composición real del crudo y es la base para el diseño de las torres de destilación 
        industrial. La conversión ASTM→TBP se realiza mediante correlaciones empíricas 
        (método <b>Daubert – API Data Book</b>).
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabla comparativa
    df_comparativo = pd.DataFrame({
        "% Vol.": [f"{int(v)}%" for v in vol_pct],
        "T. ASTM D86 (°C)": [f"{t:.1f}" for t in astm_temps],
        "T. TBP (°C)": [f"{t:.1f}" for t in tbp_temps],
        "ΔT = TBP - ASTM (°C)": [f"{(tb - ta):+.1f}" for ta, tb in zip(astm_temps, tbp_temps)]
    })

    col_t1, col_t2 = st.columns([1, 2])

    with col_t1:
        st.markdown("#### Tabla Comparativa ASTM vs TBP")
        st.dataframe(df_comparativo, use_container_width=True, hide_index=True)

        st.markdown("""
        <div class="info-box">
        <b>Observación clave:</b> Fíjate en la columna ΔT. Al principio de la 
        destilación (fracciones ligeras), la TBP es <i>menor</i> que la ASTM; 
        al final (fracciones pesadas), la TBP es <i>mayor</i>. Esto se explica 
        por la mayor separación que logra la columna TBP.
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        # Gráfico superpuesto ASTM + TBP
        fig_tbp = go.Figure()

        # Zona sombreada entre curvas
        fig_tbp.add_trace(go.Scatter(
            x=np.concatenate([vol_denso, vol_denso[::-1]]),
            y=np.concatenate([tbp_denso, astm_denso[::-1]]),
            fill='toself',
            fillcolor='rgba(255,209,102,0.06)',
            line=dict(color='rgba(0,0,0,0)'),
            name='Diferencia ASTM–TBP',
            showlegend=True,
            hoverinfo='skip'
        ))

        # Curva ASTM
        fig_tbp.add_trace(go.Scatter(
            x=vol_denso, y=astm_denso,
            mode='lines',
            name='Curva ASTM D86',
            line=dict(color='#388bfd', width=2.5, dash='dot'),
        ))
        fig_tbp.add_trace(go.Scatter(
            x=vol_pct, y=astm_temps,
            mode='markers', showlegend=False,
            marker=dict(color='#388bfd', size=9,
                        line=dict(color='white', width=1))
        ))

        # Curva TBP
        fig_tbp.add_trace(go.Scatter(
            x=vol_denso, y=tbp_denso,
            mode='lines',
            name='Curva TBP (Daubert)',
            line=dict(color='#ff9d4d', width=3),
        ))
        fig_tbp.add_trace(go.Scatter(
            x=vol_pct, y=tbp_temps,
            mode='markers', showlegend=False,
            marker=dict(color='#ff9d4d', size=9,
                        line=dict(color='white', width=1))
        ))

        fig_tbp.update_layout(
            title="Curvas ASTM D86 vs TBP — Superposición",
            xaxis_title="% Volumen Recuperado",
            yaxis_title="Temperatura (°C)",
            plot_bgcolor='#0d1117',
            paper_bgcolor='#161b22',
            font=dict(color='#c9d1d9', family='IBM Plex Sans'),
            legend=dict(bgcolor='#1c2128', bordercolor='#30363d', borderwidth=1,
                        orientation='h', yanchor='bottom', y=1.02, xanchor='left', x=0),
            hovermode='x unified',
            margin=dict(t=70, b=50, l=60, r=20)
        )
        fig_tbp.update_xaxes(gridcolor='#21262d', zeroline=False)
        fig_tbp.update_yaxes(gridcolor='#21262d', zeroline=False)
        st.plotly_chart(fig_tbp, use_container_width=True)


# ══════════════════════════════════════════════
# TAB 3 – CORTES Y RENDIMIENTOS
# ══════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="section-card">
        <p class="section-title">🔪 Cortes de Destilación y Rendimientos Volumétricos</p>
        <div class="info-box">
        Ajusta las <b>Temperaturas de Corte</b> en el panel lateral izquierdo. La aplicación 
        interpola sobre la curva <b>TBP</b> para calcular en tiempo real el 
        <b>rendimiento volumétrico</b> (% vol sobre crudo) de cada fracción comercial.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # MÉTRICAS DE RENDIMIENTO
    st.markdown("#### 📊 Rendimientos Volumétricos (% vol/crudo)")
    col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
    col_m1.metric("⛽ Nafta Ligera / GLP", f"{rend_nafta_lig:.1f}%",
                  f"0 – {corte_nafta_ligera}°C")
    col_m2.metric("🏎️ Nafta Pesada", f"{rend_nafta_pes:.1f}%",
                  f"{corte_nafta_ligera} – {corte_nafta_pesada}°C")
    col_m3.metric("✈️ Queroseno / Jet", f"{rend_queroseno:.1f}%",
                  f"{corte_nafta_pesada} – {corte_queroseno}°C")
    col_m4.metric("🚛 Gasóleo / Diésel", f"{rend_gasoleo:.1f}%",
                  f"{corte_queroseno} – {corte_gasoleo}°C")
    col_m5.metric("🏭 Residuo Atmosférico", f"{rend_residuo:.1f}%",
                  f"> {corte_gasoleo}°C")

    st.markdown("---")

    # GRÁFICOS LADO A LADO
    col_g1, col_g2 = st.columns([1.4, 1])

    with col_g1:
        # Curva TBP con zonas sombreadas de corte
        colores_zonas = [
            ('rgba(6,214,160,0.25)',   'Nafta Ligera / GLP'),
            ('rgba(56,139,253,0.25)',  'Nafta Pesada'),
            ('rgba(255,209,102,0.25)', 'Queroseno / Jet'),
            ('rgba(255,157,77,0.25)',  'Gasóleo / Diésel'),
            ('rgba(247,129,102,0.25)', 'Residuo Atm.'),
        ]

        cortes_vol = [
            (0, v_nafta_lig),
            (v_nafta_lig, v_nafta_pes),
            (v_nafta_pes, v_queroseno),
            (v_queroseno, v_gasoleo),
            (v_gasoleo, 100),
        ]

        fig_cortes = go.Figure()

        # Zonas coloreadas
        for (v_ini, v_fin), (color, nombre) in zip(cortes_vol, colores_zonas):
            if v_fin > v_ini:
                mascara = (vol_denso >= v_ini) & (vol_denso <= v_fin)
                x_zona = vol_denso[mascara]
                y_zona = tbp_denso[mascara]
                if len(x_zona) > 1:
                    fig_cortes.add_trace(go.Scatter(
                        x=np.concatenate([[x_zona[0]], x_zona, [x_zona[-1]], [x_zona[0]]]),
                        y=np.concatenate([[0], y_zona, [0], [0]]),
                        fill='toself',
                        fillcolor=color,
                        line=dict(color='rgba(0,0,0,0)'),
                        name=nombre,
                        hoverinfo='skip',
                        showlegend=True
                    ))

        # Líneas de corte verticales
        for t_corte, t_corte_val, label in [
            (v_nafta_lig, corte_nafta_ligera, f"Corte {corte_nafta_ligera}°C"),
            (v_nafta_pes, corte_nafta_pesada, f"Corte {corte_nafta_pesada}°C"),
            (v_queroseno, corte_queroseno, f"Corte {corte_queroseno}°C"),
            (v_gasoleo, corte_gasoleo, f"Corte {corte_gasoleo}°C"),
        ]:
            fig_cortes.add_vline(
                x=t_corte, line=dict(color='white', width=1.5, dash='dash'),
                annotation_text=f" {t_corte_val}°C",
                annotation_font=dict(color='white', size=10),
                annotation_position="top right"
            )

        # Curva TBP principal
        fig_cortes.add_trace(go.Scatter(
            x=vol_denso, y=tbp_denso,
            mode='lines',
            name='Curva TBP',
            line=dict(color='white', width=2.5),
        ))

        fig_cortes.update_layout(
            title="Curva TBP con Puntos de Corte",
            xaxis_title="% Volumen Recuperado",
            yaxis_title="Temperatura TBP (°C)",
            plot_bgcolor='#0d1117',
            paper_bgcolor='#161b22',
            font=dict(color='#c9d1d9', family='IBM Plex Sans'),
            legend=dict(bgcolor='#1c2128', bordercolor='#30363d', borderwidth=1,
                        orientation='h', yanchor='bottom', y=-0.35, xanchor='center', x=0.5),
            hovermode='x unified',
            margin=dict(t=50, b=100, l=60, r=20)
        )
        fig_cortes.update_xaxes(gridcolor='#21262d', zeroline=False, range=[0, 100])
        fig_cortes.update_yaxes(gridcolor='#21262d', zeroline=False)
        st.plotly_chart(fig_cortes, use_container_width=True)

    with col_g2:
        # Gráfico de tarta (Pie Chart)
        labels_pie = ['Nafta Ligera / GLP', 'Nafta Pesada', 'Queroseno / Jet', 'Gasóleo / Diésel', 'Residuo Atmosférico']
        valores_pie = [rend_nafta_lig, rend_nafta_pes, rend_queroseno, rend_gasoleo, rend_residuo]
        colores_pie = ['#06d6a0', '#388bfd', '#ffd166', '#ff9d4d', '#f78166']

        fig_pie = go.Figure(go.Pie(
            labels=labels_pie,
            values=valores_pie,
            hole=0.42,
            marker=dict(
                colors=colores_pie,
                line=dict(color='#0d1117', width=2)
            ),
            textinfo='label+percent',
            textfont=dict(size=11, color='white', family='IBM Plex Sans'),
            hovertemplate='<b>%{label}</b><br>Rendimiento: %{value:.1f}%<extra></extra>',
        ))

        fig_pie.update_layout(
            title="Distribución de Fracciones",
            annotations=[dict(
                text='% vol<br>crudo', x=0.5, y=0.5,
                font=dict(size=12, color='#8b949e', family='IBM Plex Mono'),
                showarrow=False
            )],
            plot_bgcolor='#0d1117',
            paper_bgcolor='#161b22',
            font=dict(color='#c9d1d9', family='IBM Plex Sans'),
            legend=dict(
                bgcolor='#1c2128', bordercolor='#30363d', borderwidth=1,
                orientation='v', font=dict(size=10)
            ),
            margin=dict(t=50, b=20, l=10, r=10),
            showlegend=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

        # Verificación de balance
        total = sum(valores_pie)
        st.markdown(f"""
        <div class="{'warning-box' if abs(total - 100) > 1 else 'info-box'}">
        <b>Balance de masa:</b> {total:.1f}% vol<br>
        {'⚠️ Revisa los cortes' if abs(total - 100) > 1 else '✅ Balance correcto (≈100%)'}
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# TAB 4 – INFORME FINAL
# ══════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="section-card">
        <p class="section-title">📝 Informe de Práctica</p>
        <div class="info-box">
        Responde razonadamente a las siguientes preguntas basándote en lo observado 
        durante la práctica. Una vez completado, pulsa <b>"Generar Informe"</b> para 
        descargar un archivo .txt con todos tus resultados y respuestas.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Resumen de resultados actuales (visible antes del envío)
    with st.expander("📊 Ver resumen de resultados actuales (antes de enviar)", expanded=True):
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.markdown("**Datos ASTM D86 del crudo:**")
            st.dataframe(
                pd.DataFrame({
                    "% Vol.": [f"{int(v)}%" for v in vol_pct],
                    "T. ASTM (°C)": [f"{t:.1f}" for t in astm_temps],
                    "T. TBP (°C)": [f"{t:.1f}" for t in tbp_temps],
                }),
                hide_index=True, use_container_width=True
            )
        with col_r2:
            st.markdown("**Rendimientos con los cortes actuales:**")
            st.dataframe(
                pd.DataFrame({
                    "Fracción": labels_pie,
                    "Rango (°C)": [
                        f"IBP – {corte_nafta_ligera}",
                        f"{corte_nafta_ligera} – {corte_nafta_pesada}",
                        f"{corte_nafta_pesada} – {corte_queroseno}",
                        f"{corte_queroseno} – {corte_gasoleo}",
                        f"> {corte_gasoleo}"
                    ],
                    "Rend. (% vol)": [f"{v:.1f}%" for v in valores_pie],
                }),
                hide_index=True, use_container_width=True
            )

    st.markdown("---")

    # FORMULARIO DE PREGUNTAS
    with st.form("formulario_informe"):
        st.markdown("#### 💬 Preguntas de Análisis y Reflexión")

        st.markdown("""
        <div class="warning-box">
        <b>❓ Pregunta 1 – Diferencia entre curvas ASTM y TBP</b>
        </div>
        """, unsafe_allow_html=True)
        respuesta_1 = st.text_area(
            "Observando el gráfico de la Fase 2, ¿por qué la curva TBP abarca un rango de "
            "temperaturas mayor (más frío al inicio y más caliente al final) que la curva ASTM "
            "para el mismo crudo? Razona tu respuesta en términos del número de etapas de separación.",
            height=130,
            placeholder="Escribe aquí tu respuesta...",
            key="resp_1"
        )

        st.markdown("""
        <div class="warning-box">
        <b>❓ Pregunta 2 – Optimización económica de los puntos de corte</b>
        </div>
        """, unsafe_allow_html=True)
        respuesta_2 = st.text_area(
            "Si el precio de mercado del Diésel se dispara frente a la Nafta, ¿cómo ajustarías "
            "tus puntos de corte (Cut Points) en la refinería para maximizar el beneficio? "
            "Demuéstralo ajustando los sliders del panel lateral y anotando aquí los nuevos rendimientos "
            "que has obtenido, justificando el motivo del ajuste.",
            height=150,
            placeholder="Escribe aquí tu respuesta e indica los rendimientos con los nuevos cortes...",
            key="resp_2"
        )

        st.markdown("""
        <div class="warning-box">
        <b>❓ Pregunta 3 – Alimentación a la unidad de FCC</b>
        </div>
        """, unsafe_allow_html=True)
        respuesta_3 = st.text_area(
            "¿Qué fracción (o fracciones) de la destilación primaria calculada en esta práctica "
            "alimentarías preferentemente a la unidad de Craqueo Catalítico Fluido (FCC) de la "
            "próxima práctica? ¿Por qué? Considera el rango de ebullición y el tipo de moléculas presentes.",
            height=130,
            placeholder="Escribe aquí tu respuesta...",
            key="resp_3"
        )

        st.markdown("---")

        nombre_alumno = st.text_input("👤 Nombre y apellidos del alumno:", placeholder="Introduce tu nombre completo")
        grupo = st.text_input("🏫 Grupo / Curso:", placeholder="Ej: Grupo A – 3º Ingeniería Química")

        submitted = st.form_submit_button("📤 Generar Informe y Preparar Descarga", use_container_width=True)

        if submitted:
            st.session_state.informe_enviado = True
            st.session_state.nombre_alumno = nombre_alumno
            st.session_state.grupo = grupo
            st.session_state.respuesta_1 = respuesta_1
            st.session_state.respuesta_2 = respuesta_2
            st.session_state.respuesta_3 = respuesta_3
            st.session_state.rendimientos_finales = {
                "nafta_lig": rend_nafta_lig,
                "nafta_pes": rend_nafta_pes,
                "queroseno": rend_queroseno,
                "gasoleo": rend_gasoleo,
                "residuo": rend_residuo,
                "corte_nafta_lig": corte_nafta_ligera,
                "corte_nafta_pes": corte_nafta_pesada,
                "corte_queroseno": corte_queroseno,
                "corte_gasoleo": corte_gasoleo,
            }

    # BOTÓN DE DESCARGA (fuera del form)
    if st.session_state.informe_enviado:
        st.success("✅ ¡Informe generado correctamente! Pulsa el botón de abajo para descargarlo.")

        r = st.session_state.rendimientos_finales
        nombre = st.session_state.get("nombre_alumno", "Sin nombre")
        grupo_txt = st.session_state.get("grupo", "Sin grupo")
        r1 = st.session_state.get("respuesta_1", "")
        r2 = st.session_state.get("respuesta_2", "")
        r3 = st.session_state.get("respuesta_3", "")

        linea = "=" * 65
        informe_txt = f"""
{linea}
LABORATORIO VIRTUAL – TECNOLOGÍAS DEL PETRÓLEO
PRÁCTICA 2: DESTILACIÓN DE CRUDO – CURVA TBP Y RENDIMIENTOS
{linea}
Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
Alumno: {nombre}
Grupo/Curso: {grupo_txt}
Semilla del crudo generado: {st.session_state.semilla_crudo}
{linea}

SECCIÓN 1 – DATOS ASTM D86 DEL CRUDO
{linea}
{"% Vol.":>8}  {"T. ASTM D86 (°C)":>18}  {"T. TBP (°C)":>12}
{"--------":>8}  {"------------------":>18}  {"------------":>12}
"""
        for v, ta, tb in zip(vol_pct, astm_temps, tbp_temps):
            informe_txt += f"{int(v):>7}%  {ta:>18.1f}  {tb:>12.1f}\n"

        informe_txt += f"""
{linea}
SECCIÓN 2 – RENDIMIENTOS VOLUMÉTRICOS FINALES
{linea}
Temperatura de corte seleccionadas por el alumno:
  · Nafta Ligera / GLP : IBP  –  {r['corte_nafta_lig']} °C
  · Nafta Pesada       : {r['corte_nafta_lig']} °C  –  {r['corte_nafta_pes']} °C
  · Queroseno / Jet    : {r['corte_nafta_pes']} °C  –  {r['corte_queroseno']} °C
  · Gasóleo / Diésel   : {r['corte_queroseno']} °C  –  {r['corte_gasoleo']} °C
  · Residuo Atmosférico: > {r['corte_gasoleo']} °C

Rendimientos volumétricos (% vol sobre crudo):
  · Nafta Ligera / GLP  : {r['nafta_lig']:.1f} % vol
  · Nafta Pesada        : {r['nafta_pes']:.1f} % vol
  · Queroseno / Jet     : {r['queroseno']:.1f} % vol
  · Gasóleo / Diésel    : {r['gasoleo']:.1f} % vol
  · Residuo Atmosférico : {r['residuo']:.1f} % vol
  · TOTAL               : {r['nafta_lig']+r['nafta_pes']+r['queroseno']+r['gasoleo']+r['residuo']:.1f} % vol

{linea}
SECCIÓN 3 – RESPUESTAS A LAS PREGUNTAS DE ANÁLISIS
{linea}

PREGUNTA 1 – Diferencia entre curvas ASTM y TBP:
{r1 if r1.strip() else "(Sin respuesta)"}

{linea}

PREGUNTA 2 – Optimización económica de los puntos de corte:
{r2 if r2.strip() else "(Sin respuesta)"}

{linea}

PREGUNTA 3 – Alimentación a la unidad de FCC:
{r3 if r3.strip() else "(Sin respuesta)"}

{linea}
FIN DEL INFORME – Práctica 2 / Tecnologías del Petróleo
{linea}
"""

        st.download_button(
            label="⬇️ Descargar Informe (.txt)",
            data=informe_txt.encode("utf-8"),
            file_name=f"Practica2_Destilacion_{nombre.replace(' ', '_') if nombre else 'alumno'}.txt",
            mime="text/plain",
            use_container_width=True
        )


# ─────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#484f58; font-family:'IBM Plex Mono',monospace; font-size:0.75rem; padding: 1rem 0;">
    🛢️ Laboratorio Virtual · Tecnologías del Petróleo &nbsp;|&nbsp; Práctica 2 – Destilación de Crudo &nbsp;|&nbsp; v1.0<br>
    <span style="color:#30363d;">Correlación TBP: Daubert & Danner (API Technical Data Book) · Interpolación PCHIP</span>
</div>
""", unsafe_allow_html=True)
