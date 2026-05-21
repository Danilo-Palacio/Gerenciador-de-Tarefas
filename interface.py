import tkinter as tk
from tkinter import ttk

from tarefas import remover_tarefa, adicionar_tarefa, carregar_lista


def atualizar_lista(lista_box):
    lista_box.delete(0, tk.END)
    tarefas = carregar_lista()
    for tarefa in tarefas:
        lista_box.insert(tk.END, tarefa)


def iniciar_app():

    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x450")

    janela = ttk.Frame(root)
    lista_box = tk.Listbox(janela, selectmode=tk.MULTIPLE)

    janela.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
    titulo.pack(padx=10, pady=10, anchor=tk.CENTER, fill="x")

    campo_texto = ttk.Entry(janela)
    campo_texto.pack(pady=20, fill="x")
    campo_texto.bind("<Return>", lambda e: adicionar_tarefa(
                                        campo_texto, lista_box))

    botao_inserir_tarefa = ttk.Button(
        janela, text="Inserir", command=lambda: adicionar_tarefa(
                                                campo_texto, lista_box))
    botao_inserir_tarefa.pack(pady=5, fill="x")

    lista_box.pack(pady=10, fill="both", expand=True)

    atualizar_lista(lista_box)

    botao_remover_tarefa = ttk.Button(
        janela, text="Remover", command=lambda: remover_tarefa(lista_box))
    botao_remover_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
