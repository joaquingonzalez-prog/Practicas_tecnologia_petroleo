"""
=============================================================================
PRÁCTICA 3 – Laboratorio Virtual de Refino
Simulación de Unidad FCC y Blending de Gasolina
=============================================================================
Asignatura : Tecnología del Petróleo y Petroquímica
Autor      : Laboratorio Virtual – Generado automáticamente
Descripción: App Streamlit que simula un reactor FCC y una unidad de Blending
             para formular gasolina comercial de 95 RON al menor coste posible.
=============================================================================
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Práctica 3 – FCC & Blending",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONALIZADO  –  Estética industrial / refino
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Exo 2', sans-serif;
}

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b2838 60%, #0d1b2a 100%);
    color: #e0e6ed;
}

/* Cabecera principal */
.main-header {
    background: linear-gradient(90deg, #ff6b35, #f7931e, #ff6b35);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-align: center;
    padding: 10px 0 4px 0;
}

.sub-header {
    text-align: center;
    color: #8899aa;
    font-size: 0.9rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

/* Tarjetas métricas */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,107,53,0.3);
    border-radius: 10px;
    padding: 15px 20px;
    text-align: center;
    backdrop-filter: blur(5px);
}

.metric-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2rem;
    color: #f7931e;
    font-weight: 700;
}

.metric-label {
    font-size: 0.75rem;
    color: #8899aa;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Pestañas */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,27,42,0.8);
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #8899aa;
    border-radius: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 1px;
    padding: 8px 20px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ff6b35, #f7931e) !important;
    color: white !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] {
    margin-top: 6px;
}

/* Botones */
.stButton > button {
    background: linear-gradient(135deg, #ff6b35, #f7931e);
    color: white;
    border: none;
    border-radius: 8px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 1px;
    padding: 10px 24px;
    transition: all 0.3s;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(255,107,53,0.4);
}

/* Info / warning / error */
.stAlert {
    border-radius: 10px;
}

/* Divisor */
hr {
    border-color: rgba(255,107,53,0.2);
}

/* Sección de estado de operación */
.status-box {
    background: rgba(255,107,53,0.1);
    border-left: 4px solid #ff6b35;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 10px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #f7931e;
}

.status-box-green {
    background: rgba(46,213,115,0.1);
    border-left: 4px solid #2ed573;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 10px 0;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #2ed573;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN DEL SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_session_state():
    """Inicializa todas las variables del estado de sesión con valores por defecto."""
    defaults = {
        # Resultados del FCC (vacíos hasta que el alumno pulse el botón)
        "fcc_operacion_fijada": False,
        "fcc_rendimiento_nafta": None,   # % en volumen de nafta FCC producida
        "fcc_ron_nafta": None,           # RON de la nafta FCC producida
        "fcc_temperatura": 510,
        "fcc_co_ratio": 6.0,
        # Blending
        "blend_pct_nafta_fcc": 20.0,
        "blend_pct_nafta_ligera": 20.0,
        "blend_pct_reformado": 30.0,
        "blend_pct_alquilato": 30.0,
        # Informe
        "respuesta_1": "",
        "respuesta_2": "",
        "respuesta_3": "",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()

# ─────────────────────────────────────────────────────────────────────────────
# MODELOS MATEMÁTICOS DEL FCC
# ─────────────────────────────────────────────────────────────────────────────
def calcular_fcc(temp: float, co_ratio: float) -> dict:
    """
    Modelo simplificado del FCC.
    Parámetros:
        temp     : Temperatura del reactor (°C), rango 480–550
        co_ratio : Relación catalizador/carga (adimensional), rango 4–9
    Retorna dict con rendimientos (% masa sobre carga fresca) y RON.
    """
    # ── Conversión total ──────────────────────────────────────────────────────
    # Sube con T y C/O de forma cuasi-lineal
    conv = 55 + (temp - 480) * 0.45 + (co_ratio - 4) * 1.8
    conv = np.clip(conv, 0, 98)

    # ── Rendimiento de nafta (C5-221°C) ──────────────────────────────────────
    # Tiene un máximo cerca de 525°C; sube hasta ahí, luego baja por sobrecraqueo
    temp_optima = 525.0
    nafta = 48 + (temp - 480) * 0.35 - ((temp - temp_optima) ** 2) * 0.018
    nafta += (co_ratio - 4) * 0.4
    nafta = np.clip(nafta, 5, 58)

    # ── Gas seco (C1-C2) ─────────────────────────────────────────────────────
    # Aumenta fuertemente por encima de 520°C (craqueo térmico secundario)
    gas_seco = 1.5 + max(0, (temp - 510)) * 0.12 + (co_ratio - 4) * 0.05
    gas_seco = np.clip(gas_seco, 0, 8)

    # ── GLP (C3-C4) ──────────────────────────────────────────────────────────
    glp = 12 + (temp - 480) * 0.08 + (co_ratio - 4) * 0.3
    glp = np.clip(glp, 5, 22)

    # ── Coque ─────────────────────────────────────────────────────────────────
    coque = 3.5 + (co_ratio - 4) * 0.35 + (temp - 480) * 0.025
    coque = np.clip(coque, 0, 10)

    # ── Residuo sin convertir (HCO) ──────────────────────────────────────────
    residuo = max(0, 100 - nafta - gas_seco - glp - coque)
    residuo = np.clip(residuo, 0, 50)

    # ── RON de la nafta FCC ──────────────────────────────────────────────────
    # Relación lineal: 88 a 480°C → 95 a 550°C
    ron = 88 + (temp - 480) * (7 / 70)
    ron = np.clip(ron, 88, 95)

    return {
        "conv": round(conv, 1),
        "nafta": round(nafta, 1),
        "gas_seco": round(gas_seco, 1),
        "glp": round(glp, 1),
        "coque": round(coque, 1),
        "residuo": round(residuo, 1),
        "ron": round(ron, 1),
    }

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS DE GRÁFICOS  (Plotly)
# ─────────────────────────────────────────────────────────────────────────────
COLORES_PLOTLY = {
    "nafta":    "#f7931e",
    "glp":      "#ffd166",
    "gas_seco": "#ef476f",
    "coque":    "#555555",
    "residuo":  "#264653",
}

def gauge_ron(ron_value: float, titulo: str = "RON Final") -> go.Figure:
    """Gauge de RON con semáforo verde/rojo según supere 95."""
    color = "#2ed573" if ron_value >= 95 else "#ff4757"
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=ron_value,
        delta={"reference": 95, "valueformat": ".1f",
               "increasing": {"color": "#2ed573"},
               "decreasing": {"color": "#ff4757"}},
        title={"text": titulo, "font": {"size": 16, "color": "#e0e6ed",
                                         "family": "Share Tech Mono"}},
        number={"font": {"size": 40, "color": color, "family": "Share Tech Mono"},
                "valueformat": ".1f"},
        gauge={
            "axis": {"range": [60, 110], "tickwidth": 1,
                     "tickcolor": "#8899aa", "tickfont": {"color": "#8899aa"}},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [60, 80],  "color": "rgba(255,71,87,0.15)"},
                {"range": [80, 95],  "color": "rgba(255,165,0,0.15)"},
                {"range": [95, 110], "color": "rgba(46,213,115,0.15)"},
            ],
            "threshold": {
                "line": {"color": "#ff6b35", "width": 3},
                "thickness": 0.8,
                "value": 95,
            },
        }
    ))
    fig.update_layout(
        height=280,
        margin=dict(l=20, r=20, t=60, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

def barras_rendimientos(datos: dict) -> go.Figure:
    """Gráfico de barras apiladas con los rendimientos del FCC."""
    categorias = ["Nafta FCC", "GLP", "Gas Seco", "Coque", "Residuo (HCO)"]
    valores    = [datos["nafta"], datos["glp"], datos["gas_seco"],
                  datos["coque"], datos["residuo"]]
    colores_barra = [COLORES_PLOTLY["nafta"], COLORES_PLOTLY["glp"],
                     COLORES_PLOTLY["gas_seco"], COLORES_PLOTLY["coque"],
                     COLORES_PLOTLY["residuo"]]

    fig = go.Figure()
    for cat, val, col in zip(categorias, valores, colores_barra):
        fig.add_trace(go.Bar(
            name=cat, x=["Rendimiento FCC"], y=[val],
            marker_color=col, text=[f"{val:.1f}%"],
            textposition="inside", textfont={"color": "white", "size": 11},
        ))

    fig.update_layout(
        barmode="stack",
        height=340,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, x=0.5,
                    xanchor="center", font=dict(color="#e0e6ed", size=11)),
        yaxis=dict(title="% sobre carga fresca",
                   gridcolor="rgba(255,255,255,0.05)", color="#8899aa"),
        xaxis=dict(color="#8899aa"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=80),
        font=dict(family="Exo 2", color="#e0e6ed"),
    )
    return fig

def pie_blend(pcts: dict, labels: list) -> go.Figure:
    """Gráfico de tarta para la receta de blending."""
    colores = ["#f7931e", "#ffd166", "#ef476f", "#06d6a0"]
    fig = go.Figure(go.Pie(
        labels=labels, values=[pcts[k] for k in pcts],
        marker=dict(colors=colores,
                    line=dict(color="#0d1b2a", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, color="white"),
        hole=0.4,
    ))
    fig.update_layout(
        height=300,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=20, b=20),
        showlegend=False,
        font=dict(family="Exo 2", color="#e0e6ed"),
    )
    return fig

# ─────────────────────────────────────────────────────────────────────────────
# CABECERA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🛢️ LABORATORIO VIRTUAL DE REFINO</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Práctica 3 · FCC + Blending de Gasolina · Tecnología del Petróleo</div>', unsafe_allow_html=True)
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# PESTAÑAS PRINCIPALES
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "⚙️  1. Unidad FCC",
    "🧪  2. Unidad de Blending",
    "📋  3. Informe Final",
])

# ═════════════════════════════════════════════════════════════════════════════
#  PESTAÑA 1 – UNIDAD FCC
# ═════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### ⚙️ Simulación del Reactor de Craqueo Catalítico Fluido (FCC)")
    st.markdown(
        "Ajusta las variables de operación y observa cómo cambian los rendimientos. "
        "Cuando estés satisfecho con tu configuración, pulsa el botón para enviar "
        "la nafta producida a los tanques intermedios."
    )
    st.markdown("---")

    col_ctrl, col_res = st.columns([1, 2], gap="large")

    # ── Controles de operación ─────────────────────────────────────────────
    with col_ctrl:
        st.markdown("#### 🎛️ Variables de Operación")
        temperatura = st.slider(
            "**Temperatura del Reactor (°C)**",
            min_value=480, max_value=550, value=st.session_state.fcc_temperatura,
            step=1, key="slider_temp",
            help="A mayor temperatura aumenta la conversión pero puede producir sobrecraqueo y más gas seco.",
        )
        co_ratio = st.slider(
            "**Relación Catalizador/Carga (C/O)**",
            min_value=4.0, max_value=9.0, value=st.session_state.fcc_co_ratio,
            step=0.1, key="slider_co",
            help="Mayor C/O implica más actividad catalítica pero también más depósito de coque.",
        )
        st.session_state.fcc_temperatura = temperatura
        st.session_state.fcc_co_ratio    = co_ratio

    # ── Cálculo del modelo ─────────────────────────────────────────────────
    datos_fcc = calcular_fcc(temperatura, co_ratio)
    unidad_parada = datos_fcc["coque"] > 5.5

    with col_ctrl:
        st.markdown("---")
        st.markdown("#### 📊 Parámetros Clave")

        m1, m2 = st.columns(2)
        m1.metric("Conversión total", f"{datos_fcc['conv']} %")
        m2.metric("RON nafta FCC",     f"{datos_fcc['ron']:.1f}")
        m3, m4 = st.columns(2)
        m3.metric("Rendimiento nafta", f"{datos_fcc['nafta']} %",
                  delta=None if unidad_parada else None)
        m4.metric("Coque generado",    f"{datos_fcc['coque']} %",
                  delta=f"{datos_fcc['coque'] - 5.5:.2f} vs límite" if datos_fcc["coque"] > 5.0 else None,
                  delta_color="inverse")

    # ── Alarma de sobrecalentamiento ───────────────────────────────────────
    with col_res:
        if unidad_parada:
            st.error(
                f"🚨 **ALARMA CRÍTICA – REGENERADOR SOBRECALENTADO**\n\n"
                f"El coque generado ({datos_fcc['coque']} %) supera el límite de diseño del regenerador (5.5 %). "
                f"La temperatura del lecho ha alcanzado niveles peligrosos. **UNIDAD PARADA POR SEGURIDAD.**\n\n"
                f"👉 Reduce la relación C/O o la temperatura para retomar la operación.",
                icon="🔥",
            )
            datos_fcc["nafta"]    = 0.0
            datos_fcc["glp"]      = 0.0
            datos_fcc["gas_seco"] = 0.0
            datos_fcc["residuo"]  = 100.0
        else:
            if datos_fcc["coque"] > 4.8:
                st.warning(
                    f"⚠️ Coque en {datos_fcc['coque']} % – Cerca del límite del regenerador (5.5 %). "
                    "Considera reducir C/O o temperatura.",
                    icon="⚠️",
                )

        # ── Gráfico de rendimientos ────────────────────────────────────────
        st.markdown("#### 📈 Distribución de Rendimientos")
        st.plotly_chart(barras_rendimientos(datos_fcc), use_container_width=True)

        # ── Gauge de RON de nafta producida ──────────────────────────────
        col_gauge, col_info = st.columns([1, 1])
        with col_gauge:
            st.plotly_chart(
                gauge_ron(datos_fcc["ron"], "RON Nafta FCC"),
                use_container_width=True,
            )
        with col_info:
            st.markdown("#### ℹ️ Notas de Proceso")
            st.markdown(f"""
| Corriente      | Valor       |
|----------------|-------------|
| Nafta FCC      | **{datos_fcc['nafta']} %** |
| GLP (C3–C4)    | {datos_fcc['glp']} % |
| Gas Seco (C1–C2) | {datos_fcc['gas_seco']} % |
| Coque          | {datos_fcc['coque']} % |
| Residuo (HCO)  | {datos_fcc['residuo']} % |
| **Total**      | **{datos_fcc['nafta']+datos_fcc['glp']+datos_fcc['gas_seco']+datos_fcc['coque']+datos_fcc['residuo']:.1f} %** |
""")

    st.markdown("---")

    # ── Botón de fijación de operación ─────────────────────────────────────
    col_btn, col_status = st.columns([1, 2])
    with col_btn:
        boton_fijar = st.button(
            "✅ Fijar Operación y Enviar a Tanques",
            type="primary",
            disabled=unidad_parada,
            help="Guarda los resultados del FCC para usarlos en la unidad de Blending.",
        )

    if boton_fijar and not unidad_parada:
        st.session_state.fcc_operacion_fijada  = True
        st.session_state.fcc_rendimiento_nafta = datos_fcc["nafta"]
        st.session_state.fcc_ron_nafta         = datos_fcc["ron"]
        with col_status:
            st.markdown(
                f'<div class="status-box-green">'
                f'✅ OPERACIÓN FIJADA — Nafta enviada a tanques<br>'
                f'▸ Rendimiento: {datos_fcc["nafta"]} % &nbsp;|&nbsp; RON: {datos_fcc["ron"]:.1f}<br>'
                f'▸ T = {temperatura} °C &nbsp;|&nbsp; C/O = {co_ratio:.1f}<br>'
                f'▸ Ahora ve a la pestaña  👉  "2. Unidad de Blending"'
                f'</div>',
                unsafe_allow_html=True,
            )

    # Mostrar estado actual si ya se fijó antes
    if st.session_state.fcc_operacion_fijada and not boton_fijar:
        with col_status:
            st.markdown(
                f'<div class="status-box">'
                f'📦 NAFTA EN TANQUES (última operación fijada)<br>'
                f'▸ Rendimiento: {st.session_state.fcc_rendimiento_nafta} % &nbsp;|&nbsp;'
                f'RON: {st.session_state.fcc_ron_nafta:.1f}'
                f'</div>',
                unsafe_allow_html=True,
            )

# ═════════════════════════════════════════════════════════════════════════════
#  PESTAÑA 2 – UNIDAD DE BLENDING
# ═════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 🧪 Unidad de Blending – Formulación de Gasolina 95 RON")

    # ── Comprobación: ¿se ha fijado el FCC? ───────────────────────────────
    if not st.session_state.fcc_operacion_fijada:
        st.warning(
            "⚠️ **Aún no has fijado la operación del FCC.**\n\n"
            "Ve primero a la pestaña **'1. Unidad FCC'**, ajusta las condiciones de operación "
            "y pulsa el botón **'Fijar Operación y Enviar a Tanques'** para disponer de nafta FCC "
            "en los tanques intermedios.",
            icon="⚠️",
        )
        st.stop()

    # ── Datos recibidos del FCC ────────────────────────────────────────────
    nafta_fcc_max = st.session_state.fcc_rendimiento_nafta   # % máx disponible
    nafta_fcc_ron = st.session_state.fcc_ron_nafta            # RON de la nafta FCC

    st.info(
        f"📦 **Nafta FCC disponible en tanques:** {nafta_fcc_max:.1f} % de la carga  |  "
        f"RON = {nafta_fcc_ron:.1f}  |  Coste = 90 $/bbl",
        icon="ℹ️",
    )
    st.markdown(
        "Formula la gasolina ajustando los porcentajes de cada corriente. "
        "La suma **debe ser exactamente 100 %**. El objetivo es alcanzar **≥ 95 RON** "
        "al **menor coste posible**."
    )
    st.markdown("---")

    # ── Propiedades fijas de las corrientes ───────────────────────────────
    corrientes = {
        "Nafta FCC":              {"ron": nafta_fcc_ron, "coste": 90,  "color": "#f7931e"},
        "Nafta Ligera Destilación":{"ron": 70,            "coste": 70,  "color": "#ffd166"},
        "Reformado Catalítico":   {"ron": 100,            "coste": 115, "color": "#ef476f"},
        "Alquilato":              {"ron": 97,             "coste": 105, "color": "#06d6a0"},
    }

    col_slid, col_gauges = st.columns([1, 1], gap="large")

    with col_slid:
        st.markdown("#### 🎛️ Receta de Mezcla")

        pct_nafta_fcc     = st.slider(
            f"**Nafta FCC** (RON {nafta_fcc_ron:.1f} | 90 $/bbl)  [máx {nafta_fcc_max:.0f}%]",
            0.0, float(nafta_fcc_max),
            value=min(st.session_state.blend_pct_nafta_fcc, float(nafta_fcc_max)),
            step=0.5, key="sl_nafta_fcc",
        )
        pct_nafta_ligera  = st.slider(
            "**Nafta Ligera** (RON 70 | 70 $/bbl)",
            0.0, 100.0, value=st.session_state.blend_pct_nafta_ligera,
            step=0.5, key="sl_nafta_ligera",
        )
        pct_reformado     = st.slider(
            "**Reformado Catalítico** (RON 100 | 115 $/bbl)",
            0.0, 100.0, value=st.session_state.blend_pct_reformado,
            step=0.5, key="sl_reformado",
        )
        pct_alquilato     = st.slider(
            "**Alquilato** (RON 97 | 105 $/bbl)",
            0.0, 100.0, value=st.session_state.blend_pct_alquilato,
            step=0.5, key="sl_alquilato",
        )

        # Guardar en session_state
        st.session_state.blend_pct_nafta_fcc    = pct_nafta_fcc
        st.session_state.blend_pct_nafta_ligera = pct_nafta_ligera
        st.session_state.blend_pct_reformado    = pct_reformado
        st.session_state.blend_pct_alquilato    = pct_alquilato

        total_pct = pct_nafta_fcc + pct_nafta_ligera + pct_reformado + pct_alquilato
        desviacion = abs(total_pct - 100.0)

        # Indicador de suma
        if desviacion < 0.01:
            st.markdown(
                '<div class="status-box-green">✅ Suma = 100.0 % — Receta válida</div>',
                unsafe_allow_html=True,
            )
        else:
            diferencia = total_pct - 100.0
            signo = "+" if diferencia > 0 else ""
            st.markdown(
                f'<div class="status-box">⚠️ Suma = {total_pct:.1f} % '
                f'({signo}{diferencia:.1f} % respecto a 100 %)<br>'
                f'Ajusta los sliders hasta sumar exactamente 100 %</div>',
                unsafe_allow_html=True,
            )

    # ── Cálculo del blending ───────────────────────────────────────────────
    if desviacion < 0.01:
        # Fracciones (entre 0 y 1)
        f_nfcc = pct_nafta_fcc    / 100
        f_nl   = pct_nafta_ligera / 100
        f_ref  = pct_reformado    / 100
        f_alk  = pct_alquilato    / 100

        ron_final   = (f_nfcc * nafta_fcc_ron +
                       f_nl   * 70 +
                       f_ref  * 100 +
                       f_alk  * 97)
        coste_final = (f_nfcc * 90 +
                       f_nl   * 70 +
                       f_ref  * 115 +
                       f_alk  * 105)

        with col_gauges:
            st.markdown("#### 🎯 Gasolina Final")
            st.plotly_chart(gauge_ron(ron_final, "RON Gasolina Final"), use_container_width=True)

            mc1, mc2 = st.columns(2)
            mc1.metric("RON Final", f"{ron_final:.2f}",
                       delta=f"{ron_final - 95:.2f} vs 95",
                       delta_color="normal")
            mc2.metric("Coste Total", f"{coste_final:.2f} $/bbl")

            if ron_final >= 95:
                st.success(f"✅ **Especificación alcanzada** – RON {ron_final:.2f} ≥ 95", icon="✅")
            else:
                st.error(
                    f"❌ **Fuera de especificación** – RON {ron_final:.2f} < 95\n\n"
                    "Aumenta la proporción de Reformado o Alquilato.",
                    icon="❌",
                )

            # Tarta de receta
            st.markdown("#### 🥧 Composición de la Mezcla")
            pcts_dict = {
                "Nafta FCC": pct_nafta_fcc,
                "Nafta Ligera": pct_nafta_ligera,
                "Reformado": pct_reformado,
                "Alquilato": pct_alquilato,
            }
            st.plotly_chart(pie_blend(pcts_dict, list(pcts_dict.keys())), use_container_width=True)

    else:
        with col_gauges:
            st.warning("Ajusta la receta hasta que la suma sea exactamente 100 % para ver los resultados.", icon="⚙️")

# ═════════════════════════════════════════════════════════════════════════════
#  PESTAÑA 3 – INFORME FINAL
# ═════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 📋 Informe Final de la Práctica 3")
    st.markdown(
        "Responde razonadamente a las preguntas siguientes. "
        "Al pulsar **'Enviar Informe'** se generará un archivo `.txt` descargable "
        "con todos los datos de tu sesión y tus respuestas."
    )
    st.markdown("---")

    # ── Resumen de resultados ──────────────────────────────────────────────
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        st.markdown("#### ⚙️ Resultados FCC Fijados")
        if st.session_state.fcc_operacion_fijada:
            st.markdown(f"""
| Parámetro            | Valor |
|----------------------|-------|
| Temperatura          | {st.session_state.fcc_temperatura} °C |
| C/O Ratio            | {st.session_state.fcc_co_ratio:.1f} |
| Rendimiento nafta    | {st.session_state.fcc_rendimiento_nafta:.1f} % |
| RON nafta FCC        | {st.session_state.fcc_ron_nafta:.1f} |
""")
        else:
            st.warning("No has fijado aún la operación del FCC.", icon="⚠️")

    with col_r2:
        st.markdown("#### 🧪 Receta de Blending")
        blend_sum = (st.session_state.blend_pct_nafta_fcc +
                     st.session_state.blend_pct_nafta_ligera +
                     st.session_state.blend_pct_reformado +
                     st.session_state.blend_pct_alquilato)
        if abs(blend_sum - 100) < 0.1 and st.session_state.fcc_operacion_fijada:
            f_nfcc = st.session_state.blend_pct_nafta_fcc    / 100
            f_nl   = st.session_state.blend_pct_nafta_ligera / 100
            f_ref  = st.session_state.blend_pct_reformado    / 100
            f_alk  = st.session_state.blend_pct_alquilato    / 100
            ron_inf   = (f_nfcc * st.session_state.fcc_ron_nafta + f_nl*70 + f_ref*100 + f_alk*97)
            coste_inf = (f_nfcc * 90 + f_nl*70 + f_ref*115 + f_alk*105)
            st.markdown(f"""
| Corriente                | %     |
|--------------------------|-------|
| Nafta FCC                | {st.session_state.blend_pct_nafta_fcc:.1f} % |
| Nafta Ligera Destilación | {st.session_state.blend_pct_nafta_ligera:.1f} % |
| Reformado Catalítico     | {st.session_state.blend_pct_reformado:.1f} % |
| Alquilato                | {st.session_state.blend_pct_alquilato:.1f} % |
| **RON Final**            | **{ron_inf:.2f}** |
| **Coste Total**          | **{coste_inf:.2f} $/bbl** |
""")
        else:
            st.info("Completa el blending en la pestaña 2 antes de enviar el informe.", icon="ℹ️")

    st.markdown("---")

    # ── Formulario de preguntas ───────────────────────────────────────────
    with st.form("formulario_informe"):
        st.markdown("#### ✍️ Preguntas de Análisis")

        st.markdown("**Pregunta 1 · Operación del FCC**")
        st.markdown(
            "_¿Qué temperatura elegiste en el FCC y por qué? ¿Qué pasaba con la producción de nafta "
            "líquida y el gas seco si subías la temperatura al máximo (550 °C)?_"
        )
        r1 = st.text_area("Respuesta 1", value=st.session_state.respuesta_1,
                          height=130, key="ta_r1",
                          placeholder="Escribe aquí tu análisis (mínimo 3–4 líneas)...")

        st.markdown("---")
        st.markdown("**Pregunta 2 · Receta de Blending**")
        st.markdown(
            "_Anota tu receta final de Blending (% de cada corriente). "
            "¿Por qué no pudiste usar solo Nafta Ligera de Destilación y Nafta FCC "
            "para alcanzar los 95 RON? Justifica con números._"
        )
        r2 = st.text_area("Respuesta 2", value=st.session_state.respuesta_2,
                          height=130, key="ta_r2",
                          placeholder="Escribe aquí tu receta y el razonamiento...")

        st.markdown("---")
        st.markdown("**Pregunta 3 · Optimización Económica**")
        st.markdown(
            "_El Reformado Catalítico es la corriente más cara (115 $/bbl). "
            "¿Qué cambiarías en la operación del FCC para necesitar comprar menos Reformado "
            "y abaratar el coste total de la gasolina?_"
        )
        r3 = st.text_area("Respuesta 3", value=st.session_state.respuesta_3,
                          height=130, key="ta_r3",
                          placeholder="Escribe aquí tu propuesta de optimización...")

        submitted = st.form_submit_button("📤 Enviar Informe", type="primary")

    # ── Procesamiento del formulario ──────────────────────────────────────
    if submitted:
        st.session_state.respuesta_1 = r1
        st.session_state.respuesta_2 = r2
        st.session_state.respuesta_3 = r3

        # Calcular RON y coste para el informe
        if st.session_state.fcc_operacion_fijada and abs(blend_sum - 100) < 0.1:
            f_nfcc_i = st.session_state.blend_pct_nafta_fcc    / 100
            f_nl_i   = st.session_state.blend_pct_nafta_ligera / 100
            f_ref_i  = st.session_state.blend_pct_reformado    / 100
            f_alk_i  = st.session_state.blend_pct_alquilato    / 100
            ron_txt   = f"{f_nfcc_i*st.session_state.fcc_ron_nafta + f_nl_i*70 + f_ref_i*100 + f_alk_i*97:.2f}"
            coste_txt = f"{f_nfcc_i*90 + f_nl_i*70 + f_ref_i*115 + f_alk_i*105:.2f}"
        else:
            ron_txt   = "N/D"
            coste_txt = "N/D"

        # Generar contenido del archivo .txt
        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contenido_txt = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        INFORME DE PRÁCTICA 3 – FCC & BLENDING DE GASOLINA                  ║
║        Tecnología del Petróleo y Petroquímica                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
Fecha y hora de envío: {fecha_hora}

════════════════════════════════════════════════════════════════
 SECCIÓN A – RESULTADOS DEL FCC
════════════════════════════════════════════════════════════════
Temperatura del reactor         : {st.session_state.fcc_temperatura} °C
Relación Catalizador/Carga (C/O): {st.session_state.fcc_co_ratio:.1f}
Rendimiento de Nafta FCC        : {st.session_state.fcc_rendimiento_nafta if st.session_state.fcc_operacion_fijada else "N/D"} %
RON de la Nafta FCC             : {st.session_state.fcc_ron_nafta if st.session_state.fcc_operacion_fijada else "N/D"}

════════════════════════════════════════════════════════════════
 SECCIÓN B – RECETA DE BLENDING
════════════════════════════════════════════════════════════════
Nafta FCC                       : {st.session_state.blend_pct_nafta_fcc:.1f} %  (RON {st.session_state.fcc_ron_nafta if st.session_state.fcc_operacion_fijada else "N/D"} | 90 $/bbl)
Nafta Ligera de Destilación     : {st.session_state.blend_pct_nafta_ligera:.1f} %  (RON 70 | 70 $/bbl)
Reformado Catalítico            : {st.session_state.blend_pct_reformado:.1f} %  (RON 100 | 115 $/bbl)
Alquilato                       : {st.session_state.blend_pct_alquilato:.1f} %  (RON 97 | 105 $/bbl)
────────────────────────────────────────────────────────────────
RON Final de la Gasolina        : {ron_txt}
Coste Total                     : {coste_txt} $/bbl

════════════════════════════════════════════════════════════════
 SECCIÓN C – RESPUESTAS DEL ALUMNO
════════════════════════════════════════════════════════════════

PREGUNTA 1 – Temperatura del FCC y producción de nafta/gas:
────────────────────────────────────────────────────────────────
{r1 if r1.strip() else "[Sin respuesta]"}

PREGUNTA 2 – Receta de Blending y limitaciones del RON:
────────────────────────────────────────────────────────────────
{r2 if r2.strip() else "[Sin respuesta]"}

PREGUNTA 3 – Optimización económica del proceso:
────────────────────────────────────────────────────────────────
{r3 if r3.strip() else "[Sin respuesta]"}

════════════════════════════════════════════════════════════════
 FIN DEL INFORME
════════════════════════════════════════════════════════════════
"""

        st.success("✅ Informe generado correctamente. Descárgalo con el botón siguiente.", icon="✅")
        st.download_button(
            label="⬇️ Descargar Informe (.txt)",
            data=contenido_txt.encode("utf-8"),
            file_name=f"Practica3_Informe_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )

# ─────────────────────────────────────────────────────────────────────────────
# PIE DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="text-align:center; color:#445566; font-size:0.75rem; '
    'font-family:Share Tech Mono,monospace; letter-spacing:1px;">'
    'LABORATORIO VIRTUAL DE REFINO · Práctica 3 · FCC &amp; Blending'
    '</p>',
    unsafe_allow_html=True,
)
