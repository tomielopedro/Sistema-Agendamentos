from flask import Blueprint, jsonify, request
from src.models.user import User, db

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Lista todos os usuários
    ---
    responses:
      200:
        description: Lista de usuários
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              username:
                type: string
              email:
                type: string
    """
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Cria um novo usuário
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            email:
              type: string
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
    """
    data = request.json
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retorna um usuário pelo ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Usuário encontrado
        schema:
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
    """
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualiza um usuário
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            username:
              type: string
            email:
              type: string
    responses:
      200:
        description: Usuário atualizado com sucesso
        schema:
          properties:
            id:
              type: integer
            username:
              type: string
            email:
              type: string
    """
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify(user.to_dict())


@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deleta um usuário
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
    responses:
      204:
        description: Usuário deletado com sucesso
    """
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
