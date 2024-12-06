#importar as bibliotecas oracle e pandas

import oracledb as cx_Oracle
import pandas as pd
import os

'''Operações referente a sensores'''
# Função para criar um novo sensor
def criar_sensor(conexao):
    try:
        cursor = conexao.cursor()
        print('-------------CADASTRAR SENSOR------------------\n')
        tipo = input('Digite o tipo de sensor......: ')
        tipo = tipo.upper()
        descricao = input(' Digite uma breve descrição para o sensor:   ')
        localizacao = input(' Digite a localizacao do sensor:   ')

        cadastro = f""" 
            INSERT INTO sensores (id_sensor,tipo, descricao, localizacao) 
            VALUES (seq_sensores.NEXTVAL,'{tipo}', '{descricao}','{localizacao}')
            """
        cursor.execute(cadastro)
        conexao.commit()
        cursor.close()
        print('\n Sensor cadastrado com sucesso')
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar sensor: {e}")        
    input(' Pressione enter para continuar')



# Função para ler sensores
def listar_sensores(conexao):
    try:

        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM sensores")
        #Captura os registros e armazena no obj sensores
        sensores = cursor.fetchall()
        for sensor in sensores:
            lista_dados.append(sensor)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id','Tipo','Descricao',  'Localizacao'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há sensores cadastrados!!')
        else:
            print(dados_df)
        print('\nLISTADOS!')
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao ler sensores: {e}")
    input(' Pressione enter para continuar')



# Função para atualizar um sensor
def alterar_sensor(conexao):
    try:
        
        print('------------Alterar dados do sensor')
        lista_dados = [] #lista para captura de dados 
        id_sensor = int(input('Informe o id sensor a ser alterado....:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há um sensor cadastrado com o ID = {id_sensor}')
        else:
            # Captura os novos dados
            novo_tipo = input('Digite o tipo de sensor......:    ')
            nova_descricao = input(' Digite uma breve descrição para o sensor: \n')
            nova_localizacao = input(' Digite a localizacao do sensor........:   ')

            alteracao = f""" UPDATE sensores SET 
                tipo='{novo_tipo}', 
                descricao='{nova_descricao}', 
                localizacao='{nova_localizacao}' 
                            """
            cursor.execute(alteracao)
            conexao.commit()
            cursor.close()
        
        print(f"Sensor {id_sensor} atualizado com sucesso.")
   
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao atualizar sensor: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')


# Função para deletar um sensor
def deletar_sensor(conexao):
    try:
        lista_dados = [] #lista para captura de dados
        id_sensor = int(input('Informe o id do sensor a ser deletado:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM sensores WHERE id_sensor = {id_sensor}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
     
        if len(lista_dados)==0:
            print(f'Não há um sensor cadastrado com o ID = {id_sensor}')
        else:
            exclusao = f"""DELETE FROM sensores WHERE id_sensor = {id_sensor} """
            cursor.execute(exclusao)
            conexao.commit()
            cursor.close()
            print(f"Sensor {id_sensor} deletado com sucesso.")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar sensor: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')



# Função para criar um Menu para sensores
def menu_sensor(conexao,conectado):
    
    while conectado:
        os.system('clear')
        print('-----------Operacoes Sensores-----------------')
        print("""
        1 - Cadastrar Sensor
        2 - Listar Sensores
        3 - Alterar Sensor
        4 - Excluir Sensor
        5 - Menu Inicial
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
                criar_sensor(conexao)
            case 2:
                listar_sensores(conexao)
            case 3:
                alterar_sensor(conexao)
            case 4:
                deletar_sensor(conexao)
            case 5:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')