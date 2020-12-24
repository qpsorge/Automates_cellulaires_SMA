import numpy as np
import pandas as pd
import re
print(os.listdir())

EXPLORE = False
#Traitement du fichier json
if(EXPLORE):
    with open('C:/Users/asus/simulation_ac_feu.json','r') as doc:
        json_results= doc.read()
        json_results=json_results.replace('{','')
        json_results=json_results.replace('}','')
        json_results=json_results.replace('"','')
        split2t     = json_results.split(",")
        split_total = [x.split(": ") for x in split2t]
        split_hyperparams   = [re.findall(r'\d+', x[0]) for x in split_total]
        split_percolation_threshold = [[x[1]] for x in split_total]
        results = [split_hyperparams[i]+split_percolation_threshold[i] for i in range(min(len(split_hyperparams),len(split_percolation_threshold)))]
    print(split_hyperparams[:5])
    print(split_percolation_threshold[:5])
    columns    = ["neighbor_burning","neighbor_birth","alea_burning","Green_proportion"]
    df_results = pd.DataFrame(results,columns=columns)
    df_results["Green_proportion"] = [float(x) for x in df_results["Green_proportion"]]

    df_results.to_csv("hyperparameters_gridsearch_percolation_threshold.csv")

else :
    columns    = ["neighbor_burning","neighbor_birth","alea_burning","Green_proportion"]
    df_results = pd.read_csv("hyperparameters_gridsearch_percolation_threshold.csv", columns=columns)
    percolation_threshold = 0.99
    print(df_results[df_results["Green_proportion"]>percolation_threshold])
    