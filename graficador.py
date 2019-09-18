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

    def execute(self):
        for url_params in self.urls_ficheros_propiedades:
            param = yaml.load(open(url_params, 'r'), Loader=yaml.Loader)
            print('LEIDO FICHERO PROPIEDADES ' + url_params)

            # crear el directorio de salida en caso de que no exista
            output_path = param["input_base_url"] + param["output_path"]
            if not os.path.exists(output_path):
                os.makedirs(output_path)

            '''direccion URL base donde obtener los ficheros'''
            url = param["input_base_url"]

            self.exportar(param, url, output_path)

    def inicializar_df(self, param, url, num_str):
        filename = param["input_name"] + num_str + '.csv'
        print('DATOS LEIDOS DE ' + url + filename)
        return pd.read_csv(url + filename, sep=';', names=['iteracion', 'tiempo (ms)', 'fitness mejor',
                                                           'fitness 1', 'fitness 2', 'fitness 3', 'fitness 4',
                                                           'tamaño', 'numIterSinMejora', 'vecindad', 'porcentaje mejora'
                                                                                                     'fitness sol actual',
                                                           'fitness BL', 'distancia'],
                           skiprows=[0])

    def leer_datos(self, param, url, id_list):
        shift = param["start_id"]
        num_iter_max = 0
        plot_info = []

        for i in range(shift, len(id_list) + 1 + shift):
            df = self.inicializar_df(param, url, str(i))
            plot_info.append(df[param["column_to_plot"]])

            if len(df['iteracion']) > num_iter_max:
                num_iter_max = len(df['iteracion'])

        plot_info.append([i for i in range(0, num_iter_max)])  # componente 0 = eje X
        return plot_info

    # layout
    def create_layout(self, param):
        y_name = param["name_y_axis"]
        # noinspection PyUnresolvedReferences
        lay = go.Layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            legend_orientation="h",
            title=dict(text=param["fig_title"], x=0.5, xanchor="center", y=0.9),
            xaxis=dict(showgrid=False, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                       zeroline=True, zerolinecolor='lightgray', title_text='Iteraciones'),
            yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray', zerolinewidth=1,
                       zeroline=True, zerolinecolor='lightgray', title_text=y_name, range=[None, 1])  # tick0=0,dtick=0.05,
        )
        lay.yaxis.zerolinecolor = 'lightgray'
        lay.yaxis.zeroline=True

        return lay

    def add_lines(self, param, fig, valores, mejor_fitness, x):
        p = param["parametro"]
        for c, n in zip(mejor_fitness, valores):
            # noinspection PyUnresolvedReferences
            fig.add_trace(go.Scatter(x=x, y=c,
                                     # line=dict(
                                     # color='firebrick',
                                     # width=2
                                     # ),
                                     name=p + str(n)))

    def exportar(self, param, url, output_path):
        valores = param["valores"]
        plot_info = self.leer_datos(param, url, range(param["start_id"], param["start_id"] + len(valores) - 1))

        print('EXPORTANDO (' + output_path + ') ... ', end='')
        # Definir grafica
        # noinspection PyUnresolvedReferences
        fig = go.Figure(layout=self.create_layout(param))

        self.add_lines(param, fig, valores, plot_info[:-1], plot_info[-1])

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

        fig_name = param["fig_name"]

        # fig.show(renderer='browser', scale=1.25, width=800,
        #          height=500)  # default size: width=700, height=450, scale=None
        # fig.show(renderer='notebook', scale=1.25,  width=800, height=500) # default size: width=700, height=450, scale=None

        # Dynamic format
        py.io.write_html(fig, file=output_path + fig_name + '.html', auto_open=False)

        # en el output estatico no queremos Slider en ningun caso
        if param["show_slider"]:
            fig.update_layout(
                xaxis=go.layout.XAxis(
                    rangeslider=dict(
                        visible=False
                    )
                )  # , xaxis_domain=[0, 1]
            )

        # LaTeX format
        fig.write_image(output_path + fig_name + ".eps", scale=7)

        # Static format
        fig.write_image(output_path + fig_name + ".png", scale=10)

        print('PROCESAMIENTO FINALIZADO\n')
