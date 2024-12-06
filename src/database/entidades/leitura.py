import oracledb as cx_Oracle
import pandas as pd
import os
from irrigacao import *

def check_cultura(conexao): # Verifica se a cultura está cadastrado
      
        id = int(input(f' Digite o id da cultura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT id_cultura FROM culturas WHERE id_cultura = {id}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            msg = f'Não há uma cultura cadastrada com o ID = {id}'
        else:    
            return id,msg



def check_sensor(conexao): # Verifica se o sensor está cadastrado
    try:
        id_sensor = int(input(f' Digite o id do sensor da leitura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            msg = f'Não há um sensor cadastrado com o ID = {id_sensor}' 
            id_sensor = 0  
        # cursor.close()
        return id_sensor, msg
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao verificar sensor: {e}")
    except ValueError:
        print(' Digite somente numero(s) no(s) campo(s) solicitado(s) ')
    except:
        print('check_sensor: Erro desconhecido')
    input(' Pressione enter para continuar')   
       


'''Operações referente as leituras'''
# Função para criar um nova Leitura
def criar_leitura(conexao):
    try:
        os.system('clear')
        print('-------------CADASTRAR LEITURA------------------\n')
        cursor = conexao.cursor()

        id_cultura = int(input(f' Digite o id da cultura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT id_cultura FROM culturas WHERE id_cultura = {id_cultura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            print(f'Não há uma cultura cadastrada com o ID = {id}')
            id_cultura = 0
        
        id_sensor = int(input(f' Digite o id do sensor da leitura:   '))
        lista_dados = [] #lista para captura de dados
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
        if len(lista_dados)==0:
            print(f'Não há um sensor cadastrado com o ID = {id_sensor}')
            id_sensor = 0
        if  (id_sensor) and (id_cultura):            
            valor_p = float(input(' Digite a valor de Fosforo (P):   '))
            valor_k = float(input(' Digite a valor de Potassio(K):   '))
            # Validação para valor_ph entre 0 e 14
            while True:
                valor_ph = float(input('Digite o valor de pH do solo (0 a 14): '))
                if 0 <= valor_ph <= 14:
                    break
                print("Erro: O valor de pH deve estar no intervalo de 0 a 14. Tente novamente.")
            valor_umidade = float(input(' Digite a valor de umidade:   '))
            valor_temperatura = float(input(' Digite a valor de umidade:   '))
            cadastro = f"""
                INSERT INTO leituras (id_leitura,id_cultura,id_sensor, leit_p,leit_k,leit_ph,leit_umidade,leit_temperatura,data_leitura)
                VALUES (seq_leituras.NEXTVAL,{id_cultura},{id_sensor},{valor_p},{valor_k},{valor_ph},{valor_umidade},{valor_temperatura}, SYSDATE)
                
            """            
            cursor.execute(cadastro)
            conexao.commit()
            cursor.close()
            print('Leitura criada com sucesso!!')
              

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar leitura: {e}")
    except ValueError:
        print(' Digite somente numero(s) no(s) campo(s) solicitado(s) ')
    except:
        print('criar_leit: Erro desconhecido')
    input(' Pressione enter para continuar')

# Função para listar leituras
def listar_leituras(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM leituras")
        #Captura os registros e armazena no obj leituras
        leituras = cursor.fetchall()
        for leitura in leituras:
            lista_dados.append(leitura)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','id_cultura','id_sensor','valor_p','valor_k','valor_ph','valor_umidade','valor_temperatura','data_leitura'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há leituras cadastradas!!')
        else:
            print(dados_df)
        print('\nLISTADOS!')       
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao ler leituras: {e}")
    input(' Pressione enter para continuar')


# Função para deletar um sensor
def deletar_leitura(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_leitura = int(input('Informe o id da leitura a ser deletada'))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM leituras WHERE id_leitura = {id_leitura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há uma leitura cadastrada com o ID = {id_leitura}')
        else:
            exclusao = f"""DELETE FROM leituras WHERE id_leitura = {id_leitura} """
            cursor.execute(exclusao)
            conexao.commit()
            print(f"Leitura {id_leitura} deletado com sucesso.")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione qualquer tecla para continuar')

# Função para criar um Menu para Leituras
def menu_leitura(conexao, conectado):
    while conectado:
        os.system('clear')
        print('----------- Operações Leitura -----------------')
        print("""
        1 - Cadastrar Leitura
        2 - Listar Leituras
        3 - Excluir Leitura
        4 - Menu Inicial
        """)
        escolha = input('Escolha -> ')

        if not escolha.isdigit():  # Verificar se a entrada é um número
            print("Erro: Você deve digitar um número.\nReinicie a aplicação!")
            escolha = 4  # Retornar ao menu inicial
        else:
            escolha = int(escolha)

        os.system('clear')

        match escolha:
            case 1:
                try:
                    criar_leitura(conexao)  # Criar uma nova leitura
                    #print("Leitura cadastrada com sucesso.")
                    aplicar_irrigacao(conexao)  # Chamar função para aplicar irrigação
                except Exception as e:
                    print(f"Erro ao cadastrar leitura ou aplicar irrigação: {e}")
                input("Pressione Enter para continuar...")
            case 2:
                try:
                    listar_leituras(conexao)  # Listar todas as leituras
                except Exception as e:
                    print(f"Erro ao listar leituras: {e}")
                input("Pressione Enter para continuar...")
            case 3:
                try:
                    deletar_leitura(conexao)  # Excluir uma leitura
                except Exception as e:
                    print(f"Erro ao excluir leitura: {e}")
                input("Pressione Enter para continuar...")
            case 4:
                conectado = False  # Sair do menu
            case _:
                print("Erro: Opção inválida. Escolha um número entre 1 e 4.")
                input("Pressione Enter para continuar...")

