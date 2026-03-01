import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Lord Flores", layout="centered")
st.title("💎 Valuador Automotriz Pro")

df = ml.cargar_inventario_excel()
data_versiones = ml.obtener_versiones()

if df is not None:
    tab1, tab2 = st.tabs(["📊 Calculadora", "🔍 Análisis de Oferta IA"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            marca = st.selectbox("Marca", sorted(df['marca'].unique()))
            modelo = st.selectbox("Modelo", sorted(df[df['marca'] == marca]['modelo'].unique()))
            anio = st.selectbox("Año", sorted(df[(df['marca'] == marca) & (df['modelo'] == modelo)]['anio'].unique(), reverse=True))
        with c2:
            # MAGIA: Solo muestra las versiones que pertenecen a ese modelo específico
            versiones_posibles = list(data_versiones.get(modelo, {'Base': 1.0}).keys())
            version = st.selectbox("Versión Específica", versiones_posibles)
            km = st.number_input("Kilometraje", 0, 1000000, 100000)

        with st.expander("🛠️ Detalles de Estado"):
            ch = st.checkbox("¿Reporta Choque anterior?")
            pi = st.checkbox("¿Detalles de Pintura?")
            me = st.checkbox("¿Fallas Mecánicas?")

        if st.button("CALCULAR VALOR", use_container_width=True):
            res = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", pi, me)
            st.success(f"## Valor de Mercado: ${res:,.2f} USD")

    with tab2:
        st.subheader("Veredicto de Negocio")
        p_pide = st.number_input("¿Cuánto te están pidiendo? ($)", 0.0)
        
        if st.button("ANALIZAR NEGOCIO", use_container_width=True):
            v_real = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", pi, me)
            diff = ((p_pide - v_real) / v_real) * 100
            
            if diff < -10: st.balloons(); st.success("💎 ¡OFERTA IMPERDIBLE!")
            elif diff <= 8: st.info("✅ PRECIO DENTRO DEL RANGO")
            else: st.error("🚨 SOBREPRECIO DETECTADO")
            st.write(f"Según tu base de datos, este carro vale **${v_real:,.0f}**.")

else:
    st.error("⚠️ Su Nobleza, falta el archivo 'precios.csv' en GitHub.")

st.sidebar.caption("Lord Flores - Puerto Cabello 2026")
