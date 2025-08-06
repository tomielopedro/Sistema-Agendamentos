from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.agendamento import Agendamento
from src.models.cliente import Cliente
from src.models.servico import Servico
from datetime import datetime, timedelta
from sqlalchemy import func, and_

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard/estatisticas', methods=['GET'])
def obter_estatisticas():
    """Obtém estatísticas gerais do salão"""
    try:
        hoje = datetime.now().date()
        inicio_mes = hoje.replace(day=1)
        inicio_semana = hoje - timedelta(days=hoje.weekday())
        
        # Estatísticas básicas
        total_clientes = Cliente.query.count()
        total_servicos = Servico.query.filter_by(ativo=True).count()
        
        # Agendamentos de hoje
        agendamentos_hoje = Agendamento.query.filter(
            func.date(Agendamento.data_agendamento) == hoje
        ).count()
        
        # Agendamentos desta semana
        agendamentos_semana = Agendamento.query.filter(
            and_(
                Agendamento.data_agendamento >= inicio_semana,
                Agendamento.data_agendamento < inicio_semana + timedelta(days=7)
            )
        ).count()
        
        # Agendamentos deste mês
        agendamentos_mes = Agendamento.query.filter(
            Agendamento.data_agendamento >= inicio_mes
        ).count()
        
        # Receita do mês (apenas agendamentos concluídos)
        receita_mes = db.session.query(func.sum(Servico.preco)).join(
            Agendamento, Servico.id == Agendamento.servico_id
        ).filter(
            and_(
                Agendamento.data_agendamento >= inicio_mes,
                Agendamento.status == 'concluido'
            )
        ).scalar() or 0
        
        # Agendamentos por status
        agendamentos_por_status = db.session.query(
            Agendamento.status,
            func.count(Agendamento.id)
        ).group_by(Agendamento.status).all()
        
        status_dict = {status: count for status, count in agendamentos_por_status}
        
        return jsonify({
            'total_clientes': total_clientes,
            'total_servicos': total_servicos,
            'agendamentos_hoje': agendamentos_hoje,
            'agendamentos_semana': agendamentos_semana,
            'agendamentos_mes': agendamentos_mes,
            'receita_mes': float(receita_mes),
            'agendamentos_por_status': status_dict
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/agendamentos-hoje', methods=['GET'])
def agendamentos_hoje():
    """Obtém agendamentos de hoje"""
    try:
        hoje = datetime.now().date()
        
        agendamentos = Agendamento.query.filter(
            func.date(Agendamento.data_agendamento) == hoje
        ).order_by(Agendamento.data_agendamento.asc()).all()
        
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/proximos-agendamentos', methods=['GET'])
def proximos_agendamentos():
    """Obtém próximos agendamentos (próximos 7 dias)"""
    try:
        agora = datetime.now()
        limite = agora + timedelta(days=7)
        
        agendamentos = Agendamento.query.filter(
            and_(
                Agendamento.data_agendamento >= agora,
                Agendamento.data_agendamento <= limite,
                Agendamento.status == 'agendado'
            )
        ).order_by(Agendamento.data_agendamento.asc()).limit(10).all()
        
        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/servicos-populares', methods=['GET'])
def servicos_populares():
    """Obtém serviços mais populares do mês"""
    try:
        inicio_mes = datetime.now().replace(day=1)
        
        servicos_populares = db.session.query(
            Servico.nome,
            Servico.preco,
            func.count(Agendamento.id).label('total_agendamentos'),
            func.sum(Servico.preco).label('receita_total')
        ).join(
            Agendamento, Servico.id == Agendamento.servico_id
        ).filter(
            Agendamento.data_agendamento >= inicio_mes
        ).group_by(
            Servico.id, Servico.nome, Servico.preco
        ).order_by(
            func.count(Agendamento.id).desc()
        ).limit(5).all()
        
        resultado = []
        for nome, preco, total, receita in servicos_populares:
            resultado.append({
                'nome': nome,
                'preco': float(preco),
                'total_agendamentos': total,
                'receita_total': float(receita or 0)
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/receita-diaria', methods=['GET'])
def receita_diaria():
    """Obtém receita diária dos últimos 30 dias"""
    try:
        inicio = datetime.now() - timedelta(days=30)
        
        receita_diaria = db.session.query(
            func.date(Agendamento.data_agendamento).label('data'),
            func.sum(Servico.preco).label('receita')
        ).join(
            Servico, Agendamento.servico_id == Servico.id
        ).filter(
            and_(
                Agendamento.data_agendamento >= inicio,
                Agendamento.status == 'concluido'
            )
        ).group_by(
            func.date(Agendamento.data_agendamento)
        ).order_by(
            func.date(Agendamento.data_agendamento).asc()
        ).all()
        
        resultado = []
        for data, receita in receita_diaria:
            resultado.append({
                'data': data.isoformat(),
                'receita': float(receita or 0)
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@dashboard_bp.route('/dashboard/clientes-frequentes', methods=['GET'])
def clientes_frequentes():
    """Obtém clientes mais frequentes"""
    try:
        clientes_frequentes = db.session.query(
            Cliente.nome,
            Cliente.telefone,
            func.count(Agendamento.id).label('total_agendamentos'),
            func.max(Agendamento.data_agendamento).label('ultimo_agendamento')
        ).join(
            Agendamento, Cliente.id == Agendamento.cliente_id
        ).group_by(
            Cliente.id, Cliente.nome, Cliente.telefone
        ).order_by(
            func.count(Agendamento.id).desc()
        ).limit(10).all()
        
        resultado = []
        for nome, telefone, total, ultimo in clientes_frequentes:
            resultado.append({
                'nome': nome,
                'telefone': telefone,
                'total_agendamentos': total,
                'ultimo_agendamento': ultimo.isoformat() if ultimo else None
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

