import pandas as pd
from os import listdir, path, makedirs, walk
import matplotlib.pyplot as plt
from IPython.display import display


def cargar_ejecuciones(path):
    dfs = []
    for ejecucion in listdir(path):
        df = pd.read_csv(path + "\\" + ejecucion, sep=';', encoding="utf-8")
        dfs.append(df)
    return dfs


def procesar_medias(dfs):
    lista = []
    for df in dfs:
        df.loc[df['fitness 1'] <= 0.0, 'fitness 1'] = 1
        lista.append(df.iloc[-1])
    df_concat = pd.DataFrame(data=lista, index=range(0, len(lista)))
    return df_concat.mean()


def calcular_datos(base_path, sub_paths):
    datos_medios_dict = {}

    for sub_path in sub_paths:
        dfs = cargar_ejecuciones(base_path + "\\" + sub_path)
        datos_medios_dict[sub_path] = procesar_medias(dfs)

    # presentar_datos_medios, ordenador de mejor a peor
    datos_medios = pd.DataFrame(data=datos_medios_dict).transpose()
    datos_ordenados = datos_medios.sort_values(by=['fitness total'])
    display(datos_ordenados)
    return datos_medios, datos_ordenados


def dibujar_datos(datos, out_path, file_name, figure_title="", multiple=True):
    columns = ["fitness total", "fitness 1", "fitness 2", "fitness 3", "fitness 4"]
    if not multiple:
        columns = ["fitness total"]

    ax = datos[columns].plot.bar(title=figure_title)

    if not multiple:
        low = datos[columns[0]].min()
        high = datos[columns[0]].max()
    else:
        low = 1
        high = 0
        for col in columns:
            min = datos[col].min()
            max = datos[col].max()

            if min < low: low = min
            if max > high: high = max

    multiplicador=0.01
    if not multiple: multiplicador=0.01

    for p in ax.patches:
        ax.annotate(str(round(p.get_height(), 3)),
                    (p.get_x() * 1.0005, p.get_height() + (high-low)*multiplicador))

    plt.legend(loc='lower left', bbox_to_anchor=(1.0, 0.0))
    plt.ylim([low - 0.1 * (high - low), high + 0.1 * (high - low)])
    plt.xticks(range(len(datos)), datos.index.tolist(), rotation=0)
    plt.savefig(out_path + str(file_name) + "_bars.png", dpi=150)
    plt.show()

    datos[columns].plot(style='.-', title=figure_title)
    plt.legend(loc='lower left', bbox_to_anchor=(1.0, 0.0))
    plt.xticks(range(len(datos)), datos.index.tolist(), rotation=0)
    plt.savefig(out_path + str(file_name) + "_lines.png", dpi=150)
    plt.show()


def ajuste_parametrico(base_path, sub_paths, out_path, parametro, *args):

    # if sub_paths is "":
    #     sub_paths=get_subpaths(base_path, key=sub_paths_type)
    print(sub_paths)

    # HACER MEDIAS Y MOSTRAR DATOS
    datos, datos_ordenados = calcular_datos(base_path, sub_paths)

    if not path.exists(out_path):
        makedirs(out_path)

    datos.to_excel(out_path + parametro + ".xlsx")
    datos.to_csv(out_path + parametro + ".csv", sep=";", encoding="UTF-8")

    # REPRESENTAR GRAFICAMENTE
    if args:
        for plotter in args:
            if plotter["ordenados"]:
                datos_empleados = datos_ordenados
                nombre = "Datos ordenados"
            else:
                datos_empleados = datos
            nombre = "Datos no ordenados"

            if plotter["multiple"]:
                multiple_empleado = True
                nombre = nombre + " multiple"
            else:
                multiple_empleado = False

            dibujar_datos(datos_empleados, out_path, file_name=nombre, figure_title=parametro,
                          multiple=multiple_empleado)
    else:
        dibujar_datos(datos, out_path, file_name="Datos no ordenados", figure_title=parametro, multiple=False)
        # dibujar_datos(datos, out_path, file_name="Datos no ordenados multiple", figure_title=parametro, multiple=True)
        dibujar_datos(datos_ordenados, out_path, figure_title=parametro, file_name="Datos ordenados por mejor fitness")

def get_subpaths(path, key=str.lower):
    return sorted(next(walk(path))[1], key=key)