import numpy as np
import pandas as pd
from src.database.entidades.conection import conectar_banco
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import datetime
import time


class SmartIrrigationSystem:
    def __init__(self, data_file='leituras.csv'):
        """
        Inicialização do sistema de irrigação inteligente com machine learning.
        
        Parâmetros:
        - data_file: Arquivo CSV para armazenar dados históricos.
        """
        self.data_file = data_file
        self.model = None
        self.scaler = StandardScaler()
        
        # Configurações de irrigação
        self.UMIDADE_IDEAL = 65.0  # Umidade ideal para a maioria das culturas
        self.INTERVALO_COLETA = 3600  # Coleta de dados a cada hora
    
    def coletar_dados_sensores(self):
        """
        Simulação da coleta de dados de sensores.
        Em um cenário real, substituir por leitura de sensores físicos.
        """
        # Dados simulados de sensores
        data = {
            'leit_p': np.random.choice([0, 1]),
            'leit_k': np.random.choice([0, 1]),
            'leit_ph': np.random.uniform(5.5, 14.0),
            'leit_umidade': np.random.uniform(40, 80),  # %
            'leit_temperatura': np.random.uniform(20, 35),  # °C
            'data_leitura': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        return data
    
    def salvar_dados(self, dados):
        """
        Salva os dados coletados em um arquivo CSV.
        """
        novo_dado = pd.DataFrame([dados])
        try:
            # Carrega dados existentes e concatena novos dados
            df = pd.read_csv(self.data_file)
            df = pd.concat([df, novo_dado], ignore_index=True)
        except FileNotFoundError:
            # Cria novo DataFrame se arquivo não existir
            df = novo_dado
        
        # Salva no arquivo
        df.to_csv(self.data_file, index=False)
    
    def preparar_dados_treinamento(self):
        """
        Prepara dados para treinamento do modelo de machine learning.
        """
        try:
            df = pd.read_csv(self.data_file)
        except FileNotFoundError:
            raise FileNotFoundError("O arquivo de dados históricos não foi encontrado.")

        # Preparação de features e target
        features = ['leit_p', 'leit_k', 'leit_ph', 'leit_temperatura']
        X = df[features]
        y = df['leit_umidade']
        
        # Divisão de dados de treino 70% e teste 30%
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        # Normalização dos dados
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test
    
    def treinar_modelo(self):
        """
        Treina modelo de Random Forest para previsão de umidade.
        """
        try:
            X_train, X_test, y_train, y_test = self.preparar_dados_treinamento()
        except FileNotFoundError as e:
            print(f"Erro: {e}")
            return
        
        # Inicialização e treinamento do modelo
        self.model = RandomForestRegressor(
            n_estimators=100, 
            random_state=42
        )
        self.model.fit(X_train, y_train)
        
        # Avaliação do modelo
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Métricas do Modelo:")
        print(f"Erro Quadrático Médio: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")
        
        # Salva modelo treinado
        joblib.dump(self.model, 'irrigacao_modelo.pkl')
        joblib.dump(self.scaler, 'irrigacao_scaler.pkl')
    
    def prever_necessidade_irrigacao(self, dados_atuais):
        """
        Prevê a necessidade de irrigação baseado em dados atuais.
        
        Parâmetros:
        - dados_atuais: Dicionário com dados do sensor.
        
        Retorna:
        - Recomendação de irrigação e tempo.
        """
        if self.model is None:
            try:
                # Carrega modelo previamente treinado
                self.model = joblib.load('irrigacao_modelo.pkl')
                self.scaler = joblib.load('irrigacao_scaler.pkl')
            except FileNotFoundError:
                print("Nenhum modelo treinado encontrado. Treine primeiro.")
                return None
        
        # Preparação dos dados para previsão
        features = ['leit_p', 'leit_k', 'leit_ph', 'leit_temperatura']
        dados_previsao = np.array([
            dados_atuais['leit_p'], 
            dados_atuais['leit_k'], 
            dados_atuais['leit_ph'], 
            dados_atuais['leit_temperatura']
        ]).reshape(1, -1)
        
        # Normalização dos dados
        dados_previsao_scaled = self.scaler.transform(dados_previsao)
        
        # Previsão de umidade
        umidade_prevista = self.model.predict(dados_previsao_scaled)[0]
        
        # Lógica de decisão de irrigação
        if umidade_prevista < self.UMIDADE_IDEAL:
            tempo_irrigacao = int((self.UMIDADE_IDEAL - umidade_prevista) * 10)  # Ajuste conforme necessidade
            return {
                'irriga': True, 
                'tempo_irrigacao': min(tempo_irrigacao, 300),  # Máximo 5 minutos
                'umidade_prevista': umidade_prevista
            }
        else:
            return {
                'irriga': False, 
                'tempo_irrigacao': 0,
                'umidade_prevista': umidade_prevista
            }
    
    def monitoramento_continuo(self, duracao_horas=24):
        """
        Monitora continuamente o sistema de irrigação.
        
        Parâmetros:
        - duracao_horas: Tempo total de monitoramento.
        """
        inicio = time.time()
        
        while time.time() - inicio < duracao_horas * 3600:
            # Coleta de dados
            dados = self.coletar_dados_sensores()
            self.salvar_dados(dados)
            
            # Previsão de irrigação
            recomendacao = self.prever_necessidade_irrigacao(dados)
            
            if recomendacao and recomendacao['irriga']:
                print(f"Irrigação recomendada por {recomendacao['tempo_irrigacao']} segundos")
                print(f"Umidade prevista: {recomendacao['umidade_prevista']:.2f}%")
            
            # Intervalo entre coletas
            time.sleep(self.INTERVALO_COLETA)


def leiturasBD(conexao):
    """
    Captura leituras do banco de dados e salva em CSV.
    """
    try:
        lista_dados = []
        cursor = conexao.cursor()
        
        query = """
        SELECT leit_p, leit_k, leit_ph, leit_umidade, leit_temperatura, data_leitura
        FROM leituras
        """
        cursor.execute(query)
        leituras = cursor.fetchall()
        
        colunas = ['leit_p', 'leit_k', 'leit_ph', 'leit_umidade', 'leit_temperatura', 'data_leitura']
        dados_df = pd.DataFrame(leituras, columns=colunas)
        
        if not dados_df.empty:
            dados_df.to_csv('leituras.csv', index=False)
        else:
            print('Não há leituras cadastradas!')
        cursor.close()
    except Exception as e:
        print(f"Erro ao ler leituras: {e}")
    input('Pressione enter para continuar')


if __name__ == "__main__":
    conexao, conectado = conectar_banco()
    leiturasBD(conexao)

    sistema = SmartIrrigationSystem()
    sistema.treinar_modelo()
    sistema.monitoramento_continuo(duracao_horas=1)  # Monitoramento por 1 hora
