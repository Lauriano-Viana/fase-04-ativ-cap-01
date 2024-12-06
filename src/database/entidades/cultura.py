import oracledb as cx_Oracle
import pandas as pd
import os

'''Operações referente a culturas'''
# Função para criar um novo cultura
def criar_cultura(conexao):
    try:
        os.system('clear')
        cursor = conexao.cursor()
        print('-------------CADASTRAR CULTURA------------------\n')
        nome = input('Digite o nome do cultura......: ')
        print(f'Para cultura de {nome} informe os niveis ideais de:')
        nivel_p = float(input('Fosforo: '))
        nivel_k = float(input('Potassio: '))
        # Validação para nivel_ph entre 0 e 14
        while True:
            nivel_ph = float(input('Digite o valor de pH do solo (0 a 14): '))
            if 0 <= nivel_ph <= 14:
                break
        umidade = float(input('Umidade: '))
        
        cadastro = f""" 
            INSERT INTO culturas (id_cultura, nome, nivel_p, nivel_k, nivel_ph, umidade ) 
            VALUES (seq_culturas.NEXTVAL,'{nome}', {nivel_p}, {nivel_k},
                    {nivel_ph},{umidade})            
                    """
        cursor.execute(cadastro)
        conexao.commit()
        cursor.close()
        print('\n cultura cadastrado com sucesso')
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao criar cultura: {e}")
    input(' Pressione enter para continuar')



# Função para ler culturas
def listar_culturas(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM culturas")
        #Captura os registros e armazena no obj culturas
        culturas = cursor.fetchall()
        for cultura in culturas:
            lista_dados.append(cultura)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id', 'nome', 'nivel_p', 'nivel_k', 'nivel_ph', 'umidade'], 
                                             index ='Id')
        if dados_df.empty:
            print(f'Não há culturas cadastrados!!')
        else:
            print(dados_df)
        print('\nLISTADOS!')
        cursor.close()

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao ler culturas: {e}")
    input(' Pressione enter para continuar')



# Função para atualizar um cultura
def alterar_cultura(conexao):
    try:
        os.system('clear')
        print('------------Alterar dados do cultura')
        lista_dados = [] #lista para captura de dados 
        id_cultura = int(input('Informe o id do cultura a ser alterado....:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM culturas WHERE id_cultura = {id_cultura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há um cultura cadastrada com o ID = {id_cultura}')
        else:
            # Captura os novos dados
            nome = input('Digite o nome do cultura......: ')
            print(f'Para cultura de {nome} informe os niveis ideais de:')
            nivel_p = float(input('Fosforo: '))
            nivel_k = float(input('Potassio: '))
            nivel_ph = float(input('Ph do Solo: '))
            umidade = float(input('Umidade: '))

            alteracao = f""" UPDATE culturas SET nome='{nome}',
                        nivel_p={nivel_p},  
                        nivel_k={nivel_k}, 
                        nivel_ph={nivel_ph},
                        umidade={umidade}
                        """
        
            cursor.execute(alteracao)
            conexao.commit()
            cursor.close()
            print(f"cultura {id_cultura} atualizado com sucesso.")
   
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao atualizar cultura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')



# Função para deletar um cultura
def deletar_cultura(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_cultura = int(input('Informe o id do cultura a ser deletado:   '))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM culturas WHERE id_cultura = {id_cultura}"""
        cursor.execute(consulta)
        data = cursor.fetchall()
        for dt in data:
            lista_dados.append(dt)
     
        if len(lista_dados)==0:
            print(f'Não há um cultura cadastrado com o ID = {id_cultura}')
        else:
            exclusao = f"""DELETE FROM culturas WHERE id_cultura = {id_cultura} """
            cursor.execute(exclusao)
            conexao.commit()
            cursor.close()
            print(f"cultura {id_cultura} deletado com sucesso.")
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar cultura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione enter para continuar')



# Função para criar um Menu para cultura
def menu_cultura(conexao,conectado):
    os.system('clear')
    while conectado:
        print('-----------Operacoes Cultura-----------------')
        print("""
        1 - Cadastrar cultura
        2 - Listar cultura
        3 - Alterar cultura
        4 - Excluir cultura
        5 - Menu inicial
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
                criar_cultura(conexao)
            case 2:
                listar_culturas(conexao)
            case 3:
                alterar_cultura(conexao)
            case 4:
                deletar_cultura(conexao)
            case 5:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 5.')