# Gerenciador de Tarefas Simples

## Descrição  
Este é um projeto simples de gerenciamento de tarefas, onde cada usuário pode:  
- Cadastrar uma conta com senha criptografada.  
- Realizar login e logout.  
- Gerenciar suas tarefas, com funcionalidades de adicionar, listar, editar e excluir.  

O objetivo é fornecer uma interface básica e funcional para organizar tarefas pessoais.  

---

## Tecnologias Utilizadas  
- **Python**: Linguagem principal do projeto.  
- **Flask**: Framework para criação das rotas e da aplicação web.  
- **PostgreSQL**: Banco de dados utilizado para armazenar usuários e tarefas.  
- **Argon2 (PasswordHasher)**: Para criptografar senhas dos usuários.  
- **UUID**: Para gerar identificadores únicos.  

---

## Funcionalidades  
1. **Cadastro de Usuário**  
   - Os usuários podem se registrar com email e senha.  
   - A senha é armazenada de forma segura utilizando Argon2.  

2. **Login e Logout**  
   - Login com email e senha.  
   - A sessão do usuário é gerenciada para acessar funcionalidades protegidas.  

3. **Gerenciamento de Tarefas**  
   - Adicionar novas tarefas.  
   - Listar tarefas cadastradas.  
   - Editar descrições, status e prazos das tarefas.  
   - Excluir tarefas.  

---

## Como Rodar o Projeto  

### Pré-requisitos  
- Python 3.10+  

### Passos  

1. **Clone o repositório:**  
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio
   ```  

2. **Instale as dependências:**  
   ```bash
   pip install -r requirements.txt
   ```  

3. **Execute a aplicação:**  
   ```bash
   python3 app.py
   ```  

4. **Acesse no navegador:**  
   - Acesse a aplicação em `http://127.0.0.1:5000`.  


## Autor  
Desenvolvido por **Leonardo**.

