from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Import and register blueprints
    from app.api.products import products_bp
    from app.api.orders import orders_bp
    
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)

    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}, 200

    return app
