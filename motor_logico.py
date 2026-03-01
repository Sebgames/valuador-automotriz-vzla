import pandas as pd

def cargar_inventario_excel():
    try:
        # 1. Leemos con separador de punto y coma (;) como está su archivo
        df = pd.read_csv('precios.csv', sep=';')
        
        # 2. Limpiamos nombres de columnas por si hay espacios
        df.columns = df.columns.str.strip()
        
        # 3. Limpiamos los precios: Convertimos "24.900" en 24900.0
        # Primero aseguramos que sea texto, quitamos el punto de mil y pasamos a número
        df['precio_tope'] = df['precio_tope'].astype(str).str.replace('.', '', regex=False).astype(float)
        
        return df
    except Exception as e:
        # Si sale este error, es que el archivo no está en la raíz de GitHub
        return None

def obtener_versiones():
    """Potenciadores de precio según el modelo"""
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
    
    # Buscamos la fila exacta
    filtro = df[(df['marca'] == marca) & (df['modelo'] == modelo) & (df['anio'] == anio)]
    
    if not filtro.empty:
        valor = float(filtro['precio_tope'].values[0])
    else:
        return 0

    # Aplicamos versión
    data_v = obtener_versiones()
    multiplicador = data_v.get(modelo, {}).get(version, 1.0)
    valor *= multiplicador
    
    # Castigos por estado (Ajuste suave estilo Lord Flores)
    if km > 150000: valor *= 0.97
    if choque == "Sí": valor *= 0.80
    if e: valor *= 0.96 # Pintura
    if m: valor *= 0.92 # Mecánica
    
    return round(valor, 2)
