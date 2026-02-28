# MOTOR DE CÁLCULO PROFESIONAL - MERCADO VENEZUELA 2026

def obtener_data_maestra():
    return {
        'Toyota': {
            'Corolla': [36000, 0.98], '4Runner': [118000, 0.985], 'Hilux': [68000, 0.98], 
            'Machito': [108000, 0.99], 'Yaris': [28000, 0.97], 'Meru': [34000, 0.975], 
            'Fortuner': [92000, 0.98], 'Prado': [52000, 0.97]
        },
        'Chevrolet': {
            'Aveo': [28000, 0.975], 'Silverado': [92000, 0.985], 'Tahoe': [110000, 0.985],
            'Spark': [18000, 0.965], 'Optra': [16000, 0.93], 'Cruze': [30000, 0.95]
        },
        'Ford': {
            'Fiesta': [28000, 0.97], 'Explorer': [82000, 0.975], 'F-150': [88000, 0.98],
            'Super Duty': [115000, 0.99], 'EcoSport': [26000, 0.95]
        },
        'Hyundai': { 'Getz': [25000, 0.975], 'Tucson': [50000, 0.97] },
        'Mitsubishi': { 'Lancer': [30000, 0.97], 'Montero': [58000, 0.98] }
    }

def calcular_valor_vzla(marca, modelo, version, anio, km, duenos, choques, det_est, det_mec):
    gen_data = obtener_data_maestra()
    
    if marca in gen_data and modelo in gen_data[marca]:
        ref, factor = gen_data[marca][modelo]
        valor = ref * (factor ** (2026 - anio))
    else: return 0

    # 1. Ajuste por Versión
    lujo = ["Full", "Limited", "GLI", "Titanium", "Kavak", "Z71", "SEG", "Overland"]
    if any(k in version for k in lujo): valor *= 1.22
    elif any(k in version for k in ["Base", "Chasis", "Sencilla", "LS"]): valor *= 0.88

    # 2. Ajuste por Kilometraje (Uso Proporcional)
    km_anual_promedio = 16000
    tasa = km / (max(2026 - anio, 1) * km_anual_promedio)
    if tasa > 1.8: valor *= 0.88
    elif tasa < 0.35: valor *= 1.12

    # 3. Castigo por Propietarios (A partir del 3ero se deprecia más)
    if duenos == 1: valor *= 1.05
    elif duenos > 3: valor *= (1.0 - (min((duenos-3)*0.04, 0.20)))

    # 4. Evaluación de Daños y Detalles
    if choques == "Sí": valor *= 0.75
    if det_est: valor *= 0.94 # Latonería/Pintura
    if det_mec: valor *= 0.91 # Fallas mecánicas

    return round(valor, 2)

def analizar_oferta_ia(precio_oferta, valor_mercado):
    dif = ((precio_oferta - valor_mercado) / valor_mercado) * 100
    if dif < -25:
        return "🕵️ SOSPECHOSAMENTE BARATO", "¡Alerta! El precio es demasiado bajo. Verifique procedencia legal y daños ocultos.", "warning"
    elif -25 <= dif < -9:
        return "✅ ¡GANGUIZASO!", "Precio de oportunidad real. Negocio altamente rentable.", "success"
    elif -9 <= dif <= 7:
        return "⚖️ PRECIO DE MERCADO", "Valor justo y equilibrado para las condiciones actuales.", "info"
    elif 7 < dif <= 22:
        return "⚠️ PRECIO ELEVADO", f"Existe un sobreprecio del {round(dif)}%. Se recomienda negociar.", "warning"
    else:
        return "🚫 ROBO A MANO ARMADA", "El precio excede totalmente los límites lógicos del mercado.", "error"