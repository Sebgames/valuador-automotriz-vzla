import pandas as pd

def cargar_inventario_excel():
    try:
        # Cargamos el CSV (ya configurado con comas)
        df = pd.read_csv('precios.csv')
        
        # Limpieza de nombres de columnas
        df.columns = df.columns.str.strip()
        
        # EL ESCUDO: Por si quedó algún punto como "24.900", lo quitamos
        # Si el número ya viene limpio como "24900", no hace nada malo
        df['precio_tope'] = df['precio_tope'].astype(str).str.replace('.', '', regex=False).astype(float)
        
        return df
    except Exception as e:
        return None

def obtener_versiones():
    """Mega Data de versiones para que el usuario elija"""
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
        'Spark': {'LS': 1.00, 'LT': 1.10},
        'Tahoe': {'LS': 0.90, 'LT': 1.00, 'Z71': 1.20},
        'Optra': {'Design': 1.00, 'Advance': 1.10, 'Limited': 1.15}
    }

def calcular_valor_final(marca, modelo, version, anio, km, duenos, choque, e, m):
    df = cargar_inventario_excel()
    if df is None: return 0
    
    # Buscamos en su investigación de mercado
    filtro = df[(df['marca'] == marca) & (df['modelo'] == modelo) & (df['anio'] == anio)]
    
    if not filtro.empty:
        valor = float(filtro['precio_tope'].values[0])
    else:
        return 0

    # Potenciador de versión automático
    data_v = obtener_versiones()
    multiplicador = data_v.get(modelo, {}).get(version, 1.0)
    valor *= multiplicador
    
    # Castigos de estado (Estilo Lord Flores: Justos pero realistas)
    if km > 25000: valor *= 0.97
    if choque == "Sí": valor *= 0.80
    if e: valor *= 0.96 # Pintura
    if m: valor *= 0.92 # Mecánica
    
    return round(valor, 2)

