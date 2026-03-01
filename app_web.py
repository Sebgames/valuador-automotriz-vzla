import streamlit as st
import motor_logico as ml
import pandas as pd

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

st.title("💎 Valuador Automotriz Pro")
st.caption("Base de Datos Maestra de Lord Flores")

# Intentamos cargar la data
df = ml.cargar_inventario_excel()
data_versiones = ml.obtener_versiones()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Calculadora", "🕵️ Analizador de Ofertas"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            marca = st.selectbox("Marca", sorted(df['marca'].unique()), key="m_web")
            modelo = st.selectbox("Modelo", sorted(df[df['marca'] == marca]['modelo'].unique()), key="mo_web")
            anio = st.selectbox("Año", sorted(df[(df['marca'] == marca) & (df['modelo'] == modelo)]['anio'].unique(), reverse=True), key="a_web")
        with c2:
            versiones_f = list(data_versiones.get(modelo, {'Base': 1.0}).keys())
            version = st.selectbox("Versión Específica", versiones_f, key="v_web")
            km = st.number_input("Kilometraje", 0, 1000000, 100000, key="k_web")

        ch = st.checkbox("¿Reporta Choque?", key="ch_web")
        
        if st.button("CALCULAR VALOR", use_container_width=True):
            res = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", False, False)
            st.success(f"## Valor Estimado: ${res:,.2f} USD")

    with tab2:
        st.subheader("Veredicto de Negocio")
        p_oferta = st.number_input("Precio que te piden ($)", 0.0, key="p_oferta_web")
        
        if st.button("¿ES BUENA OFERTA?", use_container_width=True):
            v_real = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", False, False)
            if v_real > 0:
                diff = ((p_oferta - v_real) / v_real) * 100
                if diff < -10: st.balloons(); st.success("💎 ¡OFERTA IMPERDIBLE!")
                elif diff <= 8: st.info("✅ PRECIO JUSTO")
                else: st.error("🚨 SOBREPRECIO")
            else:
                st.warning("Verifica los datos del vehículo.")
else:
    st.error("⚠️ Su Nobleza, el archivo 'precios.csv' no se encuentra en GitHub o tiene errores.")
    st.info("Asegúrese de subir el archivo CSV con las columnas: marca, modelo, anio, precio_base")
