from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import uuid 
import pillow 

app = Flask(__name__)
app.secret_key = "projetoFinal"

usuario = "adm"
senha = "123"

# FUNÇÃO PARA VERIFICAR SESSÃO
def verifica_sessao():
    return "login" in session and session["login"]

# CONEXÃO COM O BANCO DE DADOS
def conecta_database():
    conexao = sql.connect("Banco_de_dados_name.db")
    conexao.row_factory = sql.Row
    return conexao

# INICIAR O BANCO DE DADOS
def iniciar_db():
    conexao = conecta_database()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

# ROTA DA PÁGINA INICIAL
@app.route("/")
def index():
    iniciar_db()
    conexao = conecta_database()
    vagas = conexao.execute('SELECT * FROM vagas ORDER BY id_vaga DESC').fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", vagas=vagas, title=title)

# ROTA DA PÁGINA ACESSO
@app.route("/acesso", methods=['post'])
def acesso():
    usuario_informado = request.form["usuario"]
    senha_informada = request.form["senha"]
    if usuario == usuario_informado and senha == senha_informada:
        session["login"] = True
        return redirect('/adm')
    else:
        return render_template("login.html", msg="Usuário/Senha estão incorretos!")

# ROTA DA PÁGINA LOGIN
@app.route("/login")
def login():
    title = "Login"
    return render_template("login.html", title=title)

# ROTA DA PÁGINA ADM
@app.route("/adm")
def adm():
    if verifica_sessao():
        iniciar_db()
        conexao = conecta_database()
        vagas = conexao.execute('SELECT * FROM vagas ORDER BY id_vaga DESC').fetchall()
        conexao.close()
        title = "Administração"
        return render_template("adm.html", vagas=vagas, title=title)
    else:
        return redirect("/login")

# CÓDIGO DO LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')

# ROTA DA PÁGINA DE CADASTRO
@app.route("/cadProd")
def cadProd():
    if verifica_sessao():
        title = "Cadastro de Produtos"
        return render_template("cadProd.html", title=title)
    else:
        return redirect("/login")

# ROTA DA PÁGINA DE CADASTRO NO BANCO
@app.route("/cadastro", methods=["post"])
def cadastro():
    if verifica_sessao():
        nome_produto = request.form['tipo_vaga']
        quantidade_produto = request.form['cargo_vaga']
        validade_produto = request.form['requisitos_vaga']
        descricao_produto = request.form['salario_vaga']
        dropdown_produto = request.form['local_vaga']
        composicao_produto = request.form['email_vaga']
        img_produto = request.files['img_vaga']

        id_foto = str(uuid.uuid4().hex)
        filename = id_foto + nome_produto + '.png'
        img_produto.save("static/img/produtos/" + filename)

        conexao = conecta_database()
        conexao.execute('INSERT INTO vagas (cargo_vaga, requisitos_vaga, periodo_vaga, tipo_vaga, local_vaga, salario_vaga, email_vaga, img_vaga) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',(cargo_vaga, requisitos_vaga, periodo_vaga, tipo_vaga, local_vaga, salario_vaga, email_vaga, filename))
        conexao.commit()
        conexao.close() 

        return redirect("/adm")
    else:
        return redirect("/login")

# ROTA DE EXCLUSAO
@app.route("/excluir/<id_vaga>")
def excluir_vaga(id_vaga):
    if verifica_sessao():
        conexao = conecta_database()
        conexao.execute('DELETE FROM vagas WHERE id_vaga = ?', (id_vaga,))
        conexao.commit()
        conexao.close()
        return redirect("/adm")
    else:
        return redirect("/login")
    
# CRIAR A ROTA DO EDITAR
@app.route("/editvagas/<id_vaga>")
def editar(id_vaga):
    if verifica_sessao():
        conexao = conecta_database()
        vagas = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga)).fetchall()
        conexao.close()
        title = "Edição de vagas"
        return render_template("editvagas.html", vagas=vagas, title=title)
    else:
        return redirect("/login")
    
# CRIAR A ROTA PARA TRATAR A EDIÇÃO
@app.route("/editvagas", methods=['POST'])
def editvaga():
    id_vaga = request.form['id_vaga']
    nome_produto = request.form['tipo_vaga']
    quantidade_produto = request.form['cargo_vaga']
    validade_produto = request.form['requisitos_vaga']
    descricao_produto = request.form['salario_vaga']
    dropdown_produto = request.form['local_vaga']
    composicao_produto = request.form['email_vaga']
    img_produto = request.files['img_vaga']
    if img_produto:
        nomeantigo = request.form['nomeantigo']
        img_produto.save("static/img/vagas/" + nomeantigo)
    conexao = conecta_database()
    conexao.execute('UPDATE vagas SET tipo_vaga=?, cargo_vaga=?, requisitos_vaga=?, salario_vaga=? , local_vaga=? , email_vaga=? WHERE id_vaga=?',(tipo_vaga, cargo_vaga, requisitos_vaga, salario_vaga, local_vaga, email_vaga, id_vaga))
    conexao.commit()
    conexao.close()
    return redirect('/adm')

# ROTA DA PÁGINA DE BUSCA
@app.route("/busca", methods=["post"])
def busca():
    busca = request.form['buscar']
    conexao = conecta_database()
    vagas = conexao.execute('SELECT * FROM vagas WHERE cargo_vaga LIKE "%" || ? || "%"', (busca,)).fetchall()
    conexao.close()
    title = "Home"
    return render_template("home.html", vagas=vagas, title=title)

@app.route("/vervaga/<id_vaga>")
def vervaga(id_vaga):
    iniciar_db()
    conexao = conecta_database()
    vagas = conexao.execute('SELECT * FROM vagas WHERE id_vaga = ?', (id_vaga)).fetchall()
    conexao.close()
    title = "Exibição de vagas"
    return render_template("vervagas.html", vagas=vagas, title=title)

# FINAL DO CÓDIGO - EXECUTANDO O SERVIDOR
if __name__ == "__main__":
    app.run(debug=True)