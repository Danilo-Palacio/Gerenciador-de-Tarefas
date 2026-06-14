import json
import os

CAMINHO_ARQUIVO = "dados.json"


def carregar_lista():
    if os.path.exists(CAMINHO_ARQUIVO):
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
        return []


def ordenar_alfabetica(indices_visiveis, lista_tarefas):
    indices_ordenados = sorted(
        indices_visiveis,
        key=lambda indice: lista_tarefas[indice]['texto']
    )
    return indices_ordenados


def ordenar_prioridade(indices_visiveis, lista_tarefas):
    pesos = {'Alta': 0, 'Média': 1, 'Baixa': 2}
    indices_ordenados = sorted(
        indices_visiveis,
        key=lambda indice: pesos.get(lista_tarefas[indice]['prioridade'], 3)
    )
    return indices_ordenados


def ordenar_pendentes(indices_visiveis, lista_tarefas):
    indices_ordenados = sorted(
        indices_visiveis,
        key=lambda indice: lista_tarefas[indice]['concluida']
    )
    return indices_ordenados


def adicionar_tarefa(texto, tarefas, prioridade):
    concluida = False
    if texto == "":
        return
    texto_dicionario = {
        "texto": texto,
        "concluida": concluida,
        "prioridade": prioridade
        }
    tarefas.append(texto_dicionario)
    salvar_dados(tarefas)
    return tarefas


def remover_tarefa(tarefa_selecionada, tarefas):
    tarefas.pop(tarefa_selecionada)
    salvar_dados(tarefas)
    return tarefas


def concluir_tarefa(tarefa_selecionada, tarefas):
    if not tarefas[tarefa_selecionada]["concluida"]:
        tarefas[tarefa_selecionada]["concluida"] = True
    else:
        tarefas[tarefa_selecionada]["concluida"] = False
    salvar_dados(tarefas)
    return tarefas


def alterar_tarefa(entrada_str, indice_real, tarefas, prioridade):
    tarefas[indice_real].update({"texto": entrada_str})
    tarefas[indice_real].update({"prioridade": prioridade})
    salvar_dados(tarefas)
    return tarefas


def filtro(status, lista_tarefas):
    indices_filtrados = []
    for indice, tarefa in enumerate(lista_tarefas):
        if status == "Todas":
            indices_filtrados.append(indice)
        elif status == "Pendentes":
            if not tarefa['concluida']:
                indices_filtrados.append(indice)
        elif status == "Concluidas":
            if tarefa['concluida']:
                indices_filtrados.append(indice)

    return indices_filtrados


def obter_texto_tarefa(indice, tarefas):
    return tarefas[indice]["texto"]


def salvar_dados(tarefas):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)
