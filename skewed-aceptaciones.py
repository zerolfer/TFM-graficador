import pandas as pd


df = pd.read_csv(
    "C:\\Users\\Administrador\\Documents\\Proyecto-Salomon\\resultados\\Caso1Id1m-01-01-2019\\VNS\\Trazas\\output1.csv",
    sep=';', skiprows=[0],
    names=["iteracion", "tiempo (ms)", "fitness total", "fitness 1", "fitness 2", "fitness 3", "fitness 4", "tamaño",
           "porcentajeMejora", "vecindad", "mejor fitness", "distancia"])

df2 = df.copy(deep=True)
df2.apply(lambda row: round(float(row["mejor fitness"]), 6), axis=1)
df2['diferentes'] = df.apply(lambda row: row["fitness total"] != row["mejor fitness"], axis=1)

print(df2[["fitness total", "mejor fitness", "diferentes"]].to_string())
