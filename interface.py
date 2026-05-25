import tkinter as tk
from tkinter import ttk

from tarefas import remover_tarefa, adicionar_tarefa
from tarefas import carregar_lista, concluir_tarefa


def atualizar_lista(list_box):
    list_box.delete(0, tk.END)
    tarefas = carregar_lista()
    for tarefa in tarefas:
        concluida = tarefa["concluida"]
        if not concluida:
            texto = "[  ]"
        else:
            texto = "[X]"
        list_box.insert(tk.END, f"{texto} {tarefa['texto']}")


def adicionar(campo_texto, list_box):
    texto = campo_texto.get().strip()
    adicionar_tarefa(texto)
    atualizar_lista(list_box)
    campo_texto.delete(0, tk.END)
    campo_texto.focus()


def remover(list_box):
    tarefa_selecionada = list_box.curselection()
    remover_tarefa(tarefa_selecionada)
    atualizar_lista(list_box)


def concluir(list_box):
    tarefa_selecionada = list_box.curselection()
    concluir_tarefa(tarefa_selecionada)
    atualizar_lista(list_box)


def iniciar_app():

    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x450")

    janela = ttk.Frame(root)
    list_box = tk.Listbox(janela, selectmode=tk.MULTIPLE)

    janela.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
    titulo.pack(padx=10, pady=10, anchor=tk.CENTER, fill="x")

    campo_texto = ttk.Entry(janela)
    campo_texto.pack(pady=20, fill="x")
    campo_texto.bind("<Return>", lambda e: adicionar(campo_texto, list_box))

    botao_inserir_tarefa = ttk.Button(
        janela, text="Inserir", command=lambda: adicionar(
            campo_texto, list_box))
    botao_inserir_tarefa.pack(pady=5, fill="x")

    list_box.pack(pady=10, fill="both", expand=True)

    atualizar_lista(list_box)

    botao_concluir_tarefa = ttk.Button(
        janela, text="Concluir", command=lambda: concluir(list_box))
    botao_concluir_tarefa.pack(pady=5, fill="x")

    botao_remover_tarefa = ttk.Button(
        janela, text="Remover", command=lambda: remover(list_box))
    botao_remover_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
