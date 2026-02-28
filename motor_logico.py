def cargar_inventario():
    # Estructura: 'Marca': {'Modelo': { 'Generaciones': [(Año_Fin, Precio_Ref)], 'Versiones': {Nombre: Multiplicador} }}
    return {
        'Toyota': {
            'Corolla': {
                'checkpoints': [(2002, 8500), (2008, 11500), (2014, 16000), (2020, 28000), (2026, 42000)],
                'versiones': {'XLI': 0.9, 'GLI': 1.0, 'SEG': 1.15, 'Hybrid': 1.25},
                'factor': 0.97
            },
            'Fortuner': {
                'checkpoints': [(2015, 35000), (2020, 55000), (2026, 85000)],
                'versiones': {'SR5 (4x2)': 0.9, 'SR5 (4x4)': 1.0, 'Diamond': 1.2},
                'factor': 0.98
            },
            'Yaris': {
                'checkpoints': [(2005, 7500), (2010, 10500), (2020, 18000), (2026, 28000)],
                'versiones': {'Versión E': 0.9, 'Versión G': 1.0, 'S': 1.1},
                'factor': 0.96
            }
        },
        'Chevrolet': {
            'Silverado': {
                'checkpoints': [(2006, 12000), (2013, 22000), (2019, 45000), (2026, 85000)],
                'versiones': {'LS': 0.9, 'LT': 1.0, 'LTZ': 1.15, 'Z71': 1.25},
                'factor': 0.97
            }
        }
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    inv = cargar_inventario()
    if marca not in inv or modelo not in inv[marca]: return 0
    
    data = inv[marca][modelo]
    # Buscar el Checkpoint (Precio de referencia para esa época)
    precio_base = 0
    for anio_limite, precio in data['checkpoints']:
        if anio <= anio_limite:
            precio_base = precio
            break
    
    # Aplicar multiplicador de Versión
    multiplicador_v = data['versiones'].get(version, 1.0)
    valor = precio_base * multiplicador_v
    
    # Depreciación menor por año dentro de su misma época
    años_dif = 2026 - anio
    valor = valor * (data['factor'] ** (años_dif / 2)) # Depreciación suavizada

    # Castigos técnicos
    if km > 120000: valor *= 0.92
    if duenos > 3: valor *= 0.90
    if choque == "Sí": valor *= 0.70
    if e: valor *= 0.93 # Pintura
    if m: valor *= 0.88 # Mecánica
    
    return round(valor, 2)
