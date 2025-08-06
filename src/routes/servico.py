from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.servico import Servico

servico_bp = Blueprint('servico', __name__)

@servico_bp.route('/servicos', methods=['GET'])
def listar_servicos():
    """Lista todos os serviços"""
    try:
        # Filtrar apenas serviços ativos por padrão
        apenas_ativos = request.args.get('apenas_ativos', 'true').lower() == 'true'
        
        if apenas_ativos:
            servicos = Servico.query.filter_by(ativo=True).all()
        else:
            servicos = Servico.query.all()
            
        return jsonify([servico.to_dict() for servico in servicos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos', methods=['POST'])
def criar_servico():
    """Cria um novo serviço"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('preco') or not data.get('duracao_minutos'):
            return jsonify({'erro': 'Nome, preço e duração são obrigatórios'}), 400
        
        if data['preco'] <= 0:
            return jsonify({'erro': 'Preço deve ser maior que zero'}), 400
            
        if data['duracao_minutos'] <= 0:
            return jsonify({'erro': 'Duração deve ser maior que zero'}), 400
        
        servico = Servico(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            preco=float(data['preco']),
            duracao_minutos=int(data['duracao_minutos']),
            ativo=data.get('ativo', True)
        )
        
        db.session.add(servico)
        db.session.commit()
        
        return jsonify(servico.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['GET'])
def obter_servico(servico_id):
    """Obtém um serviço específico"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        return jsonify(servico.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['PUT'])
def atualizar_servico(servico_id):
    """Atualiza um serviço"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('preco') or not data.get('duracao_minutos'):
            return jsonify({'erro': 'Nome, preço e duração são obrigatórios'}), 400
        
        if data['preco'] <= 0:
            return jsonify({'erro': 'Preço deve ser maior que zero'}), 400
            
        if data['duracao_minutos'] <= 0:
            return jsonify({'erro': 'Duração deve ser maior que zero'}), 400
        
        servico.nome = data['nome']
        servico.descricao = data.get('descricao', '')
        servico.preco = float(data['preco'])
        servico.duracao_minutos = int(data['duracao_minutos'])
        servico.ativo = data.get('ativo', True)
        
        db.session.commit()
        
        return jsonify(servico.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>', methods=['DELETE'])
def deletar_servico(servico_id):
    """Deleta um serviço"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        
        # Verifica se o serviço tem agendamentos
        if servico.agendamentos:
            return jsonify({'erro': 'Não é possível deletar serviço com agendamentos'}), 400
        
        db.session.delete(servico)
        db.session.commit()
        
        return jsonify({'mensagem': 'Serviço deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@servico_bp.route('/servicos/<int:servico_id>/toggle', methods=['PATCH'])
def toggle_servico_ativo(servico_id):
    """Ativa/desativa um serviço"""
    try:
        servico = Servico.query.get_or_404(servico_id)
        servico.ativo = not servico.ativo
        
        db.session.commit()
        
        return jsonify(servico.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

