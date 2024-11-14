from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

# Cargar los datos de ejemplo
data_venta = pd.read_csv(r'dataframes/venta_deptos_limpio.csv')
data_alquiler = pd.read_csv(r'dataframes/alquiler_deptos_limpio.csv')
df_venta = pd.DataFrame(data_venta)
df_alquiler = pd.DataFrame(data_alquiler)

# Modelo de entrada para la recomendación por KNN
class NuevaPropiedad(BaseModel):
    precio: float
    metros_totales: float
    ambientes: int
    dormitorios: int
    banios: int
    cocheras: int

# Función de recomendación por puntuación personalizada
def recomendar_por_puntuacion(df, rango_precio, peso_ambientes=1, peso_dormitorios=1, peso_banios=1, peso_cocheras=1):
    # Filtrar por rango de precio
    df_filtrado = df[(df['precio'] >= rango_precio[0]) & (df['precio'] <= rango_precio[1])]
    # Calcular puntuación basada en las características
    df_filtrado['puntuacion'] = (
        peso_ambientes * df_filtrado['ambientes'] +
        peso_dormitorios * df_filtrado['dormitorios'] +
        peso_banios * df_filtrado['banios'] +
        peso_cocheras * df_filtrado['cocheras']
    )
    # Ordenar por puntuación
    df_recomendadas = df_filtrado.sort_values(by='puntuacion', ascending=False)
    return df_recomendadas[['urls', 'precio', 'puntuacion']]

# Función de recomendación usando KNN
def recomendar_por_knn(df, nueva_propiedad, k=5):
    # Normalizar las características relevantes
    X = df[['precio', 'metros_totales', 'ambientes', 'dormitorios', 'banios', 'cocheras']]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    # Ajustar el modelo KNN
    knn = NearestNeighbors(n_neighbors=k, metric='euclidean')
    knn.fit(X_scaled)
    # Escalar la nueva propiedad
    nueva_propiedad_scaled = scaler.transform([nueva_propiedad])
    # Encontrar los k vecinos más cercanos
    distancias, indices = knn.kneighbors(nueva_propiedad_scaled, n_neighbors=k)
    # Devolver las propiedades recomendadas
    return df.iloc[indices[0]][['urls', 'precio', 'metros_totales', 'ambientes', 'dormitorios', 'banios', 'cocheras']]

# Rutas de la API

# Recomendación por puntuación personalizada
@app.get("/venta/recomendar/puntuacion")
def recomendar_puntuacion_venta(
    rango_precio_min: float = Query(..., description="Precio mínimo"),
    rango_precio_max: float = Query(..., description="Precio máximo"),
    peso_ambientes: Optional[float] = 1,
    peso_dormitorios: Optional[float] = 1,
    peso_banios: Optional[float] = 1,
    peso_cocheras: Optional[float] = 1
):
    rango_precio = (rango_precio_min, rango_precio_max)
    recomendaciones = recomendar_por_puntuacion(
        df_venta, rango_precio, peso_ambientes, peso_dormitorios, peso_banios, peso_cocheras
    )
    return recomendaciones.to_dict(orient="records")

@app.get("/alquiler/recomendar/puntuacion")
def recomendar_puntuacion_alquiler(
    rango_precio_min: float = Query(..., description="Precio mínimo"),
    rango_precio_max: float = Query(..., description="Precio máximo"),
    peso_ambientes: Optional[float] = 1,
    peso_dormitorios: Optional[float] = 1,
    peso_banios: Optional[float] = 1,
    peso_cocheras: Optional[float] = 1
):
    rango_precio = (rango_precio_min, rango_precio_max)
    recomendaciones = recomendar_por_puntuacion(
        df_alquiler, rango_precio, peso_ambientes, peso_dormitorios, peso_banios, peso_cocheras
    )
    return recomendaciones.to_dict(orient="records")

# Recomendación por KNN
@app.post("/venta/recomendar/knn")
def recomendar_knn_venta(propiedad: NuevaPropiedad, k: int = 5):
    nueva_propiedad = [
        propiedad.precio,
        propiedad.metros_totales,
        propiedad.ambientes,
        propiedad.dormitorios,
        propiedad.banios,
        propiedad.cocheras
    ]
    recomendaciones = recomendar_por_knn(df_venta, nueva_propiedad, k)
    return recomendaciones.to_dict(orient="records")

@app.post("/alquiler/recomendar/knn")
def recomendar_knn_alquiler(propiedad: NuevaPropiedad, k: int = 5):
    nueva_propiedad = [
        propiedad.precio,
        propiedad.metros_totales,
        propiedad.ambientes,
        propiedad.dormitorios,
        propiedad.banios,
        propiedad.cocheras
    ]
    recomendaciones = recomendar_por_knn(df_alquiler, nueva_propiedad, k)
    return recomendaciones.to_dict(orient="records")

# Para inicializar la API
# uvicorn main:app --reload
# Poner /docs al final del enlace para probar la API