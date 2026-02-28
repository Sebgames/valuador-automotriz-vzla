import streamlit as st
import motor_logico as ml
import time

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

# Estilo visual premium
st.markdown("""
    <style>
    .main { background-color: #0f172a; }
    .stMetric { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; }
    .stAlert { border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("💎 Valuador Automotriz Pro")
st.caption("Especialista en Mercado Venezolano")

# Cargamos el inventario una sola vez
inv = ml.cargar_inventario()

t1, t2 = st.tabs(["📊 Calculadora", "🔍 Scanner de Negocios"])

with t1:
    st.subheader("Tasación de Mercado")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(inv.keys()), key="m1")
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()), key="mo1")
        anio = st.number_input("Año", 1990, 2026, 2015, key="a1")
    with c2:
        version = st.selectbox("Versión", list(inv[marca][modelo]['versiones'].keys()), key="v1")
        km = st.number_input("Kilometraje", 0, 1000000, 80000, key="k1")

    with st.expander("🛠️ Estado Físico"):
        ch1 = st.checkbox("¿Choques?", key="ch1")
        me1 = st.checkbox("¿Fallas mecánicas?", key="me1")
        pi1 = st.checkbox("¿Detalles Pintura?", key="pi1")
        d1 = st.slider("Dueños", 1, 6, 1, key="d1")

    if st.button("CALCULAR VALOR", use_container_width=True):
        precio = ml.calcular_valor_final(marca, modelo, version, anio, km, d1, "Sí" if ch1 else "No", pi1, me1)
        st.metric("Precio Sugerido", f"${precio:,.2f} USD")

with t2:
    st.subheader("🕵️ Analizador de Ofertas IA")
    col_a, col_b = st.columns(2)
    with col_a:
        m2 = st.selectbox("Marca", sorted(inv.keys()), key="m2")
        mo2 = st.selectbox("Modelo", sorted(inv[m_ia := m2].keys()), key="mo2")
        a2 = st.number_input("Año", 1990, 2026, 2015, key="a2")
    with col_b:
        v2 = st.selectbox("Versión", list(inv[m2][mo2]['versiones'].keys()), key="v2")
        p_pide = st.number_input("Precio que te piden ($)", 0.0, key="p_ia")

    if st.button("ESCANEAR NEGOCIO", use_container_width=True):
        with st.status("Verificando precios de mercado...") as s:
            time.sleep(1)
            # Valor real de referencia
            v_ref = ml.calcular_valor_final(m2, mo2, v2, a2, 80000, 2, "No", False, False)
            diff = ((p_pide - v_ref) / v_ref) * 100
            s.update(label="Análisis Completo", state="complete")

        st.divider()
        
        # EL VEREDICTO DINÁMICO
        if p_pide == 0:
            st.warning("Por favor, ingresa el precio de la oferta.")
        elif diff < -35:
            st.error("### ⚠️ ALERTA: DEMASIADO BUENO PARA SER VERDAD")
            st.write(f"El precio está un {abs(diff):.1f}% por debajo del mercado. **Riesgo de estafa o problemas legales.**")
        elif diff < -8:
            st.balloons()
            st.success("### 💎 ¡GANGA DETECTADA!")
            st.write(f"Ahorras unos ${v_ref - p_pide:,.0f}. ¡Es un excelente negocio!")
        elif diff <= 8:
            st.info("### ✅ PRECIO JUSTO")
            st.write("El precio es coherente con el valor actual en calle.")
        else:
            st.error("### 🚨 SOBREPRECIO")
            st.write(f"El vendedor pide ${p_pide - v_ref:,.0f} de más. Intenta negociar.")

st.sidebar.markdown(f"**Usuario:** Usuario")
