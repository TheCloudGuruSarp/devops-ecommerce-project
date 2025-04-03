from flask import Blueprint, jsonify, request
from app.models.product import Product

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

# Sample product data (in a real app, this would come from a database)
product_list = [
    Product(1, "Smartphone", "Latest model with high-end features", 999.99),
    Product(2, "Laptop", "Powerful laptop for professionals", 1499.99),
    Product(3, "Headphones", "Noise-cancelling wireless headphones", 299.99),
    Product(4, "Smartwatch", "Fitness and health tracking", 249.99),
    Product(5, "Tablet", "Lightweight and portable", 599.99)
]

@products_bp.route('/')
def get_products():
    return jsonify([product.to_dict() for product in product_list])

@products_bp.route('/<int:product_id>')
def get_product(product_id):
    product = next((p for p in product_list if p.id == product_id), None)
    if product:
        return jsonify(product.to_dict())
    return jsonify({"error": "Product not found"}), 404

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'description', 'price')):
        return jsonify({"error": "Missing required fields"}), 400
    
    # In a real app, we would save to a database and get a new ID
    new_id = max(p.id for p in product_list) + 1
    new_product = Product(
        new_id,
        data['name'],
        data['description'],
        float(data['price'])
    )
    product_list.append(new_product)
    return jsonify(new_product.to_dict()), 201
