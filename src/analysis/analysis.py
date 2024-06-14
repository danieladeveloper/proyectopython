import pandas as pd #para manejar y analizar datos
import os #para interactuar con el sistema operativo
from ..decorators.decorators import timeit, logit

@logit
@timeit
def load_data(data_path):
    #carga los datos desde un archivo, en este caso csv.
    if data_path.endswith(".csv"):
        df= pd.read_csv(data_path)
    elif data_path.endwith("xlsx"):
        df= pd.read_excel(data_path)
    else:
        raise ValueError("Unsupported file format")
    print("data loaded successfully")
    return df

@logit
@timeit
def clean_data(df):
    df["price"]= df["price"].replace(r"[\$]","", regex=True).astype(float)
    df["promo"]= df["promo"].replace(r"[\$]","", regex=True).astype(float)
    print("data cleaned successfully")
    return df

@logit
@timeit
def analyze_data(df):
    print("basic data analysis: ") #imprime encabezado para análisis de datos
    print(df.describe()) #resumen estadístico de los datos
    print("\nProducts with highest prices: ") #imprimimos un encabezado con precios altos.
    highestPrices= df.nlargest(60,"price") #10 productos precios altos
    print(highestPrices)
    return highestPrices


@logit
@timeit
def save_clean_data(df, output_path):
    if output_path.endswith(".csv"):
        df.to_csv(output_path, index=False)
    elif output_path.endwith(".txt"):
        df.to_excel(output_path, index=False)
    else:
        raise ValueError("Unssupported file format")
    print(f"clean data saved to {output_path}")
    
if __name__ == "__main__": #el script se ejecuta en este archivo
    data_path = "data/raw/products.csv" #es la ruta del archivo de datos sin procesar
    output_path = "data/processed/cleaned_products.csv" #ruta del archivo de datos procesados.
    
    df = load_data(data_path) #carga los archivos
    df = clean_data (df) #limpieza de datos
    df = analyze_data(df) # analiza los datos
    os.makedirs("data/processed", exist_ok=True) #crea el directorio para los datos procesados si no existe
    save_clean_data(df, output_path) #datos guardados