import streamlit as st
import motor_logico as ml
import time

# 1. CONFIGURACIÓN DE PÁGINA Y PWA
st.set_page_config(page_title="Valuador Automotriz Pro", page_icon="📊", layout="centered")

# Inyección de metadatos para instalación en móvil
st.markdown('<link rel="manifest" href="/manifest.json">', unsafe_allow_html=True)

# 2. ESTILOS CSS AVANZADOS (EL LOOK PREMIUM)
st.markdown("""
    <style>
    /* Fondo y tipografía general */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    
    /* Contenedor de Cristal */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    
    /* Botón Principal Animado */
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4em;
        background: linear-gradient(90deg, #1e3799, #0984e3);
        color: white;
        font-weight: bold;
        font-size: 18px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 55, 153, 0.4);
    }
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(30, 55, 153, 0.6);
        background: linear-gradient(90deg, #0984e3, #1e3799);
    }
    
    /* Inputs con estilo */
    .stSelectbox, .stNumberInput {
        background-color: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
    }
    
    /* Banner de Publicidad Discreto */
    .ad-slot {
        background: rgba(241, 196, 15, 0.1);
        border: 1px dashed #f1c40f;
        color: #f1c40f;
        padding: 10px;
        text-align: center;
        border-radius: 10px;
        font-size: 12px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. INTERFAZ DE USUARIO
st.markdown('<div class="ad-slot">🚀 ESPACIO PUBLICITARIO DISPONIBLE - CONTACTAR ADMINISTRADOR</div>', unsafe_allow_html=True)

st.title("💎 Valuador Inteligente")
st.markdown("##### Inteligencia de Mercado para Venezuela 2026")

# --- MANUAL DE INSTALACIÓN (SUTIL) ---
with st.expander("📲 Instalar en mi Pantalla de Inicio"):
    st.info("iPhone: Compartir -> Añadir a inicio | Android: Menú (⋮) -> Instalar app")

st.divider()

# Cargamos la data desde su lógica existente
inv = ml.cargar_inventario()

# Bloque de Selección Estilizado
with st.container():
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        marca = st.selectbox("Marca del Activo", sorted(inv.keys()))
        modelo = st.selectbox("Modelo", sorted(inv[marca].keys()))
    with c2:
        anio = st.number_input("Año", 1990, 2026, 2018)
        version = st.select_slider("Equipamiento", options=["Base", "Gama Media", "Full / Lujo"], value="Gama Media")
    st.markdown('</div>', unsafe_allow_html=True)

# Bloque de Detalles (Colapsable para no estorbar)
with st.expander("🛠️ Detalles de Estado y Uso"):
    c3, c4 = st.columns(2)
    with c3:
        km = st.number_input("Kilometraje Real", 0, 1000000, 100000)
        duenos = st.slider("Dueños anteriores", 1, 6, 2)
    with c4:
        choque = st.checkbox("¿Reporta Colisiones?")
        estetico = st.checkbox("Detalles de Pintura")
        mecanico = st.checkbox("Fallas Mecánicas")

st.write("") # Espacio estético

# 4. ACCIÓN Y RESULTADO
if st.button("✨ CALCULAR VALOR DE CALLE"):
    with st.status("🔮 Analizando variables de mercado...", expanded=False) as status:
        time.sleep(0.7)
        st.write("Verificando precios de referencia en Carabobo...")
        time.sleep(0.7)
        st.write("Aplicando factores de depreciación Lord Flores...")
        
        # Llamada a su lógica
        res = ml.calcular_valor_final(marca, modelo, version, anio, km, duenos, "Sí" if choque else "No", estetico, mecanico)
        status.update(label="✅ Análisis Finalizado", state="complete")

    # Cuadro de Resultado Premium
    st.balloons()
    st.markdown(f"""
        <div style="text-align: center; margin-top: 20px; padding: 30px; background: rgba(46, 204, 113, 0.15); border-radius: 20px; border: 2px solid #2ecc71;">
            <p style="color: #bdc3c7; margin-bottom: 0;">VALOR ESTIMADO DE MERCADO</p>
            <h1 style="color: #2ecc71; font-size: 55px; margin-top: 0;">$ {res:,.2f} <span style="font-size: 20px;">USD</span></h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="ad-slot" style="margin-top:20px;">💰 ¿Necesitas financiamiento? Consulta con nuestros aliados.</div>', unsafe_allow_html=True)

st.sidebar.caption("Consultoría Automotriz v7.0")
st.sidebar.markdown("---")
st.sidebar.write("👑 **Excelentísimo Mr. Flores**")
