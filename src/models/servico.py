from src.models.user import db

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    preco = db.Column(db.Float, nullable=False)
    duracao_minutos = db.Column(db.Integer, nullable=False)  # duração em minutos
    ativo = db.Column(db.Boolean, default=True)
    
    # Relacionamento com agendamentos
    agendamentos = db.relationship('Agendamento', backref='servico', lazy=True)

    def __repr__(self):
        return f'<Servico {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': self.preco,
            'duracao_minutos': self.duracao_minutos,
            'ativo': self.ativo
        }

