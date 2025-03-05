import pandas as pd
import numpy as np
import re
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.community import greedy_modularity_communities



def preprocess_df(path_and_name,limit_df_value:int=None):
   
   df = pd.read_csv(path_and_name)
   drops = ['DOI','Abstract','Cited References']
   df_dropped = df.dropna(subset=drops)
   if limit_df_value is not None:
      df_dropped = df_dropped.head(limit_df_value)
   df_dropped['DOI'] = df_dropped['DOI'].str.upper()
   df_dropped = df_dropped.drop_duplicates(subset='DOI')
   
   return df_dropped



def articles_to_dict(df,remove_unknow_articles:bool=False,print_progress:bool = False, 
                     save_csv:bool=False,save_name:str="any"):
    dictionary = {}
    index = df.index
    df_dois = "DOI " + df['DOI'].str.upper()
    df_dois_list = list(df_dois)
    max_index = index[-1]
    for i in index:
        if print_progress:
            print(f"Progresso:{i} de {max_index}",end='\r')
            
        cited_references = df['Cited References'][i]
        collected_dois = re.findall(r'DOI [^;]+;', cited_references)
        
        collected_dois_correction = []
        for j in collected_dois:
            doi = j.removesuffix(";").upper()
            if "DOI [" in doi:
                doi_list_str = doi.removeprefix("DOI [").replace(']','').replace(',','').split()                
                doi = f"DOI {doi_list_str[0]}"
                
            if remove_unknow_articles:
                if doi in df_dois_list:
                    collected_dois_correction.append(doi)
                else:
                    continue
                
            if not remove_unknow_articles:
                collected_dois_correction.append(doi)
        
        doi_key = df_dois[i]
        dictionary[doi_key] = collected_dois_correction
    
    if save_csv:
        save_df = pd.DataFrame.from_dict(dictionary, orient='index').transpose()
        save_df.to_csv(f"{save_name}.csv", index=False)

        if print_progress:
            print("\n Save concluído")
    
    return dictionary



def open_dict_from_csv(path_and_name:str):
    
    dictionary = pd.read_csv(path_and_name,index_col=False).to_dict(orient="list")
    dictionary_clean = {key: [value for value in values if pd.notna(value)] for key, values in dictionary.items()}

    return dictionary_clean



def find_groups(graph,dictionary:dict,use_modularity:bool=False,save_csv:bool=False,
                save_name:str='any',print_progress:bool=False,n_step_progress:int=1):
    
    if not use_modularity:
        connections = list(nx.connected_components(graph))
        
    if use_modularity:
        if print_progress:
            print("Modularização Iniciada")
        connections = list(nx.community.louvain_communities(graph))
        if print_progress:
            print("Modularização Concluída")
        
    groups_dictionary = {}
    all_cited_articles = list(dictionary.keys())

    if print_progress:
        print("Processo inicial feito")


    for i,group in enumerate(connections):
        articles = []
        for j,article in enumerate(group):
            if article in all_cited_articles:
                articles.append(article)
            if print_progress and (j+1)%n_step_progress == 0:
                print(f"Progresso: {j+1} de {len(group)}, em {i+1} de {len(connections)}",end='\r')
        if print_progress:
            if not use_modularity:
                print(f"\n Tamanho do grupo:{len(articles)}")
            if use_modularity:
                print(f"\n Tamanho da comunidade:{len(articles)}")
            
        if not use_modularity:
            groups_dictionary[f"Grupo {i+1}"] = articles
        if use_modularity:
            groups_dictionary[f"Comunidade {i+1}"] = articles

    if save_csv:
        if print_progress:
            print("Saving dataset")
        df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in groups_dictionary.items()]))
        df.to_csv(f'{save_name}.csv', index=False, encoding='utf-8')


    return groups_dictionary



def plot_graph(graph,dictionary,node_size,width):
   
    isolated_nodes = set(graph.nodes) - set(dictionary.keys())

    pos = nx.spring_layout(graph, seed=20)

    # nós isolados (vermelhos)
    nx.draw_networkx_nodes(graph, pos, nodelist=isolated_nodes, node_color='red', node_size=node_size, edgecolors='black',
                        label="Artigos fora da amostra")

    # nós conectados (azuis)
    nx.draw_networkx_nodes(graph, pos, nodelist=set(graph.nodes) - isolated_nodes, node_color='skyblue', node_size=node_size, edgecolors='black',
                        label="Artigos presentes na amostra")

    nx.draw_networkx_edges(graph, pos,width=width)

    plt.axis("off") 
    plt.legend()
    plt.show()
    
    
    
def encontrar_grupos_isolados(dictionary,graph,labels_plot=False):
    
    componentes = list(nx.connected_components(graph))

    pos = nx.spring_layout(graph, seed=20)
    colors = [
    'red', 'blue', 'green', 'orange', 'purple', 'pink', 'cyan', 'yellow',
    'brown', 'gray', 'black', 'lime', 'magenta', 'teal', 'navy',
    'gold', 'indigo', 'violet', 'turquoise', 'salmon', 'maroon',
    'olive', 'chocolate', 'orchid', 'plum', 'slateblue', 'crimson', 'darkgreen',
    'darkblue', 'darkred', 'darkorange', 'deeppink', 'deepskyblue', 'dodgerblue',
    'greenyellow', 'lightblue', 'lightcoral', 'lightgreen', 'lightpink',
    'lightsalmon', 'lightseagreen', 'lightskyblue', 'lime']
    plt.figure(figsize=(8, 6))

    for i, grupo in enumerate(componentes):
        nx.draw_networkx_nodes(graph, pos, nodelist=grupo, node_color=colors[i % len(colors)], label=f'Grupo {i+1}', node_size=200)

    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    
    isolated_nodes = set(graph.nodes) - set(dictionary.keys())


    nx.draw_networkx_nodes(graph, pos, nodelist=isolated_nodes, node_color='red', node_size=20, edgecolors='black',
                        label="Artigos fora da amostra")

    nx.draw_networkx_nodes(graph, pos, nodelist=set(graph.nodes) - isolated_nodes, node_color='skyblue', node_size=20, edgecolors='black',
                        label="Artigos presentes na amostra")
    nx.draw_networkx_edges(graph, pos)
    
    if labels_plot:
        plt.legend()
    plt.show()
    


def identify_group(df:pd.core.frame.DataFrame,df_groups:pd.core.frame.DataFrame):
   
    df_dois = list("DOI " + df['DOI'].str.upper())
    column_identify_group = [0]*len(df_dois)
    columns = list(df_groups.columns)


    for column in columns:
        list_dois = df_groups[column].dropna()
        max = len(list_dois)
        for i,doi in enumerate(list_dois):
            print(f"{i} de {max} em {column}              ",end='\r')
            posicao = df_dois.index(doi)
            column_identify_group[posicao] = column
   

    df_copy = df.copy()

    df_copy['Group'] = column_identify_group

    return df_copy



def mean_times_cited(df:pd.core.frame.DataFrame,groups:list,
                     save_excel=False,save_name="any"):
   
   medias = []
   maximos = []
   minimos = []
   desvios_padrao = []
   quantidades = []

   for group in groups:
      filtro = df['Group'] == group
      df_filtrado = df[filtro]['Times Cited, All Databases']
      medias.append(df_filtrado.mean())
      desvios_padrao.append(df_filtrado.std())
      quantidades.append(len(df_filtrado))
      maximos.append(df_filtrado.max())
      minimos.append(df_filtrado.min())

      
   means_df = pd.DataFrame()
   means_df['Grupo'] = groups
   means_df['Média de Vezes Citados'] = medias
   means_df['Máximo de Vezes Citados'] = maximos
   means_df['Mínimo de Vezes Citados'] = minimos
   means_df['Exemplares'] = quantidades
   means_df['Devios'] = desvios_padrao

   if save_excel:
      means_df.to_excel(save_name)
   return means_df