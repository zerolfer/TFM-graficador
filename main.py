from graficador import GeneradorGraficas

if __name__ == '__main__':
    base = ['ejecuciones/entornos probabilisticos/2_6-11-2019/config.yaml']

    # url_fichero_propiedades = [
    # 'ejecuciones/analisis parametrico/SVNS/alphas/config.yaml',
    # 'ejecuciones/analisis parametrico/SVNS/alphas.parte2/config.yaml',
    # "C:\Users\Administrador\Documents\Proyecto - Salomon\resultados\Caso1Id1m - 01 - 01 - 2019\VNS\Trazas",
    # 'ejecuciones/analisis parametrico/SVNS/alphas.distanciaSlots/Caso1Id1m-01-01-2019/config.yaml',
    # ]
    # GeneradorGraficas(url_fichero_propiedades).execute()
    GeneradorGraficas(base).execute(
        {
            # dynamic
            "html":2,

            # static raster
            "png": 0.75,
            # "jpg": 0.75,

            # static vectorial
            "pdf": 8,
            # "eps": 8, # ??
            # "svg":8
        }
    )
