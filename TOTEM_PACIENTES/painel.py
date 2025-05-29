from flask import Blueprint, render_template, jsonify
from database import get_db_cursor
from paciente import format_cpf

bp = Blueprint('painel', __name__)

@bp.route('/painel')
def painel():
    return render_template('painel.html')

@bp.route('/api/fila')
def api_fila():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.nome, f.id as senha, f.prioridade, f.preferencial
                FROM fila f 
                JOIN pacientes p ON f.paciente_id = p.id 
                WHERE f.em_atendimento = TRUE AND f.atendido = FALSE
                ORDER BY f.data_entrada
                LIMIT 1
            """)
            em_atendimento = cursor.fetchone()

            cursor.execute("""
                SELECT p.id, p.nome, f.id as senha, f.prioridade, f.preferencial,
                       f.data_entrada
                FROM fila f 
                JOIN pacientes p ON f.paciente_id = p.id 
                WHERE f.atendido = FALSE AND f.em_atendimento = FALSE
                ORDER BY 
                    CASE 
                        WHEN f.prioridade = 'urgente' THEN 1
                        WHEN f.preferencial = TRUE THEN 2
                        ELSE 3
                    END,
                    f.data_entrada
                LIMIT 10
            """)
            fila_espera = cursor.fetchall()

            cursor.execute("""
                SELECT p.nome, f.id as senha, f.prioridade, f.preferencial
                FROM fila f 
                JOIN pacientes p ON f.paciente_id = p.id 
                WHERE f.atendido = TRUE 
                ORDER BY f.data_entrada DESC 
                LIMIT 3
            """)
            ultimos_atendidos = cursor.fetchall()

            grupos = {
                'em_atendimento': em_atendimento,
                'urgentes': [p for p in fila_espera if p['prioridade'] == 'urgente'],
                'preferenciais': [p for p in fila_espera if p['preferencial'] and p['prioridade'] != 'urgente'],
                'normais': [p for p in fila_espera if not p['preferencial'] and p['prioridade'] == 'normal'],
                'ultimos_atendidos': ultimos_atendidos
            }
            
            return jsonify(grupos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/api/chamar_proximo')
def api_chamar_proximo():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.nome, f.id as senha
                FROM fila f 
                JOIN pacientes p ON f.paciente_id = p.id 
                WHERE f.atendido = FALSE AND f.em_atendimento = FALSE
                AND f.prioridade = 'urgente'
                ORDER BY f.data_entrada
                LIMIT 1
            """)
            proximo = cursor.fetchone()

            if not proximo:
                cursor.execute("""
                    SELECT p.id, p.nome, f.id as senha
                    FROM fila f 
                    JOIN pacientes p ON f.paciente_id = p.id 
                    WHERE f.atendido = FALSE AND f.em_atendimento = FALSE
                    AND f.preferencial = TRUE
                    ORDER BY f.data_entrada
                    LIMIT 1
                """)
                proximo = cursor.fetchone()

            if not proximo:
                cursor.execute("""
                    SELECT p.id, p.nome, f.id as senha
                    FROM fila f 
                    JOIN pacientes p ON f.paciente_id = p.id 
                    WHERE f.atendido = FALSE AND f.em_atendimento = FALSE
                    ORDER BY f.data_entrada
                    LIMIT 1
                """)
                proximo = cursor.fetchone()

            if proximo:
                cursor.execute("""
                    UPDATE fila SET em_atendimento = TRUE
                    WHERE id = %s
                """, (proximo['senha'],))
                
                return jsonify({
                    'success': True,
                    'paciente': {
                        'id': proximo['id'],
                        'nome': proximo['nome'],
                        'senha': proximo['senha']
                    }
                })
            
            return jsonify({'success': False, 'message': 'Nenhum paciente na fila'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/finalizar_atendimento/<int:senha>', methods=['POST'])
def api_finalizar_atendimento(senha):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                UPDATE fila SET 
                em_atendimento = FALSE,
                atendido = TRUE
                WHERE id = %s
            """, (senha,))
            
            return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500