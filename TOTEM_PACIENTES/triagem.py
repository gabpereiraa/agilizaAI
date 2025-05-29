from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from database import get_db_cursor

bp = Blueprint('triagem', __name__)

@bp.route('/atender/<int:paciente_id>', methods=['GET', 'POST'])
def atender_paciente(paciente_id):
    if request.method == 'POST':
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    UPDATE fila SET atendido = TRUE 
                    WHERE paciente_id = %s AND atendido = FALSE
                """, (paciente_id,))
                
                cursor.execute("""
                    INSERT INTO atendimentos 
                    (paciente_id, febre, descricao)
                    VALUES (%s, %s, %s)
                """, (
                    paciente_id,
                    True if request.form.get('febre') == 'on' else False,
                    request.form.get('descricao', '')
                ))
                
                flash('Atendimento registrado com sucesso!', 'success')
                return redirect(url_for('fila.fila'))
        except Exception as e:
            flash(f"Erro ao registrar atendimento: {str(e)}", 'error')
    
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT p.*, f.id as senha 
                FROM pacientes p
                JOIN fila f ON p.id = f.paciente_id
                WHERE p.id = %s AND f.atendido = FALSE
            """, (paciente_id,))
            paciente = cursor.fetchone()
            
            if not paciente:
                flash('Paciente não encontrado ou já atendido', 'error')
                return redirect(url_for('fila.fila'))
            
            cursor.execute("""
                UPDATE fila SET 
                em_atendimento = TRUE
                WHERE paciente_id = %s AND atendido = FALSE
            """, (paciente_id,))
            
            return render_template('triagem.html', paciente=paciente)
    except Exception as e:
        flash(f"Erro ao carregar paciente: {str(e)}", 'error')
        return redirect(url_for('fila.fila'))

@bp.route('/chamar/<int:paciente_id>', methods=['POST'])
def chamar_paciente(paciente_id):
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT p.nome, p.id, f.id as senha, f.prioridade, f.preferencial
                FROM pacientes p
                JOIN fila f ON f.paciente_id = p.id 
                WHERE p.id = %s AND f.atendido = FALSE
            """, (paciente_id,))
            paciente = cursor.fetchone()
            
            if not paciente:
                return jsonify({'success': False, 'message': 'Paciente não encontrado'})
            
            cursor.execute("""
                UPDATE fila SET 
                em_atendimento = TRUE
                WHERE paciente_id = %s AND atendido = FALSE
            """, (paciente_id,))
            
            return jsonify({
                'success': True,
                'paciente': {
                    'id': paciente['id'],
                    'nome': paciente['nome'],
                    'senha': paciente['senha'],
                    'prioridade': paciente['prioridade'],
                    'preferencial': paciente['preferencial']
                }
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})