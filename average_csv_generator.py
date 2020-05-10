import os

import pandas as pd
from shutil import copyfile
from csv_manipulator import cambiar_orden_columnas


def template(ids, _accion, _nombre):
    for id in ids:
        print("[{1}] [EJECUTANDO {0}]".format(id, _nombre))
        for caso in params[id]["casos"]:

            base = params[id]["base1"] + caso + params[id]["base2"]
            output_dir = "{0}{1}\\{2}{3}".format(params[id]["destino1"], caso, _nombre, params[id]["destino2"])

            print(" |_\tcaso: {0}\t|\tDestino: {1}".format(caso, output_dir))

            # si no está definido un mapa de nombres, se hace en orden
            if not "parametros" in params[id]:
                for idx, parametro in enumerate(os.listdir(base)):
                    if "log" in parametro: continue
                    _accion(base, output_dir, idx, parametro)

            else:
                names = params[id]["parametros"]
                for idx, parametro in enumerate(names):
                    _accion(base, output_dir, idx, parametro)

        print(" |_ [END {0}]".format(id))


def accion_calcular_medias(base, output_dir, idx, parametro):
    print(" |\t\t\t |_ " + "parametro: " + parametro, end='')

    # paths
    current_path = base + parametro + "\\"
    if os.path.exists(current_path):

        # medias
        df_mean = calcular_medias(current_path)

        # output
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        df_mean.to_csv("{0}output{1}.csv".format(output_dir, str(idx + 1)),
                       sep=";", index=False)
        print()
    else:
        print(" <-- NO EXISTE EL DIRECTORIO " + current_path)


def calcular_medias(current_path):
    dfs = []
    for file in os.listdir(current_path):
        if "log" in file: continue
        dfs.append(pd.read_csv(current_path + file,
                               sep=';', skiprows=[0],
                               names=['iteracion', 'tiempo', 'fitness total',
                                      'fitness 1', 'fitness 2', 'fitness 3', 'fitness 4',
                                      'tamaño', 'porcentaje mejora', 'vecindad',
                                      "mejor fitness", "distancia", "restricciones incumplidas", "reinicios"]
                               )
                   )
    df_concat = dfs[0]
    for i in range(1, len(dfs)): df_concat = pd.concat((df_concat, dfs[i]))
    df_groupby = df_concat.groupby(df_concat.index)
    return df_groupby.mean()


def accion_copiar_ficheros_una_ejecucion(base, output_dir, idx, parametro):
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    copyfile(base + parametro + '\\output1.csv',
             '{0}output{1}.csv'.format(output_dir, str(idx + 1)))


def copy_one_execution_files(ids):
    template(ids, accion_copiar_ficheros_una_ejecucion, subpath_1_ejecucion)


def compute_averages(ids):
    template(ids, accion_calcular_medias, subpath_medias)


params = {
    "determinista_vs_probabilistico_caso1": {
        "base1": "C:\\Users\\GL753V\\OneDrive - Universidad Politécnica de Madrid\\· TFM\\proyecto\\ajuste-parametrico\\",
        "base2": "\\segunda-itearacion\\3-Vecindades\\TipoEntornos\\",
        "casos": ["."],  # Se añadirá entre los paths 1 y 2 tanto base como destino
        "parametros": ["determinista", "probabilistico"],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\tipo-entornos\\",
        "destino2": "\\"
    },

    "determinista_vs_probabilistico": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\3-Vecindades\\TipoEntornos\\",
        "casos": [
            # "caso3"
            # "caso4",
            # "caso5",
            # "caso6",
            "caso7",
            "caso8",
            "caso9"
        ],  # Se añadirá entre los paths 1 y 2 tanto base como output
        "parametros": ["determinista", "probabilistico"],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\tipo-entornos\\",
        "destino2": "\\"

    },

    "svns-caso3,4,8,9-alphas-comparator": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS\\slots\\",
        "casos": [
            "caso3",
            "caso4",
            "caso8",
            "caso9"],  # Se añadirá entre los paths 1 y 2 tanto base como output
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-alphas\\",
        "destino2": "\\",
    },

    "comparativa_alphas_caso3": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS\\slots\\",
        "casos": [
            "caso3"
        ],  # Se añadirá entre los paths 1 y 2 tanto base como output
        "parametros": [
            "0.5",
            "1.0",
            "2.0",
            "5.0",
            "10.0"
        ],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-alphas\\",
        "destino2": "\\"
    },

    "comparativa_alphas_caso4": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS\\fitness\\",
        "casos": [
            "caso4"
        ],  # Se añadirá entre los paths 1 y 2 tanto base como output
        "parametros": [
            "-0.5",
            "0.5",
            "0.25",
            "1.0",
            "1.5",
            "1.25",
            "2.0",
            "5.0",
            "10.0"
        ],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-alphas\\",
        "destino2": "\\..\\ejecuciones-medias\\"
    },
    "comparativa-tipos-vns": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\1-TipoVNS\\",
        "casos": [
            "caso3",
            "caso4",
            "caso6",
            "caso7",
            "caso8",
            "caso9"
        ],  # Se añadirá entre los paths 1 y 2 tanto base como output
        "parametros": ["VND", "RVNS", "BVNS", "GVNS", "SVNS-optimo"],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\",
        "destino2": "\\"
    },

    "svns-oscilante": {
        "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS-optimo\\",
        "casos": [
            "caso3",
            "caso4",
            "caso6",
            "caso7",
            "caso8"
        ],
        "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\svns-oscilante\\",
        "destino2": "\\",
    },

}

subpath_1_ejecucion = "1-ejecucion"
subpath_medias = "ejecuciones-medias"

if __name__ == "__main__":
    ids = ["determinista_vs_probabilistico"]

    copy_one_execution_files(ids)
    compute_averages(ids)


    # for id in ids:
    #     for caso in params[id]["casos"]:
    #         path = params[id]["destino1"] + caso + params[id]["destino2"] + "\\"
    #
    #         cambiar_orden_columnas(path + subpath_1_ejecucion + "\\", medias=False)
    #         cambiar_orden_columnas(path + subpath_medias      + "\\", medias=True)
