import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

st.title("💎 Valuador Automotriz Pro")
inv = ml.cargar_inventario()

# --- PESTAÑAS SEPARADAS ---
tab1, tab2 = st.tabs(["📊 Calculadora de Valor", "🔍 Análisis de Oferta IA"])

with tab1:
    st.subheader("Paso 1: Calcular Valor Real")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(inv.keys()), key="m1")
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()), key="mo1")
        anio = st.number_input("Año", 1990, 2026, 2015)
    with c2:
        opciones_v = list(inv[marca][modelo]['versiones'].keys())
        version = st.selectbox("Versión", opciones_v)
    
    with st.expander("🛠️ Detalles de Estado Actual"):
        c3, c4 = st.columns(2)
        km = st.number_input("Kilometraje", 0, 1000000, 100000)
        with c3:
            choque = st.checkbox("¿Tuvo choques?")
            mecanica = st.checkbox("Fallas de Motor/Caja")
        with c4:
            pintura = st.checkbox("Detalles de Pintura")
            duenos = st.slider("Dueños", 1, 6, 2)

    if st.button("CALCULAR VALOR"):
        resultado = ml.calcular_valor_final(marca, modelo, version, anio, km, duenos, "Sí" if choque else "No", pintura, mecanica)
        st.session_state['valor_calculado'] = resultado
        st.success(f"### Valor Sugerido: $ {resultado:,.2f} USD")

with tab2:
    st.subheader("Paso 2: ¿Es un buen negocio?")
    st.write("Usa esta herramienta para saber si el precio que te piden es justo.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        v_real = st.number_input("Valor de Mercado ($)", value=st.session_state.get('valor_calculado', 0.0))
    with col_b:
        v_pide = st.number_input("Precio que te piden ($)", value=0.0)

    if st.button("OBTENER VEREDICTO"):
        if v_real > 0 and v_pide > 0:
            diff = ((v_pide - v_real) / v_real) * 100
            if diff < -10:
                st.balloons()
                st.markdown(f"<h2 style='color: #2ecc71;'>💎 OFERTA DIAMANTE</h2>", unsafe_allow_html=True)
                st.write(f"¡Cómpralo! El precio es un {abs(diff):.1f}% más bajo que el mercado.")
            elif diff <= 7:
                st.markdown(f"<h2 style='color: #3498db;'>✅ PRECIO JUSTO</h2>", unsafe_allow_html=True)
            else:
                st.markdown(f"<h2 style='color: #e74c3c;'>🚨 SOBREPRECIO</h2>", unsafe_allow_html=True)
                st.write(f"Cuidado, estás pagando un {diff:.1f}% por encima del valor.")
        else:
            st.warning("Asegúrate de tener ambos precios para analizar.")
