import PySimpleGUI as sg

### Inclusoes ###

import os
import sqlite3

directorio_corrente = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(directorio_corrente, 'database.db')

conexao = sqlite3.connect(db_path)
query = ('''CREATE TABLE IF NOT EXISTS SUPLEMENTO (LOTE CHAR(10), PRODUTO TEXT, FORNECEDOR TEXT)''')
conexao.execute(query)
conexao.close()
#####

dados =[]
Titulos = ['Lote', 'Produto', 'Fornecedor']

layout = [
        [sg.Text(Titulos[0]), sg.Input(size= 5, key=Titulos[0])],
        [sg.Text(Titulos[1]), sg.Input(size= 20, key=Titulos[1])], 
        [sg.Text(Titulos[2]), sg.Combo(['Fornecedo 1', 'Fornecedor 2', 'Fornecedor 3'], key=Titulos[2])],
        [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Salvar'), sg.Button('Excluir'), sg.Exit('Sair')],
        [sg.Table(dados, Titulos, key='tabela')]
        ]

window = sg.Window('Sistema de Gerenciamento  de Suplementos', layout)

while True:
    event, values = window.read()
    print(values)

    if event == 'Adicionar':
        dados.append([values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]])
        window['tabela'].update(values=dados)
        for i in range(3): #limpa as caixa de texto
            window[Titulos[i]].update(value='')

        conexao = sqlite3.connect(db_path)
        conexao.execute("INSERT INTO SUPLEMENTO (LOTE, PRODUTO, FORNECEDOR) VALUES (?,?,?)", ([values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]]))
        conexao.commit()
        conexao.close()

    if event == 'Editar':
        if values['tabela']==[]:
            sg.popup('Nenhuma linha selecionada')
        else:
            editarLinha = values['tabela'][0]
            sg.popup('Editar linha selecionada')
            for i in range(3):
                window[Titulos[i]].update(value=dados[editarLinha][i])
            window['Salvar'].update(disable=False)
    if event == 'Salvar':
        dados[editarLinha]=[values[Titulos[0]], values[Titulos[1]], values[Titulos[2]]]
        window['tabela'].update(values=dados)
        for i in range(3):
            window[Titulos[i]].update(value='')
        window['Salvar'].update(disable=True)

        conexao = sqlite3.connect(db_path)
        conexao.execute("UPDATE SUPLEMENTO set PRODUTO = ?, FORNECEDOR = ? where LOTE = ?", ([values[Titulos[1]], values[Titulos[2]], values[Titulos[0]]]))
        conexao.commit()
        conexao.close()

    if event == 'Excluir':
        if values['tabela']==[]:
            sg.popup('Nenhuma Linha Selecionada')
        else:
            if sg.popup_ok_cancel('Está operação não pode ser desfeita, confirma?') == 'OK':

                conexao = sqlite3.connect(db_path)
                conexao.execute("DELETE FROM SUPLEMENTO WHERE LOTE = ?", ([values[Titulos[0]]]))
                conexao.close()

                del dados[values['tabela'][0]]
                window['tabela'].update(values=dados)

    if event in (sg.WIN_CLOSED, 'Sair'):
        break
    
window.close()