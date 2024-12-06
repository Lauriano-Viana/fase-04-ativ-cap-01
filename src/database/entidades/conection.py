import oracledb as cx_Oracle
# Função para conectar ao banco de dados Oracle
def conectar_banco():
    try:
        #Conecta o servidor
        dsnStr = cx_Oracle.makedsn("oracle.fiap.com.br", "1521","ORCL")

        # Efetua a conexão com o Usuário no servidor
        conexao = cx_Oracle.connect(user='rm559475', password="DtNasc#081279", dsn=dsnStr)
        print("Conectado ao banco de dados Oracle")
        conectado = True
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        conectado = False
    else:
        return conexao,conectado
    