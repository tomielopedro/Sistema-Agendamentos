import os
import sys
from flask import Flask, send_from_directory
from flasgger import Swagger

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.models.user import db
from src.models.cliente import Cliente
from src.models.servico import Servico
from src.models.agendamento import Agendamento
from src.routes.user import user_bp
from src.routes.cliente import cliente_bp
from src.routes.servico import servico_bp
from src.routes.agendamento import agendamento_bp
from src.routes.dashboard import dashboard_bp

# Configuração básica do Flask
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialização do banco de dados
db.init_app(app)
with app.app_context():
    db.create_all()

# Swagger config
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/api/docs/swagger.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Agendamentos",
        "description": "Documentação da API com Swagger UI",
        "version": "1.0.0"
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

# Registro de blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(cliente_bp, url_prefix='/api')
app.register_blueprint(servico_bp, url_prefix='/api')
app.register_blueprint(agendamento_bp, url_prefix='/api')
app.register_blueprint(dashboard_bp, url_prefix='/api')

# Rota para servir o front (SPA)
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

# Inicialização do servidor
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
