from datetime import timedelta
import re
import traceback
import uuid
from flask import Flask, flash
from flask import render_template, jsonify, redirect, url_for
from flask import request, session
from esquema.esquema import Usuario, Tarefa
import secrets
from argon2 import PasswordHasher
from peewee import DoesNotExist
from argon2.exceptions import InvalidHashError

app = Flask(__name__)


app.config['SECRET_KEY'] = secrets.token_hex(16)
app.permanent_session_lifetime = timedelta(hours=3)

ph = PasswordHasher()

@app.route('/')
def index():
  return render_template('index.html')



@app.route('/cadastro')
def cadastro():
  return render_template('cadastro.html')



@app.route('/inserir_usuario', methods=["POST"])
def inserir_usuario():

  def validar_senha(senha):
    regex = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(regex, senha))

  try:
      user_id = str(uuid.uuid4()) 
      
      id = user_id
      nome = request.form.get('nome')
      email = request.form.get('email')
      senha = request.form.get('senha')
      confirm_senha = request.form.get('confirm_senha')

      if senha != confirm_senha:
        return redirect(url_for('cadastro'))
      
      if not validar_senha(senha):
        return "As senha devem conter pelo menos uma letra maiúscula, uma minúscula, um número e um caractér especial!"

      senha = ph.hash(senha)
       
      novo_usuario = Usuario.create(id=id, nome=nome, email=email, senha=senha, confirm_senha=confirm_senha)
      novo_usuario.save()
      return redirect(url_for('index'))

  except Exception as e:
    print(f'Erro inesperado: {e}')
    return jsonify({'message': 'Erro ao inserir usuario!', 'error': str(e)})


@app.route('/login')
def login():
  return render_template('login.html')


@app.route('/logar', methods=["POST"])
def logar():
    try:

        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email or not senha:
            return jsonify({'message': 'Email e senha são obrigatórios!'}), 400

        try:
            usuario = Usuario.get(Usuario.email == email)
        except DoesNotExist:
            print("Usuário não encontrado no banco de dados.")
            return jsonify({'message': 'Email ou senha inválidos!'}), 401

        try:
            if not ph.verify(usuario.senha, senha):
                print("Senha inválida.")
                return jsonify({'message': 'Email ou senha inválidos!'}), 401
        except InvalidHashError:
            print("Hash de senha inválido.")
            return jsonify({'message': 'Erro interno: Hash inválido!'}), 500
        print("Login bem-sucedido!")

        session.permanent = True
        session['user_id'] = usuario.id

        return render_template('dashboard.html', usuario=usuario)
        #return redirect(url_for('dashboard'))  # Substitua pela sua rota de dashboard

    except Exception as e:
        print("Erro no servidor:")
        traceback.print_exc()
        return jsonify({'message': 'Erro no servidor!', 'error': str(e)}), 500



@app.route('/adicionar_tarefa')
def adicionar_tarefa():
  return render_template('adicionar_tarefa.html')  


@app.route('/inserir_tarefa', methods=['POST'])
def inserir_tarefa():


    usuario_id = session.get('user_id')
   
    descricao = request.form.get('descricao')
    status = request.form.get('status')
    data_limite = request.form.get('data_limite')

    tabela_id = uuid.uuid4()

    tarefa = Tarefa.create(id=tabela_id, usuario_id=usuario_id, descricao=descricao, status=status, data_limite=data_limite)
    tarefa.save()

    flash('Tarefa criada co sucesso!', 'success')
    return jsonify({'message': 'tarefa criada com sucesso!'})


@app.route('/minhas_tarefas')
def minhas_tarefas():
   
    usuario_id = session.get('user_id')
    if not usuario_id:
        return jsonify({'message': 'Usuário não está logado!'})
   
    tarefas = Tarefa.select().where(Tarefa.usuario_id == usuario_id)

    return render_template('minhas_tarefas.html', tarefas=tarefas)
  
  
@app.route('/editar_tarefa/<string:id>')
def editar_tarefa(id):

  tarefa = Tarefa.get_or_none(Tarefa.id == id)
  if not tarefa:
    return jsonify({'message': 'Tarefa não encontrado!'})
  return render_template('editar_tarefa.html', tarefa=tarefa)

@app.route('/form_editar/<string:id>', methods=['POST'])
def form_editar(id):

  try:
    tarefa = Tarefa.get_or_none(Tarefa.id == id)
    if not tarefa:
      return jsonify({'message': 'Tarefa não encontrada!'})
    
    tarefa.descricao = request.form.get('descricao')
    tarefa.status = request.form.get('status')
    tarefa.data_limite = request.form.get('data_limite')
    tarefa.save()
    return jsonify({'message': 'Tarefa editada com sucesso!'})
  
  except Exception as e:
     print(f'Error: {e}')
     return jsonify({'message': 'Erro ao editar a tarefa!'})

   
@app.route('/excluir_tarefa/<string:id>', methods=['GET', 'POST'])
def excluir_tarefa(id):
   
    try:
      tarefa = Tarefa.get_or_none(Tarefa.id == id)
      if not tarefa:
         return jsonify({'message': 'Tarefa não encontrada!'})
      
      tarefa.delete_instance()
      return redirect(url_for('minhas_tarefas'))

    except Exception as e:
       print(f'Error: {e}')
       return jsonify({'message': 'Erro inesperado ao excluir tarefa!'})
    

@app.route('/logout')
def logout():
  session.pop('user_id', None)

  return redirect(url_for('login'))

   

if __name__ == '__main__':
    app.run(debug=True)
