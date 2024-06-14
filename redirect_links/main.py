import os
import requests
import pandas as pd
import csv

def fetch_redirects(url_list):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    i = 0

    for url in url_list:
        try:    
            i += 1  # Incrementa o contador
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            final_url = response.url  # This is the final destination URL after any redirects
            results.append((url, final_url))
            print(f"Link {i}: {url}")  # Printa o número do link e a URL
        except requests.RequestException as e:
            results.append((url, str(e)))  # Append error message if request fails

    return results

# Função para formatar os resultados em uma tabela
def format_results_table(results):
    df = pd.DataFrame(results, columns=['Original URL', 'Destination URL'])
    return df

# Lendo o arquivo CSV na pasta 'input'
def read_csv_file(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path, usecols=[0])
    else:
        print("O arquivo CSV especificado não foi encontrado.")
        return None

# Especificando o caminho completo para a pasta 'input' e para o arquivo CSV
input_folder = os.path.join(os.getcwd(), 'input')
input_file_path = os.path.join(input_folder, 'links_input2.csv')

# Lendo o arquivo CSV
df_csv = read_csv_file(input_file_path)

urls_to_check = df_csv['URL'].tolist()

# Verificando se o arquivo CSV foi lido com sucesso
if df_csv is not None:
    # Obtendo as URLs a partir do arquivo CSV
    urls_to_check = df_csv['URL'].tolist()  # Supondo que a primeira coluna com as URLs se chama 'URL'
    
    # Obtendo os resultados dos redirecionamentos
    redirect_results = fetch_redirects(urls_to_check)

    # Formatando os resultados em uma tabela
    results_table = format_results_table(redirect_results)

    # Especificando o caminho completo para a pasta 'output'
    output_folder = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_folder, exist_ok=True)

    # Exportando os resultados para CSV
    output_file_path = os.path.join(output_folder, 'result_redirect2.csv')
    results_table.to_csv(output_file_path, sep=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, index=False)
    
    # Exibindo os dados do arquivo CSV
    print("Finalizado")
