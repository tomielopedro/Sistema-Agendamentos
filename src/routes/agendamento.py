from flask import Blueprint, request, jsonify
from src.models.user import db
from src.models.agendamento import Agendamento
from src.models.cliente import Cliente
from src.models.servico import Servico
from datetime import datetime, timedelta, timezone
from sqlalchemy import and_, or_

agendamento_bp = Blueprint('agendamento', __name__)


@agendamento_bp.route('/agendamentos', methods=['GET'])
def listar_agendamentos():

    """Lista todos os agendamentos com filtros opcionais
    ---
    tags:
      - Agendamentos
    parameters:
      - name: data_inicio
        in: query
        type: string
        required: false
        description: Data inicial para filtrar (ISO 8601)
      - name: data_fim
        in: query
        type: string
        required: false
        description: Data final para filtrar (ISO 8601)
      - name: status
        in: query
        type: string
        required: false
        description: Status do agendamento (agendado, concluido, cancelado)
      - name: cliente_id
        in: query
        type: integer
        required: false
    responses:
      200:
        description: Lista de agendamentos
    """
    try:
        # Parâmetros de filtro
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        status = request.args.get('status')
        cliente_id = request.args.get('cliente_id')

        query = Agendamento.query

        # Aplicar filtros
        if data_inicio:
            data_inicio_dt = datetime.fromisoformat(data_inicio)
            query = query.filter(Agendamento.data_agendamento >= data_inicio_dt)

        if data_fim:
            data_fim_dt = datetime.fromisoformat(data_fim)
            query = query.filter(Agendamento.data_agendamento <= data_fim_dt)

        if status:
            query = query.filter(Agendamento.status == status)

        if cliente_id:
            query = query.filter(Agendamento.cliente_id == cliente_id)

        # Ordenar por data de agendamento
        agendamentos = query.order_by(Agendamento.data_agendamento.asc()).all()

        return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos', methods=['POST'])
def criar_agendamento():
    """Cria um novo agendamento
    ---
    tags:
      - Agendamentos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          properties:
            cliente_id:
              type: integer
              example: 1
            servico_id:
              type: integer
              example: 2
            data_agendamento:
              type: string
              example: "2025-08-06T15:00:00Z"
            observacoes:
              type: string
              example: "Cliente prefere o período da tarde."
    responses:
      201:
        description: Agendamento criado com sucesso
    """
    try:
        data = request.get_json()

        # Validação básica
        if not data.get('cliente_id') or not data.get('servico_id') or not data.get('data_agendamento'):
            return jsonify({'erro': 'Cliente, serviço e data são obrigatórios'}), 400

        # Verificar se cliente existe
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404

        # Verificar se serviço existe e está ativo
        servico = Servico.query.get(data['servico_id'])
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404
        if not servico.ativo:
            return jsonify({'erro': 'Serviço não está ativo'}), 400

        # Converter data
        try:
            data_agendamento = datetime.fromisoformat(data['data_agendamento']).replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use ISO format'}), 400

        # Verificar se a data não é no passado
        if data_agendamento < datetime.now(timezone.utc):
            return jsonify({'erro': 'Não é possível agendar para datas passadas'}), 400

        # Verificar conflitos de horário
        data_fim = data_agendamento + timedelta(minutes=servico.duracao_minutos)

        agendamentos_existentes = Agendamento.query.filter_by(status='agendado').all()

        for ag in agendamentos_existentes:
            servico_existente = Servico.query.get(ag.servico_id)
            if not servico_existente:
                continue

            inicio_existente = ag.data_agendamento
            fim_existente = inicio_existente + timedelta(minutes=servico_existente.duracao_minutos)

            inicio_novo = data_agendamento
            fim_novo = data_agendamento + timedelta(minutes=servico.duracao_minutos)

            if (inicio_novo < fim_existente and fim_novo > inicio_existente):
                return jsonify({'erro': 'Horário não disponível. Há conflito com outro agendamento'}), 400


        agendamento = Agendamento(
            cliente_id=data['cliente_id'],
            servico_id=data['servico_id'],
            data_agendamento=data_agendamento,
            observacoes=data.get('observacoes', '')
        )

        db.session.add(agendamento)
        db.session.commit()

        return jsonify(agendamento.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['GET'])
def obter_agendamento(agendamento_id):
    """Obtém um agendamento específico"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['PUT'])
def atualizar_agendamento(agendamento_id):
    """Atualiza um agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        data = request.get_json()

        # Validação básica
        if not data.get('cliente_id') or not data.get('servico_id') or not data.get('data_agendamento'):
            return jsonify({'erro': 'Cliente, serviço e data são obrigatórios'}), 400

        # Verificar se cliente existe
        cliente = Cliente.query.get(data['cliente_id'])
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404

        # Verificar se serviço existe e está ativo
        servico = Servico.query.get(data['servico_id'])
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404
        if not servico.ativo:
            return jsonify({'erro': 'Serviço não está ativo'}), 400

        # Converter data
        try:
            data_agendamento = datetime.fromisoformat(data['data_agendamento']).replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use ISO format'}), 400

        # Verificar se a data não é no passado (apenas se mudou)
        if data_agendamento != agendamento.data_agendamento and data_agendamento < datetime.now(timezone.utc):
            return jsonify({'erro': 'Não é possível agendar para datas passadas'}), 400

        agendamento.cliente_id = data['cliente_id']
        agendamento.servico_id = data['servico_id']
        agendamento.data_agendamento = data_agendamento
        agendamento.observacoes = data.get('observacoes', '')
        agendamento.status = data.get('status', agendamento.status)

        db.session.commit()

        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos/<int:agendamento_id>/status', methods=['PATCH'])
def atualizar_status_agendamento(agendamento_id):
    """Atualiza apenas o status de um agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)
        data = request.get_json()

        if not data.get('status'):
            return jsonify({'erro': 'Status é obrigatório'}), 400

        status_validos = ['agendado', 'concluido', 'cancelado']
        if data['status'] not in status_validos:
            return jsonify({'erro': f'Status deve ser um dos: {", ".join(status_validos)}'}), 400

        agendamento.status = data['status']
        db.session.commit()

        return jsonify(agendamento.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos/<int:agendamento_id>', methods=['DELETE'])
def deletar_agendamento(agendamento_id):
    """Deleta um agendamento"""
    try:
        agendamento = Agendamento.query.get_or_404(agendamento_id)

        db.session.delete(agendamento)
        db.session.commit()

        return jsonify({'mensagem': 'Agendamento deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


@agendamento_bp.route('/agendamentos/disponibilidade', methods=['GET'])
def verificar_disponibilidade():
    """Verifica disponibilidade para uma data e serviço específicos"""
    try:
        data_str = request.args.get('data')
        servico_id = request.args.get('servico_id')

        if not data_str or not servico_id:
            return jsonify({'erro': 'Data e serviço são obrigatórios'}), 400

        try:
            data_agendamento = datetime.fromisoformat(data_str).replace(tzinfo=timezone.utc)
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido. Use ISO format'}), 400

        servico = Servico.query.get(servico_id)
        if not servico:
            return jsonify({'erro': 'Serviço não encontrado'}), 404

        # Verificar conflitos
        data_fim = data_agendamento + timedelta(minutes=servico.duracao_minutos)

        conflitos = Agendamento.query.filter(
            and_(
                Agendamento.status == 'agendado',
                or_(
                    and_(
                        Agendamento.data_agendamento <= data_agendamento,
                        Agendamento.data_agendamento + timedelta(minutes=servico.duracao_minutos) > data_agendamento
                    ),
                    and_(
                        Agendamento.data_agendamento < data_fim,
                        Agendamento.data_agendamento + timedelta(minutes=servico.duracao_minutos) >= data_fim
                    )
                )
            )
        ).first()

        disponivel = conflitos is None and data_agendamento >= datetime.now(timezone.utc)

        return jsonify({
            'disponivel': disponivel,
            'data': data_str,
            'servico_id': servico_id,
            'motivo': 'Horário ocupado' if conflitos else (
                'Data no passado' if data_agendamento < datetime.now() else 'Disponível')
        }), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

