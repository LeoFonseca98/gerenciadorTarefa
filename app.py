from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
'''
TodoList
1. Criar usuario
3. Realizar Login 
4. Criar tarefa de usuario
    - editar tarefa
    - excluir tarefa
    - listar tarefas
5. Realizar Logout 

Usuario: id, nome, email.
Conta: id, usuario_id, data_criacao.
Tarefas: id, conta_id, descricao, status, data_limite.
'''

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/cadastro')
def cadastro():
  return render_template('cadastro.html')

@app.route('/senha')
def senha():
  data = request()
  if data.senha == data.confirm_senha:
    return jsonify({"message": "Conta criada com sucesso!"})
  else:
    return jsonify({"message":"As senhas não são iguais!"})
  
    #return render_template('senha.html')

@app.route('/login')
def login():
  return render_template('login.html')


'''@app.route('/login', methods="POST")
def logar():
  return render_template('conta_usuario.html')
'''

if __name__ == '__main__':
    app.run(debug=True)