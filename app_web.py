import streamlit as st
import motor_logico as ml
import time

st.set_page_config(page_title="Valuador Automotriz Pro", page_icon="💎", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: #f8fafc; }
    .glass-card { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 25px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); }
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background: linear-gradient(90deg, #1e3799, #0984e3); color: white; font-weight: bold; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("💎 Valuador Inteligente")
st.caption("Análisis de Mercado & Veredicto de Oferta")

inv = ml.cargar_inventario()

with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(inv.keys()))
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()))
        anio = st.number_input("Año", 1990, 2026, 2018)
    with c2:
        opciones_v = list(inv[marca][modelo].keys())
        if 'factor' in opciones_v: opciones_v.remove('factor')
        version = st.selectbox("Versión", opciones_v)
        precio_vendedor = st.number_input("Precio que te piden ($)", 0, 500000, 10000)
    st.markdown('</div>', unsafe_allow_html=True)

with st.expander("🛠️ Detalles del Vehículo"):
    c3, c4 = st.columns(2)
    with c3:
        km = st.number_input("Kilometraje", 0, 1000000, 80000)
        duenos = st.slider("Dueños", 1, 6, 1)
    with c4:
        choque = st.checkbox("¿Tuvo choques?")
        estetico = st.checkbox("Detalles Pintura")
        mecanico = st.checkbox("Detalles Mecánicos")

if st.button("✨ REALIZAR ANÁLISIS COMPLETO"):
    with st.status("🔮 Consultando base de datos...", expanded=False) as s:
        time.sleep(1)
        res_real = ml.calcular_valor_final(marca, modelo, version, anio, km, duenos, "Sí" if choque else "No", estetico, mecanico)
        titulo_ia, desc_ia, color_ia = ml.analizar_oferta(res_real, precio_vendedor)
        s.update(label="✅ Análisis IA Finalizado", state="complete")

    st.balloons()
    
    # Mostrar Valor Real
    st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: rgba(255,255,255,0.05); border-radius: 15px; margin-bottom: 15px;">
            <p style="margin:0; color:#bdc3c7;">VALOR REAL ESTIMADO</p>
            <h2 style="margin:0; color:#fff;">$ {res_real:,.2f} USD</h2>
        </div>
    """, unsafe_allow_html=True)

    # Mostrar Veredicto IA
    st.markdown(f"""
        <div style="text-align: center; padding: 25px; background: {color_ia}22; border-radius: 20px; border: 2px solid {color_ia};">
            <h2 style="color: {color_ia}; margin-top:0;">{titulo_ia}</h2>
            <p style="color: #f8fafc; font-size: 16px;">{desc_ia}</p>
        </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("👑 **Lord Flores Edition**")
