def cargar_inventario():
    return {
        'Toyota': {
            'Corolla': {'checkpoints': [(2002, 9500), (2008, 13000), (2014, 18500), (2020, 32000), (2026, 45000)],
                        'versiones': {'XLI': 0.9, 'GLI': 1.0, 'SEG': 1.15}, 'factor': 0.97},
            'Yaris': {'checkpoints': [(2005, 9800), (2011, 13500), (2026, 29500)],
                      'versiones': {'E': 0.9, 'G': 1.0, 'Sport': 1.1}, 'factor': 0.96},
            'Fortuner': {'checkpoints': [(2015, 42000), (2020, 62000), (2026, 92000)],
                         'versiones': {'SR5': 1.0, 'Diamond': 1.2}, 'factor': 0.98},
            'Hilux': {'checkpoints': [(2005, 18000), (2015, 38000), (2026, 78000)],
                      'versiones': {'SR': 1.0, 'Kavak': 1.2, 'Revo': 1.35}, 'factor': 0.98},
            '4Runner': {'checkpoints': [(2009, 22000), (2019, 58000), (2026, 125000)],
                        'versiones': {'SR5': 1.0, 'Limited': 1.2, 'TRD': 1.3}, 'factor': 0.985},
            'Machito': {'checkpoints': [(2026, 115000)], 'versiones': {'Chasis': 0.85, 'Techo Duro': 1.0}, 'factor': 0.99}
        },
        'Chevrolet': {
            'Silverado': {'checkpoints': [(2007, 15000), (2014, 28000), (2026, 95000)],
                          'versiones': {'LS': 0.9, 'LT': 1.0, 'LTZ': 1.15}, 'factor': 0.975},
            'Aveo': {'checkpoints': [(2018, 11500), (2026, 26000)],
                     'versiones': {'LT': 1.0, 'LTZ': 1.1}, 'factor': 0.96},
            'Tahoe': {'checkpoints': [(2014, 32000), (2026, 135000)],
                      'versiones': {'LS': 0.9, 'LT': 1.0, 'Z71': 1.2}, 'factor': 0.98}
        },
        'Ford': {
            'Explorer': {'checkpoints': [(2010, 14500), (2019, 38000), (2026, 92000)],
                         'versiones': {'XLT': 1.0, 'Limited': 1.15, 'ST': 1.3}, 'factor': 0.97},
            'Fiesta': {'checkpoints': [(2014, 10500), (2026, 28000)],
                       'versiones': {'Power/Max': 0.8, 'Move': 0.9, 'Titanium': 1.0}, 'factor': 0.96}
        },
        'Hyundai': {
            'Getz': {'checkpoints': [(2012, 9800)], 'versiones': {'1.3 GL': 0.9, '1.6 GLS': 1.0}, 'factor': 0.96},
            'Tucson': {'checkpoints': [(2009, 11500), (2026, 52000)], 'versiones': {'GLS': 1.0, 'Limited': 1.15}, 'factor': 0.97}
        }
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    inv = cargar_inventario()
    if marca not in inv or modelo not in inv[marca]: return 0
    data = inv[marca][modelo]
    
    # 1. Buscar Checkpoint (Valor TOPE)
    precio_tope = 0
    for anio_limite, precio in data['checkpoints']:
        if anio <= anio_limite:
            precio_tope = precio
            break
    
    # 2. Aplicar Versión
    valor = precio_tope * data['versiones'].get(version, 1.0)
    
    # 3. Desgaste por Antigüedad (Incluso si no tiene fallas, el tiempo cobra)
    antiguedad = 2026 - anio
    desgaste_natural = (data['factor'] ** antiguedad)
    valor *= desgaste_natural
    
    # 4. Descuentos por estado (Siendo realistas con Vzla)
    if km > 120000: valor *= 0.93
    if duenos > 2: valor *= 0.95
    if choque == "Sí": valor *= 0.70
    if e: valor *= 0.92 # Pintura
    if m: valor *= 0.88 # Mecánica
    
    return round(valor, 2)
