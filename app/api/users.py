from flask import Blueprint, jsonify, request
from models.user import User

users_bp = Blueprint('users', __name__)

# Sample user data (in a real app, this would come from a database)
user_list = [
    User(101, 'john.doe@example.com', 'John', 'Doe', 'password123', 'customer'),
    User(102, 'jane.smith@example.com', 'Jane', 'Smith', 'password456', 'customer'),
    User(103, 'admin@example.com', 'Admin', 'User', 'adminpass', 'admin')
]

@users_bp.route('/', methods=['GET'])
def get_users():
    """Get all users (admin only in a real app)"""
    # Add pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    start = (page - 1) * per_page
    end = start + per_page
    
    users_page = user_list[start:end]
    
    # In a real app, we would not return passwords
    return jsonify({
        'users': [user.to_dict(exclude_password=True) for user in users_page],
        'total': len(user_list),
        'page': page,
        'per_page': per_page,
        'pages': (len(user_list) + per_page - 1) // per_page
    })

@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = next((u for u in user_list if u.id == user_id), None)
    
    if user:
        return jsonify(user.to_dict(exclude_password=True))
    else:
        return jsonify({'error': 'User not found'}), 404

@users_bp.route('/', methods=['POST'])
def create_user():
    """Create a new user (register)"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    required_fields = ['email', 'first_name', 'last_name', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if email already exists
    if any(u.email == data['email'] for u in user_list):
        return jsonify({'error': 'Email already registered'}), 400
    
    # Generate a new ID (in a real app, the database would handle this)
    new_id = max(u.id for u in user_list) + 1
    
    # In a real app, we would hash the password
    new_user = User(
        id=new_id,
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        password=data['password'],  # This would be hashed in a real app
        role=data.get('role', 'customer')  # Default to customer role
    )
    
    user_list.append(new_user)
    
    return jsonify(new_user.to_dict(exclude_password=True)), 201

@users_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    user = next((u for u in user_list if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Update user fields
    if 'email' in data:
        # Check if new email already exists for another user
        if data['email'] != user.email and any(u.email == data['email'] for u in user_list):
            return jsonify({'error': 'Email already registered'}), 400
        user.email = data['email']
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'password' in data:
        # In a real app, we would hash the password
        user.password = data['password']
    
    if 'role' in data:
        valid_roles = ['customer', 'admin']
        if data['role'] not in valid_roles:
            return jsonify({'error': f'Invalid role. Must be one of: {valid_roles}'}), 400
        user.role = data['role']
    
    return jsonify(user.to_dict(exclude_password=True))

@users_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    user = next((u for u in user_list if u.id == user_id), None)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    user_list.remove(user)
    
    return jsonify({'message': f'User {user_id} deleted successfully'})

@users_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user = next((u for u in user_list if u.email == data['email']), None)
    
    if not user or user.password != data['password']:  # In a real app, we would verify the hashed password
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # In a real app, we would generate and return a JWT token here
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(exclude_password=True),
        'token': 'sample-jwt-token-would-be-generated-here'
    })