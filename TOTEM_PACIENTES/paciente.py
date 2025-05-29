from flask import Blueprint, render_template, request, jsonify
import re
import requests
from database import get_db_cursor

bp = Blueprint('paciente', __name__)

def is_cpf_valid(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = 11 - (soma % 11)
    dig1 = 0 if dig1 > 9 else dig1

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = 11 - (soma % 11)
    dig2 = 0 if dig2 > 9 else dig2

    return cpf[-2:] == f"{dig1}{dig2}"

def format_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}"

def buscar_endereco_por_cep(cep):
    cep = re.sub(r'[^0-9]', '', cep)
    if len(cep) != 8:
        return None
    try:
        response = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        if response.status_code == 200:
            dados = response.json()
            return dados if not dados.get('erro') else None
    except requests.RequestException:
        return None
    return None

@bp.route('/buscar_paciente', methods=['POST'])
def buscar_paciente():
    cpf = re.sub(r'[^0-9]', '', request.form.get('cpf', ''))
    if len(cpf) != 11:
        return jsonify({'success': False, 'message': 'CPF deve ter 11 dígitos'})
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT nome, telefone, email, cep, numero 
                FROM pacientes 
                WHERE cpf = %s
            """, (cpf,))
            paciente = cursor.fetchone()
            
            if paciente:
                return jsonify({
                    'success': True,
                    'paciente': {
                        'nome': paciente['nome'],
                        'telefone': paciente['telefone'],
                        'email': paciente['email'],
                        'cep': paciente['cep'],
                        'numero': paciente['numero']
                    }
                })
            return jsonify({'success': False, 'message': 'Paciente não cadastrado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        cpf = re.sub(r'[^0-9]', '', request.form.get('cpf', ''))
        nome = request.form.get('nome', '').strip()
        telefone = re.sub(r'[^0-9]', '', request.form.get('telefone', ''))
        email = request.form.get('email', '').strip()
        cep = re.sub(r'[^0-9]', '', request.form.get('cep', ''))
        numero = request.form.get('numero', '').strip()
        preferencial = True if request.form.get('preferencial') == 'on' else False
        prioridade = request.form.get('prioridade', 'normal')

        if not is_cpf_valid(cpf):
            return jsonify({
                'success': False,
                'message': 'CPF inválido. Por favor, verifique o número digitado.'
            })

        if not telefone:
            return jsonify({
                'success': False,
                'message': 'Telefone é obrigatório.'
            })

        try:
            with get_db_cursor() as cursor:
                cursor.execute("SELECT id, nome FROM pacientes WHERE cpf = %s", (cpf,))
                paciente = cursor.fetchone()

                if paciente:
                    cursor.execute("""
                        UPDATE pacientes SET 
                        nome = %s, telefone = %s, email = %s, cep = %s, numero = %s
                        WHERE cpf = %s
                    """, (nome, telefone, email, cep, numero, cpf))
                    
                    cursor.execute("""
                        INSERT INTO fila (paciente_id, preferencial, prioridade)
                        SELECT %s, %s, %s FROM DUAL
                        WHERE NOT EXISTS (
                            SELECT 1 FROM fila 
                            WHERE paciente_id = %s AND atendido = FALSE
                        )
                    """, (paciente['id'], preferencial, prioridade, paciente['id']))
                    
                    fila_id = cursor.lastrowid
                else:
                    endereco_info = buscar_endereco_por_cep(cep)
                    if not endereco_info:
                        return jsonify({
                            'success': False,
                            'message': 'CEP inválido ou não encontrado.'
                        })

                    cursor.execute("""
                        INSERT INTO pacientes 
                        (cpf, nome, telefone, email, endereco, numero, bairro, cidade, cep)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        cpf, nome, telefone, email,
                        endereco_info.get('logradouro', ''), 
                        numero, 
                        endereco_info.get('bairro', ''), 
                        endereco_info.get('localidade', ''), 
                        cep
                    ))
                    paciente_id = cursor.lastrowid
                    cursor.execute("""
                        INSERT INTO fila (paciente_id, preferencial, prioridade)
                        VALUES (%s, %s, %s)
                    """, (paciente_id, preferencial, prioridade))
                    fila_id = cursor.lastrowid

                return jsonify({
                    'success': True,
                    'senha': fila_id,
                    'message': f'Cadastro realizado! Sua senha é: {fila_id}'
                })
                
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Erro no sistema: {str(e)}'
            })

    return render_template('index.html')