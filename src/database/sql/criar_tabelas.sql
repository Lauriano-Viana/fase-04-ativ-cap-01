-- Criação da tabela 'culturas'
CREATE TABLE culturas (
    id_cultura NUMBER PRIMARY KEY,
    nome VARCHAR2(100) NOT NULL,
    nivel_p NUMBER(5, 2),
    nivel_k NUMBER(5, 2),
    nivel_ph NUMBER(5, 2),
    umidade NUMBER(5, 2)
);
-- Sequência para gerar IDs automáticos para a tabela culturas
CREATE SEQUENCE seq_culturas
START WITH 1 -- Valor inicial
INCREMENT BY 1 -- Incremento
NOCACHE -- Sem cache (pode usar CACHE para desempenho em alta escala)
NOCYCLE; -- Não reiniciar após atingir o valor máximo

-- Criação da tabela 'sensores'
CREATE TABLE sensores (
    id_sensor NUMBER PRIMARY KEY,
    tipo VARCHAR2(50) NOT NULL,
    descricao VARCHAR2(200),
    localizacao VARCHAR2(100)
);
-- Sequência para gerar IDs automáticos para a tabela sensores
CREATE SEQUENCE seq_sensores
START WITH 1 -- Valor inicial
INCREMENT BY 1 -- Incremento
NOCACHE -- Sem cache (pode usar CACHE para desempenho em alta escala)
NOCYCLE; -- Não reiniciar após atingir o valor máximo


-- Criação da tabela 'leituras'
CREATE TABLE leituras (
    id_leitura NUMBER PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    id_sensor NUMBER NOT NULL,
    leit_p NUMBER(5, 2),
    leit_k NUMBER(5, 2),
    leit_ph NUMBER(5, 2),
    leit_umidade NUMBER(5, 2),
    leit_temperatura NUMBER(5, 2),
    data_leitura DATE NOT NULL,
    CONSTRAINT fk_leituras_cultura FOREIGN KEY (id_cultura) REFERENCES culturas (id_cultura),
    CONSTRAINT fk_leituras_sensor FOREIGN KEY (id_sensor) REFERENCES sensores (id_sensor)
);

-- Sequência para gerar IDs automáticos para a tabela leituras
CREATE SEQUENCE seq_leituras
START WITH 1 -- Valor inicial
INCREMENT BY 1 -- Incremento
NOCACHE -- Sem cache (pode usar CACHE para desempenho em alta escala)
NOCYCLE; -- Não reiniciar após atingir o valor máximo

-- Criação da tabela 'irrigacoes'
CREATE TABLE irrigacoes (
    id_irrigacao NUMBER PRIMARY KEY,
    id_cultura NUMBER NOT NULL,
    id_leitura NUMBER NOT NULL,
    tempo NUMBER(10, 2) NOT NULL,
    motivo VARCHAR2(200),
    data_aplicacao DATE NOT NULL,
    CONSTRAINT fk_irrigacoes_cultura FOREIGN KEY (id_cultura) REFERENCES culturas (id_cultura),
    CONSTRAINT fk_irrigacoes_leitura FOREIGN KEY (id_leitura) REFERENCES leituras (id_leitura)
);

-- Sequência para gerar IDs automáticos para a tabela irrigacoes
CREATE SEQUENCE seq_irrigacoes
START WITH 1 -- Valor inicial
INCREMENT BY 1 -- Incremento
NOCACHE -- Sem cache (pode usar CACHE para desempenho em alta escala)
NOCYCLE; -- Não reiniciar após atingir o valor máximo

