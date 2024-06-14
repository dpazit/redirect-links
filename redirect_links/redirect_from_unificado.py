import os
import requests
import pandas as pd
import csv

def fetch_redirects(url_list):
    results = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    for index, (url, source_file) in enumerate(url_list, start=1):
        try:
            response = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            final_url = response.url  # URL final após qualquer redirecionamento
            fl_redirect = (url != final_url)
            results.append((url, final_url, fl_redirect, source_file))
            print(f"Link {index}: {url} (from {source_file})")  # Printa o número do link, a URL e o arquivo de origem
        except requests.RequestException as e:
            results.append((url, str(e), False, source_file))  # Em caso de erro, mantenha a URL original e marque fl_redirect como False
            print(f"Link {index}: {url} (from {source_file}) - Error: {e}")

    return results

# Função para formatar os resultados em uma tabela
def format_results_table(results):
    df = pd.DataFrame(results, columns=['Original URL', 'Destination URL', 'fl_redirect', 'Source File'])
    return df

# Lendo o arquivo unificado na pasta 'sitemap_urls'
def read_unified_csv(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print("O arquivo CSV especificado não foi encontrado.")
        return None

# Especificando o caminho completo para a pasta 'sitemap_urls' e para o arquivo CSV unificado
input_folder = os.path.join(os.getcwd(), 'sitemap_urls')
input_file_path = os.path.join(input_folder, 'sitemap_urls_unificado.csv')

# Lendo o arquivo CSV unificado
df_csv = read_unified_csv(input_file_path)

# Verificando se o arquivo CSV foi lido com sucesso
if df_csv is not None:
    # Obtendo as URLs e os arquivos de origem a partir do arquivo CSV unificado
    urls_to_check = df_csv[['URL', 'Source File']].values.tolist()
    
    # Obtendo os resultados dos redirecionamentos
    redirect_results = fetch_redirects(urls_to_check)

    # Formatando os resultados em uma tabela
    results_table = format_results_table(redirect_results)

    # Especificando o caminho completo para a pasta 'output'
    output_folder = os.path.join(os.getcwd(), 'output')
    os.makedirs(output_folder, exist_ok=True)

    # Exportando os resultados para CSV
    output_file_path = os.path.join(output_folder, 'sitemap_urls_redirect.csv')
    results_table.to_csv(output_file_path, sep=';', quotechar='"', quoting=csv.QUOTE_NONNUMERIC, index=False)
    
    # Exibindo os dados do arquivo CSV
    print(f"URLs redirecionadas e salvas em {output_file_path}")

else:
    print("O arquivo CSV unificado não foi encontrado ou está vazio.")
