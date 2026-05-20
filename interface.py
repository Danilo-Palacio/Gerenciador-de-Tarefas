import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.title("Gerenciador de Tarefas")
root.geometry("300x400")

janela = ttk.Frame(root)
janela.pack()


titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
titulo.pack(padx=10, pady=10, anchor=tk.CENTER)

campo_texto = ttk.Entry(janela)
campo_texto.pack(pady=20)

botao_inserir_tarefa = ttk.Button(janela, text="Inserir")
botao_inserir_tarefa.pack(pady=5)

lista_box = tk.Listbox(janela, selectmode=tk.MULTIPLE)
lista_box.pack(pady=10, fill="both", expand=True)

itens_iniciais = ["Maçã", "Banana", "Laranja", "Uva"]
for item in itens_iniciais:
    lista_box.insert(tk.END, item)

botao = ttk.Button(janela, text="Quit", command=root.destroy)
botao.pack(padx=10, pady=10, anchor=tk.CENTER)

root.mainloop()
