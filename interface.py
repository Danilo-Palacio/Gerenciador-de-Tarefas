import tkinter as tk
from tkinter import ttk
import json
import os

CAMINHO_ARQUIVO = "dados.json"

root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("300x450")


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


def remover_tarefa():
    tarefas_selecionada = lista_box.curselection()
    if not tarefas_selecionada:
        return
    for tarefa in reversed(tarefas_selecionada):
        tarefas.pop(tarefa)
    salvar_dados(tarefas)
    atualizar_lista()


def adicionar_tarefa(event=None):
    tarefa = campo_texto.get().strip()
    if tarefa == "":
        return
    tarefas.append(tarefa)
    salvar_dados(tarefas)
    atualizar_lista()
    campo_texto.delete(0, tk.END)
    campo_texto.focus()


def atualizar_lista():
    lista_box.delete(0, tk.END)
    for tarefa in tarefas:
        lista_box.insert(tk.END, tarefa)


janela = ttk.Frame(root)
lista_box = tk.Listbox(janela, selectmode=tk.MULTIPLE)

janela.pack(fill="both", expand=True, padx=10, pady=10)

titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
titulo.pack(padx=10, pady=10, anchor=tk.CENTER, fill="x")

campo_texto = ttk.Entry(janela)
campo_texto.pack(pady=20, fill="x")
campo_texto.bind("<Return>", adicionar_tarefa)

botao_inserir_tarefa = ttk.Button(
    janela, text="Inserir", command=adicionar_tarefa)
botao_inserir_tarefa.pack(pady=5, fill="x")

lista_box.pack(pady=10, fill="both", expand=True)

tarefas = carregar_lista()
atualizar_lista()

botao_remover_tarefa = ttk.Button(
    janela, text="Remover", command=remover_tarefa)
botao_remover_tarefa.pack(pady=5, fill="x")

botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

root.mainloop()
