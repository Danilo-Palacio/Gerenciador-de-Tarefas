import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("300x400")


def adicionar_tarefa(event=None):
    texto = campo_texto.get().strip()
    if texto == "":
        return
    lista_box.insert(tk.END, texto)
    campo_texto.delete(0, tk.END)

janela = ttk.Frame(root)
janela.pack(fill="both", expand=True, padx=10, pady=10)

titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
titulo.pack(padx=10, pady=10, anchor=tk.CENTER, fill="x")

campo_texto = ttk.Entry(janela)
campo_texto.pack(pady=20, fill="x")
campo_texto.bind("<Return>", adicionar_tarefa)

botao_inserir_tarefa = ttk.Button(
    janela, text="Inserir", command=adicionar_tarefa)
botao_inserir_tarefa.pack(pady=5, fill="x")

lista_box = tk.Listbox(janela, selectmode=tk.MULTIPLE)
lista_box.pack(pady=10, fill="both", expand=True)

itens_iniciais = []
for item in itens_iniciais:
    lista_box.insert(tk.END, item)

botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
botao_sair.pack(anchor=tk.CENTER, fill="x")

root.mainloop()
