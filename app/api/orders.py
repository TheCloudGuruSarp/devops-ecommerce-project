from flask import Blueprint, jsonify, request
from app.models.order import Order
import uuid
from datetime import datetime

orders_bp = Blueprint('orders', __name__, url_prefix='/api/orders')

# Sample order data (in a real app, this would come from a database)
order_list = [
    Order(
        "ord-001",
        "user123",
        [{'product_id': 1, 'quantity': 2}, {'product_id': 3, 'quantity': 1}],
        "processing",
        datetime(2023, 4, 1).isoformat()
    ),
    Order(
        "ord-002",
        "user456",
        [{'product_id': 2, 'quantity': 1}, {'product_id': 5, 'quantity': 3}],
        "shipped",
        datetime(2023, 3, 28).isoformat()
    )
]

@orders_bp.route('/')
def get_orders():
    return jsonify([order.to_dict() for order in order_list])

@orders_bp.route('/<string:order_id>')
def get_order(order_id):
    order = next((o for o in order_list if o.id == order_id), None)
    if order:
        return jsonify(order.to_dict())
    return jsonify({"error": "Order not found"}), 404

@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    if not data or not all(k in data for k in ('user_id', 'items')):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Generate a unique order ID
    order_id = f"ord-{uuid.uuid4().hex[:6]}"
    
    new_order = Order(
        order_id,
        data['user_id'],
        data['items'],
        "pending",
        datetime.now().isoformat()
    )
    order_list.append(new_order)
    return jsonify(new_order.to_dict()), 201

@orders_bp.route('/<string:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({"error": "Missing status field"}), 400
    
    order = next((o for o in order_list if o.id == order_id), None)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    order.status = data['status']
    return jsonify(order.to_dict())
