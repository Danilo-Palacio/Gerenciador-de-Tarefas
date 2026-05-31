import tkinter as tk
from tkinter import ttk
from tarefas import remover_tarefa, adicionar_tarefa, alterar_tarefa, filtro
from tarefas import carregar_lista, concluir_tarefa, obter_texto_tarefa

lista_tarefas = carregar_lista()
indices_visiveis = []
tarefas_visiveis = []


def texto_list_box(lista, list_box):
    print("função texto_list_box")
    print("Alterou o list_box")
    print(f"A lista enviada foi: {lista}")
    for tarefa in lista:
        concluida = tarefa["concluida"]
        if not concluida:
            texto = "[  ]"
        else:
            texto = "[X]"
        texto_completo = f"{texto} {tarefa['texto']}"
        list_box.insert(tk.END, texto_completo)


status_ativo = "Todas"
print(f'ultimo_status: {status_ativo}')


def indice_selecao(list_box):
    print("função: indice_selecao")
    indice_escolhido = list_box.curselection()
    indice_real = indices_visiveis[indice_escolhido[0]]
    return indice_real


def acao_tarefa(list_box, lista_tarefas, acao, campo_texto):
    print("função: acao_tarefa")
    if acao != "adicionar":
        indice_real = indice_selecao(list_box)
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
    renderizar_tela(list_box, atualizar, status_ativo)


def atualizar(entrada, indice_real, lista_tarefas, list_box):
    print("função: atualizar")
    entrada_str = entrada.get().strip()
    atualizar = alterar_tarefa(entrada_str, indice_real, lista_tarefas)
    renderizar_tela(list_box, atualizar, status_ativo)


def alterar(entrada, indice_real):
    print("função: alterar")
    if not entrada:
        return
    alterar_tarefa(entrada, indice_real, lista_tarefas)


def fluxo_alterar(indice_real, entrada, popup, list_box):
    print("função: fluxo_alterar")
    entrada_str = entrada.get().strip()
    alterar(entrada_str, indice_real)
    renderizar = renderizar_tela(list_box, lista_tarefas, status_ativo)
    popup.destroy()
    return renderizar


def renderizar_tela(list_box, lista_tarefa, status_ativo):
    status_ativo = status_ativo
    print("função: renderizar_tela")
    print(f'ultimo_status: {status_ativo}')
    tarefas_filtradas, indices_filtrados = filtro(status_ativo, lista_tarefa)
    indices_visiveis.clear()
    indices_visiveis.extend(indices_filtrados)
    tarefas_visiveis.append(tarefas_filtradas)
    list_box.delete(0, tk.END)
    texto_list_box(tarefas_filtradas, list_box)
    return len(indices_filtrados)


def interface_popup(root, list_box):
    print("função: interface_popup")
    indice_escolhido = indice_selecao(list_box)
    tarefa = obter_texto_tarefa(indice_escolhido, lista_tarefas)

    popup = tk.Toplevel(root)
    popup.title("Editar Tarefa")
    popup.geometry("200x100")

    tk.Label(popup, text="Alterar tarefa").pack(pady=3)

    entrada = tk.Entry(popup)
    entrada.insert(0, tarefa)
    entrada.pack(padx=5, anchor=tk.CENTER, fill="x")
    entrada.bind("<Return>", lambda e: fluxo_alterar(
        indice_escolhido, entrada, popup))
    botao_salvar = tk.Button(popup, text="Salvar",
                             command=lambda: fluxo_alterar(
                                 indice_escolhido, entrada, popup, list_box))
    botao_salvar.pack(pady=5, padx=5, anchor=tk.CENTER, fill="x")


def iniciar_app():
    print("função: iniciar_app")
    root = tk.Tk()
    root.title("Gerenciador de Tarefas")
    root.geometry("300x450")

    janela = ttk.Frame(root)
    list_box = tk.Listbox(janela)

    todas = renderizar_tela(list_box, lista_tarefas, "Todas")
    concluidas = renderizar_tela(list_box, lista_tarefas, "Concluidas")
    pendentes = renderizar_tela(list_box, lista_tarefas, "Pendentes")

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
        command=lambda: renderizar_tela(list_box, lista_tarefas, "Todas"))
    botao_todas.pack(side=tk.LEFT)

    botao_concluidas = ttk.Button(
        frame_botoes_filtro, text=f"Concluidas ({concluidas})",
        command=lambda: renderizar_tela(list_box, lista_tarefas, "Concluidas"))
    botao_concluidas.pack(side=tk.LEFT)

    botao_pendentes = ttk.Button(
        frame_botoes_filtro, text=f"Pendentes ({pendentes})",
        command=lambda: renderizar_tela(list_box, lista_tarefas, "Pendentes"))
    botao_pendentes.pack(side=tk.LEFT)

    list_box.pack(pady=10, fill="both", expand=True)

    renderizar_tela(list_box, lista_tarefas, status_ativo)

    frame_botoes_editar = tk.Frame(janela)
    frame_botoes_editar.pack(pady=5)

    botao_remover_tarefa = ttk.Button(
        frame_botoes_editar, text="Remover",
        command=lambda: acao_tarefa(
            list_box, lista_tarefas, "remover", campo_texto))
    botao_remover_tarefa.pack(side=tk.LEFT)

    botao_alterar_tarefa = ttk.Button(
        frame_botoes_editar, text="Alterar",
        command=lambda: interface_popup(root, list_box))
    botao_alterar_tarefa.pack(side=tk.RIGHT)

    botao_concluir_tarefa = ttk.Button(
        janela, text="Concluir",
        command=lambda: acao_tarefa(
            list_box, lista_tarefas, "concluir", campo_texto))
    botao_concluir_tarefa.pack(pady=5, fill="x")

    botao_sair = ttk.Button(janela, text="Quit", command=root.destroy)
    botao_sair.pack(pady=5, anchor=tk.CENTER, fill="x")

    root.mainloop()
