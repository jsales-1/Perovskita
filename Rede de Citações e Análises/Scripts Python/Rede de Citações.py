# %%
import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
from functions import *

# %%
path = "../../Dataset/df_final_oficial_concatenado_com_referencias.csv"
df = preprocess_df(path)

# %%
dicionario = articles_to_dict(df,remove_unknow_articles=True,
                              print_progress = True,save_csv=False,
                              save_name="Dicionário_sem_artigos_desconhecidos")
grafo = nx.Graph(dicionario)

# %%
grupos = find_groups(grafo,dicionario,use_modularity=False,save_csv=True,
                     save_name="Grupos_sem_artigos_desconhecidos",
                     print_progress=True,n_step_progress=1000)

# %%
#plot_graph(grafo,dicionario)

# %%
#encontrar_grupos_isolados(dicionario,grafo)


