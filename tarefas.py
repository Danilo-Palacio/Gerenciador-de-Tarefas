import json
import os
import tkinter as tk

CAMINHO_ARQUIVO = "dados.json"


def adicionar_tarefa(campo_texto, lista_box):
    from interface import atualizar_lista
    tarefas = carregar_lista()
    tarefa = campo_texto.get().strip()
    if tarefa == "":
        return
    tarefas.append(tarefa)
    salvar_dados(tarefas)
    atualizar_lista(lista_box)
    campo_texto.delete(0, tk.END)
    campo_texto.focus()


def remover_tarefa(lista_box):
    from interface import atualizar_lista
    tarefas_selecionada = lista_box.curselection()
    tarefas = carregar_lista()
    if not tarefas_selecionada:
        return
    for tarefa in reversed(tarefas_selecionada):
        tarefas.pop(tarefa)
    salvar_dados(tarefas)
    atualizar_lista(lista_box)


def carregar_lista():
    if os.path.exists(CAMINHO_ARQUIVO):
        try:
            with open(CAMINHO_ARQUIVO, "r") as arquivo:
                return json.load(arquivo)
        except json.JSONDecodeError:
            return []
    return []


def salvar_dados(texto):
    with open(CAMINHO_ARQUIVO, "w") as arquivo:
        json.dump(texto, arquivo, indent=4)
