from conection import conectar_banco
from sensor import menu_sensor
from leitura import menu_leitura
from cultura import menu_cultura
from irrigacao import menu_irrigacao

import os


# Função principal para executar o CRUD
def main():
    
    conexao,conectado = conectar_banco()
    while conectado:
        os.system('clear')
        print('-----------Controle Irrigação-----------------')
        print("""
        1 - Sensores
        2 - Leituras
        3 - culturas
        4 - Irrigacao        
        5 - Sair
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 5
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                menu_sensor(conexao,conectado)
            case 2:
                menu_leitura(conexao,conectado)
            case 3:
                menu_cultura(conexao,conectado)
            case 4:
                menu_irrigacao(conexao,conectado)
            case 5:
                conexao.close()
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')
    else:
        print('Obrigado, por utilizar a nossa Aplicação! :)')
       
 
   

if __name__ == "__main__":
    main()