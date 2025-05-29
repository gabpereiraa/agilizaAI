from flask import Flask
import paciente
import fila
import triagem
import painel

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui'

app.register_blueprint(paciente.bp)
app.register_blueprint(fila.bp)
app.register_blueprint(triagem.bp)
app.register_blueprint(painel.bp)

if __name__ == '__main__':
    app.run(debug=True)