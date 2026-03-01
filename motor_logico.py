import pandas as pd

def cargar_inventario_excel():
    """Lee la base de datos de precios desde el archivo CSV"""
    try:
        # Intenta leer el archivo que usted subirá a GitHub
        df = pd.read_csv('precios.csv')
        # Limpia espacios por si acaso
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        # Si el archivo no existe o está mal formado, devuelve None
        return None

def obtener_versiones():
    """Super Data de versiones y sus potenciadores de precio"""
    return {
        'Corolla': {'XLI': 0.90, 'GLI': 1.00, 'SEG': 1.15},
        'Yaris': {'Versión E': 0.85, 'Versión G': 1.00, 'Sport': 1.10},
        'Fortuner': {'SR5 (4x2)': 0.90, 'SR5 (4x4)': 1.00, 'Diamond': 1.25},
        'Hilux': {'SR': 1.00, 'Kavak': 1.20, 'Revo': 1.35},
        '4Runner': {'SR5': 1.00, 'Limited': 1.20, 'TRD Pro': 1.35},
        'Aveo': {'LS': 0.90, 'LT': 1.00, 'LTZ': 1.12},
        'Silverado': {'LS': 0.90, 'LT': 1.00, 'LTZ': 1.20, 'High Country': 1.35},
        'Explorer': {'XLT': 1.00, 'Limited': 1.15, 'ST': 1.30},
        'Fiesta': {'Power/Max': 0.85, 'Move': 0.95, 'Titanium': 1.05},
        'Getz': {'1.3 GL': 0.90, '1.6 GLS': 1.00},
        'Tucson': {'GL': 0.90, 'GLS': 1.00, 'Limited': 1.15}
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    df = cargar_inventario_excel()
    if df is None:
        return 0
    
    # Buscamos la fila exacta en su Excel
    filtro = df[(df['marca'] == marca) & (df['modelo'] == modelo) & (df['anio'] == anio)]
    
    if not filtro.empty:
        valor = float(filtro['precio_base'].values[0])
    else:
        return 0

    # Aplicamos el potenciador de la versión
    data_v = obtener_versiones()
    multiplicador = data_v.get(modelo, {}).get(version, 1.0)
    valor *= multiplicador
    
    # Descuentos por estado físico
    if km > 150000: valor *= 0.95
    if choque == "Sí": valor *= 0.75
    if e: valor *= 0.94 # Pintura
    if m: valor *= 0.88 # Mecánica
    
    return round(valor, 2)
