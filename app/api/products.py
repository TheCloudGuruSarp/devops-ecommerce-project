from flask import Blueprint, jsonify, request
from models.product import Product

products_bp = Blueprint('products', __name__)

# Sample product data (in a real app, this would come from a database)
product_list = [
    Product(1, 'Smartphone', 'Latest model smartphone with high-end features', 999.99, 50),
    Product(2, 'Laptop', 'Powerful laptop for professional use', 1499.99, 30),
    Product(3, 'Headphones', 'Noise cancelling wireless headphones', 249.99, 100),
    Product(4, 'Smartwatch', 'Fitness tracking smartwatch', 199.99, 75),
    Product(5, 'Tablet', '10-inch tablet with retina display', 399.99, 40)
]

@products_bp.route('/', methods=['GET'])
def get_products():
    """Get all products"""
    # Add pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    products_page = product_list[start:end]
    
    return jsonify({
        'products': [product.to_dict() for product in products_page],
        'total': len(product_list),
        'page': page,
        'per_page': per_page,
        'pages': (len(product_list) + per_page - 1) // per_page
    })

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = next((p for p in product_list if p.id == product_id), None)
    
    if product:
        return jsonify(product.to_dict())
    else:
        return jsonify({'error': 'Product not found'}), 404

@products_bp.route('/', methods=['POST'])
def create_product():
    """Create a new product"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    required_fields = ['name', 'description', 'price', 'stock']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Generate a new ID (in a real app, the database would handle this)
    new_id = max(p.id for p in product_list) + 1
    
    new_product = Product(
        id=new_id,
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        stock=int(data['stock'])
    )
    
    product_list.append(new_product)
    
    return jsonify(new_product.to_dict()), 201

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update an existing product"""
    product = next((p for p in product_list if p.id == product_id), None)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Update product fields
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = float(data['price'])
    if 'stock' in data:
        product.stock = int(data['stock'])
    
    return jsonify(product.to_dict())

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    product = next((p for p in product_list if p.id == product_id), None)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product_list.remove(product)
    
    return jsonify({'message': f'Product {product_id} deleted successfully'})