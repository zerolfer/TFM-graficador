from graficador import GeneradorGraficas

if __name__ == '__main__':
    base = [
        'ejecuciones/tipo entornos/probabilisticos/condicion-parada-tiempo/config.yaml',
    ]

    GeneradorGraficas(base).execute(
        {
            # dynamic
            "html": 2,

            # static raster
            # "png": 0.75,
            # "jpg": 0.75,

            # static vectorial
            # "pdf": 8,
            # "eps": 8, # ??
            # "svg":8
        }
    )

    # url_parametros = [
    #     # [  ## PARÁMETRO 1: Tipo de Entornos
    #     #     [  # Probabilísticos
    #
    #     ## CONDICIÓN DE PARADA
    #     [  # Tiempo (10 min)
    #         'ejecuciones/tipo entornos/probabilisticos/condicion-parada-tiempo/config-tiempo.yaml',
    #         'ejecuciones/tipo entornos/probabilisticos/condicion-parada-tiempo/config-iteraciones.yaml'
    #         # ]
    #
    #         # [  # Iteraciones sin mejora
    #         'ejecuciones/entornos probabilisticos/2_6-11-2019/config-tiempo.yaml',  # Casos + tipos VNS
    #         'ejecuciones/entornos probabilisticos/2_6-11-2019/config-iteraciones.yaml'
    #         # ]
    #
    #     ],
    #     # [  # Deterministas
    #     #
    #     #     ## CONDICIÓN DE PARADA
    #     [  # Tiempo (10 min)
    #         'ejecuciones/tipo entornos/deterministas/condicion-parada-tiempo/config-tiempo.yaml',
    #         'ejecuciones/tipo entornos/deterministas/condicion-parada-tiempo/config-iteraciones.yaml'
    #         # ]
    #         #
    #         #     # [  # Iteraciones sin mejora
    #         #     'ejecuciones/entornos probabilisticos/2_6-11-2019/config-tiempo.yaml',  # Casos + tipos VNS
    #         #     'ejecuciones/entornos probabilisticos/2_6-11-2019/config-iteraciones.yaml'
    #         #     # ]
    #         #
    #         # ]
    #     ],  # Fin Tipo de Entornos
    #
    #     # [  ## PARÁMETRO 2: ...
    #     #     [  # Valor A
    #     #
    #     #         ## CONDICIÓN DE PARADA
    #     #         [  # Tiempo (10 min)
    #     #             'ejecuciones/entornos probabilisticos/2_6-11-2019/config-tiempo.yaml',  # Casos + tipos VNS
    #     #             'ejecuciones/entornos probabilisticos/2_6-11-2019/config-iteraciones.yaml'
    #     #         ]
    #     #
    #     #         # [  # Iteraciones sin mejora
    #     #         #     'ejecuciones/entornos probabilisticos/2_6-11-2019/config-tiempo.yaml',  # Casos + tipos VNS
    #     #         #     'ejecuciones/entornos probabilisticos/2_6-11-2019/config-iteraciones.yaml'
    #     #         # ]
    #     #
    #     #     ],
    #     #     [  # Valor B
    #     #
    #     #     ]
    #     # ]  # Fin parametro 2
    #
    # ]
    # test = [
    #     'ejecuciones/tipo entornos/probabilisticos/condicion-parada-tiempo/config.yaml',
    #     'ejecuciones/tipo entornos/probabilisticos/condicion-parada-porcentaje-mejora/config.yaml'
    # ]
    #
    # output_path = 'ejecuciones/'
    # ComparadorMultiplesGraficas(test).execute()
