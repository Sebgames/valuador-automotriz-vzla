import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

st.title("💎 Valuador Automotriz Pro")
inv = ml.cargar_inventario()

# LAS DOS FUNCIONES CLAVE
tab1, tab2 = st.tabs(["📊 Calculadora de Valor", "💰 ¿Es Buen Negocio?"])

with tab1:
    st.subheader("Estimar Precio de Mercado")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(inv.keys()), key="m1")
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()), key="mo1")
        anio = st.number_input("Año", 1990, 2026, 2015, key="a1")
    with c2:
        opciones_v = list(inv[marca][modelo]['versiones'].keys())
        version = st.selectbox("Versión", opciones_v, key="v1")
        km = st.number_input("Kilometraje", 0, 1000000, 100000, key="k1")

    with st.expander("🛠️ Detalles del Vehículo"):
        c3, c4 = st.columns(2)
        with c3:
            choque = st.checkbox("¿Tuvo Choques?", key="ch1")
            mecanica = st.checkbox("¿Fallas Mecánicas?", key="me1")
        with c4:
            pintura = st.checkbox("¿Detalles Pintura?", key="pi1")
            duenos = st.slider("Dueños", 1, 6, 2, key="d1")

    if st.button("CALCULAR VALOR", key="btn_calc"):
        res = ml.calcular_valor_final(marca, modelo, version, anio, km, duenos, "Sí" if choque else "No", pintura, mecanica)
        st.success(f"## Valor Estimado: $ {res:,.2f} USD")

with tab2:
    st.subheader("Veredicto de la IA")
    st.write("Escribe el precio que te piden y evaluaremos si vale la pena.")
    
    col1, col2 = st.columns(2)
    with col1:
        m_ia = st.selectbox("Marca", sorted(inv.keys()), key="m2")
        mo_ia = st.selectbox("Modelo", sorted(inv[m_ia].keys()), key="mo2")
        a_ia = st.number_input("Año", 1990, 2026, 2015, key="a2")
    with col2:
        v_ia = st.selectbox("Versión", list(inv[m_ia][mo_ia]['versiones'].keys()), key="v2")
        precio_oferta = st.number_input("Precio que te piden ($)", 0.0, key="p_ia")

    if st.button("¿VALE LA PENA?", key="btn_ia"):
        # Calculamos valor real con condiciones estándar para comparar
        v_real = ml.calcular_valor_final(m_ia, mo_ia, v_ia, a_ia, 100000, 2, "No", False, False)
        diff = ((precio_oferta - v_real) / v_real) * 100
        
        if diff < -7:
            st.balloons()
            st.success(f"### 💎 ¡ES UNA GANGA!")
            st.write(f"El valor de mercado es de aprox. ${v_real:,.0f}. Te ahorras un {abs(diff):.1f}%.")
        elif diff <= 7:
            st.info(f"### ✅ PRECIO JUSTO")
            st.write("El precio está acorde a la realidad actual.")
        else:
            st.error(f"### 🚨 NO VALE LA PENA")
            st.write(f"Está sobrevalorado. El valor real debería ser cerca de ${v_real:,.0f}.")

st.sidebar.write("👑 **Lord Flores Edition**")
