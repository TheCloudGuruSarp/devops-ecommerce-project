from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import json
from api.products import products_bp
from api.orders import orders_bp
from api.users import users_bp
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app)

# Prometheus metrics
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'E-Commerce Application', version='1.0.0')

# Register blueprints
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(users_bp, url_prefix='/api/users')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'version': '1.0.0',
        'environment': os.environ.get('FLASK_ENV', 'development')
    })

# Root endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Welcome to E-Commerce API',
        'endpoints': [
            '/api/products',
            '/api/orders',
            '/api/users',
            '/health'
        ]
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'The requested resource was not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'error': 'Internal server error',
        'message': 'An unexpected error occurred'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('FLASK_ENV') == 'development')