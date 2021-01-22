import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

def aceptar_cookies(año, liga, jornada = None):
    '''
    Inicia el driver de un año, liga y jornada que accede
    al código de la página para extraer los datos

    Parameters
    ----------
    año: int
        Año de los datos a extraer
    liga: str
        Nombre de la liga de los datos a extraer
    jornada: int
        Número de la jornada a partir de la cual empezar la búsqueda
        En caso de no especificarlo, el driver a la página principal
        la cual corresponde a la última jornada de ese año
    
    Returns
    -------
    driver: webdriver
        Elemento webdriver con los datos de la página con los datos del 
        año, liga y jornada. Se usará este driver para extraer el código html
    '''
    
    driver_dir = 'chrome_driver/chromedriver.exe'
    driver=webdriver.Chrome(driver_dir)
    if jornada:
        driver.get("https://www.resultados-futbol.com/"+liga+str(año)+"/grupo1/jornada"+str(jornada))
    else:
        driver.get("https://www.resultados-futbol.com/"+liga+str(año))

    accept_cookies = driver.find_elements_by_xpath('//button[@class="sc-ifAKCX hYNOwJ"]')
    
    try:
        for button in accept_cookies:
            if button.text == "ACEPTO":
                relevant_button = button
                relevant_button.click()
    except:
        pass
    finally:
        return driver

def extraer_datos_jornada(soup):
    '''
    Devuelve los datos de la tabla de posiciones

    Parameters
    ----------
    soup: BeautifulSoup
        Contiene toda la información del código html de la 
        página con los datos sobre el año, liga y jornada

    Returns
    -------
    tabla_jornada: list
        Si el scraping ha salido bien, devuelve una lista de listas con:
        Posicion, Equipo, Puntos, Jornada, Partidos ganados, Partidos empatados,
        Partidos perdidos, Goles a favor, y goles en contra
        En caso de que haya habido algún problema, tabla_jornada se convierte en 
        una lista de valores nulos
    '''
    
    if soup.find("table", {"id": 'tabla2'}):
        table_soup = soup.find("table", {"id": 'tabla2'}).find('tbody').find_all('tr')
    else:
        return None
    num_equipos = len(table_soup)

    Posicion = [table_soup[i].find('th').text for i in range(num_equipos)]
    Equipo = [table_soup[i].find('td', {'class':'equipo'}).find('img').get('alt') for i in range(num_equipos)]
    Puntos = [table_soup[i].find('td', {'class':'pts'}).text for i in range(num_equipos)]
    Jornada = [table_soup[i].find('td', {'class':'pj'}).text for i in range(num_equipos)]
    Ganados = [table_soup[i].find('td', {'class':'win'}).text for i in range(num_equipos)]
    Empatados = [table_soup[i].find('td', {'class':'draw'}).text for i in range(num_equipos)]
    Perdidos = [table_soup[i].find('td', {'class':'lose'}).text for i in range(num_equipos)]
    Goles_a_favor= [table_soup[i].find('td', {'class':'f'}).text for i in range(num_equipos)]
    Goles_en_contra= [table_soup[i].find('td', {'class':'c'}).text for i in range(num_equipos)]

    tabla_jornada = [Posicion, Equipo, Puntos, Jornada, Ganados, Empatados, Perdidos, Goles_a_favor, Goles_en_contra]

    # Nos aseguramos que ningun dato se ha saltado, y que hemos encontrado todos
    if len(set([len(i) for i in tabla_jornada])) == 1:
        return tabla_jornada
    else:
        return [None] * len(tabla_jornada)

