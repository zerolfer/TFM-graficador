import os

import pandas as pd
import plotly.graph_objects as go
import plotly as py
import yaml
import plotly.tools as tls


def modify_HTML_for_embedding(url_file):
    """Con este metodo adaptamos el HTML para empotrarlo"""
    with open(url_file, 'r', encoding='utf8') as html:
        data = html.readlines()

    data[3] = "    <div style=\"height: 90vh; width: 90vw\">\n"

    with open(url_file, 'w') as html:
        html.writelines(data)


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

            print('LEYENDO FICHERO PROPIEDADES ' + url_params + ' ... ', end='')

            with open(url_params, 'rt', encoding='utf8') as yml:
                param = yaml.load(yml, Loader=yaml.Loader)

            print('LEÍDO')

            # crear el directorio de salida en caso de que no exista
            if param["output_path_absolute"]:
                output_paths = [param["output_path"]] * len(param["input_base_url"])
                if not os.path.exists(param["output_path"]):
                    os.makedirs(param["output_path"])

            else:
                output_paths = [base + param["output_path"] for base in param["input_base_url"]]

                for path in output_paths:
                    if not os.path.exists(path):
                        os.makedirs(path)

            '''direccion URL base donde obtener los ficheros'''
            if len(param["fig_subtitles"]) != len(param["input_base_url"]):
                exit("INPUT FATAL ERROR AT " + url_params +
                     ": La longitud de los casos y el número de ficheros de entrada no concuerda")
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
        X = [[] for __ in range(len(param["x_axis_variable"]))]

        for i in range(shift, len(id_list) + 1 + shift):
            df = self.inicializar_df(param, url, str(i))
            plot_info.append(df[param["y_axis_variable"]])

            for x_idx, x_var in enumerate(param["x_axis_variable"]):
                if "tiempo" in x_var:
                    df[x_var] = df[x_var] / 1000  # lo convertimos a segundos
                X[x_idx].append(df[x_var])

        # plot_info.append(num_iter_max)  # componente 0 = eje X
        return plot_info, X

    # layout
    def create_layout(self, param, caso_name, x_name):
        y_name = param["name_y_axis"]

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

        for x_idx, (x_axis_variable, x_axis_name) in enumerate(zip(param["x_axis_variable"], param["name_x_axis"])):

            fig_name = '{0}_{1}_{2}'.format(caso_name.replace(" ", ""), param['fig_name'], x_axis_variable)

            print('EXPORTANDO\t[{1}]\t({0})\t...\t'.format(output_path, x_axis_variable), end='')
            for extension in output_formats:

                line_width = output_formats[extension]

                # Definir grafica
                # noinspection PyUnresolvedReferences
                fig = go.Figure(layout=self.create_layout(param, caso_name, x_axis_variable))

                if "limite_iteraciones_raster" in param:
                    if caso_name in param["limite_iteraciones_raster"]:
                        limite = param["limite_iteraciones_raster"][caso_name]
                    else:
                        limite = param["limite_iteraciones_raster"]["default"]

                    if extension not in ["html", "embedded"]:
                        if limite <= X[x_idx][-1]:
                            # counter = sum(1 for df in X if df.iloc[-1] > self.limite_iteraciones_raster)
                            counter = 0
                            for i, df in enumerate(X[x_idx]):
                                if df.iloc[-1] > limite:
                                    X[x_idx][i] = df.loc[:limite]
                                    counter += 1
                            if counter > len(X[x_idx]) // 2:
                                print("[Warning: Demasiados truncamientos ({0}]".format(counter), end='')
                    else:  # if HTML:
                        if not self.range_setted(X, fig, limite, param, x_idx):
                            # En este punto no se ha ejecutado lo del slider
                            fig.update_layout(
                                xaxis_rangeslider=dict(
                                    visible=param["show_slider"]
                                )
                            )

                elif extension in ["html", "embedded"]:
                    fig.update_layout(
                        xaxis_rangeslider=dict(
                            visible=param["show_slider"]
                        )
                    )

                self.add_lines(param, fig, valores, plot_info, X[x_idx], line_width)

                # fig.show(renderer='browser', scale=1.25, width=800,
                #          height=500)  # default size: width=700, height=450, scale=None
                # fig.show(renderer='notebook', scale=1.25,  width=800, height=500) # default size: width=700, height=450, scale=None

                # Dynamic format
                if extension == "html":
                    py.io.write_html(fig, file=output_path + fig_name + '.html', auto_open=False)
                    modify_HTML_for_embedding("{0}{1}.{2}".format(output_path, fig_name, extension))

                elif extension == "embedded":
                    file_name = '{0}_{1}'.format(caso_name.replace(" ", ""), x_axis_variable)
                    py.io.write_html(fig, file=output_path + file_name + "__embedded" + '.html', auto_open=False,
                                     include_plotlyjs=False, full_html=False)
                    # modify_HTML_for_embedding("{0}{1}.{2}".format(output_path, file_name, extension))

                else:
                    # # en el output estatico no queremos Slider en ningun caso
                    # if param["show_slider"]:
                    #     fig.update_layout(
                    #         xaxis_rangeslider=dict(
                    #             visible=False
                    #         )
                    #     )

                    fig.update_layout(
                        xaxis_title="",
                        legend_y=-0.13,
                        annotations=[
                            go.layout.Annotation(
                                x=0.5,
                                y=-0.12,
                                showarrow=False,
                                text=x_axis_name,
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
                        scale = 3
                    elif extension == "pdf":
                        scale = 7
                    else:
                        scale = 2  # valor por defecto

                    fig.write_image("{0}{1}.{2}".format(output_path, fig_name, extension), scale=scale)

                print("{0} ✓\t".format(extension), end='')

            print('PROCESAMIENTO FINALIZADO')
        print()

    def range_setted(self, X, fig, limite, param, x_idx):
        for df in X[x_idx]:
            if df.iloc[-1] > limite:
                fig.update_layout(
                    xaxis=dict(
                        # autorange=False,
                        rangeslider=dict(
                            range=[int(0), limite],
                            visible=param["show_slider"]
                        ))

                )
                return True
        return False
