import tkinter as tk
from tkinter import ttk
from tarefas import remover_tarefa, adicionar_tarefa, alterar_tarefa, filtro
from tarefas import carregar_lista, concluir_tarefa, obter_texto_tarefa

lista_tarefas = carregar_lista()
indices_visiveis = []


def filtro_ativo(status, list_box, lista_tarefas):
    lista_filtrada, visiveis = filtro(status, lista_tarefas)
    indices_visiveis.clear()
    indices_visiveis.extend(visiveis)
    mostrar_lista(list_box, lista_filtrada, status)
    return len(indices_visiveis)


def mostrar_lista(list_box, lista, status):
    list_box.delete(0, tk.END)
    for tarefa in lista:
        concluida = tarefa["concluida"]
        if not concluida:
            texto = "[  ]"
        else:
            texto = "[X]"
        list_box.insert(tk.END, f"{texto} {tarefa['texto']}")
    return status


ultimo_status = "Todas"


def acao_tarefa(list_box, lista_tarefas, acao, campo_texto):
    if acao != "adicionar":
        indice_escolhido = list_box.curselection()
        indice_real = indices_visiveis[indice_escolhido[0]]
        if acao == "remover":
            atualizar = remover_tarefa(indice_real, lista_tarefas)
        elif acao == "concluir":
            atualizar = concluir_tarefa(indice_real, lista_tarefas)
    elif acao == "adicionar":
        texto = campo_texto.get().strip()
        atualizar = adicionar_tarefa(texto, lista_tarefas)
        campo_texto.delete(0, tk.END)
        campo_texto.focus()
    else:
        return
    filtro_ativo(ultimo_status, list_box, atualizar)


def alterar(texto, indice_real, list_box, popup, lista_tarefas):
    texto_str = texto.get().strip()
    if not texto_str:
        return
    atualizar = alterar_tarefa(texto_str, indice_real, lista_tarefas)
    filtro_ativo(ultimo_status, list_box, atualizar)
    popup.destroy()


def abrir_popup(root, list_box):
    indice_escolhido = list_box.curselection()
    indice_real = indices_visiveis[indice_escolhido[0]]

    tarefa = obter_texto_tarefa(indice_real, lista_tarefas)
    popup = tk.Toplevel(root)
    popup.title("Editar Tarefa")
    popup.geometry("200x100")

    tk.Label(popup, text="Alterar tarefa").pack(pady=3)
    entrada = tk.Entry(popup)
    entrada.insert(0, tarefa)
    entrada.pack(padx=5, anchor=tk.CENTER, fill="x")
    entrada.bind("<Return>", lambda e: alterar(
        entrada, indice_real, list_box, popup, lista_tarefas))
    botao_salvar = tk.Button(popup, text="Salvar",
                             command=lambda: alterar(
                                entrada, indice_real,
                                list_box, popup, lista_tarefas))
    botao_salvar.pack(pady=5, padx=5, anchor=tk.CENTER, fill="x")


def iniciar_app():
    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x450")

    janela = ttk.Frame(root)
    list_box = tk.Listbox(janela)

    todas = filtro_ativo("Todas", list_box, lista_tarefas)
    concluidas = filtro_ativo("Concluidas", list_box, lista_tarefas)
    pendentes = filtro_ativo("Pendentes", list_box, lista_tarefas)

    janela.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
    titulo.pack(padx=10, pady=10, anchor=tk.CENTER)

    frame_campo_inserir = tk.Frame(janela)
    frame_campo_inserir.pack(pady=5, fill="x")

    campo_texto = ttk.Entry(frame_campo_inserir)
    campo_texto.pack(fill="x")
    campo_texto.bind("<Return>",
                     lambda e: acao_tarefa(
                         list_box, lista_tarefas, "adicionar", campo_texto))

    botao_inserir_tarefa = ttk.Button(
        frame_campo_inserir, text="Inserir", command=lambda: acao_tarefa(
                         list_box, lista_tarefas, "adicionar", campo_texto))
    botao_inserir_tarefa.pack(pady=1, fill="x")

    frame_botoes_filtro = tk.Frame(janela)
    frame_botoes_filtro.pack(pady=5)

    botao_todas = ttk.Button(
        frame_botoes_filtro, text=f"Todas ({todas})",
        command=lambda: filtro_ativo("Todas", list_box, lista_tarefas))
    botao_todas.pack(side=tk.LEFT)

    botao_concluidas = ttk.Button(
        frame_botoes_filtro, text=f"Concluidas ({concluidas})",
        command=lambda: filtro_ativo("Concluidas", list_box, lista_tarefas))
    botao_concluidas.pack(side=tk.LEFT)

    botao_pendentes = ttk.Button(
        frame_botoes_filtro, text=f"Pendentes ({pendentes})",
        command=lambda: filtro_ativo("Pendentes", list_box, lista_tarefas))
    botao_pendentes.pack(side=tk.LEFT)

    list_box.pack(pady=10, fill="both", expand=True)

    filtro_ativo(ultimo_status, list_box, lista_tarefas)

    frame_botoes_editar = tk.Frame(janela)
    frame_botoes_editar.pack(pady=5)

    botao_remover_tarefa = ttk.Button(
        frame_botoes_editar, text="Remover",
        command=lambda: acao_tarefa(
            list_box, lista_tarefas, "remover", campo_texto))
    botao_remover_tarefa.pack(side=tk.LEFT)

    botao_alterar_tarefa = ttk.Button(
        frame_botoes_editar, text="Alterar",
        command=lambda: abrir_popup(root, list_box))
    botao_alterar_tarefa.pack(side=tk.RIGHT)

    botao_concluir_tarefa = ttk.Button(
        janela, text="Concluir",
        command=lambda: acao_tarefa(
            list_box, lista_tarefas, "concluir", campo_texto))
    botao_concluir_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
