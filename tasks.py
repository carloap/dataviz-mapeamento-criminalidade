from invoke import task
from src.data.Extracao import Extracao as ext

# Tarefa teste de saudação em shell
@task
def hello(c, name="There"):
    c.run("echo 'Hello {}'".format(name))

# Tarefa de ajuda para mostrar tarefas válidas disponíveis
@task
def help(c):
    print("Tarefas válidas ")
    import tasks as tsks
    lista_funcoes = dir(tsks)
    lista_funcoes = list( filter(lambda f: f[:2] not in "__" and f not in ['task','help'], lista_funcoes) )
    print(lista_funcoes)

# Tarefa para extrair dados dos arquivos PDF do SSPDS-CE
@task
def extrairPDF(c):
    print("Identificando arquivos de fontes PDF")
    caminho_fontes_pdf = 'data/external/sspds-ce/cvli/2014'
    lista_fontes_pdf = ext.identificarArquivos(caminho_fontes_pdf)

    print("Extraindo conteúdo para CSV")
    for arquivo in lista_fontes_pdf:
        ext.extrairPdfSSPCE(arquivo)

# Tarefa para gerar dataset consolidado
@task
def gerarDataset(c):
    print("Identificar arquivos extraidos")
    caminho_dos_extraidos = 'data/processed/sspds-ce/cvli'
    lista_extraidos = ext.identificarArquivos(caminho_dos_extraidos)
    print("Gerar dataset consolidado para analise exploratoria")
    ext.gerarDataset(lista_extraidos)

    print("Removendo arquivos sem uso")
    c.run("rm -rf data/processed/sspds-ce/cvli")

    print("OK!")

