import streamlit as st
import motor_logico as ml
import time

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

st.markdown("""
    <style>
    .reportview-container { background: #0f172a; }
    .metric-box { background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border-top: 4px solid #3498db; }
    .warning-box { background: rgba(231, 76, 60, 0.2); border: 2px solid #e74c3c; padding: 20px; border-radius: 15px; }
    </style>
""", unsafe_allow_html=True)

st.title("💎 Valuador Automotriz Pro")
inv = ml.cargar_inventario()

t1, t2 = st.tabs(["📊 Calculadora", "🔍 Scanner de Negocios"])

with t1:
    st.subheader("Tasación Real de Mercado")
    col1, col2 = st.columns(2)
    with col1:
        m1 = st.selectbox("Marca", sorted(inv.keys()), key="m1")
        mo1 = st.selectbox("Modelo", sorted(inv[m1].keys()), key="mo1")
        a1 = st.number_input("Año", 1990, 2026, 2018, key="a1")
    with col2:
        v1 = st.selectbox("Versión", list(inv[m1][mo1]['versiones'].keys()), key="v1")
        k1 = st.number_input("Kilometraje", 0, 1000000, 80000, key="k1")

    with st.expander("🛠️ Evaluar Desgaste"):
        ch1 = st.checkbox("¿Choques?", key="ch1")
        me1 = st.checkbox("¿Fallas mecánicas?", key="me1")
        pi1 = st.checkbox("¿Pintura?", key="pi1")
        d1 = st.slider("Dueños", 1, 6, 1, key="d1")

    if st.button("CALCULAR PRECIO", use_container_width=True):
        precio = ml.calcular_valor_final(m1, mo1, v1, a1, k1, d1, "Sí" if ch1 else "No", pi1, me1)
        st.markdown(f'<div class="metric-box"><h3>Valor Estimado: ${precio:,.2f} USD</h3></div>', unsafe_allow_html=True)

with t2:
    st.subheader("🕵️ Analizador de Ofertas IA")
    st.write("¿La oferta que recibiste es real o un riesgo?")
    
    ca, cb = st.columns(2)
    with ca:
        m2 = st.selectbox("Marca", sorted(inv.keys()), key="m2")
        mo2 = st.selectbox("Modelo", sorted(inv[m2].keys()), key="mo2")
        a2 = st.number_input("Año", 1990, 2026, 2018, key="a2")
    with cb:
        v2 = st.selectbox("Versión", list(inv[m2][mo2]['versiones'].keys()), key="v2")
        p_oferta = st.number_input("Precio que te piden ($)", 0.0, key="p_ia")

    if st.button("ESCANEAR OFERTA", use_container_width=True):
        with st.status("Verificando coherencia de precios...") as s:
            time.sleep(1)
            # Valor real base para comparar
            v_ref = ml.calcular_valor_final(m2, mo2, v2, a2, 80000, 2, "No", False, False)
            diff = ((p_oferta - v_ref) / v_ref) * 100
            s.update(label="Análisis finalizado", state="complete")

        st.divider()
        
        if p_oferta == 0:
            st.warning("Ingresa un precio válido.")
        elif diff < -35:
            st.markdown(f"""<div class="warning-box">
                <h2 style="color: #e74c3c; margin:0;">⚠️ ALERTA: SOSPECHOSAMENTE BARATO</h2>
                <p>El precio es un {abs(diff):.1f}% menor al mercado. <b>¡Cuidado!</b> Podría ser una estafa, un problema legal o un daño oculto grave. No entregues dinero sin ver el carro.</p>
                </div>""", unsafe_allow_html=True)
        elif diff < -8:
            st.balloons()
            st.success(f"### 💎 ¡GANGA DETECTADA!")
            st.write(f"Excelente oportunidad. Ahorras un {abs(diff):.1f}% respecto al mercado (${v_ref:,.0f}).")
        elif diff <= 8:
            st.info("### ✅ PRECIO JUSTO")
            st.write(f"El precio de ${p_oferta:,.0f} es coherente con el mercado actual.")
        else:
            st.error(f"### 🚨 SOBREPRECIO")
            st.write(f"Estás pagando un {diff:.1f}% de más. El valor real ronda los ${v_ref:,.0f}.")

st.sidebar.caption("Lord Flores - Puerto Cabello Edition")
