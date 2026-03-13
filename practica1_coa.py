"""
=============================================================================
PRÁCTICA 1 - LABORATORIO VIRTUAL: CARACTERIZACIÓN DE CRUDOS (Crude Oil Assay)
Asignatura: Tecnologías del Petróleo
=============================================================================
Autor: José Joaquín González Cortés
Descripción: Aplicación interactiva que simula un ensayo de caracterización
             de crudo desconocido, guiando al alumno paso a paso.
=============================================================================
Ejecución: streamlit run practica1_coa.py
=============================================================================
"""

import streamlit as st
import random
import math
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Práctica 1 – Caracterización de Crudos",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONALIZADO – Estética industrial/refinería
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Barlow:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

/* Fondo principal oscuro tipo sala de control */
.stApp {
    background-color: #0d1117;
    color: #c9d1d9;
}

/* Cabecera principal */
.main-header {
    background: linear-gradient(135deg, #1a2332 0%, #0d1117 50%, #1a1a2e 100%);
    border: 1px solid #f0a500;
    border-left: 6px solid #f0a500;
    padding: 24px 32px;
    border-radius: 8px;
    margin-bottom: 28px;
    box-shadow: 0 4px 24px rgba(240,165,0,0.15);
}

.main-header h1 {
    font-family: 'Share Tech Mono', monospace;
    color: #f0a500;
    font-size: 1.8rem;
    margin: 0;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.main-header p {
    color: #8b949e;
    font-size: 0.9rem;
    margin-top: 8px;
    letter-spacing: 1px;
}

/* Tarjetas de fase */
.phase-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 20px 24px;
    margin-bottom: 16px;
    border-top: 3px solid #f0a500;
}

.phase-card.locked {
    border-top-color: #484f58;
    opacity: 0.5;
}

.phase-card.completed {
    border-top-color: #3fb950;
    background: #0d1f16;
}

.phase-title {
    font-family: 'Share Tech Mono', monospace;
    color: #f0a500;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.phase-title.locked {
    color: #484f58;
}

.phase-title.completed {
    color: #3fb950;
}

/* Badge de estado */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 1px;
    font-family: 'Share Tech Mono', monospace;
}
.badge-active  { background: #1f3a5f; color: #58a6ff; border: 1px solid #1f6feb; }
.badge-locked  { background: #21262d; color: #484f58; border: 1px solid #30363d; }
.badge-done    { background: #0d2818; color: #3fb950; border: 1px solid #238636; }

/* Datos de laboratorio */
.lab-data-box {
    background: #0d1117;
    border: 1px solid #f0a500;
    border-radius: 6px;
    padding: 16px 20px;
    font-family: 'Share Tech Mono', monospace;
    color: #f0a500;
    font-size: 0.95rem;
    line-height: 2;
}

/* Fórmula */
.formula-box {
    background: #1a1f2e;
    border-left: 4px solid #58a6ff;
    padding: 12px 16px;
    border-radius: 4px;
    font-family: 'Share Tech Mono', monospace;
    color: #79c0ff;
    font-size: 0.9rem;
    margin: 10px 0;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #161b22 !important;
    border-right: 1px solid #30363d;
}

section[data-testid="stSidebar"] .stMarkdown {
    color: #8b949e;
}

/* Botones */
.stButton > button {
    background: linear-gradient(90deg, #f0a500, #d4870a);
    color: #0d1117;
    font-family: 'Barlow', sans-serif;
    font-weight: 700;
    letter-spacing: 1px;
    border: none;
    border-radius: 6px;
    padding: 10px 24px;
    transition: all 0.2s;
    text-transform: uppercase;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #ffc340, #f0a500);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(240,165,0,0.4);
}

/* Inputs */
.stNumberInput input, .stTextArea textarea {
    background-color: #0d1117 !important;
    color: #c9d1d9 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
}

/* Métricas */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
}

/* Divider */
hr { border-color: #21262d; }

/* Texto de progreso */
.progress-label {
    font-family: 'Share Tech Mono', monospace;
    color: #8b949e;
    font-size: 0.8rem;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# INICIALIZACIÓN DE SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────

def inicializar_crudo():
    """
    Genera los datos aleatorios del crudo desconocido y los guarda en
    st.session_state. Solo se ejecuta UNA VEZ por sesión.
    """
    if "crudo_generado" not in st.session_state:

        # --- Datos de laboratorio ---
        densidad_lab = round(random.uniform(0.800, 0.980), 4)
        temp_lab     = round(random.uniform(20.0, 35.0), 1)

        # --- Datos de destilación ASTM D86 coherentes ---
        t10 = round(random.uniform(90.0, 130.0), 1)
        t50 = round(random.uniform(250.0, 290.0), 1)
        t90 = round(random.uniform(450.0, 520.0), 1)

        # --- Contenido de azufre ---
        pct_azufre = round(random.uniform(0.1, 2.5), 2)

        # --- Cálculos de referencia (la "solución correcta") ---
        sg_156  = round(densidad_lab + 0.0007 * (temp_lab - 15.6), 4)
        api_ref = round(141.5 / sg_156 - 131.5, 2)

        # TMP en Kelvin: media ponderada pesos 1:2:1 para T10, T50, T90
        tmp_c   = (t10 + 2 * t50 + t90) / 4.0
        tmp_k   = round(tmp_c + 273.15, 2)
        kuop    = round((1.8 * tmp_k) ** (1 / 3) / sg_156, 3)

        st.session_state.update({
            "crudo_generado": True,
            # Datos brutos
            "densidad_lab": densidad_lab,
            "temp_lab": temp_lab,
            "t10": t10, "t50": t50, "t90": t90,
            "pct_azufre": pct_azufre,
            # Soluciones correctas
            "sg_156_ref": sg_156,
            "api_ref": api_ref,
            "tmp_k_ref": tmp_k,
            "kuop_ref": kuop,
            # Variables validadas (se rellenan al superar cada fase)
            "sg_156_alumno": None,
            "api_alumno": None,
            "kuop_alumno": None,
            # Fases desbloqueadas
            "fase1_ok": False,
            "fase2_ok": False,
            "fase3_ok": False,
            "informe_enviado": False,
            "informe_txt": "",
        })


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR – Instrucciones y progreso
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar():
    with st.sidebar:
        st.markdown("## 🛢️ Laboratorio Virtual")
        st.markdown("**Asignatura:** Tecnología de Petróleo y Petroquímica. Grado en Ingeniería en Tecnologías Industriales")
        st.markdown("**Práctica 1** – Crude Oil Assay")
        st.markdown("**Autor:** José Joaquín González Cortés")
        st.divider()

        st.markdown("### 📋 Instrucciones")
        st.markdown("""
1. Se te proporciona un crudo **desconocido** con datos de laboratorio.
2. Debes completar **4 Fases** en orden.
3. Cada fase se desbloquea al validar el cálculo anterior.
4. Utiliza las **fórmulas indicadas** y respeta el número de decimales.
5. Al finalizar, genera y descarga tu **Informe COA**.
        """)
        st.divider()

        # Barra de progreso
        fases_ok = sum([
            st.session_state.get("fase1_ok", False),
            st.session_state.get("fase2_ok", False),
            st.session_state.get("fase3_ok", False),
            st.session_state.get("informe_enviado", False),
        ])
        st.markdown(f"### 🎯 Progreso: {fases_ok}/4 fases")
        st.progress(fases_ok / 4)

        emojis = ["🔓" if st.session_state.get(f"fase{i}_ok") else "🔒" for i in range(1, 4)]
        inf_emoji = "🔓" if st.session_state.get("informe_enviado") else "🔒"
        st.markdown(f"""
- {emojis[0]} Fase 1: Corrección de Densidad
- {emojis[1]} Fase 2: Grados API
- {emojis[2]} Fase 3: Factor K_UOP
- {inf_emoji} Fase 4: Informe Final
        """)

        st.divider()
        st.markdown("### ⚙️ Tolerancia de error")
        st.markdown("±0.05 en valores calculados.")
        st.markdown("±2 K en temperaturas.")

        st.divider()
        if st.button("🔄 Nueva Muestra de Crudo", use_container_width=True):
            # Borra el estado para generar un nuevo crudo
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# CABECERA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def render_header():
    st.markdown("""
    <div class="main-header">
        <h1>🛢️ Práctica 1 — Crude Oil Assay</h1>
        <p>LABORATORIO VIRTUAL · CARACTERIZACIÓN DE CRUDO DESCONOCIDO · TECNOLOGÍA DEL PETRÓLEO Y PETROQUÍMICA</p>
        <p>Autor: José Joaquín González Cortés</p>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# FASE 1 – Corrección de Densidad
# ─────────────────────────────────────────────────────────────────────────────

def render_fase1():
    ss = st.session_state
    completada = ss["fase1_ok"]

    badge_html = '<span class="badge badge-done">✓ COMPLETADA</span>' if completada \
        else '<span class="badge badge-active">▶ ACTIVA</span>'

    st.markdown(f"""
    <div class="phase-card {'completed' if completada else ''}">
        <div class="phase-title {'completed' if completada else ''}">
            FASE 1 — Corrección de Densidad &nbsp; {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📐 Fase 1: Corrección de Densidad a 15.6 °C", expanded=not completada):

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔬 Datos de Laboratorio")
            st.markdown(f"""
            <div class="lab-data-box">
            📏 Densidad medida: <b>{ss['densidad_lab']:.4f} g/ml</b><br>
            🌡️ Temperatura de medición: <b>{ss['temp_lab']:.1f} °C</b>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 📖 Fórmula de Corrección")
            st.markdown("""
            <div class="formula-box">
            SG<sub>15.6</sub> = ρ_T + 0.0007 × (T – 15.6)<br><br>
            Donde:<br>
            &nbsp;ρ_T = densidad medida (g/ml)<br>
            &nbsp;T   = temperatura de medición (°C)<br>
            &nbsp;15.6°C ≡ 60°F (referencia estándar)
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### ✏️ Tu Cálculo")

        sg_input = st.number_input(
            "Introduce SG₁₅.₆ (4 decimales):",
            min_value=0.7000, max_value=1.1000,
            value=0.8500, step=0.0001, format="%.4f",
            key="input_sg"
        )

        if not completada:
            if st.button("✅ Validar Fase 1", key="btn_fase1"):
                tolerancia = 0.05
                if abs(sg_input - ss["sg_156_ref"]) <= tolerancia:
                    ss["fase1_ok"] = True
                    ss["sg_156_alumno"] = sg_input
                    st.success(f"✅ ¡Correcto! SG₁₅.₆ = {sg_input:.4f}  →  Fase 2 desbloqueada.")
                    st.rerun()
                else:
                    diferencia = abs(sg_input - ss["sg_156_ref"])
                    st.error(f"❌ Resultado incorrecto. Tu error es {diferencia:.4f}. Revisa la fórmula y los datos.")
        else:
            st.metric("SG₁₅.₆ validada", f"{ss['sg_156_alumno']:.4f}")
            st.success("✅ Fase 1 completada.")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 2 – Grados API
# ─────────────────────────────────────────────────────────────────────────────

def render_fase2():
    ss = st.session_state
    desbloqueada = ss["fase1_ok"]
    completada   = ss["fase2_ok"]

    if not desbloqueada:
        st.markdown("""
        <div class="phase-card locked">
            <div class="phase-title locked">
                FASE 2 — Grados API &nbsp;
                <span class="badge badge-locked">🔒 BLOQUEADA</span>
            </div>
            <p style="color:#484f58; font-size:0.85rem;">Completa la Fase 1 para desbloquear.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    badge_html = '<span class="badge badge-done">✓ COMPLETADA</span>' if completada \
        else '<span class="badge badge-active">▶ ACTIVA</span>'

    st.markdown(f"""
    <div class="phase-card {'completed' if completada else ''}">
        <div class="phase-title {'completed' if completada else ''}">
            FASE 2 — Grados API &nbsp; {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("⚗️ Fase 2: Cálculo de Grados API", expanded=not completada):

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📊 Dato disponible")
            st.metric("SG₁₅.₆ validada", f"{ss['sg_156_alumno']:.4f}")

        with col2:
            st.markdown("#### 📖 Fórmula API")
            st.markdown("""
            <div class="formula-box">
            °API = (141.5 / SG<sub>15.6</sub>) – 131.5<br><br>
            Clasificación orientativa:<br>
            &nbsp;°API &gt; 31.1  → Crudo Ligero<br>
            &nbsp;°API 22.3–31.1 → Crudo Medio<br>
            &nbsp;°API &lt; 22.3  → Crudo Pesado
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### ✏️ Tu Cálculo")

        api_input = st.number_input(
            "Introduce °API (2 decimales):",
            min_value=0.00, max_value=100.00,
            value=30.00, step=0.01, format="%.2f",
            key="input_api"
        )

        if not completada:
            if st.button("✅ Validar Fase 2", key="btn_fase2"):
                if abs(api_input - ss["api_ref"]) <= 0.05:
                    ss["fase2_ok"] = True
                    ss["api_alumno"] = api_input

                    # Clasificación
                    if api_input > 31.1:
                        clase = "🟡 Crudo Ligero"
                    elif api_input >= 22.3:
                        clase = "🟠 Crudo Medio"
                    else:
                        clase = "🔴 Crudo Pesado"

                    st.success(f"✅ ¡Correcto! °API = {api_input:.2f} → {clase}")
                    st.info("🔓 Datos de destilación ASTM D86 revelados. Continúa con la Fase 3.")
                    st.rerun()
                else:
                    st.error(f"❌ Resultado incorrecto. Recuerda usar el SG₁₅.₆ que calculaste.")
        else:
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("°API validado", f"{ss['api_alumno']:.2f}")
            with col_b:
                if ss["api_alumno"] > 31.1:
                    st.metric("Clasificación", "Crudo Ligero 🟡")
                elif ss["api_alumno"] >= 22.3:
                    st.metric("Clasificación", "Crudo Medio 🟠")
                else:
                    st.metric("Clasificación", "Crudo Pesado 🔴")
            st.success("✅ Fase 2 completada.")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 3 – Factor K_UOP
# ─────────────────────────────────────────────────────────────────────────────

def render_fase3():
    ss = st.session_state
    desbloqueada = ss["fase2_ok"]
    completada   = ss["fase3_ok"]

    if not desbloqueada:
        st.markdown("""
        <div class="phase-card locked">
            <div class="phase-title locked">
                FASE 3 — Factor K_UOP (Naturaleza Química) &nbsp;
                <span class="badge badge-locked">🔒 BLOQUEADA</span>
            </div>
            <p style="color:#484f58; font-size:0.85rem;">Completa la Fase 2 para revelar los datos de destilación.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    badge_html = '<span class="badge badge-done">✓ COMPLETADA</span>' if completada \
        else '<span class="badge badge-active">▶ ACTIVA</span>'

    st.markdown(f"""
    <div class="phase-card {'completed' if completada else ''}">
        <div class="phase-title {'completed' if completada else ''}">
            FASE 3 — Factor K_UOP (Naturaleza Química) &nbsp; {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("🧪 Fase 3: Factor de Caracterización K_UOP", expanded=not completada):

        st.markdown("#### 🔬 Datos de Destilación ASTM D86 — Revelados")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("T₁₀ (10% recuperado)", f"{ss['t10']:.1f} °C")
        with col2:
            st.metric("T₅₀ (50% recuperado)", f"{ss['t50']:.1f} °C")
        with col3:
            st.metric("T₉₀ (90% recuperado)", f"{ss['t90']:.1f} °C")

        st.markdown("---")
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            st.markdown("#### 📖 Paso 1: Temperatura Media Ponderada")
            st.markdown("""
            <div class="formula-box">
            TMP (°C) = (T₁₀ + 2·T₅₀ + T₉₀) / 4<br><br>
            TMP (K) = TMP (°C) + 273.15
            </div>
            """, unsafe_allow_html=True)
        with col_f2:
            st.markdown("#### 📖 Paso 2: Factor K_UOP")
            st.markdown("""
            <div class="formula-box">
            K_UOP = (1.8 · TMP_K)^(1/3) / SG<sub>15.6</sub><br><br>
            Interpretación:<br>
            &nbsp;K > 12.1 → Parafínico<br>
            &nbsp;K 11.5–12.1 → Mixto<br>
            &nbsp;K 11.0–11.5 → Nafténico/Asfáltico<br>
            &nbsp;K < 11.0 → Aromático
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### ✏️ Tu Cálculo")

        tmp_input  = st.number_input(
            "TMP en Kelvin (2 decimales):",
            min_value=200.00, max_value=900.00,
            value=550.00, step=0.01, format="%.2f",
            key="input_tmp"
        )
        kuop_input = st.number_input(
            "Factor K_UOP (3 decimales):",
            min_value=8.000, max_value=15.000,
            value=11.500, step=0.001, format="%.3f",
            key="input_kuop"
        )

        if not completada:
            if st.button("✅ Validar Fase 3", key="btn_fase3"):
                tol_tmp  = 2.0   # ±2 K
                tol_kuop = 0.05  # ±0.05

                tmp_ok  = abs(tmp_input  - ss["tmp_k_ref"]) <= tol_tmp
                kuop_ok = abs(kuop_input - ss["kuop_ref"])  <= tol_kuop

                if tmp_ok and kuop_ok:
                    ss["fase3_ok"]   = True
                    ss["kuop_alumno"] = kuop_input
                    st.success(f"✅ ¡Correcto! TMP = {tmp_input:.2f} K  |  K_UOP = {kuop_input:.3f}")
                    st.info(f"🔓 Contenido de azufre revelado: **{ss['pct_azufre']:.2f}%**. Continúa con el Informe Final.")
                    st.rerun()
                else:
                    msgs = []
                    if not tmp_ok:
                        msgs.append(f"TMP: tu error = {abs(tmp_input - ss['tmp_k_ref']):.2f} K (tol. ±2 K)")
                    if not kuop_ok:
                        msgs.append(f"K_UOP: tu error = {abs(kuop_input - ss['kuop_ref']):.3f} (tol. ±0.05)")
                    st.error("❌ " + " | ".join(msgs))
        else:
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("TMP (K) validada", f"{ss['tmp_k_ref']:.2f} K")
            with col_b:
                st.metric("K_UOP validado", f"{ss['kuop_alumno']:.3f}")
            with col_c:
                k = ss["kuop_alumno"]
                if   k > 12.1:             base = "Parafínico 🟢"
                elif k >= 11.5:            base = "Mixto 🟡"
                elif k >= 11.0:            base = "Nafténico 🟠"
                else:                      base = "Aromático 🔴"
                st.metric("Base del crudo", base)

            st.markdown(f"""
            <div class="lab-data-box" style="margin-top:12px;">
            🧫 Contenido de Azufre revelado: <b>{ss['pct_azufre']:.2f}%</b>
            {'&nbsp; → Crudo <b>AGRIO</b> (≥ 0.5%)' if ss['pct_azufre'] >= 0.5 else '&nbsp; → Crudo <b>DULCE</b> (< 0.5%)'}
            </div>
            """, unsafe_allow_html=True)
            st.success("✅ Fase 3 completada.")


# ─────────────────────────────────────────────────────────────────────────────
# FASE 4 – Informe Final
# ─────────────────────────────────────────────────────────────────────────────

def render_fase4():
    ss = st.session_state
    desbloqueada = ss["fase3_ok"]

    if not desbloqueada:
        st.markdown("""
        <div class="phase-card locked">
            <div class="phase-title locked">
                FASE 4 — Informe Final (COA) &nbsp;
                <span class="badge badge-locked">🔒 BLOQUEADA</span>
            </div>
            <p style="color:#484f58; font-size:0.85rem;">Completa la Fase 3 para redactar el informe.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    badge_html = '<span class="badge badge-done">✓ ENVIADO</span>' if ss["informe_enviado"] \
        else '<span class="badge badge-active">▶ ACTIVA</span>'

    st.markdown(f"""
    <div class="phase-card {'completed' if ss['informe_enviado'] else ''}">
        <div class="phase-title {'completed' if ss['informe_enviado'] else ''}">
            FASE 4 — Informe Final COA &nbsp; {badge_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📄 Fase 4: Redacta tu Informe de Caracterización", expanded=True):

        # Resumen de resultados obtenidos
        st.markdown("#### 📊 Resumen de Resultados Obtenidos")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("SG₁₅.₆",         f"{ss['sg_156_alumno']:.4f}")
        c2.metric("°API",            f"{ss['api_alumno']:.2f}")
        c3.metric("K_UOP",           f"{ss['kuop_alumno']:.3f}")
        c4.metric("% Azufre",        f"{ss['pct_azufre']:.2f}%")

        st.markdown("---")
        st.markdown("#### ✍️ Responde las siguientes preguntas de análisis:")

        with st.form("formulario_informe"):

            st.markdown("**1. Clasificación por contenido de azufre**")
            st.caption(f"Azufre revelado: {ss['pct_azufre']:.2f}%. Clasifica el crudo (Dulce < 0.5% / Agrio ≥ 0.5%) y comenta su impacto en el coste de refino.")
            resp1 = st.text_area(
                "Respuesta 1:", height=100, key="r1",
                placeholder="Ej: Con un contenido de azufre de X%, este crudo se clasifica como... El impacto en el coste de refino es..."
            )

            st.markdown("**2. Base química del crudo (K_UOP)**")
            st.caption(f"K_UOP calculado: {ss['kuop_alumno']:.3f}. Indica la base química (Parafínica, Mixta, Nafténica/Asfáltica, Aromática) y qué implica.")
            resp2 = st.text_area(
                "Respuesta 2:", height=100, key="r2",
                placeholder="Ej: Con K_UOP = X, la base de este crudo es... porque..."
            )

            st.markdown("**3. Rendimientos esperados en destilación atmosférica**")
            st.caption("Según la base del crudo, ¿esperas mayor rendimiento de naftas/lubricantes o de asfaltos/fuel-oil?")
            resp3 = st.text_area(
                "Respuesta 3:", height=100, key="r3",
                placeholder="Ej: Dado que la base es..., cabe esperar que en la destilación atmosférica predominen..."
            )

            st.markdown("**4. Conclusión y recomendación de compra**")
            st.caption("Integra todos los parámetros obtenidos, concluye si recomiendas este crudo para una refinería estándar y busca su crudo de referencia.")
            resp4 = st.text_area(
                "Respuesta 4:", height=120, key="r4",
                placeholder="Ej: En conjunto, este crudo presenta... Por tanto, mi recomendación es..."
            )

            submitted = st.form_submit_button("📤 Enviar Informe y Generar Descarga")

            if submitted:
                # Validación básica: todas las respuestas deben tener contenido
                if not all([resp1.strip(), resp2.strip(), resp3.strip(), resp4.strip()]):
                    st.warning("⚠️ Por favor, completa TODAS las preguntas antes de enviar.")
                else:
                    ss["informe_enviado"] = True

                    # ─────────────────────────────────────────────────────────
                    # Compilación del informe en texto plano
                    # ─────────────────────────────────────────────────────────
                    k = ss["kuop_alumno"]
                    if   k > 12.1:  base_str = "Parafínica (K > 12.1)"
                    elif k >= 11.5: base_str = "Mixta (11.5 ≤ K ≤ 12.1)"
                    elif k >= 11.0: base_str = "Nafténica/Asfáltica (11.0 ≤ K < 11.5)"
                    else:           base_str = "Aromática (K < 11.0)"

                    api_v = ss["api_alumno"]
                    if   api_v > 31.1:  api_str = "Ligero (°API > 31.1)"
                    elif api_v >= 22.3: api_str = "Medio (22.3 ≤ °API ≤ 31.1)"
                    else:               api_str = "Pesado (°API < 22.3)"

                    azufre_str = "Agrio (% S ≥ 0.5)" if ss["pct_azufre"] >= 0.5 else "Dulce (% S < 0.5)"
                    fecha      = datetime.now().strftime("%d/%m/%Y %H:%M")

                    informe = f"""
╔══════════════════════════════════════════════════════════════════╗
║         INFORME DE CARACTERIZACIÓN DE CRUDO (COA)               ║
║         Práctica 1 – Tecnologías del Petróleo                    ║
╚══════════════════════════════════════════════════════════════════╝

Fecha de generación: {fecha}
Autor:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECCIÓN 1 — DATOS BRUTOS DE LABORATORIO (Muestra Asignada)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Densidad medida en laboratorio : {ss['densidad_lab']:.4f} g/ml
  Temperatura de medición        : {ss['temp_lab']:.1f} °C
  T10 (ASTM D86)                 : {ss['t10']:.1f} °C
  T50 (ASTM D86)                 : {ss['t50']:.1f} °C
  T90 (ASTM D86)                 : {ss['t90']:.1f} °C
  Contenido de Azufre            : {ss['pct_azufre']:.2f} %

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECCIÓN 2 — CÁLCULOS VALIDADOS POR EL ALUMNO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Fase 1 – Gravedad Específica a 15.6°C : SG₁₅.₆ = {ss['sg_156_alumno']:.4f}
  Fase 2 – Grados API                   : °API   = {ss['api_alumno']:.2f}
  Fase 3 – TMP en Kelvin                : TMP_K  = {ss['tmp_k_ref']:.2f} K
  Fase 3 – Factor de Caracterización    : K_UOP  = {ss['kuop_alumno']:.3f}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECCIÓN 3 — CLASIFICACIÓN DEL CRUDO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Densidad API         : {api_str}
  Contenido de Azufre  : {azufre_str}
  Base Química (K_UOP) : {base_str}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SECCIÓN 4 — ANÁLISIS Y CONCLUSIONES DEL ALUMNO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[Pregunta 1 – Clasificación por azufre e impacto en coste de refino]
{resp1.strip()}

[Pregunta 2 – Base química del crudo según K_UOP]
{resp2.strip()}

[Pregunta 3 – Rendimientos esperados en destilación atmosférica]
{resp3.strip()}

[Pregunta 4 – Conclusión y recomendación de compra]
{resp4.strip()}

══════════════════════════════════════════════════════════════════
FIN DEL INFORME
══════════════════════════════════════════════════════════════════
"""
                    ss["informe_txt"] = informe
                    st.success("✅ Informe generado correctamente. ¡Descárgalo a continuación!")
                    st.rerun()

        # Botón de descarga (visible tras enviar)
        if ss["informe_enviado"] and ss["informe_txt"]:
            st.markdown("---")
            st.markdown("#### 💾 Descarga tu Informe")
            st.download_button(
                label="⬇️  Descargar Informe_COA_Alumno.txt",
                data=ss["informe_txt"].encode("utf-8"),
                file_name="Informe_COA_Alumno.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.balloons()


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIÓN PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def main():
    # 1. Inicializar datos del crudo (solo la primera vez)
    inicializar_crudo()

    # 2. Renderizar sidebar
    render_sidebar()

    # 3. Cabecera
    render_header()

    # 4. Información de bienvenida (solo si no ha empezado)
    if not st.session_state.get("fase1_ok"):
        st.info(
            "👋 **Bienvenido al laboratorio virtual.** "
            "Se te ha asignado una muestra de crudo desconocido. "
            "Completa las 4 fases siguiendo las instrucciones del sidebar. "
            "Cada fase se desbloquea al validar los cálculos de la anterior."
        )

    # 5. Renderizar las 4 fases
    render_fase1()
    st.markdown("<br>", unsafe_allow_html=True)
    render_fase2()
    st.markdown("<br>", unsafe_allow_html=True)
    render_fase3()
    st.markdown("<br>", unsafe_allow_html=True)
    render_fase4()

    # 6. Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#484f58; font-size:0.78rem; "
        "font-family:Share Tech Mono,monospace;'>"
        "LABORATORIO VIRTUAL · TECNOLOGÍAS DEL PETRÓLEO · "
        "Crude Oil Assay Simulator v1.0"
        "</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
