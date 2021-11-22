import os
import re
from src.data.ManipularArquivo import ManipularArquivo as mArq

# # Solução paliativa para obter o diretório raiz do projeto (não é necessário por enquanto)
# ROOT_DIR = os.path.dirname(os.path.abspath(f'{__file__}/../..'))

# Classe para extrair e catalogar dados de arquivos fonte
class Extracao:

    # Varrer os arquivos fontes, desconsiderando possíveis arquivos ocultos
    def identificarArquivos(caminho):
        diretorio_do_estudo = caminho

        lista_arquivos = mArq.varrerDiretorio(diretorio_do_estudo)
        ignorar = ('.', '..')
        lista_fontes_pdf = list(filter(lambda l: l.split('/')[-1][0:1] not in ignorar, lista_arquivos))

        return lista_fontes_pdf


    # Ler conteúdo das fontes em PDF do SSPDS-CE, e formatar os campos
    def extrairPdfSSPCE(arquivo):

        # Define o arquivo de origem para ler, e o arquivo final substituto, já estruturado
        arquivo_origem = arquivo
        arquivo_destino = arquivo_origem.replace('external', 'processed').replace('.pdf', '.csv')

        # Remove o arquivo destino, para criar um novo
        mArq.removerArquivo(arquivo_destino)

        conteudo_pdf = mArq.abrirPDF(arquivo_origem)

        # Inicializa cabeçalho, e modifica conforme parâmetros do ano da fonte
        cabecalho = "ID;AIS;MUNICIPIO;NATUREZA DO FATO;ARMA UTILIZADA;DATA;SEXO;IDADE"
        anos_formato_antigo = ('2019', '2018', '2017', '2016', '2015')
        if any(ano in arquivo_origem for ano in anos_formato_antigo):
            cabecalho = "ID;AIS;MUNICIPIO;NATUREZA DO FATO;ARMA UTILIZADA;DATA DA MORTE;NOME VITIMA;GUIA-CADAV;SEXO;IDADE"

        # escreve o cabeçalho em um arquivo novo
        mArq.escreverTXT(arquivo_destino, f'{cabecalho}\n')

        # compila as expressões regulares para separação de colunas (essa função é bem específica)
        r2 = re.compile(r'(\s)(AIS.[0-9]{1,2}|AIS.+DEFINIDA|AIS.+Identificada.+\)|AIS.+IDENTIFICADA.+\))(\s)')
        r4 = re.compile(r'(\s)(?!UNID|PRISI|Identific)(HOMI|FEMI|LES|ROU|MORTE SUS.+)([A-Ö]{2}.+[A-Z\)])(\s)([A-Z]{1}[a-z]{2})')
        r4_2 = re.compile(r'(\s)(HOMI|FEMI|LES|ROU|MORTE SUS.+)([A-Ö]{2}.+[A-Z\)])(\s)(ARMA.+|Arma.+|AMA.+|Ama.+|ARAM.+|Aram.+|NI|Ni|NÃO INF)(.+[0-9]{1,}/[0-9]{2}/|.+[0-9]{1,}-[A-z]{3}-)')
        r4_3 = re.compile(r'(\s)(HOMI|FEMI|LES|ROU|MORTE SUS.+)([A-Ö]{2}.+[A-Z\)])(\s)(Outros|OUTROS|OUTRO|Outro)(.+[0-9]{1,}/[0-9]{2}/|.+[0-9]{1,}-[A-z]{3}-)')
        r4_4 = re.compile(r'(\s)(HOMI|FEMI|LES|ROU|MORTE SUS.+)([A-Ö]{2}.+[A-Z\)])(\s)(.+)(\s[0-9]{1,}/[0-9]{2}/|\s[0-9]{1,}-[A-z]{3}-)')
        r4_5 = re.compile(r'(\s)(ARMA.+|Arma.+|AMA DE.+|Ama de.+|ARAM.+|Aram.+|NI|Ni|NÃO INF)(.+)(\s[0-9]{1,}/[0-9]{2}/|\s[0-9]{1,}-[A-z]{3}-)')
        r6 = re.compile(r'(\s)([0-9]{1,}/[0-9]{2}/[0-9]{4})(\s)')
        r6_2 = re.compile(r'(\s)([0-9]{1,}-[A-z]{3}-[0-9]{2,4})(\s)')
        r8 = re.compile(r'(\s)([0-9]{1,}|-)$')
        r8_2 = re.compile(r'(\s)([0-9]{1,}\-[0-9\s]{1,}\/2[0-9]{2,4}|\-\/|[0-9]{3}\s\-[0-9]{1,}\/2[0-9]{2,4}|[0-9]{3}\-[0-9]{4})(\s)')
        r8_3 = re.compile(r'(ICADO|icado)(\-)$')
        rx_1 = re.compile(r'(\s)(Unidade Prisional|UNIDADE PRISIONAL|UNIDADE PRISIONA 00L)(\s)')
        rx_3 = re.compile(r'(MORTE)(ARMA)\;') # Campos mapeados incorretamente por erro de texto #1 

        # Inicializa um acumulador para linhas quebradas
        linha_acumulada = ''
        for linha in conteudo_pdf.splitlines():

            # Remover linhas desnecessárias
            linha_limpa = re.sub(r'ID AIS MUNIC.+', '', linha)
            linha_limpa = re.sub(r'VÍTIMAS DE CRIMES VIOLENTOS.+', '', linha_limpa)
            linha_limpa = re.sub(r'DADOS CONSOLIDADOS', '', linha_limpa)
            linha_limpa = re.sub(r'Página .+', '', linha_limpa)
            linha_limpa = re.sub(r'DATA DA.+', '', linha_limpa)
            linha_limpa = re.sub(r'NOME DA V.+', '', linha_limpa)
            linha_limpa = re.sub(r'GUIA\-', '', linha_limpa)
            linha_limpa = re.sub(r'/CADAV.+', '', linha_limpa)
            linha_limpa = re.sub(r'SEXO IDADE', '', linha_limpa)
            linha_limpa = re.sub(r'UNIDADE PRISIONAL.+', '', linha_limpa) # remove a legenda
            
            # DEBUG
            # print(linha_limpa)
            # print(linha_limpa + " // " + linha_acumulada)
            # continue 

            # workaround para linhas contendo somente um número
            if len(linha_limpa)>0 and len(linha_limpa) <3:
                linha_limpa = f'{str(linha_limpa).zfill(3)} '

            # Somente linhas com conteúdo
            if len(linha_limpa)>=3:
                try:
                    # Verifica parâmetros da linha percorrida, com a linha acumulada, e unir caso esteja quebrado
                    if " AIS " in linha_acumulada and " AIS " not in linha_limpa:
                        # print(f"ACUMULAR! >>> {linha_limpa[0]}{linha_limpa[1]} <<<")
                        # print(linha_limpa + " // " + linha_acumulada)
                        linha_acumulada += f' {linha_limpa}'
                    # Validação de linha extra
                    elif ("UNIDADE" in linha_acumulada or "Unidade" in linha_acumulada) and ("UNIDADE" not in linha_limpa or "Unidade" not in linha_limpa):
                    # elif  "UNIDADE" in linha_limpa or "PRISIONAL" in linha_limpa : # Gambs para pegar uma linha extra
                        # print(f"ACUMULAR ADICIONAL! >>> {linha_limpa[0]}{linha_limpa[1]} <<<")
                        # print(linha_limpa + " // " + linha_acumulada)
                        linha_acumulada += f' {linha_limpa}'
                    elif linha_limpa[0].isnumeric(): 
                        # print(f"Conjunto Válido! >>> {linha_limpa[0]}{linha_limpa[1]} <<<")
                        # print(linha_limpa + " // " + linha_acumulada)
                        linha_acumulada = linha_limpa
                    else:
                        # TODO: Validar alguma possível exceção aqui
                        # print("Simplesmente acumula e depois ajusta...")
                        linha_acumulada += f' {linha_limpa}'

                    # Se o conjunto total da linha for válido, preencher com o valor
                    if len(linha_acumulada)>12 and linha_acumulada[0].isnumeric() and (" AIS " in linha_acumulada or "UNIDADE" in linha_acumulada or "Unidade" in linha_acumulada) and ((linha_acumulada[-1].isnumeric() and linha_acumulada[-2] in " ") or (linha_acumulada[-2:].isnumeric() and linha_acumulada[-3] in " ") or linha_acumulada[-2:] in " -"
                        or linha_acumulada[-6:] in "ICADO-"
                    ):
                        linha_limpa = linha_acumulada.replace('  ',' ')
                        linha_acumulada = '' # reseta o acumulador de linhas

                        # Aplica expressões regulares para separar as colunas das linhas percorridas
                        linha_limpa = r2.sub(r';\g<2>;', linha_limpa)
                        linha_limpa = r4.sub(r';\g<2>\g<3>;\g<5>', linha_limpa)
                        linha_limpa = r4_2.sub(r';\g<2>\g<3>;\g<5>\g<6>', linha_limpa)
                        linha_limpa = r4_3.sub(r';\g<2>\g<3>;\g<5>\g<6>', linha_limpa)
                        linha_limpa = r4_4.sub(r';\g<2>\g<3>\g<4>\g<5>;\g<6>', linha_limpa)
                        linha_limpa = r4_5.sub(r';;\g<2>\g<3>\g<4>', linha_limpa)
                        linha_limpa = r6.sub(r';\g<2>;', linha_limpa)
                        linha_limpa = r6_2.sub(r';\g<2>;', linha_limpa) # formato de data modificado
                        linha_limpa = r8.sub(r';\g<2>', linha_limpa)
                        linha_limpa = r8_2.sub(r';\g<2>;', linha_limpa) # regra para formato de PDF de 2019
                        linha_limpa = r8_3.sub(r'\g<1>;\g<2>', linha_limpa) # campo com valor "não identificado"
                        linha_limpa = rx_1.sub(r';\g<2>;', linha_limpa) # tratamento do campo "unidade prisional"
                        linha_limpa = rx_3.sub(r'\g<1>;\g<2> ', linha_limpa) # tratamento de campo mapeado incorreto por texto ruim #1

                        # DEBUG
                        # print(linha_limpa)

                        # escreve em arquivo linha a linha
                        mArq.escreverTXT(arquivo_destino, f'{linha_limpa}\n')

                except IndexError as ex:
                    print(f" - Erro no indexador: {ex}")
                    print(f" - conteudo: {linha_limpa}")


    # Gerar dataset consolidado para analise, a partir dos dados extraídos
    def gerarDataset(arquivos):
        arquivo_destino = 'data/processed/sspds-ce/dataset_consolidado.csv'

        # Remove o arquivo destino, para criar um novo
        mArq.removerArquivo(arquivo_destino)

        # cabecalho do dataset padrão (8 colunas)
        cabecalho_padronizado = "ID;AIS;MUNICIPIO;NATUREZA DO FATO;ARMA UTILIZADA;DATA;SEXO;IDADE"

        for arquivo in arquivos:
            # Lê conteúdo do arquivo
            conteudo_arquivo = mArq.abrirTXT(arquivo)

            # iterar linha a linha
            for linha in conteudo_arquivo.splitlines():
                coluna = linha.split(';')
                # tl;dr 
                # se o conjunto extraído tiver mais que 8 colunas, eliminar as informações que não interessam
                if len(coluna) == 10:
                    del coluna[7]
                    del coluna[6]

                    linha_limpa = ";".join(coluna)

                    # escreve em arquivo linha a linha
                    mArq.escreverTXT(arquivo_destino, f'{linha_limpa}\n')
                else:
                    # escreve em arquivo linha a linha
                    mArq.escreverTXT(arquivo_destino, f'{linha}\n')


