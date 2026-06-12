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


lista_tarefas = carregar_lista()


def ordenar_alfabetica(indices_visiveis):
    lista_ordenada = lista_tarefas.copy()
    lista_ordenada.sort(key=lambda lista_ordenada: lista_ordenada["texto"])
    indices_ordenados = []
    for indice, valor in enumerate(lista_ordenada):
        for i, v in enumerate(indices_visiveis):
            if valor['texto'] in lista_tarefas[v]['texto']:
                indices_ordenados.append(v)
    return indices_ordenados


def ordenar_prioridade(indices_visiveis):
    tarefas_ordenadas = []
    for indices in indices_visiveis:
        if lista_tarefas[indices]["prioridade"] == "Alta":
            ordenacao = {"indice": indices,
                         "peso": 0}
            tarefas_ordenadas.append(ordenacao)
        elif lista_tarefas[indices]["prioridade"] == "M\u00e9dia":
            ordenacao = {"indice": indices,
                         "peso": 1}
            tarefas_ordenadas.append(ordenacao)
        else:
            ordenacao = {"indice": indices,
                         "peso": 2}
            tarefas_ordenadas.append(ordenacao)
    tarefas_ordenadas.sort(
        key=lambda tarefas_ordenadas: tarefas_ordenadas["peso"])
    indices_ordenados = []
    for indices in tarefas_ordenadas:
        indices_ordenados.append(indices['indice'])
    return indices_ordenados


def ordenar_pendentes(indices_visiveis):
    tarefas_ordenadas = lista_tarefas.copy()
    tarefas_ordenadas.sort(
        key=lambda tarefas_ordenadas: tarefas_ordenadas['concluida'])
    indices_ordenados = []
    for indice, valor in enumerate(tarefas_ordenadas):
        for i, v in enumerate(indices_visiveis):
            if valor['texto'] in lista_tarefas[v]['texto']:
                indices_ordenados.append(v)
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
