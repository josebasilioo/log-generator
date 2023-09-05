import os
import datetime

current_dir = os.getcwd()
source_dir = current_dir + '/home/valcann/backupsFrom'
diretorio_destino = current_dir + '/home/valcann/'

source_files = os.listdir(source_dir)

files = [arquivo for arquivo in source_files if os.path.isfile(os.path.join(source_dir, arquivo))]

infos = []

for file in files:
    caminho_arquivo = os.path.join(source_dir, file)

    # if os.path.exists(caminho_arquivo) and os.path.isfile(caminho_arquivo):
        # print(caminho_arquivo)
        # os.remove(caminho_arquivo)
    info_arquivo = os.stat(caminho_arquivo)

    infos.append({
        'nome': file,
        'criado_em': datetime.datetime.fromtimestamp(info_arquivo.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
        'modificado_em': datetime.datetime.fromtimestamp(info_arquivo.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
    })

print(infos)

# caminho_completo = os.path.join(diretorio_destino, 'log_file_test')

# with open(caminho_completo, "w") as arquivo_log:
#     arquivo_log.write("Aqui estão algumas informações de log.\n")
#     arquivo_log.write("Outra linha de log.\n")
#     arquivo_log.write("Criado em: " + str(datetime.datetime.now()))
