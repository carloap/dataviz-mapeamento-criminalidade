from invoke import task
from src.data.Extracao import Extracao as ext
import pprint as pp

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
def extrairPDFSSPCE(c):
    lista_fontes_pdf = ext.identificarArquivosFontesPDF()
    for arquivo in lista_fontes_pdf:
        ext.extrairPdfSSPCE(arquivo)
