import os
import requests
import pandas as pd
import csv

def fetch_redirects(url_list):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for url in url_list:
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            final_url = response.url  # This is the final destination URL after any redirects
            results.append((url, final_url))
        except requests.RequestException as e:
            results.append((url, str(e)))  # Append error message if request fails

    return results

# Função para formatar os resultados em uma tabela
def format_results_table(results):
    df = pd.DataFrame(results, columns=['Original URL', 'Destination URL'])
    return df

# Lista com URLs para verificar os redirecionamentos
urls_to_check = [
    'https://www.jove.com/t/50447/-?list=U204iCLR&?list=U204iCLR&&language=Korean',
    'https://www.jove.com/t/58055/trasferimento-embrionale-minimamente-invasivo-e-vetrificazione?language=Portuguese',
    # Adicione mais URLs aqui
]

# Obtendo os resultados dos redirecionamentos
redirect_results = fetch_redirects(urls_to_check)

# Formatando os resultados em uma tabela
results_table = format_results_table(redirect_results)

# Especificando o caminho completo para a pasta 'output'
output_folder = os.path.join(os.getcwd(), 'output')
os.makedirs(output_folder, exist_ok=True)

# Exportando para CSV com as configurações desejadas
output_file_path = os.path.join(output_folder, 'result_redirect.csv')
results_table.to_csv(output_file_path, sep=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, index=False)
