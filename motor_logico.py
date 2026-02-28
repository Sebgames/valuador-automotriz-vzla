def cargar_inventario():
    return {
        'Toyota': {
            'Corolla': {
                # Checkpoints ajustados: 2014 en 19k y 2020 en 28k para que el 2015 caiga en ~23k
                'checkpoints': [(2002, 11500), (2008, 16000), (2014, 19500), (2020, 31000), (2026, 52000)],
                'versiones': {'XLI': 0.9, 'GLI': 1.0, 'SEG': 1.18}, 'factor': 0.985},
            'Yaris': {
                'checkpoints': [(2005, 11800), (2011, 16500), (2026, 35000)],
                'versiones': {'Versión E': 0.9, 'Versión G': 1.0, 'Sport': 1.2}, 'factor': 0.975},
            'Fortuner': {
                'checkpoints': [(2015, 52000), (2020, 78000), (2026, 115000)],
                'versiones': {'SR5': 1.0, 'Diamond': 1.3}, 'factor': 0.985},
            'Hilux': {
                'checkpoints': [(2005, 26000), (2015, 48000), (2026, 92000)],
                'versiones': {'SR': 1.0, 'Kavak': 1.3, 'Revo': 1.5}, 'factor': 0.98},
            '4Runner': {
                'checkpoints': [(2009, 35000), (2019, 78000), (2026, 155000)],
                'versiones': {'SR5': 1.0, 'Limited': 1.3}, 'factor': 0.985}
        },
        'Chevrolet': {
            'Silverado': {'checkpoints': [(2007, 23000), (2014, 38000), (2026, 115000)],
                          'versiones': {'LS': 0.9, 'LT': 1.0, 'LTZ': 1.25}, 'factor': 0.98},
            'Aveo': {'checkpoints': [(2018, 14500), (2026, 32000)],
                     'versiones': {'LT': 1.0, 'LTZ': 1.2}, 'factor': 0.97}
        }
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    inv = cargar_inventario()
    if marca not in inv or modelo not in inv[marca]: return 0
    data = inv[marca][modelo]
    
    # Lógica de Checkpoints
    precio_tope = next((p for a, p in data['checkpoints'] if anio <= a), data['checkpoints'][-1][1])
    valor = precio_tope * data['versiones'].get(version, 1.0)
    
    # Depreciación más lenta para Toyota (factor 0.985)
    valor *= (data['factor'] ** (2026 - anio))
    
    # Ajustes de estado realistas
    if km > 140000: valor *= 0.96
    if duenos > 3: valor *= 0.97
    if choque == "Sí": valor *= 0.75
    if e: valor *= 0.95 
    if m: valor *= 0.90 
    
    return round(valor, 2)
