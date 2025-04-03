import unittest
import json
from app import app

class ProductsTestCase(unittest.TestCase):
    """Test case for the products API"""
    
    def setUp(self):
        """Set up test client"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_get_products(self):
        """Test getting all products"""
        response = self.app.get('/api/products/')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('products', data)
        self.assertIn('total', data)
        self.assertGreater(len(data['products']), 0)
    
    def test_get_product(self):
        """Test getting a specific product"""
        # Test valid product ID
        response = self.app.get('/api/products/1')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['id'], 1)
        
        # Test invalid product ID
        response = self.app.get('/api/products/999')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
    
    def test_create_product(self):
        """Test creating a new product"""
        product_data = {
            'name': 'Test Product',
            'description': 'This is a test product',
            'price': 99.99,
            'stock': 10
        }
        
        response = self.app.post(
            '/api/products/',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], 'Test Product')
        self.assertEqual(data['price'], 99.99)
    
    def test_update_product(self):
        """Test updating a product"""
        update_data = {
            'name': 'Updated Product',
            'price': 129.99
        }
        
        response = self.app.put(
            '/api/products/1',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], 'Updated Product')
        self.assertEqual(data['price'], 129.99)
    
    def test_delete_product(self):
        """Test deleting a product"""
        # First create a product to delete
        product_data = {
            'name': 'Product to Delete',
            'description': 'This product will be deleted',
            'price': 49.99,
            'stock': 5
        }
        
        create_response = self.app.post(
            '/api/products/',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        create_data = json.loads(create_response.data)
        product_id = create_data['id']
        
        # Now delete the product
        delete_response = self.app.delete(f'/api/products/{product_id}')
        delete_data = json.loads(delete_response.data)
        
        self.assertEqual(delete_response.status_code, 200)
        self.assertIn('deleted successfully', delete_data['message'])
        
        # Verify it's gone
        get_response = self.app.get(f'/api/products/{product_id}')
        self.assertEqual(get_response.status_code, 404)

if __name__ == '__main__':
    unittest.main()