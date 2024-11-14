import requests
from bs4 import BeautifulSoup as bs
import random
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import os

def obtener_valores_depto():
    # abrir explorador
    browser = uc.Chrome()
    browser.implicitly_wait(10)
    busqueda = 'resistencia'
    busqueda = busqueda.replace(' ', '-')
    x = 1
    urls = []
    #puse para leer solo 2 paginas, serian unas 30 publcaciones, si quieres todas las que haya tienes que poner while True
    while x < 12:
        url = f'https://www.zonaprop.com.ar/departamentos-venta-{busqueda}-pagina-{x}.html'
        browser.get(url)
        time.sleep(random.randint(10, 12))
        try:
            browser.find_element("xpath", '//*[@id="didomi-notice-agree-button"]').click()
        except:
            pass
        html = browser.page_source
        soup = bs(html, 'lxml')
        articulos = soup.find('div', {'class': 'postings-container'}).find_all('div', {'data-qa': 'posting PROPERTY'})
        x += 1
        for articulo in articulos:
            url_deptos = articulo.get('data-to-posting')
            urls.append(url_deptos)
            time.sleep(random.randint(1, 3))
        urls = [deptos for deptos in urls if deptos is not None]

    id_casas = pd.DataFrame(urls)
    id_casas.columns = ['urls']


    def parsear_depto(urls_lista):
        url = 'https://www.zonaprop.com.ar' + urls_lista
        browser.get(url)
        html = browser.page_source
        soup = bs(html, 'lxml')
        if 2 < len(soup.find('div', {'class': 'price-value'}).text.strip().split()):
            precio = soup.find('div', {'class': 'price-value'}).text.strip().split()[2]
        else:
            precio = None
        direccion = soup.find('div', {'class': 'section-location-property'}).find('h4').text.strip().split(sep=',')
        c1 = soup.find('div', {'class': 'section-main-features mt-24'}).find('ul', {'class': 'section-icon-features section-icon-features-property'})
        caracteristicas = [caract.text.strip().split(sep=',') for caract in c1.find_all('li')]
        # Crear un DataFrame temporal con los datos de la casa actual
        df_temporal = pd.DataFrame({
            'urls': urls_lista,
            'precio': [precio],
            'direccion': [direccion],
            'caracteristicas': [caracteristicas]
        })
        return df_temporal


    # Crear un DataFrame vacío para almacenar los resultados
    df_final = pd.DataFrame()
    # Iterar sobre las URLs y aplicar la función parsear_depto
    for url in urls:
        df_temporal = parsear_depto(url)
        df_final = pd.concat([df_final, df_temporal])
    # Restablecer el índice del DataFrame final
    df_final.reset_index(drop=True, inplace=True)
    # Cerrar el navegador
    browser.quit()
    # Obtener la ruta del directorio actual
    directorio_actual = os.getcwd()
    ruta_deptos = os.path.join(directorio_actual, 'dataframes', 'venta_deptos.csv')
    df_final.to_csv(path_or_buf=ruta_deptos, index=False)
    # Retornar el DataFrame final
    return print('Todo salio bien')


obtener_valores_depto()