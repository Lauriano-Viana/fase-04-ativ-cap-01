import oracledb as cx_Oracle
import pandas as pd
import os



def get_leitura(conexao):  # Buscar os dados da última leitura executada
    try:
        cursor = conexao.cursor()

        # Consulta para obter o ID da última leitura
        consulta = """
        SELECT id_leitura 
        FROM leituras
        ORDER BY id_leitura DESC
        """
        cursor.execute(consulta)
        ultima_leitura = cursor.fetchone()

        # Verificar se há alguma leitura na tabela
        if ultima_leitura is None:
            print("Nenhuma leitura encontrada na tabela 'leituras'.")
            cursor.close()
            return None

        id_leitura = ultima_leitura[0]
        # print(f"Último id_leitura encontrado: {id_leitura}")

        # Obter os dados completos da última leitura
        consulta = f"""
        SELECT * 
        FROM leituras 
        WHERE id_leitura = :id_leitura
        """
        cursor.execute(consulta, {"id_leitura": id_leitura})
        leitura = cursor.fetchone()

        cursor.close()

        # Verificar se os dados foram encontrados
        if leitura is None:
            print(f"Nenhuma leitura encontrada para id_leitura = {id_leitura}.")
            return None

        return leitura

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao verificar leitura: {e}")
        return None

    except Exception as e:
        print(f"get_leitura: Erro desconhecido: {e}")
        return None

    

def get_cultura(conexao, id_cultura):
    """Buscar dados referentes à cultura da leitura."""
    try:    
        cursor = conexao.cursor()

        # Consulta usando parâmetros para evitar SQL Injection
        consulta = """
        SELECT nivel_p, nivel_k, nivel_ph, umidade 
        FROM culturas 
        WHERE id_cultura = :id_cultura
        """
        cursor.execute(consulta, {"id_cultura": id_cultura})
        cultura = cursor.fetchone()

        cursor.close()

        if cultura is None:
            print(f"Nenhuma cultura encontrada para id_cultura = {id_cultura}.")
            return None

        return cultura

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao verificar cultura: {e}")
        return None

    except Exception as e:
        print(f"Erro desconhecido em get_cultura: {e}")
        return None

    
def verificar_nutrientes(cultura, leitura):
    """Verificar se os nutrientes da leitura estão abaixo dos níveis ideais da cultura."""
    if leitura is None:
        print("Erro: Leitura é None. Não é possível verificar nutrientes.")
        return None

    if len(leitura) < 7:  # Validar o tamanho esperado da tupla leitura
        print(f"Erro: Leitura incompleta. Dados recebidos: {leitura}")
        return None

    if cultura is None:  # Garantir que os dados da cultura existem
        print("Erro: Cultura é None. Não é possível verificar nutrientes.")
        return None

    # Dados da leitura
    valor_p = leitura[3]
    valor_k = leitura[4]
    valor_ph = leitura[5]
    valor_umidade = leitura[6]

    # Dados da cultura
    nivel_p, nivel_k, nivel_ph, nivel_umidade = cultura

    # Tempo padrão de irrigação
    tempo = 2000  
    

    # Verificar se algum valor está abaixo do nível esperado
    if any(valor < nivel for valor, nivel in 
           [(valor_p, nivel_p), (valor_k, nivel_k), (valor_ph, nivel_ph), (valor_umidade, nivel_umidade)]):
        tempo = 3000  # Ajustar tempo para maior irrigação

    return tempo



def deletar_irrigacao(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados
        id_irrigacao = int(input('Informe o id da irrigacao a ser deletada'))
        cursor = conexao.cursor()
        consulta = f""" SELECT * FROM irrigacoes WHERE id_irrigacao = {id_irrigacao}"""
        cursor.execute(consulta)
        data = cursor.fetchall()

        for dt in data:
            lista_dados.append(dt)
        
        if len(lista_dados)==0:
            print(f'Não há uma irrigacao cadastrada com o ID = {id_irrigacao}')
        else:
            exclusao = f"""DELETE FROM irrigacoes WHERE id_irrigacao = {id_irrigacao} """
            cursor.execute(exclusao)
            conexao.commit()
            print(f"Leitura {id_irrigacao} deletado com sucesso.")
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao deletar leitura: {e}")
    except ValueError:
        print(' Digite um número no "Id!" ')
    input(' Pressione qualquer tecla para continuar')

# Função para listar irrigacoes
def listar_irrigacoes(conexao):
    try:
        os.system('clear')
        lista_dados = [] #lista para captura de dados 
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM irrigacoes")
        #Captura os registros e armazena no obj culturas
        irrigacoes = cursor.fetchall()
        for irrigacao in irrigacoes:
            lista_dados.append(irrigacao)
        lista_dados = sorted(lista_dados)
        # Gera um Dataframe com os dados da lista usando o Pandas
        dados_df = pd.DataFrame.from_records(lista_dados, columns = ['Id', 'id_cultura', 'id_leitura', 'tempo', 'motivo', 'data_aplicacao'], 
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



def aplicar_irrigacao(conexao):
    """Função para aplicar irrigação baseada nos dados de leitura e cultura."""
    try:
        cursor = conexao.cursor()

        # Obter a última leitura
        leitura = get_leitura(conexao)
        if leitura is None:
            print("Erro: Nenhuma leitura disponível.")
            return

        # Extrair valores da leitura
        id_leitura = leitura[0]
        id_cultura = leitura[1]

        # Obter dados da cultura
        cultura = get_cultura(conexao, id_cultura)
        if cultura is None:
            print(f"Erro: Cultura não encontrada para id_cultura = {id_cultura}")
            return

        # Verificar nutrientes e calcular o tempo
        tempo = verificar_nutrientes(cultura, leitura)
        if tempo is None:
            print("Erro: Não foi possível calcular o tempo de irrigação.")
            return

        # Decidir o motivo com base no tempo
        motivo = (
            f'Nível de nutrientes: BAIXO, tempo de irrigação mais longo {tempo/1000:.2f} segundos'
            if tempo > 2000
            else f'Nível de nutrientes: NORMAL, tempo de irrigação {tempo/1000:.2f} segundos'
        )

        # Inserir dados de irrigação no banco de dados
        consulta = """
            INSERT INTO irrigacoes 
            (id_irrigacao, id_cultura, id_leitura, tempo, motivo, data_aplicacao) 
            VALUES (seq_irrigacoes.NEXTVAL, :id_cultura, :id_leitura, :tempo, :motivo, SYSDATE)
        """
        cursor.execute(
            consulta,
            {
                "id_cultura": id_cultura,
                "id_leitura": id_leitura,
                "tempo": tempo,
                "motivo": motivo,
            }
        )

        # Confirmar as alterações
        conexao.commit()
        print(f"\nIrrigação aplicada com sucesso: \nTempo = {tempo} ms \n Motivo = '{motivo}'")

    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao aplicar irrigação: {e}")

    except Exception as e:
        print(f"Erro desconhecido em aplicar_irrigacao: {e}")

    finally:
        # Garantir o fechamento do cursor
        cursor.close()


def menu_irrigacao(conexao,conectado):
    while conectado:
        os.system('clear')
        print('-----------Operacoes Irrigacao-----------------')
        print("""
        1 - Listar Irrigacoes
        2 - Excluir Irrigacao
        3 - Menu Inicial
        """)
        escolha = input('Escolha -> ')

        if escolha.isdigit():
            escolha = int(escolha)
        else:
            escolha = 3
            print('Digite um numero.\nReinicie a Aplicação!')
        os.system('clear')
        match escolha:
            case 1:
                listar_irrigacoes(conexao)
            case 2:
                deletar_irrigacao(conexao)
            case 3:
                conectado = False
            case _:
                input('Digite um numero entre 1 e 3.')