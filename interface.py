import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tarefas import remover_tarefa, adicionar_tarefa, alterar_tarefa, filtro
from tarefas import carregar_lista, concluir_tarefa, obter_texto_tarefa

lista_tarefas = carregar_lista()
indices_visiveis = []
status_ativo = "Todas"


def renderizar_tela(indice, list_box):
    indices_visiveis.clear()
    list_box.delete(0, tk.END)
    for tarefa in indice:
        concluida = lista_tarefas[tarefa]["concluida"]
        if not concluida:
            texto = "  "
        else:
            texto = "X"
        prioridade = lista_tarefas[tarefa]["prioridade"]
        texto_completo = (
            f"[{prioridade}] | [{texto}] "
            f"{lista_tarefas[tarefa]['texto']}"
        )
        list_box.insert(tk.END, texto_completo)
    indices_visiveis.extend(indice)


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


def acao_tarefa(list_box, acao, campo_texto, botoes_filtro, combo_prioridade):
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
        prioridade = combo_prioridade.get("prioridade", "Baixa")
        texto = campo_texto.get().strip()
        adicionar_tarefa(texto, lista_tarefas, prioridade)
        campo_texto.delete(0, tk.END)
        campo_texto.focus()
    else:
        return
    atualizar_botao_filtro(botoes_filtro)
    chamar_filtro(status_ativo, list_box)


def chamar_filtro(status, list_box):
    global status_ativo
    status_ativo = status
    indices_filtrados = filtrar_tarefas(
        status, lista_tarefas)
    renderizar_tela(indices_filtrados, list_box)
    return indices_filtrados


def atualizar_botao_filtro(botoes_filtro):
    for chave, valor in botoes_filtro.items():
        botao0 = filtrar_tarefas(chave, lista_tarefas)
        valor.config(text=f"{chave} ({len(botao0)})")


def fluxo_alterar(indice_real, entrada, popup, list_box, combo_prioridade):
    prioridade = combo_prioridade.get()
    entrada_str = entrada.get().strip()
    if not entrada_str:
        return
    alterar_tarefa(entrada_str, indice_real, lista_tarefas, prioridade)
    chamar_filtro(status_ativo, list_box)
    popup.destroy()


def filtrar_tarefas(status, lista):
    indices_filtrados = filtro(status, lista)
    return indices_filtrados


def pesquisa(texto, list_box):
    indice_busca = []
    indice_status = chamar_filtro(status_ativo, list_box)
    if texto != "":
        for tarefa in indice_status:
            if texto.lower() in lista_tarefas[tarefa]["texto"].lower():
                indice_busca.append(tarefa)
        renderizar_tela(indice_busca, list_box)
    else:
        renderizar_tela(indice_status, list_box)


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
        indice_real, entrada, popup, list_box, combo_prioridade_alterar))

    combo_prioridade_alterar = ttk.Combobox(
        popup,
        values=['Baixa', 'Média', 'Alta'],
        state='readonly'
    )
    prioridade_atual = lista_tarefas[indice_real].get(
        "prioridade",
        "Baixa"
    )
    combo_prioridade_alterar.set(prioridade_atual)
    combo_prioridade_alterar.pack()

    botao_salvar = tk.Button(popup, text="Salvar",
                             command=lambda: fluxo_alterar(
                                   indice_real,
                                   entrada,
                                   popup,
                                   list_box,
                                   combo_prioridade_alterar))
    botao_salvar.pack(pady=5, padx=5, anchor=tk.CENTER, fill="x")


def iniciar_app():

    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x500")

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
                         "adicionar",
                         campo_texto,
                         botoes_filtro,
                         combo_prioridade))

    combo_prioridade = ttk.Combobox(
        frame_campo_inserir,
        values=['Baixa', 'Média', 'Alta'],
        state='readonly'
    )
    combo_prioridade.set("Baixa")
    combo_prioridade.pack()

    botao_inserir_tarefa = ttk.Button(
        frame_campo_inserir, text="Inserir", command=lambda: acao_tarefa(
                         list_box,
                         "adicionar",
                         campo_texto,
                         botoes_filtro,
                         combo_prioridade))
    botao_inserir_tarefa.pack(pady=1, fill="x")

    frame_botoes_filtro = tk.Frame(janela)
    frame_botoes_filtro.pack(pady=5)

    botao_todas = ttk.Button(
        frame_botoes_filtro, text="Todas",
        command=lambda: chamar_filtro("Todas", list_box))
    botao_todas.pack(side=tk.LEFT)

    botao_concluidas = ttk.Button(
        frame_botoes_filtro, text="Concluidas",
        command=lambda: chamar_filtro("Concluidas", list_box))
    botao_concluidas.pack(side=tk.LEFT)

    botao_pendentes = ttk.Button(
        frame_botoes_filtro, text="Pendentes",
        command=lambda: chamar_filtro("Pendentes", list_box))
    botao_pendentes.pack(side=tk.LEFT)

    list_box.pack(pady=10, fill="both", expand=True)

    botoes_filtro = {
        "Todas": botao_todas,
        "Concluidas": botao_concluidas,
        "Pendentes": botao_pendentes
        }

    atualizar_botao_filtro(botoes_filtro)
    chamar_filtro(status_ativo, list_box)

    frame_botoes_editar = tk.Frame(janela)
    frame_botoes_editar.pack(pady=5)

    botao_remover_tarefa = ttk.Button(
        frame_botoes_editar, text="Remover",
        command=lambda: acao_tarefa(
            list_box,
            "remover",
            campo_texto,
            botoes_filtro,
            None))
    botao_remover_tarefa.pack(side=tk.LEFT)

    botao_alterar_tarefa = ttk.Button(
        frame_botoes_editar, text="Alterar",
        command=lambda: interface_popup(root, list_box))
    botao_alterar_tarefa.pack(side=tk.RIGHT)

    botao_concluir_tarefa = ttk.Button(
        janela, text="Concluir",
        command=lambda: acao_tarefa(
            list_box,
            "concluir",
            campo_texto,
            botoes_filtro,
            None))
    botao_concluir_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
