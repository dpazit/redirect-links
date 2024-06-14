import requests
import xml.etree.ElementTree as ET
import csv
import os

def fetch_sitemap(url):
    response = requests.get(url)
    response.raise_for_status()  # Lança uma exceção se o pedido falhar
    return response.content

def parse_sitemap(xml_content):
    urls = []
    root = ET.fromstring(xml_content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace).text
        urls.append(loc)

    return urls

def parse_sitemap_index(xml_content):
    sitemaps = []
    root = ET.fromstring(xml_content)
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

    for sitemap in root.findall('ns:sitemap', namespace):
        loc = sitemap.find('ns:loc', namespace).text
        sitemaps.append(loc)

    return sitemaps

def write_to_csv(urls, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL'])
        for url in urls:
            writer.writerow([url])

def main(sitemap_index_url, output_folder):
    # Cria a pasta de saída se não existir
    os.makedirs(output_folder, exist_ok=True)

    # Busca e parseia o índice de sitemaps
    xml_content = fetch_sitemap(sitemap_index_url)
    sitemaps = parse_sitemap_index(xml_content)

    for sitemap_url in sitemaps:
        # Busca e parseia o sitemap individual
        sitemap_content = fetch_sitemap(sitemap_url)
        urls = parse_sitemap(sitemap_content)

        # Cria o nome do arquivo de saída baseado na URL do sitemap
        sitemap_name = os.path.basename(sitemap_url).replace('.xml', '_urls.csv')
        output_file_path = os.path.join(output_folder, sitemap_name)

        # Escreve as URLs no arquivo CSV
        write_to_csv(urls, output_file_path)
        print(f"URLs extraídas e salvas em {output_file_path}")

if __name__ == "__main__":
    sitemap_index_url = "https://www.jove.com/sitemap.xml"  # Substitua pela URL do seu índice de sitemap
    output_folder = os.path.join(os.getcwd(), 'sitemap_urls')
    main(sitemap_index_url, output_folder)
