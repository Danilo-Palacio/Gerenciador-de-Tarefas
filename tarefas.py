import json
import os

CAMINHO_ARQUIVO = "dados.json"


def adicionar_tarefa(texto, tarefas):
    concluida = False
    if texto == "":
        return
    texto_dicionario = {"texto": texto, "concluida": concluida}
    tarefas.append(texto_dicionario)
    salvar_dados(tarefas)
    print(f" Tarefas do adicionar é: {tarefas}, isso é oque retorna")
    return tarefas


def remover_tarefa(tarefa_selecionada, tarefas):
    if not tarefa_selecionada:
        return
    for tarefa in reversed(tarefa_selecionada):
        tarefas.pop(tarefa)
    salvar_dados(tarefas)


def alterar_tarefa(texto, tarefa_selecionada, tarefas):
    for tarefa in tarefa_selecionada:
        tarefas[tarefa].update({"texto": texto})
    salvar_dados(tarefas)
    return tarefas


def carregar_lista():
    if os.path.exists(CAMINHO_ARQUIVO):
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
        return []


def filtro(status, tarefas):
    tarefas_concluidas = []
    for i in tarefas:
        if status == "Concluidas":
            teste = True
        else:
            teste = False

        if teste == i["concluida"]:
            tarefa = {"texto": i["texto"], "concluida": status}
            tarefas_concluidas.append(tarefa)
            continue
        elif teste == i["concluida"]:
            tarefas_concluidas.append(i["texto"])
            continue
    return tarefas_concluidas


def obter_texto_tarefa(indice, tarefas):
    if not indice:
        return
    for tarefa in indice:
        return tarefas[tarefa]["texto"]


def salvar_dados(tarefas):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)


def concluir_tarefa(tarefa_selecionada, tarefas):
    if not tarefa_selecionada:
        return
    for tarefa in tarefa_selecionada:
        if not tarefas[tarefa]["concluida"]:
            tarefas[tarefa]["concluida"] = True
        else:
            tarefas[tarefa]["concluida"] = False
    salvar_dados(tarefas)
