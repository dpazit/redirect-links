import os
import csv

def read_csv_files(input_folder):
    unified_urls = []
    
    # Percorre todos os arquivos na pasta especificada
    for filename in os.listdir(input_folder):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_folder, filename)
            
            with open(file_path, 'r', newline='') as file:
                reader = csv.reader(file)
                next(reader)  # Pula o cabeçalho
                
                # Adiciona cada URL e o nome do arquivo ao conjunto unificado
                for row in reader:
                    if row:
                        unified_urls.append((row[0], filename))
    
    return unified_urls

def write_unified_csv(unified_urls, output_file):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Source File'])
        
        for url, source_file in unified_urls:
            writer.writerow([url, source_file])

def main(input_folder):
    output_file = os.path.join(input_folder, 'sitemap_urls_unificado.csv')
    unified_urls = read_csv_files(input_folder)
    write_unified_csv(unified_urls, output_file)
    print(f"URLs unificadas e salvas em {output_file}")

if __name__ == "__main__":
    input_folder = os.path.join(os.getcwd(), 'sitemap_urls')
    main(input_folder)
