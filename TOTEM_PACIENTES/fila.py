from flask import Blueprint, render_template, redirect, url_for, flash
from database import get_db_cursor
from paciente import format_cpf

bp = Blueprint('fila', __name__)

@bp.route('/fila')
def fila():
    try:
        with get_db_cursor() as cursor:
            cursor.execute("""
                SELECT p.id, p.nome, p.cpf, f.data_entrada, f.id as senha, 
                       f.prioridade, f.preferencial
                FROM fila f 
                JOIN pacientes p ON f.paciente_id = p.id 
                WHERE f.atendido = FALSE 
                ORDER BY 
                    CASE 
                        WHEN f.prioridade = 'urgente' THEN 1
                        WHEN f.preferencial = TRUE THEN 2
                        ELSE 3
                    END,
                    f.data_entrada
            """)
            pacientes_na_fila = cursor.fetchall()
            
            pacientes = []
            for p in pacientes_na_fila:
                pacientes.append({
                    'id': p['id'],
                    'nome': p['nome'],
                    'cpf': format_cpf(p['cpf']),
                    'data_entrada': p['data_entrada'].strftime('%d/%m/%Y %H:%M'),
                    'senha': p['senha'],
                    'prioridade': p['prioridade'],
                    'preferencial': p['preferencial']
                })
            
            return render_template('fila.html', pacientes=pacientes)
    except Exception as e:
        flash(f"Erro ao carregar fila: {str(e)}", 'error')
        return redirect(url_for('paciente.index'))