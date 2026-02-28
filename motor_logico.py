def cargar_inventario():
    return {
        'Toyota': {
            'Corolla': {'XLI': 34000, 'GLI': 38000, 'SEG': 42000, 'New Sensation': 12500, 'Baby Camry': 7800, 'factor': 0.98},
            'Yaris': {'Versión E (Base)': 24500, 'Versión G (Full)': 29800, 'Belyta': 9800, 'Sport': 12000, 'factor': 0.97},
            '4Runner': {'SR5': 105000, 'Trail': 118000, 'Limited': 135000, 'SR5 (4x2)': 85000, 'factor': 0.985},
            'Hilux': {'Chasis': 55000, 'SR': 62000, 'Kavak 2.7': 72000, 'Kavak 4.0': 85000, 'Revo': 95000, 'factor': 0.98},
            'Fortuner': {'SR5': 88000, 'Diamond': 105000, 'factor': 0.98},
            'Machito': {'Techo Duro': 105000, 'Pick-up': 98000, 'Chasis': 88000, 'factor': 0.99}
        },
        'Chevrolet': {
            'Silverado': {'LS': 82000, 'LTZ': 98000, 'Z71': 115000, '4x2': 78000, 'factor': 0.985},
            'Tahoe': {'LS': 105000, 'LT': 115000, 'Z71': 128000, 'High Country': 140000, 'factor': 0.985},
            'Aveo': {'LT (Sincrónico)': 7800, 'LT (Automático)': 8800, 'LTZ': 9800, 'Nuevo Aveo (2024)': 24500, 'factor': 0.97},
            'Spark': {'LS': 5800, 'LT': 6800, 'factor': 0.96},
            'Optra': {'Design': 6500, 'Advance': 7800, 'Limited': 8200, 'factor': 0.94}
        },
        'Ford': {
            'Explorer': {'XLT': 75000, 'Limited': 85000, 'ST': 98000, 'Eddie Bauer': 12500, 'factor': 0.975},
            'F-150': {'Lariat': 85000, 'Platinum': 98000, 'Raptor': 155000, 'Fortaleza': 9500, 'factor': 0.98},
            'Fiesta': {'Move': 24000, 'Titanium': 29500, 'Power': 6800, 'Max': 7500, 'factor': 0.97},
            'Super Duty': {'F-250': 115000, 'F-350': 125000, 'Lariat': 135000, 'factor': 0.99}
        },
        'Hyundai': {
            'Getz': {'GL 1.3': 7200, 'GLS 1.6': 8500, 'factor': 0.965},
            'Tucson': {'GL (Sencilla)': 45000, 'GLS (Full)': 52000, 'Vieja (2008)': 9500, 'factor': 0.97},
            'Elantra': {'GLS': 9500, 'Sport': 11500, 'Nuevo (2024)': 32000, 'factor': 0.97}
        },
        'Mitsubishi': {
            'Lancer': {'GLX': 8500, 'Touring': 11500, 'Signo': 6500, 'factor': 0.965},
            'Montero': {'Sport': 55000, 'Limited': 65000, 'Dakar': 14500, 'factor': 0.975}
        },
        'Jeep': {
            'Grand Cherokee': {'Laredo': 75000, 'Limited': 85000, 'Summit': 95000, 'WK2 (2012)': 18000, 'factor': 0.97},
            'Wrangler': {'Sport': 65000, 'Sahara': 78000, 'Rubicon': 95000, 'JK (2015)': 32000, 'factor': 0.985}
        },
        'Chery': {
            'Arauca': {'Base': 4800, 'factor': 0.95},
            'Orinoco': {'Base': 6800, 'factor': 0.95},
            'Tiggo': {'Tiggo 2': 18500, 'Tiggo 4': 24500, 'Tiggo 7': 32000, 'factor': 0.96}
        }
    }

def calcular_valor_final(marca, modelo, version_usuario, anio, km, duenos, choque, e, m):
    inv = cargar_inventario()
    if marca in inv and modelo in inv[marca]:
        datos = inv[marca][modelo]
        factor = datos.get('factor', 0.97)
        precio_ref = datos.get(version_usuario, list(datos.values())[0])
        valor = precio_ref * (factor ** (2026 - anio))
    else: return 0

    tasa_km = km / (max(2026 - anio, 1) * 16000)
    if tasa_km > 1.8: valor *= 0.85 
    elif tasa_km < 0.3: valor *= 1.12 

    if duenos > 3: valor *= 0.90
    if choque == "Sí": valor *= 0.70
    if e: valor *= 0.92 
    if m: valor *= 0.88 
    
    return round(valor, 2)

# NUEVA FUNCIÓN DE IA
def analizar_oferta(precio_real, precio_vendedor):
    diferencia = ((precio_vendedor - precio_real) / precio_real) * 100
    
    if diferencia < -10:
        return "💎 OFERTA DIAMANTE", "El precio está muy por debajo del mercado. ¡Aprovéchalo antes de que vuele!", "#2ecc71"
    elif -10 <= diferencia <= 5:
        return "✅ PRECIO JUSTO", "El vehículo tiene un precio acorde a su valor real de mercado.", "#3498db"
    elif 5 < diferencia <= 15:
        return "⚠️ LIGERAMENTE CARO", "El precio está un poco elevado. Intenta negociar una rebaja.", "#f1c40f"
    else:
        return "🚨 SOBREPRECIO", "Este vehículo está muy caro para su estado y año. ¡No es un buen negocio!", "#e74c3c"
