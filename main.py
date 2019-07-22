from graficador import GeneradorGraficas

if __name__ == '__main__':
    url_fichero_propiedades = [
        # 'ejecuciones/analisis parametrico/SVNS/alphas/config.yaml',
        # 'ejecuciones/analisis parametrico/SVNS/alphas.parte2/config.yaml',
        # "C:\Users\Administrador\Documents\Proyecto - Salomon\resultados\Caso1Id1m - 01 - 01 - 2019\VNS\Trazas"
    ]
    GeneradorGraficas(url_fichero_propiedades).execute()
