import streamlit as st
# Esto vincula el archivo manifest para que el celular permita "instalar" la app
st.markdown(
    """
    <link rel="manifest" href="/manifest.json">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black">
    <meta name="apple-mobile-web-app-title" content="ValuadorVzla">
    """,
    unsafe_allow_html=True,
)
import valuador_inteligente as vi
import time

st.set_page_config(page_title="Valuador Automotriz Pro", page_icon="📈", layout="wide")

# Estilos comerciales
st.markdown("""<style> .stButton>button { width: 100%; border-radius: 10px; height: 3.5em; background-color: #1e3799; color: white; font-weight: bold; } </style>""", unsafe_allow_html=True)

st.title("📈 Sistema de Valuación Automotriz")
st.write("Análisis técnico basado en depreciación, estado físico y rotación de mercado.")
st.divider()

data_m = vi.obtener_data_maestra()

tab1, tab2 = st.tabs(["💰 Calculadora Detallada", "🔍 Análisis de Oportunidad"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca", sorted(data_m.keys()), key="m1")
        modelo = st.selectbox("Modelo", sorted(data_m[marca].keys()), key="mod1")
        version = st.selectbox("Nivel de Equipamiento", ["Básico / LS", "Gama Media / XEI", "Full / Limited / Kavak"], key="v1")
        anio = st.number_input("Año de Fabricación", 1990, 2026, 2015, key="a1")
        km = st.number_input("Kilometraje Total", 0, 1000000, 120000, key="k1")

    with c2:
        duenos = st.number_input("Número de Propietarios", 1, 15, 2, key="d1")
        choque = st.radio("¿Tiene historial de colisiones?", ["No", "Sí"], horizontal=True, key="c1")
        st.write("**Detalles del Vehículo:**")
        estetico = st.checkbox("Detalles de latonería/pintura", key="e1")
        mecanico = st.checkbox("Fallas mecánicas o botes de aceite", key="mec1")

    if st.button("CALCULAR VALOR DE MERCADO"):
        with st.spinner('Procesando variables...'):
            time.sleep(1)
            precio = vi.calcular_valor_vzla(marca, modelo, version, anio, km, duenos, choque, estetico, mecanico)
            st.balloons()
            st.markdown(f"<div style='text-align: center; border: 2px solid #1e3799; padding: 25px; border-radius: 15px; background-color: #f8f9fa;'> <h3 style='color: #555;'>VALOR ESTIMADO</h3> <h1 style='color: #1e3799;'>$ {precio:,.2f} USD</h1> </div>", unsafe_allow_html=True)

with tab2:
    st.subheader("Veredicto de Inversión")
    ca, cb = st.columns(2)
    with ca:
        m_ia = st.selectbox("Marca ", sorted(data_m.keys()), key="mia")
        mod_ia = st.selectbox("Modelo ", sorted(data_m[m_ia].keys()), key="modia")
        anio_ia = st.number_input("Año ", 1990, 2026, 2015, key="aia")
    with cb:
        precio_oferta = st.number_input("Precio que le piden ($)", 0, 500000, 15000, key="po1")
        km_ia = st.number_input("Kilometraje ", 0, 1000000, 120000, key="kia")

    if st.button("ANALIZAR SI VALE LA PENA"):
        with st.status("Consultando base de datos...") as s:
            time.sleep(1)
            # Para el análisis rápido usamos valores estándar de uso
            v_ref = vi.calcular_valor_vzla(m_ia, mod_ia, "Gama Media", anio_ia, km_ia, 2, "No", False, False)
            titulo, msj, tipo = vi.analizar_oferta_ia(precio_oferta, v_ref)
            s.update(label="Análisis Finalizado", state="complete")
        
        st.divider()
        if tipo == "success": st.success(f"### {titulo}"); st.balloons()
        elif tipo == "error": st.error(f"### {titulo}")
        elif tipo == "warning": st.warning(f"### {titulo}")
        else: st.info(f"### {titulo}")
        
        st.write(f"**Análisis:** {msj}")
        st.metric("Valor Sugerido", f"${v_ref:,.2f}", delta=f"{precio_oferta - v_ref:,.2f} USD", delta_color="inverse")


st.sidebar.caption("Soporte Técnico: Consultoría Automotriz v1.0")
