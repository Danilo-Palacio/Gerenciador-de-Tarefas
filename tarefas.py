import json
import os

CAMINHO_ARQUIVO = "dados.json"


def adicionar_tarefa(texto):
    tarefas = carregar_lista()
    concluida = False
    if texto == "":
        return
    texto_dicionario = {"texto": texto, "concluida": concluida}
    tarefas.append(texto_dicionario)
    salvar_dados(tarefas)


def remover_tarefa(tarefa_selecionada):
    tarefas = carregar_lista()
    if not tarefa_selecionada:
        return
    for tarefa in reversed(tarefa_selecionada):
        tarefas.pop(tarefa)
    salvar_dados(tarefas)


def carregar_lista():
    if os.path.exists(CAMINHO_ARQUIVO):
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
    return []


def salvar_dados(tarefas):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)


def concluir_tarefa(tarefa_selecionada):
    tarefas = carregar_lista()
    if not tarefa_selecionada:
        return
    for tarefa in tarefa_selecionada:
        if not tarefas[tarefa]["concluida"]:
            tarefas[tarefa]["concluida"] = True
        else:
            tarefas[tarefa]["concluida"] = False
    salvar_dados(tarefas)
