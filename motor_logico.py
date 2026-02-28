def cargar_inventario():
    return {
        'Toyota': {
            'Corolla': {
                'checkpoints': [(2002, 10500), (2008, 14500), (2014, 23000), (2020, 35000), (2026, 48000)],
                'versiones': {'XLI': 0.9, 'GLI': 1.0, 'SEG': 1.15}, 'factor': 0.98},
            'Yaris': {
                'checkpoints': [(2005, 10800), (2011, 14500), (2026, 32000)],
                'versiones': {'Versión E': 0.9, 'Versión G': 1.0, 'Sport': 1.15}, 'factor': 0.97},
            'Fortuner': {
                'checkpoints': [(2015, 45000), (2020, 68000), (2026, 98000)],
                'versiones': {'SR5': 1.0, 'Diamond': 1.25}, 'factor': 0.985},
            'Hilux': {
                'checkpoints': [(2005, 22000), (2015, 42000), (2026, 85000)],
                'versiones': {'SR': 1.0, 'Kavak': 1.25, 'Revo': 1.4}, 'factor': 0.98},
            '4Runner': {
                'checkpoints': [(2009, 28000), (2019, 65000), (2026, 135000)],
                'versiones': {'SR5': 1.0, 'Limited': 1.25}, 'factor': 0.985}
        },
        'Chevrolet': {
            'Silverado': {
                'checkpoints': [(2007, 18000), (2014, 32000), (2026, 98000)],
                'versiones': {'LS': 0.9, 'LT': 1.0, 'LTZ': 1.2}, 'factor': 0.98},
            'Aveo': {
                'checkpoints': [(2018, 12500), (2026, 28000)],
                'versiones': {'LT': 1.0, 'LTZ': 1.15}, 'factor': 0.97}
        },
        'Hyundai': {
            'Getz': {'checkpoints': [(2012, 11500)], 'versiones': {'1.3 GL': 0.9, '1.6 GLS': 1.0}, 'factor': 0.97},
            'Tucson': {'checkpoints': [(2009, 14500), (2026, 55000)], 'versiones': {'GLS': 1.0, 'Limited': 1.2}, 'factor': 0.975}
        }
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    inv = cargar_inventario()
    if marca not in inv or modelo not in inv[marca]: return 0
    data = inv[marca][modelo]
    
    precio_tope = 0
    for anio_limite, precio in data['checkpoints']:
        if anio <= anio_limite:
            precio_tope = precio
            break
    
    valor = precio_tope * data['versiones'].get(version, 1.0)
    
    # Depreciación por año (Año actual 2026)
    antiguedad = 2026 - anio
    valor *= (data['factor'] ** antiguedad)
    
    # Castigos por detalles (ajustados para no bajar tanto el precio)
    if km > 150000: valor *= 0.90
    if duenos > 2: valor *= 0.85
    if choque == "Sí": valor *= 0.75
    if e: valor *= 0.95 # Pintura
    if m: valor *= 0.92 # Mecánica
    
    return round(valor, 2)

