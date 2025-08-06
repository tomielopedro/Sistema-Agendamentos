from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.cliente import Cliente

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """Lista todos os clientes"""
    try:
        clientes = Cliente.query.all()
        return jsonify([cliente.to_dict() for cliente in clientes]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes', methods=['POST'])
def criar_cliente():
    """Cria um novo cliente"""
    try:
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('telefone'):
            return jsonify({'erro': 'Nome e telefone são obrigatórios'}), 400
        
        # Verifica se email já existe (se fornecido)
        if data.get('email'):
            cliente_existente = Cliente.query.filter_by(email=data['email']).first()
            if cliente_existente:
                return jsonify({'erro': 'Email já cadastrado'}), 400
        
        cliente = Cliente(
            nome=data['nome'],
            telefone=data['telefone'],
            email=data.get('email')
        )
        
        db.session.add(cliente)
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['GET'])
def obter_cliente(cliente_id):
    """Obtém um cliente específico"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """Atualiza um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        data = request.get_json()
        
        # Validação básica
        if not data.get('nome') or not data.get('telefone'):
            return jsonify({'erro': 'Nome e telefone são obrigatórios'}), 400
        
        # Verifica se email já existe em outro cliente (se fornecido)
        if data.get('email') and data['email'] != cliente.email:
            cliente_existente = Cliente.query.filter_by(email=data['email']).first()
            if cliente_existente:
                return jsonify({'erro': 'Email já cadastrado'}), 400
        
        cliente.nome = data['nome']
        cliente.telefone = data['telefone']
        cliente.email = data.get('email')
        
        db.session.commit()
        
        return jsonify(cliente.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@cliente_bp.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """Deleta um cliente"""
    try:
        cliente = Cliente.query.get_or_404(cliente_id)
        
        # Verifica se o cliente tem agendamentos
        if cliente.agendamentos:
            return jsonify({'erro': 'Não é possível deletar cliente com agendamentos'}), 400
        
        db.session.delete(cliente)
        db.session.commit()
        
        return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

