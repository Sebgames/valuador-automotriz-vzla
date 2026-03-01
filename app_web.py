import streamlit as st
import motor_logico as ml

st.set_page_config(page_title="Valuador Lord Flores", layout="centered", page_icon="💎")

st.title("💎 Valuecar Pro")
st.markdown("### *Calcula el precio de automoviles con confianza con Valuecar Pro ")

df = ml.cargar_inventario_excel()
data_v = ml.obtener_versiones()

if df is not None:
    t1, t2 = st.tabs(["📊 Valuador", "🔍 Scanner de Negocios"])

    with t1:
        st.subheader("Configuración del Vehículo")
        col1, col2 = st.columns(2)
        with col1:
            marca = st.selectbox("Marca", sorted(df['marca'].unique()))
            modelo = st.selectbox("Modelo", sorted(df[df['marca'] == marca]['modelo'].unique()))
            anio = st.selectbox("Año", sorted(df[(df['marca'] == marca) & (df['modelo'] == modelo)]['anio'].unique(), reverse=True))
        with col2:
            ver_list = list(data_v.get(modelo, {'Base': 1.0}).keys())
            version = st.selectbox("Versión", ver_list)
            km = st.number_input("Kilometraje", 0, 1000000, 100000)

        with st.expander("🛠️ Detalles Técnicos y Estéticos"):
            ch = st.checkbox("¿Tiene historial de siniestros/choques?")
            pi = st.checkbox("¿Presenta detalles de pintura?")
            me = st.checkbox("¿Presenta fallas mecánicas?")

        if st.button("CALCULAR PRECIO MAESTRO", use_container_width=True):
            res = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", pi, me)
            if res > 0:
                st.balloons()
                st.success(f"## Valor sugerido: ${res:,.2f} USD")
            else:
                st.error("No se encontró ese año en el archivo CSV.")

    with t2:
        st.subheader("🕵️ Análisis de Oportunidad")
        p_oferta = st.number_input("Precio de la oferta actual ($)", 0.0)
        
        if st.button("ESCANEAR OFERTA", use_container_width=True):
            v_real = ml.calcular_valor_final(marca, modelo, version, anio, km, 1, "Sí" if ch else "No", pi, me)
            if v_real > 0:
                diff = ((p_oferta - v_real) / v_real) * 100
                st.divider()
                st.write(f"Valor de mercado según Lord Flores: **${v_real:,.0f}**")
                
                if diff < -10:
                    st.success(f"### 🔥 ¡OFERTA DETECTADA! (Ahorras {abs(diff):.1f}%)")
                    st.info("Este precio es significativamente bajo. Si el carro está sano, ¡es un negocio de oro!")
                elif diff <= 8:
                    st.info(f"### ✅ NEGOCIO JUSTO ({diff:.1f}%)")
                    st.write("El precio está en el rango correcto del mercado.")
                else:
                    st.error(f"### 🚨 SOBREPRECIO ({diff:.1f}%)")
                    st.write("El vendedor está pidiendo más de lo que dicta su base de datos.")
            else:
                st.warning("Primero defina el vehículo en la pestaña anterior.")
else:
    st.error("⚠️ Su Nobleza, el archivo 'precios.csv' no responde.")
    st.info("Verifique que el archivo en GitHub no tenga punto y coma (;) y use comas (,).")

st.sidebar.caption("💎 Potenciado por investigacion de el mercado exahustiva ")

