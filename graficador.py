import os

import pandas as pd
import plotly.graph_objects as go
import plotly as py
import yaml


class GeneradorGraficas:
    """
        Generador de gráficas simple.
        Permite graficar a multiples formatos un conjunto dado de datos.
    """
    urls_ficheros_propiedades = []

    def __init__(self, urls_ficheros_propiedades=("config.yaml")):
        # if not urls_ficheros_propiedades:
        #     self.urls_ficheros_propiedades = ["config.yaml"]  # por defecto se utiliza el fichero raiz
        # else:
        self.urls_ficheros_propiedades.extend(urls_ficheros_propiedades)

    def execute(self, output_formats):
        for url_params in self.urls_ficheros_propiedades:

            with open(url_params, 'rt', encoding='utf8') as yml:
                param = yaml.load(yml, Loader=yaml.Loader)

            print('LEIDO FICHERO PROPIEDADES ' + url_params)

            # crear el directorio de salida en caso de que no exista
            output_paths = [base + param["output_path"] for base in param["input_base_url"]]
            for path in output_paths:
                if not os.path.exists(path):
                    os.makedirs(path)

            '''direccion URL base donde obtener los ficheros'''
            for url, out, caso_name in zip(param["input_base_url"], output_paths, param["fig_subtitles"]):
                self.exportar(param, url, out, caso_name, output_formats)

    def inicializar_df(self, param, url, num_str):
        filename = param["input_name"] + num_str + '.csv'
        df = pd.read_csv(url + filename, sep=';', names=self.get_column_names(param), skiprows=[0])
        print('DATOS LEIDOS DE ' + url + filename)
        return df

    def get_column_names(self, param):
        try:
            return param["column_names"]
        except:
            return ['iteracion', 'tiempo (ms)', 'fitness mejor',
                    'fitness 1', 'fitness 2', 'fitness 3', 'fitness 4',
                    'tamaño',
                    # 'numIterSinMejora',
                    'porcentaje mejora',
                    'vecindad',
                    # 'fitness sol actual',
                    # 'fitness BL', 'distancia'
                    ]

    def leer_datos(self, param, url, id_list):
        shift = param["start_id"]
        # num_iter_max = None
        plot_info = []
        X = []

        for i in range(shift, len(id_list) + 1 + shift):
            df = self.inicializar_df(param, url, str(i))
            plot_info.append(df[param["y_axis_variable"]])

            if "tiempo" in param["x_axis_variable"]:
                df[param['x_axis_variable']] = df[param['x_axis_variable']] / 1000
                # print("Flag tiempo activado")

            X.append(df[param['x_axis_variable']])

        # plot_info.append(num_iter_max)  # componente 0 = eje X
        return plot_info, X

    # layout
    def create_layout(self, param, caso_name):
        y_name = param["name_y_axis"]
        x_name = param["name_x_axis"]

        # noinspection PyUnresolvedReferences
        lay = go.Layout(
            paper_bgcolor='white',
            plot_bgcolor='white',

            legend_orientation="h",
            title=dict(text=param["fig_title"] + "<br><span style=\"font-size:14px;\">" + caso_name + "<span>", x=0.5,
                       xanchor="center", y=0.9),
            xaxis=go.layout.XAxis(
                title=go.layout.xaxis.Title(
                    text=x_name,
                    # font=dict(
                    #     family='Courier New, monospace',
                    #     size=18,
                    #     color='#7f7f7f'
                    # )
                ),
                showgrid=False, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                zeroline=True, zerolinecolor='lightgray'
            ),
            yaxis=go.layout.YAxis(
                title=go.layout.yaxis.Title(
                    text=y_name,
                    # font=dict(
                    #     family='Courier New, monospace',
                    #     size=18,
                    #     color='#7f7f7f'
                ),
                showgrid=True, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                zeroline=True, zerolinecolor='lightgray', title_text=y_name, range=[None, 1]
            )
        )
        lay.yaxis.zerolinecolor = 'lightgray'
        lay.yaxis.zeroline = True

        return lay

    def add_lines(self, param, fig, valores, plot_info, X, line_width=2):
        p = param["parametro"]
        for c, n, x in zip(plot_info, valores, X):
            # noinspection PyUnresolvedReferences
            fig.add_trace(go.Scatter(x=x, y=c,
                                     line=dict(
                                         # color='firebrick',
                                         # width=0.75, # PARA PNG: 0.75, PARA HTML: valor por defecto, PARA PDF: 8
                                         width=line_width,
                                     ),
                                     connectgaps=True,  # para conectar los puntos separados
                                     # stackgaps="interpolate",
                                     mode='lines',
                                     name=p + str(n)))

    def exportar(self, param, url, output_path, caso_name, output_formats):
        valores = param["valores"]
        plot_info, X = self.leer_datos(param, url, range(param["start_id"], param["start_id"] + len(valores) - 1))

        print('EXPORTANDO (' + output_path + ') ... ', end='')
        for extension in output_formats:

            line_width = output_formats[extension]

            # Definir grafica
            # noinspection PyUnresolvedReferences
            fig = go.Figure(layout=self.create_layout(param, caso_name))

            if extension not in ["html"] and "limite_iteraciones_raster" in param:
                if caso_name in param["limite_iteraciones_raster"]:
                    limite = param["limite_iteraciones_raster"][caso_name]
                else:
                    limite = param["limite_iteraciones_raster"]["default"]

                # counter = sum(1 for df in X if df.iloc[-1] > self.limite_iteraciones_raster)
                counter = 0
                for i, df in enumerate(X):
                    if df.iloc[-1] > limite:
                        X[i] = df.loc[:limite]
                        counter += 1
                if counter > len(X) // 2: print("[Warning: Demasiados truncamientos ({0}]".format(counter), end='')
            self.add_lines(param, fig, valores, plot_info, X, line_width)

            # Add range slider
            fig.update_layout(
                xaxis_rangeslider=dict(
                    visible=param["show_slider"]
                )
            )

            # graficar

            fig_name = caso_name + " - " + param["fig_name"]

            # fig.show(renderer='browser', scale=1.25, width=800,
            #          height=500)  # default size: width=700, height=450, scale=None
            # fig.show(renderer='notebook', scale=1.25,  width=800, height=500) # default size: width=700, height=450, scale=None

            # Dynamic format
            if extension == "html":
                py.io.write_html(fig, file=output_path + fig_name + '.html', auto_open=False)
            else:
                # en el output estatico no queremos Slider en ningun caso
                if param["show_slider"]:
                    fig.update_layout(
                        xaxis_rangeslider=dict(
                            visible=False
                        )
                    )

                fig.update_layout(
                    xaxis_title="",
                    legend_y=-0.13,
                    annotations=[
                        go.layout.Annotation(
                            x=0.5,
                            y=-0.12,
                            showarrow=False,
                            text=param["name_x_axis"],
                            font_size=13,
                            xref="paper",
                            yref="paper"
                        ), ])

                # LaTeX format
                if extension == "eps":
                    scale = 7

                # Static format
                elif extension == "png" or extension == "jpg":
                    # scale = 7
                    scale = 5
                elif extension == "pdf":
                    scale = 7
                else:
                    scale = 2  # valor por defecto

                fig.write_image(output_path + fig_name + "." + extension, scale=scale)
            print(extension + " ", end='')

        print('PROCESAMIENTO FINALIZADO\n')


class ComparadorMultiplesGraficas:
    """
        Generador de gráficas múltiple.
        Permite graficar varios conjuntos de datos en una interfaz HTML para su comparativa
    """

    urls_parametros = []
    map_indexes = {}

    def __init__(self, urls_parametros=("config.yaml")):
        # if not urls_ficheros_propiedades:
        #     self.urls_ficheros_propiedades = ["config.yaml"]  # por defecto se utiliza el fichero raiz
        # else:
        self.urls_parametros.extend(urls_parametros)

    def execute(self, output_path, fig_name="Comparador de Graficas"):

        print('CARGANDO DATOS ... '.format(output_path))

        fig, indices = self.cargar_graficas()

        self.add_interactivity_to_layout(fig, indices)  # TODO method

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        print('EXPORTANDO en {0} ... '.format(output_path))
        py.io.write_html(fig, file=output_path + fig_name + '.html', auto_open=False)

        print('PROCESAMIENTO FINALIZADO ({0}.html) ... '.format(output_path + fig_name))

    def cargar_graficas(self):

        fig = go.Figure(layout=self.create_layout())
        indices = [[[[{"indices": []}]]]]
        # len(self.urls_parametros) * [
        #     len(self.urls_parametros[0]condiciones_parada) * [
        #         len(valor_condicion_parada) * [
        #             len(variable_eje_x) * []
        #         ]
        #     ]
        # ]
        # ]  # TODO: meter aqui los indices y tambien los 'param'

        contador = 0
        # indices.append([0])
        for i1, parametro in enumerate(self.urls_parametros):
            # if i1 > 0: indices[i1].append([])
            for i2, condiciones_parada in enumerate(parametro):
                if i2 > 0: indices[i1].append([])
                for i3, valor_condicion_parada in enumerate(condiciones_parada):
                    if i3 > 0: indices[i1][i2].append([])
                    for i4, variable_eje_x in enumerate(valor_condicion_parada):
                        if i4 > 0: indices[i1][i2][i3].append({"indices": []})
                        param = self.inicializar_yaml(variable_eje_x)
                        for i5, caso in enumerate(param["input_base_url"]):
                            # if i5 > 0: indices[i1][i2][i3][i4]["indices"].append([])

                            plot_info, X, contador = self.leer_datos(param, caso, contador)

                            self.add_lines(param, fig, param["valores"], plot_info, X)

                            indices[i1][i2][i3][i4]["indices"].append(contador)
                        indices[i1][i2][i3][i4]["param"] = param

                        if len(valor_condicion_parada) > 1: print('\t|')
                    if len(condiciones_parada) > 1: print('\n')
                if len(parametro) > 1: print("\n\n")
            if len(self.urls_parametros) > 1: print("\n\n\n")
        return fig, indices

    def create_layout(self):

        # noinspection PyUnresolvedReferences
        lay = go.Layout(
            paper_bgcolor='white',
            plot_bgcolor='white',

            legend_orientation="h",
            title=dict(text="fig_title", x=0.5, xanchor="center", y=0.9),
            xaxis=go.layout.XAxis(
                showgrid=False, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                zeroline=True, zerolinecolor='lightgray'
            ),
            yaxis=go.layout.YAxis(
                showgrid=True, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                zeroline=True, zerolinecolor='lightgray', range=[None, 1]
            ),
            xaxis_rangeslider=dict(
                visible=True
            )
        )
        lay.yaxis.zerolinecolor = 'lightgray'
        lay.yaxis.zeroline = True

        return lay

    def inicializar_yaml(self, url_params):

        with open(url_params, 'rt', encoding='utf8') as yml:
            param = yaml.load(yml, Loader=yaml.Loader)

        print('\t| LEIDO FICHERO PROPIEDADES ' + url_params)

        # '''direccion URL base donde obtener los ficheros'''
        # for url, out, caso_name in zip(param["input_base_url"], output_paths, param["fig_subtitles"]):
        #     self.exportar(param, url, out, caso_name, output_formats)
        return param

    def add_lines(self, param, fig, valores, plot_info, X):
        p = param["parametro"]
        for c, n, x in zip(plot_info, valores, X):
            # noinspection PyUnresolvedReferences
            fig.add_trace(go.Scatter(x=x, y=c,
                                     connectgaps=True,  # para conectar los puntos separados
                                     # stackgaps="interpolate",
                                     mode='lines',
                                     name=p + str(n)))

    def leer_datos(self, param, url, contador):

        id_list = range(param["start_id"], param["start_id"] + len(param["valores"]) - 1)
        shift = param["start_id"]

        # num_iter_max = None
        plot_info = []
        X = []

        for i in range(shift, len(id_list) + 1 + shift):
            df = self.inicializar_df(param, url, str(i))
            plot_info.append(df[param["y_axis_variable"]])

            if "tiempo" in param["x_axis_variable"]:
                df[param['x_axis_variable']] = df[param['x_axis_variable']] / 1000

            X.append(df[param['x_axis_variable']])
            contador += 1

        # plot_info.append(num_iter_max)  # componente 0 = eje X
        return plot_info, X, contador

    def inicializar_df(self, param, url, num_str):
        filename = param["input_name"] + num_str + '.csv'
        df = pd.read_csv(url + filename, sep=';', names=param["column_names"], skiprows=[0])
        print('\t|\t| DATOS LEIDOS DE ' + url + filename)
        return df

    def add_interactivity_to_layout(self, fig, indices):
        fig.update_layout(
            updatemenus=[
                go.layout.Updatemenu(
                    type="buttons",
                    direction="right",
                    active=0,
                    x=0.57,
                    y=1.2,
                    buttons=list([
                        dict(label="None",
                             method="update",
                             args=[{"visible": [True, False, True, False]}, # TODO: completar
                                   {"title": "Yahoo",
                                    "annotations": []}]),
                        dict(label="High",
                             method="update",
                             args=[{"visible": [True, True, False, False]},
                                   {"title": "Yahoo High",
                                    "annotations": []}]),
                        dict(label="Low",
                             method="update",
                             args=[{"visible": [False, False, True, True]},
                                   {"title": "Yahoo Low",
                                    "annotations": []}]),
                        dict(label="Both",
                             method="update",
                             args=[{"visible": [True, True, True, True]},
                                   {"title": "Yahoo",
                                    "annotations": []}]),
                    ]),
                )
            ]
        )
