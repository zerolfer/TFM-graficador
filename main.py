from graficador import GeneradorGraficas

if __name__ == '__main__':
    url_fichero_propiedades = [
        'ejecuciones/analisis parametrico/SVNS/alphas/config.yaml',
        'ejecuciones/analisis parametrico/SVNS/alphas.parte2/config.yaml',
    ]
    GeneradorGraficas(url_fichero_propiedades).execute()
