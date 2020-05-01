import os

import pandas as pd


def main():
    base_path = "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\ajuste-parametrico\\"
    casos = [
        # "caso1",
        "caso3\\",
        "caso4\\",
        "caso5\\",
        "caso6\\"
    ]
    path = "primera-iteracion\\3-Vecindades\\TipoEntornos\\"
    parametros = ["determinista\\", "probabilistico\\"]

    base_output_path = "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\tipo-entornos\\"

    for caso in casos:
        print("[EJECUTANDO] caso: " + caso)
        for parametro in parametros:
            print("\t\t |_ " + "parametro: " + parametro)

            # paths
            current_path = base_path + caso + path + parametro
            nombre_fichero = "output1" if "determinista" in parametro else "output2"
            output_dir = base_output_path + caso + "ejecuciones-medias\\"

            # medias
            df_mean = calcular_medias(current_path)

            # output
            if not os.path.exists(output_dir): os.makedirs(output_dir)
            df_mean.to_csv(output_dir + nombre_fichero + ".csv", sep=";", index=False)


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
    # df_concat.head()


if __name__ == "para_caso1":
    full_path = "C:\\Users\\GL753V\\OneDrive - Universidad Politécnica de Madrid\\· TFM\\proyecto\\ajuste-parametrico\\segunda-itearacion\\3-Vecindades\\TipoEntornos\\"
    parametros = ["determinista\\", "probabilistico\\"]
    base_output_path = "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\ejecuciones\\tipo-entornos\\caso1\\ejecuciones-medias"

    for parametro in parametros:
        current_path = full_path + parametro
        df_mean = calcular_medias(current_path)

        nombre_fichero = "output1" if "determinista" in parametro else "output2"
        output_dir = base_output_path + "\\"
        if not os.path.exists(output_dir): os.makedirs(output_dir)
        df_mean.to_csv(output_dir + nombre_fichero + ".csv", sep=";", index=False)

if __name__ == "__main__":
    main()
