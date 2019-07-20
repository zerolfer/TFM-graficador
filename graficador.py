import os

import pandas as pd
import plotly.graph_objects as go
import plotly as py
import yaml

param = yaml.load(open('config.yaml', 'r'), Loader=yaml.Loader)

# crear el directorio de salida en caso de que no exista
output_path = param["output_path"]
if not os.path.exists(output_path):
    os.mkdir(output_path)

# obtención de datos
# def leer_datos(url, number_str):


'''direccion URL base donde obtener los ficheros'''
URL = param["input_base_url"]


def inicializar_df(num_str):
    filename = param["input_name"] + num_str + '.csv'
    print('DATOS LEIDOS DE ' + URL + filename)
    return pd.read_csv(URL + filename, sep=';', names=['iteracion', 'tiempo (ms)', 'fitness mejor', 'tamaño',
                                                       'numIterSinMejora', 'vecindad', 'fitness sol actual',
                                                       'fitness BL', 'distancia'],
                       skiprows=[0])


def leer_datos(id_list):
    shift = param["start_id"]
    num_iter_max = 0
    plot_info = []

    for i in range(shift, len(id_list) + 1 + shift):
        df = inicializar_df(str(i))
        plot_info.append(df['fitness mejor'])

        if len(df['iteracion']) > num_iter_max:
            num_iter_max = len(df['iteracion'])

    plot_info.append([i for i in range(0, num_iter_max)])  # componente 0 = eje X
    return plot_info


# layout
def create_layout(y_name):
    # noinspection PyUnresolvedReferences
    return go.Layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        legend_orientation="h",
        title=dict(text=param["fig_title"], x=0.5, xanchor="center", y=0.9),
        xaxis=dict(showgrid=False, gridwidth=1, gridcolor='lightgray', title_text='Iteraciones'),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgray', tick0=0, dtick=0.05, title_text=y_name)
    )


def add_lines(fig, nombres, mejor_fitness, x):
    for c, n in zip(mejor_fitness, nombres):
        # noinspection PyUnresolvedReferences
        fig.add_trace(go.Scatter(x=x, y=c,
                                 # line=dict(
                                 # color='firebrick',
                                 # width=2
                                 # ),
                                 name=n))


# %%


def exportar():

    nombres = param["nombres"]
    plot_info = leer_datos(range(param["start_id"], param["start_id"] + len(nombres) - 1))

    print('\nEXPORTANDO...', end='')
    # Definir grafica
    # noinspection PyUnresolvedReferences
    fig = go.Figure(layout=create_layout(param["name_y_axis"]))

    add_lines(fig, nombres, plot_info[:-1], plot_info[-1])

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
    py.io.write_html(fig, file=output_path + fig_name + '.html', auto_open=True)

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

    print('PROCESAMIENTO FINALIZADO')


if __name__ == '__main__':
    exportar()
