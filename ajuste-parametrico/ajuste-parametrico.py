import pandas as pd
from os import listdir, path, makedirs
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


def dibujar_datos(datos, out_path, title="", multiple=True):
    columns = ["fitness total", "fitness 1", "fitness 2", "fitness 3", "fitness 4"]
    if not multiple:
        columns = ["fitness total"]
    ax = datos[columns].plot.bar(title=title)
    for p in ax.patches:
        ax.annotate(str(round(p.get_height(), 3)),
                    (p.get_x() * 1.005, p.get_height() * 1.005))
    plt.legend(loc='lower left', bbox_to_anchor=(1.0, 0.0))
    plt.savefig(out_path+str(title) + "_bars.png", dpi=150)
    plt.show()

    datos[columns].plot(style='.-', title=title)
    plt.legend(loc='lower left', bbox_to_anchor=(1.0, 0.0))
    plt.savefig(out_path + str(title) + "_lines.png", dpi=150)
    plt.show()


def ajuste_parametrico(base_path, sub_paths, out_path, parametro):
    # HACER MEDIAS Y MOSTRAR DATOS
    datos, datos_ordenados = calcular_datos(base_path, sub_paths)

    if not path.exists(out_path):
        makedirs(out_path)

    datos.to_excel(out_path + parametro + ".xlsx")
    datos.to_csv(out_path + parametro + ".csv", sep=";", encoding="UTF-8")

    # REPRESENTAR GRAFICAMENTE
    dibujar_datos(datos,           out_path, title="Datos no ordenados", multiple=False)
    dibujar_datos(datos_ordenados, out_path, title="Datos ordenados por mejor fitness")
