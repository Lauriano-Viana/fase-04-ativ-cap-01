# Sistema de Irrigação Automatizada e Inteligente com Machine Learning
### Introdução
Este sistema tem como objetivo otimizar a irrigação de culturas, monitorando em tempo real a umidade do solo, os níveis de nutrientes (fósforo - P e potássio - K) e o pH. O sistema utiliza **dados de sensores simulados** ou do banco de dados, aplica técnicas de aprendizado de máquina para prever a necessidade de irrigação.
Onde toma decisões baseadas nas previsões e ajusta automaticamente a quantidade de água aplicada, garantindo o crescimento saudável das plantas.


Nota: Os comportamentos de hardware dos sensores e os valores de entrada no banco de dados são gerados por um simulador no Wokwi e inseridos manualmente no sistema para análise e atuação.

## Base de Dados 
 **Tabelas:**
  * **culturas:** Armazena informações sobre as diferentes culturas, como nome, níveis ideais de nutrientes e umidade.
  * **sensores:** Guarda detalhes sobre os sensores utilizados, como tipo, descrição e localização.
  * **leituras:** Registra as medições realizadas pelos sensores em um determinado momento para uma cultura específica.
  * **irrigacoes:** Controla as ações de irrigação, como tempo, motivo e data.
## Funcionamento
1. **Coleta de Dados:**
   * **Sensores:**
     * **Umidade:** Sensor de umidade do solo mede o nível de água no solo e temperatura
     * **Nutrientes (P e K):** Botões simulam a presença ou ausência dos nutrientes.
     * **pH:** Sensor LDR mede a intensidade da luz refletida por uma solução, indicando o pH.
   * **Leitura:** Os dados coletados pelos sensores são armazenados na tabela `leituras`.

2. **Análise dos Dados:**
   * O sistema compara os dados coletados com os valores ideais definidos para cultura informada.
   * **Regra de Irrigação:** Se a umidade estiver abaixo do ideal ou se os níveis de nutrientes estiverem baixos, o sistema ativa a bomba d'água (representada por um relé).

3. **Atuação:**
   * **Bomba d'água:** A bomba é acionada por um determinado período, ajustando a quantidade de água aplicada.

4. **Registro:**
   * Toda vez que um novo registro de leitura é criado na tabela leituras, o sistema gera automaticamente um registro na tabela irrigacoes atrelado à leitura recém-criada. Isso assegura que cada medição relevante tenha uma resposta automatizada registrada no sistema.

## Operações CRUD

* **Sensores:**
  * **Criar:** Adicionar um novo sensor ao sistema.
  * **Listar:** Exibir todos os sensores cadastrados.
  * **Atualizar:** Modificar as informações de um sensor existente.
  * **Deletar:** Remover um sensor do sistema.

* **Culturas:**
  * **Criar:** Cadastrar uma nova cultura com seus respectivos níveis ideais.
  * **Listar:** Exibir todas as culturas cadastradas.
  * **Atualizar:** Modificar as informações de uma cultura existente.
  * **Deletar:** Remover uma cultura do sistema.

* **Irrigação:**
    * **Criar:** Cria uma nova irrigacao de forma automatizada, sempre que uma leitura é registrada
  * **Listar:** Exibir o histórico de irrigações.
  * **Deletar:** Remover uma irrigação do histórico (para fins de limpeza de dados).

  
  ## Código Machine Learning
  ---

  ## 1. Objetivo do Sistema
  - Monitorar condições do solo e clima.
  - Prever a necessidade de irrigação usando um modelo de **Random Forest**.
  - Automatizar a recomendação de irrigação baseada em condições ideais.

  ---

  ## 2. Estrutura do Código
  ### **Importação de Bibliotecas**
  - `numpy`, `pandas`: Manipulação de dados.
  - `sklearn`: Modelagem de dados e métricas.
  - `joblib`: Persistência do modelo treinado.
  - `datetime`, `time`: Manipulação de datas e controle de monitoramento.
  - `src.database.entidades.conection`: Conexão com banco de dados.

  ### **Classe `SmartIrrigationSystem`**
  A classe principal gerencia a coleta de dados, treinamento do modelo e decisões de irrigação.

  ---

  ## 3. Principais Métodos da Classe

  ### **`coletar_dados_sensores()`**
  - Simula a coleta de dados de sensores ambientais.
  - Retorna um dicionário com os seguintes atributos:
    - `leit_p`, `leit_k`: Níveis de nutrientes.
    - `leit_ph`: pH do solo.
    - `leit_umidade`: Umidade do solo (%).
    - `leit_temperatura`: Temperatura ambiente (°C).
    - `data_leitura`: Data e hora da coleta.

  ### **`salvar_dados(dados)`**
  - Salva as leituras coletadas em um arquivo CSV (`leituras.csv`).
  - Caso o arquivo não exista, cria um novo.

  ### **`preparar_dados_treinamento()`**
  - Lê os dados do CSV e separa as features (`leit_p`, `leit_k`, `leit_ph`, `leit_temperatura`) do target (`leit_umidade`).
  - Divide os dados em conjuntos de **treinamento (70%)** e **teste (30%)**.
  - Aplica normalização nos dados usando `StandardScaler`.

  ### **`treinar_modelo()`**
  - Treina um modelo de **Random Forest Regressor** com os dados preparados.
  - Calcula métricas de desempenho:
    - **Erro Quadrático Médio (MSE)**.
    - **Coeficiente de Determinação (R²)**.
  - Salva o modelo e o scaler em arquivos `.pkl`.

  ### **`prever_necessidade_irrigacao(dados_atuais)`**
  - Usa o modelo treinado para prever a umidade do solo baseada nos dados de sensores.
  - Compara a previsão com a **umidade ideal (65%)**:
    - Se a umidade prevista for menor, recomenda irrigação e calcula o tempo necessário.
    - Caso contrário, nenhuma irrigação é sugerida.

  ### **`monitoramento_continuo(duracao_horas)`**
  - Realiza o monitoramento por tempo configurado (em horas).
  - Coleta dados, salva no CSV, e prevê a necessidade de irrigação a cada intervalo de coleta (1 hora por padrão).
  - Exibe recomendações de irrigação no console.

  ---

  ## 4. Integração com Banco de Dados
  ### **Função `leiturasBD(conexao)`**
  - Consulta dados históricos do banco de dados com a seguinte query:
    ```sql
    SELECT leit_p, leit_k, leit_ph, leit_umidade, leit_temperatura, data_leitura
    FROM leituras;
    ```
  - Salva os dados obtidos em `leituras.csv` para uso no treinamento do modelo.

  ---

  ## 5. Execução do Sistema
  ### **Passos:**
  1. **Conexão com o Banco de Dados:**
    - Conecta ao banco e carrega leituras para o CSV.
  2. **Treinamento do Modelo:**
    - Utiliza os dados históricos salvos para treinar o modelo de previsão.
  3. **Monitoramento Contínuo:**
    - Coleta dados periodicamente, prevê umidade, e recomenda irrigação em tempo real.

  ---

  ## 6. Pontos Importantes
  - **Modelagem de Dados:**
    - Features: `leit_p`, `leit_k`, `leit_ph`, `leit_temperatura`.
    - Target: `leit_umidade`.
  - **Decisão de Irrigação:**
    - Baseada na comparação entre a **umidade prevista** e a **umidade ideal (65%)**.
  - **Persistência:**
    - Dados coletados são armazenados no arquivo CSV.
    - Modelo treinado e scaler são salvos para uso futuro.

  ---

  # Funcionamento do Dashboard do Sistema de Irrigação Inteligente

Funcionalidades e o fluxo de trabalho do dashboard desenvolvido com **Streamlit** para um sistema de irrigação inteligente. Ele permite monitorar dados, realizar previsões em tempo real e treinar o modelo de aprendizado de máquina diretamente pela interface.

---

## 1. Objetivo do Dashboard
- Proporcionar uma **interface interativa** para gerenciar e monitorar o sistema de irrigação.
- Visualizar dados coletados e suas distribuições.
- Fazer previsões em tempo real usando sensores simulados.
- Treinar o modelo diretamente pelo dashboard.

---

## 2. Estrutura do Código
### **Importação de Bibliotecas**
- `streamlit`: Para criar a interface do usuário.
- `pandas`, `numpy`: Para manipulação de dados.
- `joblib`: Para carregar e salvar o modelo e scaler.
- `plotly.express`: Para criação de gráficos interativos.
- `irrig_preditiva`: Classe principal (`SmartIrrigationSystem`) que gerencia o sistema de irrigação.

### **Inicialização**
- O sistema é instanciado usando a classe `SmartIrrigationSystem`.
- O modelo e o scaler são carregados do disco (`irrigacao_modelo.pkl` e `irrigacao_scaler.pkl`).
- Um menu lateral organiza as funcionalidades.

---

## 3. Funcionalidades do Dashboard

### **Menu Principal**
O menu lateral oferece as seguintes opções:
1. **Visualizar Dados**
2. **Previsão em Tempo Real**
3. **Treinar Modelo**

---

### **1. Visualizar Dados**
Permite explorar os dados coletados do sistema. 
- **Exibição da Tabela de Dados:**
  - Mostra as 10 leituras mais recentes.
  - Inclui atributos como `leit_p`, `leit_k`, `leit_ph`, `leit_umidade`, `leit_temperatura` e `data_leitura`.
- **Gráficos Interativos:**
  - **Gráfico de Linha:** 
    - Variação da umidade do solo ao longo do tempo.
    - Variação da temperatura ao longo do tempo.
  - **Histograma:**
    - Distribuição de variáveis selecionadas (`leit_ph`, `leit_umidade`, `leit_temperatura`).

> **Observação:** Se não houver dados disponíveis, exibe uma mensagem de aviso.

---

### **2. Previsão em Tempo Real**
Simula a coleta de dados dos sensores e utiliza o modelo treinado para gerar previsões.
- **Coleta de Dados:**
  - Simula leituras de sensores ambientais como pH, umidade, temperatura, entre outros.
  - Exibe os dados coletados em formato JSON.
- **Previsão:**
  - Calcula a umidade prevista com base nas features coletadas.
  - Recomenda irrigação caso a umidade prevista seja inferior à **umidade ideal (65%)**:
    - Mostra o tempo de irrigação sugerido (máximo de 300 segundos).
  - Caso contrário, informa que o solo está com umidade suficiente.

> **Aviso:** O modelo e o scaler devem estar carregados para realizar a previsão.

---

### **3. Treinar Modelo**
Permite treinar o modelo diretamente no dashboard.
- **Requisitos:**
  - Um arquivo CSV (`leituras.csv`) com dados coletados.
- **Processo:**
  - Ao clicar no botão de treinamento, o sistema utiliza os dados para treinar o modelo.
  - Após o treinamento, o modelo e o scaler são salvos nos arquivos correspondentes.
- **Resultado:**
  - Exibe uma mensagem de sucesso ao finalizar o treinamento.

> **Observação:** Se não houver dados suficientes para treinamento, uma mensagem de aviso é exibida.

---

## 4. Fluxo de Trabalho
1. **Inicialização:**
   - O sistema carrega o modelo e o scaler (se disponíveis).
2. **Escolha de Funcionalidade:**
   - Visualizar os dados coletados.
   - Realizar previsões em tempo real.
   - Treinar o modelo para melhorar a acurácia das previsões.
3. **Decisões de Irrigação:**
   - Baseadas na previsão de umidade em relação à umidade ideal configurada.

---

## 5. Tecnologias Utilizadas
- **Streamlit:** Framework para criação de dashboards.
- **Plotly:** Visualizações interativas.
- **Joblib:** Persistência do modelo e do scaler.
- **Machine Learning:** Modelo `RandomForestRegressor` para previsão.

---

# Funcionamento do Sistema de Controle de Irrigação com ESP32
(Simulação dos Sensores)

Este documento descreve a estrutura, otimizações e funcionalidades de um programa em **C++** para o ESP32, que monitora e controla a irrigação automática com base em variáveis como umidade, pH, temperatura e níveis de nutrientes.

---

## 1. Objetivo do Código
Automatizar o controle de irrigação de maneira eficiente, utilizando sensores e atuadores conectados ao ESP32. O sistema:
- Coleta dados ambientais e de nutrientes do solo.
- Avalia os valores em relação aos ideais configurados.
- Aciona a irrigação automaticamente, conforme a necessidade.

---

## 2. Estrutura do Código

### **1. Definição de Constantes e Configuração Inicial**
- **Pinos de Entrada e Saída:**
  - Botões (`BUTTON_PIN_P`, `BUTTON_PIN_K`) indicam níveis de nutrientes P (fósforo) e K (potássio).
  - LDR (`PIN_LDR_PH`) lê o pH do solo.
  - DHT (`PIN_DHT`) coleta dados de temperatura e umidade.
  - Relé (`PIN_RELE_IRR`) aciona o sistema de irrigação.

- **Valores Ideais Configurados:**
  - **Umidade ideal:** 80.0%.
  - **pH ideal:** 6.
  - **Duração da irrigação:** 
    - **Curta:** 1500 ms.
    - **Longa:** 3000 ms.

### **2. Inicialização dos Componentes**
- Configuração dos pinos de entrada e saída.
- Inicialização da comunicação Serial, do sensor DHT e do display LCD.
- Envio de cabeçalho formatado para o **Serial Plotter**.

---

## 3. Funcionalidades Principais

### **Leitura e Processamento dos Dados**
A cada intervalo definido (1 segundo), o sistema:
- **Níveis de Nutrientes:** Verifica os botões para identificar os níveis de fósforo e potássio (alto ou baixo).
- **pH do Solo:** Converte o valor analógico lido pelo LDR para a escala de pH (0 a 14).
- **Temperatura e Umidade:** Coleta os dados do sensor DHT.

Se as leituras forem válidas:
- Os valores são exibidos no **Serial Plotter** para análise.
- São processados para decidir se a irrigação é necessária.

---

### **Controle da Irrigação**
A irrigação é acionada com base em:
1. **Condições de Deficiência:**
   - Níveis de fósforo ou potássio baixos.
   - pH inferior ao ideal.
   - Umidade do solo abaixo do valor configurado.
2. **Duração da Irrigação:**
   - Longa: 3000 ms, caso qualquer condição esteja fora dos parâmetros.
   - Curta: 1500 ms, caso tudo esteja dentro do ideal.

---

### **Atualização no Display LCD**
As informações mais recentes são exibidas no **LCD**:
- Primeira linha: Status de nutrientes (P e K).
- Segunda linha: Valores de pH e umidade.

---

## 4. Otimizações Implementadas

1. **Uso de Tipos de Dados Menores:**
   - Variáveis como `uint8_t` e `int8_t` são usadas para economizar memória.
   - Constantes configuradas como `constexpr` permitem otimizações em tempo de compilação.

2. **Redução de Processamento:**
   - Leitura e mapeamento do pH são otimizados com menos operações.
   - Uso de variáveis locais em vez de globais para economizar memória.

3. **Organização de Configurações:**
   - Inicialização dos pinos (entrada e saída) feita em loops, minimizando repetição de código.

4. **Eficiência em Comunicação:**
   - Dados enviados ao **Serial Plotter** são formatados de maneira compacta, com casas decimais limitadas.

---

## 5. Fluxo de Execução

1. **Setup Inicial:**
   - Configura os pinos, inicializa os sensores e estabelece comunicação com o Serial e LCD.

2. **Loop Principal:**
   - Verifica se o intervalo definido foi atingido.
   - Realiza leituras dos sensores e processa os dados.
   - Decide sobre o acionamento do sistema de irrigação.
   - Atualiza o LCD com informações relevantes.

---

## 6. Componentes Utilizados

1. **Sensores:**
   - **DHT22:** Para umidade e temperatura.
   - **LDR:** Para leitura de pH (com escala mapeada).

2. **Atuadores:**
   - **Relé:** Aciona o sistema de irrigação.

3. **Display LCD (I2C):**
   - Mostra os valores de sensores e status do sistema.

4. **ESP32:**
   - Responsável pelo processamento e controle.

---

## 7. Conclusão
Este programa oferece um controle de irrigação inteligente e eficiente, ideal para aplicações agrícolas de pequeno porte. As otimizações implementadas garantem maior economia de memória e eficiência de execução, maximizando o desempenho do sistema.

## 8. Imagens do circuito da plataforma Wokwi.com as conexões dos sensores solicitados

  [diagrama Wokwi](image.png)
  
  ## link video youtube
    link do vídeo postado no Youtube (sem listagem), demonstrando o funcionamento completo do projeto
  **link:**
    https://youtu.be/WCAkkt9Af1c


