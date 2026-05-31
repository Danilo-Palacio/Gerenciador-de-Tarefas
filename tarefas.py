import json
import os

CAMINHO_ARQUIVO = "dados.json"


def adicionar_tarefa(texto, tarefas):
    print("função: adicionar_tarefa | tarefas.py")
    concluida = False
    if texto == "":
        return
    texto_dicionario = {
        "texto": texto,
        "concluida": concluida
        }
    tarefas.append(texto_dicionario)
    salvar_dados(tarefas)
    print(f"o que retorna é {tarefas}")
    return tarefas


def remover_tarefa(tarefa_selecionada, tarefas):
    print("função: remover_tarefa | tarefas.py")
    if not tarefa_selecionada:
        return
    tarefas.pop(tarefa_selecionada)
    salvar_dados(tarefas)
    print(f"o que retorna é {tarefas}")
    return tarefas


def concluir_tarefa(tarefa_selecionada, tarefas):
    print("função: concluir_tarefa | tarefas.py")
    if not tarefa_selecionada:
        return
    if not tarefas[tarefa_selecionada]["concluida"]:
        tarefas[tarefa_selecionada]["concluida"] = True
    else:
        tarefas[tarefa_selecionada]["concluida"] = False
    salvar_dados(tarefas)
    print(f"o que retorna é {tarefas}")
    return tarefas


def alterar_tarefa(entrada_str, indice_real, tarefas):
    print("função: alterar_tarefa | tarefas.py")
    tarefas[indice_real].update({"texto": entrada_str})
    salvar_dados(tarefas)
    return tarefas


def carregar_lista():
    print("função: carregar_lista | tarefas.py")
    if os.path.exists(CAMINHO_ARQUIVO):
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
        return []


def filtro(status, lista_tarefas):
    print("função: filtro | tarefas.py")
    print(f"A lista enviada ao filtro foi: {lista_tarefas}")
    tarefas_filtradas = []
    indices_filtrados = []
    teste = status
    for indice, tarefa in enumerate(lista_tarefas):
        if status == "Todas":
            teste = tarefa["concluida"]
        elif status == "Pendentes":
            teste = False
        elif status == "Concluidas":
            teste = True
        if status == "Todas":
            tarefas_filtradas.append(tarefa)
            indices_filtrados.append(indice)
            continue
        else:
            if teste == tarefa["concluida"]:
                tarefas_filtradas.append(tarefa)
                indices_filtrados.append(indice)
    print(f'status {status}')
    print(f'lista de tarefas: {lista_tarefas}')
    print(f'tarefas_filtradas: {tarefas_filtradas}')
    return tarefas_filtradas, indices_filtrados


def obter_texto_tarefa(indice, tarefas):
    print("função: obter_texto_tarefa | tarefas.py")
    if not indice:
        return
    return tarefas[indice]["texto"]


def salvar_dados(tarefas):
    print("função: salvar_dados | tarefas.py")
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(tarefas, arquivo, indent=4)
