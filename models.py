from database import db

class Tarefas(db.Model):
    
    __tablename__= "tb_tarefas"
    id_tarefas = db.Column(db.Integer, primary_key = True)
    descricao = db.Column(db.Text)
    data_conclusao = db.Column(db.Date)
    prioridade = db.Column(db.String(20))

    def __init__(self, descricao, data_conclusao, prioridade):
        self.descricao = descricao
        self.data_conclusao = data_conclusao
        self.prioridade = prioridade

    def __repr__(self):
        return "<Descricao {}>".format(self.descricao)