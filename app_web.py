import streamlit as st
import motor_logico as ml

st.markdown(f"""
    <head>
        <meta name="google-site-verification" content="<meta name="google-site-verification" content="MqNrSrBhIxlVhEkoKxy-tWUTdruDgZbEUEtriVZNZ0I" />" />
        
        <title>Lord Valuador | Precios de Carros Usados en Venezuela</title>
        <meta name="description" content="Consulte el precio real de carros usados en Venezuela. Investigación de mercado de Lord Flores en Puerto Cabello y Carabobo.">
    </head>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Valuecar PRO 🇻🇪", page_icon="https://github.com/Sebgames/valuador-automotriz-vzla/blob/main/vecteezy_compact-car_1193767.png?raw=true", 
layout="centered")

st.title("💎 Valuecar Pro")
st.markdown("#### Portal creado y diseñado para encontrar el precio correcto de tu automovil usado en el mercado venezolano 🇻🇪 ")

st.markdown(f"""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="apple-mobile-web-app-title" content="Lord Valuador">
        <link rel="apple-touch-icon" href="https://github.com/Sebgames/valuador-automotriz-vzla/blob/main/vecteezy_compact-car_1193767.png?raw=true">
    </head>
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        
    </style>
    """, unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Banner Tricolor en la parte superior */
    .stApp {
        border-top: 8px solid #f1c40f; /* Amarillo */
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 8px;
        left: 0;
        width: 100%;
        height: 8px;
        background-color: #2980b9; /* Azul */
        z-index: 999;
    }
    .stApp::after {
        content: "";
        position: fixed;
        top: 16px;
        left: 0;
        width: 100%;
        height: 8px;
        background-color: #c0392b; /* Rojo */
        z-index: 999;
    }
    
    /* Estilo para el título */
    .titulo-vzla {
        text-align: center;
        color: #f1c40f;
        background-color: #1e272e;
        padding: 15px;
        border-radius: 10px;
        border-bottom: 4px solid #2980b9;
    }
    </style>
""", unsafe_allow_html=True)

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
                st.write(f"Valor de mercado REAL: **${v_real:,.0f}**")
                
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









