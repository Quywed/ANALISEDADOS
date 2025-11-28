import os
import pandas as pd
import requests
#import kaggle as kg


"""
def download_file_if_not_exists(file_path: str, dataset_name: str):

    Checks if the given file exists. If not, downloads it from Kaggle.
   
    if not os.path.exists(file_path):
        print(f"Ficheiro não foi encontrado: {file_path}. A descarregar o dataset...")

        try:
            kg.api.dataset_download_files(dataset_name, path='./', unzip=True)
            print("Download concluído com sucesso!")
        except Exception as e:
            print(f"Erro ao descarregar: {e}")
    else:
        print(f"Ficheiro {file_path} já existe. Ignorando o download.")
 """

def format_runtime(seconds):
    """
    Converte runtime em segundos para formato 'Xh YYm'.
    """
    if pd.isnull(seconds):
        return None
    minutes = int(seconds // 60)
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins:02d}m"


def format_currency(x):
    """
    Formata valores numéricos como moeda, ex: 1.000.000 $.
    """
    if pd.isnull(x) or x == 0:
        return "0 $"
    return f"{x:,.0f}".replace(",", ".") + " $"

