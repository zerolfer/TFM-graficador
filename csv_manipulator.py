import pandas as pd


def rellenar_faltantes():
    path1 = "C:\\Users\\Administrador\\Documents\\TFM-graficador\\ejecuciones\\entornos probabilisticos\\2_6-11-2019\\"
    casos = ["Caso1Id1m-01-01-2019", "Caso3Id2m-01-01-2019", "Caso4Id3t-16-01-2019", "Caso5Id5t-16-01-2019",
             "Caso6Id4t-14-01-2019", "Caso7Id6t-19-10-2018", "Caso8Id0m-13-09-2018", "Caso9Id1m-13-09-2018"]
    path2 = "\\VNS\\Trazas\\"
    ficheros = ["output1.csv", "output2.csv", "output3.csv", "output4.csv"]

    for caso in casos:
        for fichero in ficheros:
            print("[EJECUTANDO] caso: " + caso + " | " + "fichero: " + fichero)
            df = pd.read_csv(path1 + caso + path2 + fichero,
                             sep=';', skiprows=[0],
                             names=["iteracion", "tiempo (ms)", "fitness total",
                                    "fitness 1", "fitness 2", "fitness 3", "fitness 4", "tamaño",
                                    "porcentajeMejora", "vecindad", "mejor fitness", "distancia"])

            df["mejor fitness"] = df["fitness total"]
            df["distancia"] = -1

            df.to_csv(path1 + caso + path2 + fichero, sep=";", index=False)
        print()


def cambiar_orden_columnas(path, medias=False):
    if not medias:
        names = ["iteracion", "tiempo (ms)", "fitness total", "fitness 1", "fitness 2", "fitness 3",
                 "fitness 4", "tamaño", "porcentajeMejora", "vecindad", "mejor fitness",
                 "distancia", "restricciones incumplidas", "reinicios"]
        names_alterades = ["iteracion", "tiempo (ms)", "mejor fitness", "fitness 1", "fitness 2", "fitness 3",
                           "fitness 4", "tamaño", "porcentajeMejora", "vecindad", "fitness total",
                           "distancia", "restricciones incumplidas", "reinicios"]

    else:
        names = ["iteracion", "tiempo (ms)", "fitness total", "fitness 1", "fitness 2", "fitness 3",
                 "fitness 4", "tamaño", "porcentajeMejora", "mejor fitness",
                 "distancia", "restricciones incumplidas", "reinicios"]  # para ejecuciones medias
        names_alterades = ["iteracion", "tiempo (ms)", "mejor fitness", "fitness 1", "fitness 2", "fitness 3",
                           "fitness 4", "tamaño", "porcentajeMejora", "fitness total",
                           "distancia", "restricciones incumplidas", "reinicios"]  # para ejecuciones medias

    print(path)
    df = pd.read_csv(path + 'output5.csv', sep=';', skiprows=[0], names=names)  # para ejecuciones medias

    cols = df.columns.tolist()
    print(cols)
    print(names_alterades)
    df = df[names_alterades]

    df.to_csv(path + "output6.csv", sep=';', index=False)
    print()

if __name__ == "__main__":
    cambiar_orden_columnas(
        "C:\\Users\\GL753V\\Documents\\Projects\\TFM-graficador\\graficas\\comparativa-tipos-vns\\caso7")
