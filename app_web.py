import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Automotriz", layout="centered")

st.title("💎 Valuador Lord Flores")
inv = ml.cargar_inventario()

tab1, tab2 = st.tabs(["📊 Calculadora", "💰 ¿Vale la pena comprarlo?"])

with tab1:
    st.subheader("Estimación de Precio Real")
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(inv.keys()), key="m1")
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()), key="mo1")
        anio = st.number_input("Año", 1990, 2026, 2015, key="a1")
    with c2:
        opciones_v = list(inv[marca][modelo]['versiones'].keys())
        version = st.selectbox("Versión", opciones_v, key="v1")
        km = st.number_input("Kilometraje", 0, 1000000, 100000, key="k1")

    with st.expander("🛠️ Detalles Técnicos"):
        c3, c4 = st.columns(2)
        with c3:
            choque = st.checkbox("¿Reporta Choque?")
            mecanica = st.checkbox("¿Falla Mecánica?")
        with c4:
            pintura = st.checkbox("¿Detalles Pintura?")
            duenos = st.slider("Dueños", 1, 6, 2)

    if st.button("CALCULAR"):
        res = ml.calcular_valor_final(marca, modelo, version, anio, km, duenos, "Sí" if choque else "No", pintura, mecanica)
        st.success(f"## Valor en Calle: $ {res:,.2f} USD")

with tab2:
    st.subheader("Veredicto de Compra")
    st.write("Dinos qué te ofrecen y te diremos si es un buen negocio.")
    
    col1, col2 = st.columns(2)
    with col1:
        m_ia = st.selectbox("Marca", sorted(inv.keys()), key="m2")
        mo_ia = st.selectbox("Modelo", sorted(inv[m_ia].keys()), key="mo2")
        a_ia = st.number_input("Año", 1990, 2026, 2015, key="a2")
    with col2:
        op_v_ia = list(inv[m_ia][mo_ia]['versiones'].keys())
        v_ia = st.selectbox("Versión", op_v_ia, key="v2")
        precio_oferta = st.number_input("¿Cuánto te piden? ($)", 0.0)

    if st.button("¿VALE LA PENA?"):
        # Calculamos el valor real internamente para comparar
        v_real = ml.calcular_valor_final(m_ia, mo_ia, v_ia, a_ia, 100000, 2, "No", False, False)
        
        diff = ((precio_oferta - v_real) / v_real) * 100
        
        if diff < -8:
            st.balloons()
            st.success(f"### 💎 ¡ES UNA GANGA!")
            st.write(f"El carro vale aprox. ${v_real:,.0f}. Te ahorras un {abs(diff):.1f}%.")
        elif diff <= 6:
            st.info(f"### ✅ PRECIO JUSTO")
            st.write("Está en el rango correcto de mercado.")
        else:
            st.error(f"### 🚨 NO VALE LA PENA")
            st.write(f"Está muy caro. El valor real es de ${v_real:,.0f}. Tienes un sobreprecio del {diff:.1f}%.")

st.sidebar.caption("Puerto Cabello Edition 2026")
