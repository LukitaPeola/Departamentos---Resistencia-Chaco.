# Proyecto de Web Scraping de Departamentos en Resistencia, Chaco

El tener una vivienda es vital para los ciudadanos de una localidad. Viendo esta necesidad, hemos planeado un proyecto donde todo el que quiera pueda consultar según preferencias personales cuál es la mejor opción ofrecida en el mercado. Para esto, hemos recopilado información, a través de web scraping, de departamentos en la ciudad de Resistencia, provincia del Chaco. Estos datos son extraídos del sitio web "Zonaprop" y almacenados en un archivo CSV. Posteriormente se realiza una limpieza de datos para quitar datos nulos e incoherentes y se crea otro archivo para resguardarlos. Con esta data lista, se realiza un análisis exploratorio (EDA), con una API se los disponibiliza a través de 2 sistemas de recomendación. 

Con este proyecto, los usuarios podrán encontrar, para comprar o alquilar, qué vivienda se ajusta más a sus gustos y necesidades.

## Contenido del Proyecto

### 1. scraping_deptos_ventas.py y scraping_deptos_alquiler.py

Estos archivos contienen el código para realizar el web scraping de Zonaprop. Las funciones principales son:

obtener_valores_depto():

Abre un navegador mediante undetected_chromedriver para simular un usuario real y evitar bloqueos.

Navega entre las páginas de Zonaprop para extraer enlaces a publicaciones de departamentos en venta o alquiler y guardarlos en un arreglo.

Para cada publicación en el arreglo correspondiente, obtiene detalles como el precio, dirección y características del inmueble (metros cuadrados, ambientes, baños, dormitorios, y cocheras).

Guarda los datos extraídos en un archivo CSV (venta_deptos.csv y alquiler_deptos.csv) en la carpeta dataframes.

### 2. limpiar_venta.py y limpiar_alquiler.py

Estos archivos realizan la limpieza y transformación de los datos extraídos. Las principales tareas son:

Limpieza de valores nulos y ajuste de los precios multiplicándolos por 1000 (dado que los precios suelen estar en miles en Zonaprop).

Separación de calle y altura a partir de la dirección del departamento.

Extracción de características de los inmuebles (metros totales, metros cubiertos, cantidad de ambientes, baños, dormitorios y cocheras) mediante expresiones regulares.

Guardado de los datos limpios en un nuevo archivo CSV (venta_deptos_limpio.csv y alquiler_deptos_limpio.csv) en la misma carpeta dataframes.

### 3. EDA.py

Este archivo realiza un análisis exploratorio de los datos (EDA) sobre los conjuntos de datos limpios. Aquí se puede ver gráficos y estadísticas básicas, como:

Distribución de precios, tamaños (metros cuadrados) y cantidad de ambientes.

Correlaciones entre variables.

Estadísticas descriptivas de las propiedades.

### 4. main.py

Este archivo implementa una API usando FastAPI para exponer los datos y ofrecer recomendaciones basadas en las propiedades.

## Las principales rutas de la API son:

/venta/recomendar/puntuacion y /alquiler/recomendar/puntuacion: Proporciona recomendaciones de departamentos según un rango de precio y criterios ponderados como cantidad de ambientes, dormitorios, baños y cocheras. La recomendación se basa en una puntuación calculada en base a estos pesos.

/venta/recomendar/knn y /alquiler/recomendar/knn: Proporciona recomendaciones de departamentos utilizando el algoritmo K-Nearest Neighbors (KNN). Requiere como entrada una nueva propiedad con características como precio, metros cuadrados, cantidad de ambientes, dormitorios, baños y cocheras para recomendar propiedades similares.

## Requisitos

Python 3.10

Google Chrome actualizado (actualmente 131)

## Bibliotecas necesarias (pueden instalarse con el archivo requirements.txt):

```pip install requests beautifulsoup4 pandas selenium undetected_chromedriver fastapi pydantic scikit-learn```

Selenium, beautifulsoup4, requests y undetected_chromedriver: usados para el scraping.

Matplotlib y Seaborn: usados para gráficos estadísticos.

Scikit-learn: usado para los sistemas de recomendación.

FastAPI: para implementar la API de recomendaciones.

## Ejecución del Proyecto

Ejecutar scraping_deptos_ventas.py y scraping_deptos_alquiler.py para obtener los datos iniciales de Zonaprop.

Ejecutar limpiar_venta.py y limpiar_alquiler.py para procesar y limpiar los datos.

(Opcional) Ejecutar EDA.py para analizar los datos obtenidos.

Ejecutar main.py para iniciar la API de recomendaciones:

```uvicorn main:app --reload```

## Ejemplos de Uso de la API

Recomendación por Puntuación:

```
GET venta/recomendar/puntuacion?rango_precio_min=50000&rango_precio_max=100000&peso_ambientes=2&peso_dormitorios=1&peso_banios=1&peso_cocheras=1

GET alquiler/recomendar/puntuacion?rango_precio_min=50000&rango_precio_max=100000&peso_ambientes=2&peso_dormitorios=1&peso_banios=1&peso_cocheras=1
```

Recomendación por KNN:

```
POST venta/recomendar/knn
{
  "precio": 75000,
  "metros_totales": 50,
  "ambientes": 2,
  "dormitorios": 1,
  "banios": 1,
  "cocheras": 1
}

POST alquiler/recomendar/knn
{
  "precio": 250000,
  "metros_totales": 50,
  "ambientes": 2,
  "dormitorios": 1,
  "banios": 1,
  "cocheras": 1
}
```

## Notas

Los archivos de scraping contienen pausas y una espera implícita para reducir la carga en el sitio web y evitar bloqueos.

Los archivos de limpieza de datos requieren ajustes adicionales si los datos obtenidos tienen variaciones en el formato a lo largo del tiempo.

Los precios de venta están en dólares estadounidenses (USD) y los precios de alquileres en pesos argentinos (ARS).

*ACLARACIÓN*: el proyecto fue realizado en varios días, pero hubieron problemas con el repositorio anterior así que nos vimos obligados a mudarlo, por ello figuran pocos commits. Además dejamos en claro que este proyecto no es en si el proyecto final sino que es parte de un proyecto objetivo mucho más grande.

## Contribuidores

En este proyecto hemos trabajado 2 personas, dejamos nuestros perfiles y correos electrónicos.

|                 | GitHub                                                                                             | LinkedIn                                                                                              | Correo electrónico          |
|-----------------|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|------------------------------|
| **Augusto Dor** | [![GitHub](https://img.shields.io/badge/-GitHub-333?logo=github&logoColor=white)](https://github.com/AugustoDor) | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/augusto-dor/) | augustodorjob@gmail.com        |
| **Ian Brandan** | [![GitHub](https://img.shields.io/badge/-GitHub-333?logo=github&logoColor=white)](https://github.com/LukitaPeola) | [![LinkedIn](https://img.shields.io/badge/-LinkedIn-blue?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/ian-brandan/) | ianbran16@gmail.com         |

Si quieres aportar en este proyecto o tienes recomendaciones para ser implementadas no dudes en contactarnos.
