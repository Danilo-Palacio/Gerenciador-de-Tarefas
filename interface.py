import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tarefas import remover_tarefa, adicionar_tarefa, alterar_tarefa, filtro
from tarefas import carregar_lista, concluir_tarefa, obter_texto_tarefa

lista_tarefas = carregar_lista()
indices_visiveis = []
status_ativo = "Todas"


def texto_list_box(lista, list_box):
    for tarefa in lista:
        concluida = tarefa["concluida"]
        if not concluida:
            texto = "[  ]"
        else:
            texto = "[X]"
        texto_completo = f"{texto} {tarefa['texto']}"
        list_box.insert(tk.END, texto_completo)


def indice_selecao(list_box):
    indice_escolhido = list_box.curselection()
    if indice_escolhido == ():
        messagebox.showerror(
            "Nenhuma tarefa selecionada",
            "Selecione uma tarefa para prosseguir"
            )
        return None
    else:
        indice_real = indices_visiveis[indice_escolhido[0]]
        return indice_real


def acao_tarefa(list_box, acao, campo_texto, botoes_filtro):
    if acao != "adicionar":
        indice_real = indice_selecao(list_box)
        if indice_real is None:
            return
        else:
            if acao == "remover":
                remover_tarefa(indice_real, lista_tarefas)
            elif acao == "concluir":
                concluir_tarefa(indice_real, lista_tarefas)

    elif acao == "adicionar":
        texto = campo_texto.get().strip()
        adicionar_tarefa(texto, lista_tarefas)
        campo_texto.delete(0, tk.END)
        campo_texto.focus()
    else:
        return
    atualizar_botao_filtro(botoes_filtro)
    renderizar_tela(list_box, status_ativo, lista_tarefas)


def botao_filtro(status, list_box):
    print(f"Testando o Keyrelease {status} e {list_box}")
    global status_ativo
    status_ativo = status
    renderizar_tela(list_box, status_ativo, lista_tarefas)
    return


def atualizar_botao_filtro(botoes_filtro):
    for chave, valor in botoes_filtro.items():
        botao0 = filtrar_tarefas(chave, lista_tarefas)
        valor.config(text=f"{chave} ({len(botao0[0])})")


def fluxo_alterar(indice_real, entrada, popup, list_box):
    entrada_str = entrada.get().strip()
    if not entrada_str:
        return
    alterar_tarefa(entrada_str, indice_real, lista_tarefas)
    renderizar_tela(list_box, status_ativo, lista_tarefas)
    popup.destroy()


def filtrar_tarefas(status, lista):
    indices_filtrados, tarefas_filtradas = filtro(status, lista)
    return indices_filtrados, tarefas_filtradas


def pesquisa(texto, list_box):
    texto_busca = []
    if texto != "":
        for tarefa in lista_tarefas:
            if texto.lower() in tarefa["texto"].lower():
                texto_busca.append(tarefa)
        renderizar_tela(list_box, status_ativo, texto_busca)
    else:
        renderizar_tela(list_box, status_ativo, lista_tarefas)


def renderizar_tela(list_box, status, lista_tarefas):
    indices_filtrados, tarefas_filtradas = filtrar_tarefas(
        status, lista_tarefas)
    indices_visiveis.clear()
    indices_visiveis.extend(indices_filtrados)
    list_box.delete(0, tk.END)
    texto_list_box(tarefas_filtradas, list_box)
    return indices_filtrados


def interface_popup(root, list_box):

    indice_real = indice_selecao(list_box)
    if indice_real is None:
        return

    tarefa = obter_texto_tarefa(indice_real, lista_tarefas)

    popup = tk.Toplevel(root)
    popup.title("Editar Tarefa")
    popup.geometry("200x100")

    tk.Label(popup, text="Alterar tarefa").pack(pady=3)

    entrada = tk.Entry(popup)
    entrada.insert(0, tarefa)
    entrada.pack(padx=5, anchor=tk.CENTER, fill="x")
    entrada.bind("<Return>", lambda e: fluxo_alterar(
        indice_real, entrada, popup, list_box))

    botao_salvar = tk.Button(popup, text="Salvar",
                             command=lambda: fluxo_alterar(
                                 indice_real, entrada, popup, list_box))
    botao_salvar.pack(pady=5, padx=5, anchor=tk.CENTER, fill="x")


def iniciar_app():

    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x450")

    janela = ttk.Frame(root)
    list_box = tk.Listbox(janela)

    janela.pack(fill="both", expand=True, padx=10, pady=10)

    titulo = ttk.Label(janela, text="Gerenciador de Tarefas")
    titulo.pack(padx=10, pady=10, anchor=tk.CENTER)

    campo_pesquisa = tk.Entry(janela)
    campo_pesquisa.insert(0, "Buscar tarefa...")
    campo_pesquisa.pack(pady=5, fill="x")
    campo_pesquisa.bind("<FocusIn>",
                        lambda e: campo_pesquisa.delete(0, tk.END))
    campo_pesquisa.bind("<KeyRelease>",
                        lambda e: pesquisa(campo_pesquisa.get(), list_box))

    frame_campo_inserir = tk.Frame(janela)
    frame_campo_inserir.pack(pady=5, fill="x")

    campo_texto = ttk.Entry(frame_campo_inserir)
    campo_texto.insert(0, "Digite uma nova tarefa")
    campo_texto.pack(fill="x")
    campo_texto.bind("<FocusIn>", lambda e: campo_texto.delete(0, tk.END))
    campo_texto.bind("<Return>",
                     lambda e: acao_tarefa(
                         list_box,
                         "adicionar", campo_texto, botoes_filtro))

    botao_inserir_tarefa = ttk.Button(
        frame_campo_inserir, text="Inserir", command=lambda: acao_tarefa(
                         list_box, "adicionar", campo_texto, botoes_filtro))
    botao_inserir_tarefa.pack(pady=1, fill="x")

    frame_botoes_filtro = tk.Frame(janela)
    frame_botoes_filtro.pack(pady=5)

    botao_todas = ttk.Button(
        frame_botoes_filtro, text="Todas",
        command=lambda: botao_filtro("Todas", list_box))
    botao_todas.pack(side=tk.LEFT)

    botao_concluidas = ttk.Button(
        frame_botoes_filtro, text="Concluidas",
        command=lambda: botao_filtro("Concluidas", list_box))
    botao_concluidas.pack(side=tk.LEFT)

    botao_pendentes = ttk.Button(
        frame_botoes_filtro, text="Pendentes",
        command=lambda: botao_filtro("Pendentes", list_box))
    botao_pendentes.pack(side=tk.LEFT)

    list_box.pack(pady=10, fill="both", expand=True)

    botoes_filtro = {
        "Todas": botao_todas,
        "Concluidas": botao_concluidas,
        "Pendentes": botao_pendentes
        }

    atualizar_botao_filtro(botoes_filtro)
    renderizar_tela(list_box, "Todas", lista_tarefas)

    frame_botoes_editar = tk.Frame(janela)
    frame_botoes_editar.pack(pady=5)

    botao_remover_tarefa = ttk.Button(
        frame_botoes_editar, text="Remover",
        command=lambda: acao_tarefa(
            list_box, "remover", campo_texto, botoes_filtro))
    botao_remover_tarefa.pack(side=tk.LEFT)

    botao_alterar_tarefa = ttk.Button(
        frame_botoes_editar, text="Alterar",
        command=lambda: interface_popup(root, list_box))
    botao_alterar_tarefa.pack(side=tk.RIGHT)

    botao_concluir_tarefa = ttk.Button(
        janela, text="Concluir",
        command=lambda: acao_tarefa(
            list_box, "concluir", campo_texto, botoes_filtro))
    botao_concluir_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
