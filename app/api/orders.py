from flask import Blueprint, jsonify, request
from models.order import Order, OrderItem
import datetime

orders_bp = Blueprint('orders', __name__)

# Sample order data (in a real app, this would come from a database)
order_list = [
    Order(
        id=1,
        user_id=101,
        items=[
            OrderItem(product_id=1, quantity=2, price=999.99),
            OrderItem(product_id=3, quantity=1, price=249.99)
        ],
        total=2249.97,
        status='completed',
        created_at=datetime.datetime(2023, 4, 1, 10, 30, 0)
    ),
    Order(
        id=2,
        user_id=102,
        items=[
            OrderItem(product_id=2, quantity=1, price=1499.99),
        ],
        total=1499.99,
        status='processing',
        created_at=datetime.datetime(2023, 4, 2, 14, 45, 0)
    )
]

@orders_bp.route('/', methods=['GET'])
def get_orders():
    """Get all orders"""
    # Add pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Filter by user_id if provided
    user_id = request.args.get('user_id', type=int)
    filtered_orders = order_list
    if user_id:
        filtered_orders = [order for order in order_list if order.user_id == user_id]
    
    start = (page - 1) * per_page
    end = start + per_page
    
    orders_page = filtered_orders[start:end]
    
    return jsonify({
        'orders': [order.to_dict() for order in orders_page],
        'total': len(filtered_orders),
        'page': page,
        'per_page': per_page,
        'pages': (len(filtered_orders) + per_page - 1) // per_page
    })

@orders_bp.route('/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a specific order by ID"""
    order = next((o for o in order_list if o.id == order_id), None)
    
    if order:
        return jsonify(order.to_dict())
    else:
        return jsonify({'error': 'Order not found'}), 404

@orders_bp.route('/', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    required_fields = ['user_id', 'items']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'Items must be a non-empty list'}), 400
    
    # Generate a new ID (in a real app, the database would handle this)
    new_id = max(o.id for o in order_list) + 1
    
    # Create order items
    order_items = []
    total = 0
    
    for item_data in data['items']:
        if not all(k in item_data for k in ['product_id', 'quantity', 'price']):
            return jsonify({'error': 'Each item must have product_id, quantity, and price'}), 400
        
        item = OrderItem(
            product_id=item_data['product_id'],
            quantity=int(item_data['quantity']),
            price=float(item_data['price'])
        )
        order_items.append(item)
        total += item.quantity * item.price
    
    # Create the order
    new_order = Order(
        id=new_id,
        user_id=data['user_id'],
        items=order_items,
        total=total,
        status='pending',
        created_at=datetime.datetime.now()
    )
    
    order_list.append(new_order)
    
    return jsonify(new_order.to_dict()), 201

@orders_bp.route('/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Update an existing order"""
    order = next((o for o in order_list if o.id == order_id), None)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Update order status
    if 'status' in data:
        valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled', 'completed']
        if data['status'] not in valid_statuses:
            return jsonify({'error': f'Invalid status. Must be one of: {valid_statuses}'}), 400
        order.status = data['status']
    
    return jsonify(order.to_dict())

@orders_bp.route('/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Delete an order"""
    order = next((o for o in order_list if o.id == order_id), None)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    order_list.remove(order)
    
    return jsonify({'message': f'Order {order_id} deleted successfully'})