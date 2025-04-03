class User:
    """User model"""
    
    def __init__(self, id, email, first_name, last_name, password, role):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password  # In a real app, this would be hashed
        self.role = role  # 'customer' or 'admin'
    
    def to_dict(self, exclude_password=False):
        """Convert user to dictionary"""
        user_dict = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role
        }
        
        if not exclude_password:
            user_dict['password'] = self.password
        
        return user_dict