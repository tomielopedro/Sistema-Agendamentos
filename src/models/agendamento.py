from src.models.user import db
from datetime import datetime, timezone

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico_id = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_agendamento = db.Column(db.DateTime, nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    status = db.Column(db.String(20), default='agendado')  # agendado, concluido, cancelado
    observacoes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Agendamento {self.id} - Cliente: {self.cliente_id} - Serviço: {self.servico_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'servico_id': self.servico_id,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'cliente_nome': self.cliente.nome if self.cliente else None,
            'servico_nome': self.servico.nome if self.servico else None,
            'servico_preco': self.servico.preco if self.servico else None,
            'servico_duracao': self.servico.duracao_minutos if self.servico else None
        }

