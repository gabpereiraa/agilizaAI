CREATE DATABASE sistema_pacientes;
USE sistema_pacientes;

CREATE TABLE pacientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    endereco VARCHAR(255),
    numero INT,
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    cep VARCHAR(8),
    alergia VARCHAR(255),
    medicamentos VARCHAR(255),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE fila (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    data_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    atendido BOOLEAN DEFAULT FALSE,
    em_atendimento BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (paciente_id) 
        REFERENCES pacientes(id) 
        ON DELETE CASCADE
);

CREATE TABLE atendimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paciente_id INT NOT NULL,
    data_atendimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    febre BOOLEAN,
    descricao TEXT,
    FOREIGN KEY (paciente_id) 
        REFERENCES pacientes(id)
);

CREATE INDEX idx_cpf ON pacientes(cpf);
CREATE INDEX idx_fila_paciente ON fila(paciente_id);

ALTER TABLE fila
ADD COLUMN prioridade ENUM('normal', 'urgente') NOT NULL DEFAULT 'normal',
ADD COLUMN preferencial BOOLEAN NOT NULL DEFAULT FALSE;

ALTER TABLE pacientes
ADD COLUMN email VARCHAR(100) AFTER telefone;