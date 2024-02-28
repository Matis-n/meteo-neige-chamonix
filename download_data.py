import json
import pandas as pd
import numpy as np
import os
import requests
import gzip
import shutil
import datetime

folder_gz = "data_gz"
folder_csv = "data_csv"

urls= dict()
urls["74_1949_RR_T_V"] = "https://www.data.gouv.fr/fr/datasets/r/96a9cf9d-e307-4311-b281-80e525216d4a"
urls["74_1949_other"] = "https://www.data.gouv.fr/fr/datasets/r/0fcadd70-279e-463c-8f9e-bb7493da68cd"
urls["74_2022_RR_T_V"] = "https://www.data.gouv.fr/fr/datasets/r/23a368d7-59e3-488d-afb7-3890f972dcd7"
urls["74_2022_other"] = "https://www.data.gouv.fr/fr/datasets/r/9096f970-f711-4db5-9f22-77618cb50729"
urls["74_2024_RR_T_V"] = "https://www.data.gouv.fr/fr/datasets/r/212e4fb5-e4fd-4565-af91-1fd340b23a6c"
urls["74_2024_other"] = "https://www.data.gouv.fr/fr/datasets/r/2fd676a6-c8e2-47df-adb1-974a60a5482b"

# code_chamonix = "74056001"

def convert_to_date(chaine):
    return pd.to_datetime(str(chaine), format='%Y%m%d', errors='coerce')

def download_file(url, filename):
    file= os.path.join(folder_gz, filename) + '.gz'
    print('Téléchargement: ', file)
    response = requests.get(url)
    if response.status_code == 200:
        with open(file, 'wb') as f:
            f.write(response.content)
    else:
        print("Fichier d'archive non présent à l'url habituelle: ", file)

def decompress_gz(filename):
    file= os.path.join(folder_gz, filename) + '.gz'
    
    if os.path.exists(file):
        with gzip.open(file, 'rb') as f_in:
            file= os.path.join(folder_csv, filename) 
            print('Décompression', file)
            with open(file, 'wb') as f_out:
                f_out.write(f_in.read())
    else:
        print("Fichier d'archive non trouvé: ", file)
        print("Téléchargez l'archive GZ, manuellement ou en modifiant la variable 'download', puis relancez le script.")

def read_csv(filename):
    file= os.path.join(folder_csv, filename)
    if os.path.exists(file):
        print('Lecture: ', file)
        df= pd.read_csv(file, header=0, sep=";", dtype={"NUM_POSTE":str, 'AAAAMMJJ':str}, parse_dates=['AAAAMMJJ'], date_parser= convert_to_date)
    else:
        print("Fichier CSV non trouvé: ", file)
        print("Téléchargez l'archive GZ, manuellement ou en modifiant la variable 'download', puis relancez le script")
    return df

if __name__ == "__main__":

    if not os.path.exists(folder_gz):
        os.makedirs(folder_gz)
    if not os.path.exists(folder_csv):
        os.makedirs(folder_csv)

    # Téléchargement/décompression/lecture des fichiers dans une boucle sur les départements (urls tirées du dictionnaire 'urls')
    i = 0
    departements= ["74"]
    years = ["2022", "2024"]
    template_start = "postesEnService_"
    template_end = ".csv"

    download = True

    for departement in departements:
        for year in years:
            # On récupère l'url
            key = departement + "_" + year + "_RR_T_V"
            url = urls[key]
            # Formation du nom du fichier à partir du template et du numéro de département
            filename = f"{template_start}{departement}{year}RR_T_V{template_end}"
            if download:
                download_file(url, filename)
                decompress_gz(filename)
            # Lecture du fichier CSV dans un dataframe pandas
            df_departement= read_csv(filename)
            if i == 0: # pour le premier département, initialisation du dataframe final df       
                df = df_departement
                i= i+1
            else:  # sinon concaténation du département suivant 
                df= pd.concat([df, df_departement]) 
    df.to_csv(f"{folder_csv}/{template_start}{departement}RR_T_V{template_end}", sep=";", index=False) 

    i = 0
    for departement in departements:
        for year in years:
            # On récupère l'url
            key = departement + "_" + year + "other"
            url = urls[key]
            # Formation du nom du fichier à partir du template et du numéro de département
            filename = f"{template_start}{departement}{year}other{template_end}"
            if download:
                download_file(url, filename)
                decompress_gz(filename)
            # Lecture du fichier CSV dans un dataframe pandas
            df_departement= read_csv(filename)
            if i == 0: # pour le premier département, initialisation du dataframe final df       
                df = df_departement
                i= i+1
            else:  # sinon concaténation du département suivant 
                df= pd.concat([df, df_departement])  
    df.to_csv(f"{folder_csv}/{template_start}{departement}RR_T_V{template_end}", sep=";", index=False) 

            
              
