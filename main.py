from graficador import GeneradorGraficas

if __name__ == '__main__':
    base1 = 'ejecuciones/analisis parametrico/SVNS/ajuste.parametrico.tiempo/'
    base2 = '/config.yaml'
    nombres = [
        # 'Caso1Id1m-01-01-2019',
        # 'Caso3Id2m-01-01-2019',
        # 'Caso4Id3t-16-01-2019',
        # 'Caso5Id5t-16-01-2019',
        # 'Caso6Id4t-14-01-2019',
        # 'Caso7Id6t-19-10-2018',
        # 'Caso8Id0m-13-09-2018',
        'Caso9Id1m-13-09-2018'
    ]

    # url_fichero_propiedades = [
        # 'ejecuciones/analisis parametrico/SVNS/alphas/config.yaml',
        # 'ejecuciones/analisis parametrico/SVNS/alphas.parte2/config.yaml',
        # "C:\Users\Administrador\Documents\Proyecto - Salomon\resultados\Caso1Id1m - 01 - 01 - 2019\VNS\Trazas",
        # 'ejecuciones/analisis parametrico/SVNS/alphas.distanciaSlots/Caso1Id1m-01-01-2019/config.yaml',
    # ]
    # GeneradorGraficas(url_fichero_propiedades).execute()
    GeneradorGraficas([base1 + x + base2 for x in nombres]).execute()
