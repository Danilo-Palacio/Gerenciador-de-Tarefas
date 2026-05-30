import json
import os

CAMINHO_ARQUIVO = "dados.json"


def adicionar_tarefa(texto, tarefas):
    concluida = False
    if texto == "":
        return
    texto_dicionario = {
        "texto": texto,
        "concluida": concluida
        }
    tarefas.append(texto_dicionario)
    salvar_dados(tarefas)
    return tarefas


def remover_tarefa(tarefa_selecionada, tarefas):
    if not tarefa_selecionada:
        return
    for tarefa in reversed(tarefa_selecionada):
        tarefas.pop(tarefa)
    salvar_dados(tarefas)
    return tarefas


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
    tarefas_filtradas = []
    indices_visiveis = []

    for indice, tarefa in enumerate(tarefas):
        print(f"indice: {indice}")
        print(f"tarefa: {tarefa}")
        if status == "Todas":
            teste = tarefa["concluida"]
        elif status == "Pendentes":
            teste = False
        elif status == "Concluidas":
            teste = True
        if status == "Todas":
            tarefas_filtradas.append(tarefa)
            indices_visiveis.append(indice)
            continue
        else:
            if teste == tarefa["concluida"]:
                tarefas_filtradas.append(tarefa)
                indices_visiveis.append(indice)
    return tarefas_filtradas, indices_visiveis


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
    return tarefas
