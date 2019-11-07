import os

import pandas as pd
import plotly.graph_objects as go
import plotly as py
import yaml


class GeneradorGraficas:
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
        # noinspection PyUnresolvedReferences
        lay = go.Layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend_orientation="h",
            title=dict(text=param["fig_title"] + "<br><span style=\"font-size:14px;\">" + caso_name + "<span>", x=0.5,
                       xanchor="center", y=0.9),
            xaxis=dict(showgrid=False, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                       zeroline=True, zerolinecolor='lightgray', title_text='Iteraciones'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                       zeroline=True, zerolinecolor='lightgray', title_text=y_name, range=[None, 1])
            # tick0=0,dtick=0.05,
        )
        lay.yaxis.zerolinecolor = 'lightgray'
        lay.yaxis.zeroline = True

        return lay

    def add_lines(self, param, fig, valores, mejor_fitness, X, line_width):
        p = param["parametro"]
        for c, n, x in zip(mejor_fitness, valores, X):
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

            self.add_lines(param, fig, valores, plot_info, X, line_width)

            # Add range slider
            # noinspection PyUnresolvedReferences
            fig.update_layout(
                xaxis=go.layout.XAxis(
                    rangeslider=dict(
                        visible=param["show_slider"]
                    )
                )  # , xaxis_domain=[0, 1]
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
                        xaxis=go.layout.XAxis(
                            rangeslider=dict(
                                visible=False
                            )
                        )  # , xaxis_domain=[0, 1]
                    )
                    if extension == "eps":
                        # LaTeX format
                        fig.write_image(output_path + fig_name + ".eps", scale=7)
                    elif extension == "png":
                        # Static format
                        fig.write_image(output_path + fig_name + ".png", scale=10)
                    elif extension == "pdf":
                        fig.write_image(output_path + fig_name + ".pdf", scale=7)

            print(extension + " ", end='')

        print('PROCESAMIENTO FINALIZADO\n')
