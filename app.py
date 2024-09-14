from flask import *
from database import db
from flask_migrate import Migrate
from models import Tarefas

app = Flask(__name__)
app.config["SECRET_KEY"] = "65fa568dbbc05b134708062f004c3141bd93bc79f847a490386a56d99ae6f1ab"

conexao = "mysql+pymysql://alunos:cefetmg@127.0.0.1/bd_tarefas"
app.config['SQLALCHEMY_DATABASE_URI'] = conexao
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/tarefas")
def tarefas():
    p = Tarefas.query.all()
    return render_template("tarefas.html", dados=p)

@app.route("/tarefas/add")
def tarefas_add():
    return render_template("tarefas_add.html")

@app.route("/tarefas/save", methods=["POST"])
def save():
    descricao = request.form.get("descricao")
    data_conclusao = request.form.get("data_conclusao")
    prioridade = request.form.get("prioridade")
    if descricao and data_conclusao and prioridade:
        tarefas = Tarefas(descricao, data_conclusao, prioridade)
        db.session.add(tarefas)
        db.session.commit()
        flash("Tarefa cadastrada")
        return redirect('/tarefas')
    else:
        flash("Preencha todos os campos")
        return redirect('/tarefas/add')
    
@app.route("/tarefas/remove/<int:id>")
def tarefas_remove(id):
    tarefas = Tarefas.query.get(id)
    if tarefas:
        db.session.delete(tarefas)
        db.session.commit()
        flash("Tarefa removida!!")
        return redirect("/tarefas")
    else:
        flash("Caminho Incorreto!!")
        return redirect("/tarefas")

@app.route("/tarefas/edit/<int:id>")
def tarefas_edit(id):
    try:
        tarefas = Tarefas.query.get(id)
        return render_template("tarefas_edit.html", dados=tarefas)
    except:
        flash("Tarefa Inválida")
        return redirect("/tarefas")
    
@app.route("/tarefas/editsave", methods=["POST"])
def tarefas_edit_save():
    id = request.form.get("id")
    descricao = request.form.get("descricao")
    data_conclusao = request.form.get("data_conclusao")
    prioridade = request.form.get("prioridade")

    if id and descricao and data_conclusao and prioridade:
        plano = Tarefas.query.get(id)
        plano.descricao = descricao
        plano.data_conclusao = data_conclusao
        plano.prioridade = prioridade
        db.session.commit()
        flash("Dados alterados com sucesso!!")
        return redirect("/tarefas")
    else:
        flash("Preencha todas as informações")
        return redirect("/tarefas")

if __name__ == '__main__':
    app.run()