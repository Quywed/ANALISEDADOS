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

def get_director(imdb_id: str):
    """
    Retorna o(s) diretor(es) de um filme usando a nova API IMDb.
    """
    if pd.isna(imdb_id) or not str(imdb_id).startswith("tt"):
        return "Invalid IMDb ID"

    url = f'https://api.imdbapi.dev/titles/{imdb_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        return f"HTTP error: {e}"

    data = response.json()

    if 'directors' not in data or not data['directors']:
        return "Sem info"

    # Retorna todos os nomes de diretores separados por vírgula
    director_names = [d.get("displayName", "Unknown") for d in data['directors']]
    return ", ".join(director_names)


def load_dataset_with_directors(file_path: str, limit: int = None):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"O ficheiro {file_path} não foi encontrado.")

    df = pd.read_csv(file_path, nrows=limit)

    if 'imdb_id' not in df.columns:
        raise ValueError("O dataset não contém a coluna 'imdb_id'.")

    # Aplicar a função de API para obter diretores
    df['Director'] = df['imdb_id'].apply(get_director)

    # Reordenar coluna 'Director' para ficar depois de 'title', se existir
    if 'title' in df.columns and 'Director' in df.columns:
        cols = list(df.columns)
        title_index = cols.index('title')
        cols.remove('Director')
        cols.insert(title_index + 1, 'Director')
        df = df[cols]

    return df


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

