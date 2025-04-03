class OrderItem:
    """Order item model"""
    
    def __init__(self, product_id, quantity, price):
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }

class Order:
    """Order model"""
    
    def __init__(self, id, user_id, items, total, status, created_at):
        self.id = id
        self.user_id = user_id
        self.items = items  # List of OrderItem objects
        self.total = total
        self.status = status
        self.created_at = created_at
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': [item.to_dict() for item in self.items],
            'total': self.total,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }