class Order:
    def __init__(self, id, user_id, items, status, created_at):
        self.id = id
        self.user_id = user_id
        self.items = items  # List of dicts with product_id and quantity
        self.status = status  # pending, processing, shipped, delivered
        self.created_at = created_at
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'items': self.items,
            'status': self.status,
            'created_at': self.created_at
        }
