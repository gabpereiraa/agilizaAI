# 🚀 AgilizaAi

## 📝 Resumo

Este projeto propõe uma solução web chamada **Agiliza AI**, voltada para hospitais e clínicas, com o objetivo de otimizar o fluxo de triagem. Ele permite que o paciente realize o pré-cadastro em um totem, antes de ser atendido, e que a equipe médica gerencie os atendimentos por meio de um painel inteligente de filas, priorizando casos urgentes e preferenciais. A ferramenta foi desenvolvida com foco em organização, agilidade e eficiência hospitalar.

---

## 🎯 Objetivo

O objetivo principal do **Agiliza AI** é reduzir o tempo de espera e desorganização no processo de triagem hospitalar, proporcionando uma alternativa digital ao cadastro manual. O sistema permite que os pacientes iniciem seu atendimento ao preencher seus dados em um totem, antes mesmo da avaliação médica. A fila de triagem é gerenciada com base em critérios de prioridade clínica e ordem de chegada, garantindo atendimento justo e estruturado.

A motivação do projeto vem da observação de problemas recorrentes no sistema de saúde, como sobrecarga nas recepções, demora na triagem e falta de controle automatizado de prioridades. O projeto também se relaciona com conteúdos da disciplina de **Estruturas de Dados**, como a implementação de filas com prioridade, organização modular do código e persistência em banco de dados relacional.

---

## 👨‍💻 Tecnologias Utilizadas

- **Linguagem:** Python  
- **Framework Web:** Flask  
- **Frontend:** HTML + CSS (com Jinja2)  
- **Banco de Dados:** MySQL (gerenciado via XAMPP)  
- **APIs Externas:** ViaCEP (para busca automática de endereço)  
- **Ambiente Virtual:** venv  

### Bibliotecas principais:
- `mysql-connector-python` (conexão com banco)
- `requests` (consumo da API ViaCEP)

### Outros:
- Regex para validação de CPF
- BluePrints para organização modular no Flask

---

## 🗂️ Estrutura do Projeto

```
📁 TOTEM_PACIENTES/
├── 📂 sql/
│   ├── script.sql
│   └── instrucao
├── 📂 static/
│   └── style.css
├── 📂 templates/
│   ├── fila.html
│   ├── index.html
│   ├── painel.html
│   └── triagem.html
├── app.py
├── database.py
├── fila.py
├── paciente.py
├── painel.py
└── triagem.py
```

---

## ⚙️ Como Executar

### ✅ Rodando Localmente

1. Clone o repositório:

```bash
git clone https://github.com/gabpereiraa/agilizaAI.git
cd TOTEM_PACIENTES
```

2. Crie o ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate     # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Instale as dependências:

```bash
pip install flask mysql-connector-python requests
```

4. Configure o banco de dados MySQL:

```bash
mysql -u root -p < sql/script.sql
```

5. Execute a aplicação:

```bash
python app.py
```

6. Acesse no navegador:

```
http://localhost:5000
```

---

## 📸 Demonstrações

### - Tela inicial
A imagem exibe a interface principal de cadastro do paciente no totem, onde o usuário insere suas informações antes da triagem hospitalar.  
![Interface de Cadastro do Paciente](https://i.imgur.com/mt1QnFe.png)

---

### - Exemplo de funcionalidade
Interface de visualização da fila de pacientes em tempo real, organizada por prioridade e ordem de chegada.  
[🔗 Imagem](https://imgur.com/e6kkavN)

---

### - Resultados esperados
Painel de chamada com os pacientes organizados por prioridade: emergências, preferenciais e comuns.  
[🔗 Imagem](https://imgur.com/JXKKO2u)

---

## 👥 Equipe

| Nome               | GitHub                                    |
|--------------------|-------------------------------------------|
| Aliana Moraes      | [@alianamoraes](https://github.com/alianamoraes) |
| Gabriel Anastacio  | [@gabpereiraa](https://github.com/gabpereiraa) |

---

## 🧠 Disciplinas Envolvidas

- Estrutura de Dados I

---

## 🏫 Informações Acadêmicas

- **Universidade:** Centro Universitário Braz Cubas  
- **Curso:** Ciência da Computação  
- **Semestre:** 3º  
- **Período:** Noite  
- **Professora Orientadora:** Dra. Andréa Ono Sakai  
- **Evento:** Mostra de Tecnologia – 1º Semestre de 2025  
- **Local:** Laboratório 12  
- **Datas:** 05 e 06 de junho de 2025

---

## 📄 Licença

MIT License — sinta-se à vontade para utilizar, estudar e adaptar este projeto.
