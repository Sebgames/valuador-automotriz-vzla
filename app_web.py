import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")

st.title("💎 Valuador Automotriz Pro")
st.caption("Investigación de Mercado by Lord Flores")

# Cargamos la data desde el Excel
df = ml.cargar_inventario_excel()
data_versiones = ml.obtener_versiones()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Calculadora", "🕵️ Scanner de Ofertas"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            marca = st.selectbox("Marca", sorted(df['marca'].unique()))
            modelo = st.selectbox("Modelo", sorted(df[df['marca'] == marca]['modelo'].unique()))
            anio = st.selectbox("Año", sorted(df[(df['marca'] == marca) & (df['modelo'] == modelo)]['anio'].unique(), reverse=True))
        with c2:
            # Selecciona versiones basadas en el modelo
            versiones_f = list(data_versiones.get(modelo, {'Base': 1.0}).keys())
            version = st.selectbox("Versión", versiones_f)
            km = st.number_input("Kilometraje", 0, 1000000, 100000)

        ch = st.checkbox("¿Tuvo choques?")
        
        if st.button("CALCULAR SEGÚN MI DATA", use_container_width=True):
            res = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", False, False)
            if res > 0:
                st.success(f"## Valor Estimado: ${res:,.2f} USD")
            else:
                st.error("No encontré ese año en la base de datos.")

    with tab2:
        st.subheader("Análisis de Negocio")
        p_oferta = st.number_input("Precio que te piden ($)", 0.0)
        
        if st.button("¿VALE LA PENA?", use_container_width=True):
            v_real = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", False, False)
            if v_real > 0:
                diff = ((p_oferta - v_real) / v_real) * 100
                if diff < -10: st.balloons(); st.success("💎 ¡OFERTA IMPERDIBLE!")
                elif diff <= 8: st.info("✅ PRECIO JUSTO")
                else: st.error("🚨 SOBREPRECIO")
            else:
                st.warning("Verifica los datos arriba.")
else:
    # Este mensaje sale si el archivo precios.csv no está en la misma carpeta que app_web.py
    st.error("⚠️ Su Nobleza, el archivo 'precios.csv' no se encuentra o tiene un error de formato.")
    st.info("Asegúrese de que el archivo esté en GitHub con el nombre exacto 'precios.csv' (todo en minúsculas).")
