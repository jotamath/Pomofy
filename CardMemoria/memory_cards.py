import sqlite3
import random
import flet as ft

def criar_banco_de_dados():
    conn = sqlite3.connect('CardMemoria/cartoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cartoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT,
            pergunta TEXT,
            resposta TEXT,
            dificuldade TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_cartao_bd(categoria, pergunta, resposta, dificuldade):
    conn = sqlite3.connect('CardMemoria/cartoes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cartoes (categoria, pergunta, resposta, dificuldade)
        VALUES (?, ?, ?, ?)
    ''', (categoria, pergunta, resposta, dificuldade))
    conn.commit()
    conn.close()

def recuperar_cartoes_bd(categoria):
    conn = sqlite3.connect('CardMemoria/cartoes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM cartoes WHERE categoria = ?', (categoria,))
    cartoes = cursor.fetchall()
    conn.close()
    return cartoes

def main_memory_cards(page: ft.Page):
    criar_banco_de_dados()

    def adicionar_cartao(e):
        categoria = categoria_input.value
        pergunta = pergunta_input.value
        resposta = resposta_input.value
        if categoria and pergunta and resposta:
            adicionar_cartao_bd(categoria, pergunta, resposta, "Médio")
            categoria_input.value = ""
            pergunta_input.value = ""
            resposta_input.value = ""
            page.update()

    categoria_input = ft.TextField(label="Categoria")
    pergunta_input = ft.TextField(label="Pergunta")
    resposta_input = ft.TextField(label="Resposta")
    adicionar_button = ft.ElevatedButton(text="Adicionar Cartão", on_click=adicionar_cartao)
    aba_criacao_cartoes = ft.Column([
        categoria_input,
        pergunta_input,
        resposta_input,
        adicionar_button
    ])

    def iniciar_sessao(e):
        categoria = categoria_selecao.value
        if categoria:
            cartoes = recuperar_cartoes_bd(categoria)
            if cartoes:
                random.shuffle(cartoes)
                sessao_cartoes.extend(cartoes[:20])
                exibir_proximo_cartao()

    def exibir_proximo_cartao():
        if sessao_cartoes:
            cartao = sessao_cartoes.pop(0)
            pergunta_text.value = cartao[2]
            resposta_text.value = cartao[3]
            resposta_text.visible = False
            page.update()

    def virar_cartao(e):
        resposta_text.visible = True
        page.update()

    def voltar_menu_inicial(e):
        page.clean()
        main(page)

    sessao_cartoes = []
    categoria_selecao = ft.TextField(label="Categoria para Sessão")
    iniciar_sessao_button = ft.ElevatedButton(text="Iniciar Sessão", on_click=iniciar_sessao)
    pergunta_text = ft.Text()
    resposta_text = ft.Text(visible=False)
    virar_button = ft.ElevatedButton(text="Virar", on_click=virar_cartao)
    voltar_button = ft.ElevatedButton(text="Voltar ao Menu Inicial", on_click=voltar_menu_inicial)
    aba_sessao_memorizacao = ft.Column([
        categoria_selecao,
        iniciar_sessao_button,
        pergunta_text,
        virar_button,
        resposta_text,
        ft.Row([
            ft.ElevatedButton(text="Fácil"),
            ft.ElevatedButton(text="Médio"),
            ft.ElevatedButton(text="Difícil")
        ]),
        voltar_button
    ])

    page.add(ft.Tabs(tabs=[
        ft.Tab(text="Criação de Cartões", content=aba_criacao_cartoes),
        ft.Tab(text="Sessão de Memorização", content=aba_sessao_memorizacao)
    ]))
