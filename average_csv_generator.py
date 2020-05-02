import os

import pandas as pd

''' 
    ESQUELETO: [ TODOS LOS PATHS DEBEN TERMINAR CON \\ ]
    
        "<NOMBRE_IDENTIFICATIVO>": {
        "base_path": "<Lugar donde se encuentran los casos>\\", # debe terminar en \\ al igual que todos los demás
        "casos": [
            "<caso1>\\"
            "<caso2>\\",
            
            "<casoN>\\",
        ],
        "path": "<subpath hacia los parámetros>\\",
        "parametros": ["param1\\", "param2\\",      "paramN\\"],
        "base_output_path": "<ubicación de salida. Los ficheros se llamarán outputX.csv donde X = parametros[i]>"
    },

'''
params = {

    "determinista_vs_probabilistico_caso1": {
        "base_path": "C:\\Users\\GL753V\\OneDrive - Universidad Politécnica de Madrid\\· TFM\\proyecto\\ajuste-parametrico\\",
        "casos": [""],
        "path": "segunda-itearacion\\3-Vecindades\\TipoEntornos\\",
        "parametros": ["determinista\\", "probabilistico\\"],
        "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\tipo-entornos\\"
    },

    "determinista_vs_probabilistico": {
        "base_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "casos": [
            "caso3\\"
            "caso4\\",
            "caso5\\",
            "caso6\\"
        ],
        "path": "primera-iteracion\\3-Vecindades\\TipoEntornos\\",
        "parametros": ["determinista\\", "probabilistico\\"],
        "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\tipo-entornos\\"
    },

    "comparativa_alphas_caso3": {
        "base_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "casos": [
            "caso3\\"
        ],
        "path": "primera-iteracion\\1-TipoVNS\\SVNS\\slots\\",
        "parametros": [
            "0.5\\",
            "1.0\\",
            "2.0\\",
            "5.0\\",
            "10.0\\"
        ],
        "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\comparativa-alphas\\",
    },

    "comparativa_alphas_caso4": {
        "base_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "casos": [
            "caso4\\"
        ],
        "path": "primera-iteracion\\1-TipoVNS\\SVNS\\fitness\\",
        "parametros": [
            "-0.5\\",
            "0.5\\",
            "0.25\\",
            "1.0\\",
            "1.5\\",
            "1.25\\",
            "2.0\\",
            "5.0\\",
            "10.0\\"
        ],
        "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\comparativa-alphas\\",
    },
    "comparativa-tipos-vns": {
        "base_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
        "casos": [
            "caso3\\",
            "caso4\\",
            "caso6\\",
            "caso7\\"
        ],
        "path": "primera-iteracion\\1-TipoVNS\\",
        "parametros": ["VND\\", "RVNS\\", "BVNS\\", "GVNS\\", "SVNS-optimo\\"],
        "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\"
    },

    # "comparativa-tipos-vns-caso3": {
    #     "base_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\",
    #     "casos": ["caso3\\"],
    #     "path": "primera-iteracion\\1-TipoVNS\\",
    #     "parametros": ["SVNS\\slots\\0.5\\"],
    #     "base_output_path": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\"
    # }
}


def compute_averages():
    ids = ["comparativa-tipos-vns"]

    for id in ids:
        print("[EJECUTANDO {0}]".format(id))
        for caso in params[id]["casos"]:
            print(" |_\tcaso: {0}\t|\tDestino: {1}{2}ejecuciones-medias\\".format(caso, params[id][
                "base_output_path"], caso))
            for idx, parametro in enumerate(params[id]["parametros"]):
                print(" |\t\t\t |_ " + "parametro: " + parametro, end='')

                # paths
                current_path = params[id]["base_path"] + caso + params[id]["path"] + parametro
                if os.path.exists(current_path):
                    nombre_fichero = "output" + str(idx + 1)
                    output_dir = params[id]["base_output_path"] + caso + "ejecuciones-medias\\"

                    # medias
                    df_mean = calcular_medias(current_path)

                    # output
                    if not os.path.exists(output_dir): os.makedirs(output_dir)
                    df_mean.to_csv(output_dir + nombre_fichero + ".csv", sep=";", index=False)

                    print()
                else:
                    print(" <-- NO EXISTE EL DIRECTORIO " + current_path)
            # print()
        print(" |_ [END {0}]".format(id))


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


# if __name__ == "para_caso1":
#     full_path = "C:\\Users\\GL753V\\OneDrive - Universidad Politécnica de Madrid\\· TFM\\proyecto\\ajuste-parametrico\\segunda-itearacion\\3-Vecindades\\TipoEntornos\\"
#     parametros = ["determinista\\", "probabilistico\\"]
#     base_output_path = "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\tipo-entornos\\caso1\\ejecuciones-medias"
#
#     for parametro in parametros:
#         current_path = full_path + parametro
#         df_mean = calcular_medias(current_path)
#
#         nombre_fichero = "output1" if "determinista" in parametro else "output2"
#         output_dir = base_output_path + "\\"
#         if not os.path.exists(output_dir): os.makedirs(output_dir)
#         df_mean.to_csv(output_dir + nombre_fichero + ".csv", sep=";", index=False)
#


''' 
    ESQUELETO: [ TODOS LOS PATHS DEBEN TERMINAR CON \\ ]

        "<NOMBRE_IDENTIFICATIVO>": {
        "base_path": "<Lugar donde se encuentran los casos>\\", # debe terminar en \\ al igual que todos los demás
        "casos": [
            "<caso1>\\"
            "<caso2>\\",

            "<casoN>\\",
        ],
        "path": "<subpath hacia los parámetros>\\",
        "parametros": ["param1\\", "param2\\",      "paramN\\"],
        "base_output_path": "<ubicación de salida. Los ficheros se llamarán outputX.csv donde X = parametros[i]>"
    },

'''


def copy_one_execution_files():
    params_copies = {
        "comparativa-alphas-caso3": {
            "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\caso",
            "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS\\slots\\",
            "casos": ["3"],
            "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-alphas\\caso",
            "destino2": "\\1-ejecucion\\",
        },
        "comparativa-alphas-caso4": {
            "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\caso",
            "base2": "\\primera-iteracion\\1-TipoVNS\\SVNS\\fitness\\",
            "casos": ["4"],
            "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-alphas\\caso",
            "destino2": "\\1-ejecucion\\",
        },
        "comparativa-tipos-vns-caso3": {
            "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\caso",
            "base2": "\\primera-iteracion\\1-TipoVNS\\",
            "casos": ["3"],
            "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\caso",
            "destino2": "\\1-ejecucion\\",
            "names": {
                "VND": "1",
                "RVNS": "2",
                "BVNS": "3",
                "GVNS": "4",
                "SVNS-optimo": "5"
            }
        },
        "comparativa-tipos-vns": {
            "base1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\caso",
            "base2": "\\primera-iteracion\\1-TipoVNS\\",
            "casos": ["3", "4", "6", "7"],
            "destino1": "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\caso",
            "destino2": "\\1-ejecucion\\",
            "names": {
                "VND": "1",
                "RVNS": "2",
                "BVNS": "3",
                "GVNS": "4",
                "SVNS-optimo": "5"
            }
        }

    }
    from shutil import copyfile
    ids = ["comparativa-tipos-vns"]
    for id in ids:
        for caso in params_copies[id]["casos"]:
            base = params_copies[id]["base1"] + caso + params_copies[id]["base2"]
            destino = params_copies[id]["destino1"] + caso + params_copies[id]["destino2"]
            names = params_copies[id]["names"]
            print("Moviendo datos de {3}: caso {2}\n\tdesde: {0}\n\thasta: {1}\n... ".format(base, destino, caso, id),
                  end='')

            if not os.path.exists(destino): os.makedirs(destino)

            # for i, sub in enumerate(os.listdir(base)):
            #     if "log" in sub or "SVNS" in sub: continue
            #     copyfile(base + sub + '\\output1.csv',
            #              "{0}output{1}.csv".format(
            #                  destino, str(i + 1))
            #              )
            for i, sub in enumerate(os.listdir(base)):
                if "log" in sub: continue

                # si no está definido un mapa de nombres, se hace en orden
                if not names:
                    copyfile(base + sub + '\\output1.csv',
                             "{0}output{1}.csv".format(
                                 destino, str(i + 1))
                             )
                elif sub in names:
                    copyfile(base + sub + '\\output1.csv',
                             '{0}output{1}.csv'.format(destino, names[sub]))

            print("Hecho!\n")


if __name__ == "__main__":
    copy_one_execution_files()
    compute_averages()
