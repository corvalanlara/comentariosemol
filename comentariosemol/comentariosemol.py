#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import pickle
import argparse
from datetime import datetime
from . import __version__

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as expected

if sys.version < '3':
    import unicodecsv as csv
    import codecs
    from urlparse import urlparse
    import cStringIO
    def u(x):
        return codecs.unicode_escape_decode(x)[0]
else:
    import csv
    from urllib.parse import urlparse
    def u(x):
        return x

#Variables necesarias
ahora = datetime.today()
sep = "-"
tiempo = str(ahora.day) + sep + str(ahora.month) + \
"_" + str(ahora.hour) + sep + str(ahora.minute)
current = os.getcwd()
datapersistente = os.path.join(current, 'path.e')

def limitar(lista, numero):
    if len(lista) <= numero:
        return lista
    elif isinstance(lista, int):
        return [lista]
    else:
        lista.pop()
        limitar(lista, numero)

def crear_navegador(path):
    try:
        driver = Chrome(executable_path=path)
        return driver
    except:
        pass
    try:
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path=path, 
                        firefox_options=options)
        return driver
    except:
        pass
    print('No tiene un navegador compatible o no ha configurado correctamente este programa para trabajar con éste.')
    sys.exit()

def get_pagina(url, driver):
    wait = WebDriverWait(driver, timeout=1)
    driver.get(url)
    wait.until(expected.visibility_of_element_located((By.ID, 'cont_comment')))
    boton = driver.find_element_by_id('show_more_btn')
    while True:
        try:
            boton.click()
        except:
            break
    a = driver.page_source
    print('Código fuente descargado.')
    return a

def get_comentarios(page):
    soup = BeautifulSoup(page, 'html.parser')
    comentarios = soup.find_all('div', {'class' : 'cm_txt_data'})
    aidis = soup.find_all('div', {'class' : 'nombre_perfil_usuario'})
    nombres = soup.find_all('b', {'id' : 'opt-name-c1_F_pop'})
    dislikes = soup.find_all('span', {'class' : 'dislikes_txt'})
    likes = soup.find_all('span', {'class' : 'likes_txt'})
    fecha = soup.find('div', {'class' : 'info-notaemol-porfecha'}).text.strip()
    lista_comentarios = []
    lista_nombres = []
    lista_likes = []
    lista_dislikes = []
    lista_aidis = []
    lista_respuesta = []
    for x in comentarios:
        lista_comentarios.append(x.text.strip())
    for x in nombres:
        lista_nombres.append(x.text.strip().split('\n',1)[0])
    for x in likes:
        lista_likes.append(x.text.strip())
    for x in dislikes:
        lista_dislikes.append(x.text.strip())
    for x in aidis:
        lista_aidis.append(x['id'].split('_', 2)[-1])
    for x in lista_comentarios:
        if x.startswith(tuple(lista_nombres)):
            lista_respuesta.append('R')
        else:
            lista_respuesta.append('O')

    listas = [lista_comentarios, lista_nombres, lista_likes, 
              lista_dislikes, fecha, lista_aidis, lista_respuesta]
    print('Comentarios extraidos.')
    return listas

def crear_csv(listas, url, path):
    fecha = listas[4]
    unidos = zip(listas[0], listas[1], listas[2], 
                 listas[3], listas[5], listas[6])

    if sys.version > '3':
        with open(path, 'w') as csvfile:
            escriba = csv.writer(csvfile, delimiter=',',
                                 quoting=csv.QUOTE_ALL)
            escriba.writerow(['URL', 'Fecha', 'Autor', 'ID',
                              'Original o Respuesta', 'Comentario', 
                              'Likes', 'Dislikes'])
            for comentario, nombre, likes, dislikes, iden, resp  in unidos:
                escriba.writerow([url, fecha, nombre, iden, resp, 
                                 comentario, likes, dislikes])
    else:
        with open(path, mode='wb') as csvfile:
            escriba = csv.writer(csvfile, delimiter=',',
                                 quoting=csv.QUOTE_ALL,
                                encoding = 'utf-8')
            escriba.writerow(['URL', 'Fecha', 'Autor', 'ID',
                              'Original o Respuesta', 'Comentario', 
                              'Likes', 'Dislikes'])
            for comentario, nombre, likes, dislikes, iden, resp  in unidos:
                escriba.writerow([url, fecha, nombre, iden, resp, 
                                 comentario, likes, dislikes])

    if os.path.isfile(path):
        print('Archivo guardado en {}'.format(path))

def get_parser():
    descripcion = """Este programa devuelve una lista 
    de comentarios publicadas en EMOL en formato csv.
    Más información de uso y configuración en 
    https://github.com/corvalanlara/comentariosemol"""
    parser = argparse.ArgumentParser(description = descripcion)
    parser.add_argument('url', metavar='URL', type=str, 
                        help='URL de la cual se obtendrán los comentarios. \
                        También se puede ingresar un archivo txt con URls \
                        separadas por comas.')
    parser.add_argument('filepath', nargs='?', default = os.getcwd(), 
                        type=str, help='Opcional. Path al [aún inexistente] \
                        archivo .csv donde se guardarán los comentarios')
    parser.add_argument('-n', '--numero', help='Número límite de \
                        comentarios a extraer.', default = 0, type=int)
    parser.add_argument('-c', '--configurar', 
                        help='Ingresar ubicación del archivo ejecutable \
                        vinculado al navegador de preferencia',
                        action = 'store_true')
    parser.add_argument('-v', '--version', help='Imprime la versión \
                        actual de comentariosemol. Utilizar escribiendo \
                        "[texto] -v"', action='store_true')
    
    return parser

def ejecutar(noticia, filepath, limite, navegador):
    page = get_pagina(noticia, navegador)
    listas = get_comentarios(page)

    if limite > 0:
        #Limita las listas exceptuando la de fechas
        for x in listas:
            if isinstance(x, list):
                limitar(x, limite)

    crear_csv(listas, noticia, filepath)

def nombrar(filepath, url):
    primero = url.netloc.replace('www.', '').replace('.com', '')
    segundo = url.path.split('/')[-1].replace('.html', '')[:40]
    nombre_archivo = "{}.csv".format(filepath + '/' + primero + segundo + tiempo)
    return nombre_archivo

def configurar():
    if sys.version > '3':
        path = input('Ingrese ubicación del archivo ejecutable correspondiente a su navegador de preferencia (Leer documentación para más información)\n')
    else:
        path = raw_input('Ingrese ubicación del archivo ejecutable correspondiente a su navegador de preferencia (Leer documentación para más información)\n')
    driver = crear_navegador(path)
    driver.quit()
    
    archivo = open(datapersistente, 'wb')
    pickle.dump(path, archivo)
    archivo.close()

    print('Configuración exitosa')

    return path

def main():
    parser = get_parser()
    args = vars(parser.parse_args())
    datos = ''

    if os.path.isfile(datapersistente):
        archivo = open(datapersistente, 'rb')
        datos = pickle.load(archivo)
        archivo.close

    if (datos  == '' or args['configurar']):
        datos = configurar()

    if args['version']:
        print(__version__)
        return

    if not args['url']:
        parser.print_help()
        return

    noticia = args['url']
    if noticia.endswith('.txt') and args['filepath'] != os.getcwd():
        print('Si ingresas un archivo txt, \
            no puedes elegir el nombre del archivo csv a crear.')
        return
    elif noticia.endswith('.txt') and args['filepath'] == os.getcwd():
        if not os.path.isfile(noticia):
            print('El archivo txt al que se hace referencia no existe.')
            return
        else:
            with open(noticia) as f:
                todas = f.readlines()
                todas = ''.join(todas).strip().replace('\n', ',').replace(' ','')
                todas = todas.split(',')
                if '' in todas:
                    todas.remove('')
                noticia = todas
    
    if isinstance(noticia, str):
        url = urlparse(noticia)

        if not url.scheme and not url.netloc:
            parser.print_help()
            return

        if url.netloc != 'www.emol.com':
            print('La URL debe ser de una noticia de EMOL')
            return
    elif isinstance(noticia, list):
        url = []
        for x in noticia:
            url.append(urlparse(x))
        for x in url:
            if not x.scheme and not x.netloc:
                print('El archivo txt debe contener direcciones URL')
                parser.print_help()
                return

            if x.netloc != 'www.emol.com':
                print('Las URLs deben ser de noticias de EMOL')
                return
    
    filepath = args['filepath']

    if filepath == os.getcwd():
        if isinstance(noticia, str):
            filepath = nombrar(filepath, url)
        elif isinstance(noticia, list):
            lista_filepaths = []
            for x in url:
                nombre_archivo = nombrar(filepath, x)
                lista_filepaths.append(nombre_archivo)
    else:
        if not filepath.endswith('.csv'):
            print('El archivo por crear debe terminar en .csv')
            return

        if os.path.isfile(filepath):
            print('El archivo csv no debe existir')
            return

    limite = args['numero']
    
    exec_path = os.getenv('COMENTARIOS_EMOL')
    navegador = crear_navegador(datos)
    if isinstance(noticia, str):
        ejecutar(noticia, filepath, limite, navegador)
    elif isinstance(noticia, list):
        tuplas = zip(noticia, lista_filepaths)
        for noticia, filepath in tuplas:
            ejecutar(noticia, filepath, limite, navegador)
    navegador.quit()

if __name__ == '__main__':
    main()
