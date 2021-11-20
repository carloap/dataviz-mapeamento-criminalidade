import os
from pathlib import Path
from tika import parser

# Classe para manipulação de arquivos e diretórios
class ManipularArquivo:

    def varrerDiretorio(caminho, lista_arquivos=[]):
        if os.path.isfile(caminho):
            lista_arquivos.append(caminho)
        else:
            for objeto in os.listdir(caminho):
                ManipularArquivo.varrerDiretorio(f'{caminho}/{objeto}', lista_arquivos)
        return lista_arquivos

    def abrirTXT(arquivo):
        with open(arquivo, 'r', encoding='utf8') as objeto:
            return objeto.read()

    def abrirPDF(arquivo):
        raw_pdf = parser.from_file(arquivo)
        return raw_pdf['content']

    def escreverTXT(arquivo, conteudo):
        caminho_arquivo = Path('/'.join(arquivo.split('/')[0:-1]))
        caminho_arquivo.mkdir(parents=True, exist_ok=True)
        with open(arquivo, 'a', encoding='utf8') as saida_arquivo:
            saida_arquivo.write(conteudo)

    def removerArquivo(arquivo):
        if os.path.exists(arquivo):
            os.remove(arquivo)
