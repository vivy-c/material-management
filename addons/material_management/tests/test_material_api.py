import json
import time
from odoo.tests.common import HttpCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestMaterialAPI(HttpCase):
    
    def setUp(self):
        super().setUp()
        # Create test data with unique names
        timestamp = str(int(time.time()))
        self.supplier = self.env['material.supplier'].create({
            'code': f'TESTSUP{timestamp}',
            'name': f'Test Supplier {timestamp}',
            'email': f'test{timestamp}@supplier.com'
        })
        
        self.material = self.env['material.management'].create({
            'code': f'TESTMAT{timestamp}',
            'name': f'Test Material {timestamp}',
            'type': 'cotton',
            'buy_price': 150.0,
            'supplier_id': self.supplier.id
        })
        
        # APIs are now public - no authentication needed
    
    def test_get_materials_public(self):
        """Test GET /api/materials with public access"""
        response = self.url_open(
            '/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {'operation': 'list'},  # Added missing operation parameter
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])
        self.assertGreater(result['result']['count'], 0)
    
    def test_public_access_without_session(self):
        """Test API access without any session/authentication"""
        # Ensure we're logged out
        self.logout()
        
        response = self.url_open(
            '/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {'operation': 'list'},  # Added missing operation parameter
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        # Should work fine since APIs are public
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])

    # Remove the conflicting test_get_materials_unauthenticated method
    # since APIs are now public and should work without authentication
    
    def test_create_material_success(self):
        """Test POST /api/materials with valid data"""
        timestamp = str(int(time.time()))
        material_data = {
            'operation': 'create',  # Added missing operation parameter
            'code': f'NEWMAT{timestamp}',
            'name': f'New Test Material {timestamp}',
            'type': 'fabric',
            'buy_price': 200.0,
            'supplier_id': self.supplier.id
        }
        
        response = self.url_open(
            '/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': material_data,
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])
        self.assertEqual(result['result']['data']['code'], f'NEWMAT{timestamp}')
    
    def test_create_material_validation_error(self):
        """Test POST /api/materials with invalid data"""
        invalid_data = {
            'operation': 'create',  # Added missing operation parameter
            'code': 'INVALID',
            'name': 'Invalid Material',
            'type': 'invalid_type',  # Invalid type
            'buy_price': 50,  # Below minimum
            'supplier_id': 999  # Non-existent supplier
        }
        
        response = self.url_open(
            '/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': invalid_data,
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertFalse(result['result']['success'])
        self.assertIn('error', result['result'])
    
    def test_update_material(self):
        """Test PUT /api/materials/<id>"""
        update_data = {
            'operation': 'update',  # Added missing operation parameter
            'name': 'Updated Material Name',
            'buy_price': 175.0
        }
        
        response = self.url_open(
            f'/api/materials/{self.material.id}',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': update_data,
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])
        self.assertEqual(result['result']['data']['name'], 'Updated Material Name')
    
    def test_delete_material(self):
        """Test DELETE /api/materials/<id>"""
        response = self.url_open(
            f'/api/materials/{self.material.id}',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {'operation': 'delete'},  # Added missing operation parameter
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])
        
        # Verify material is deleted
        self.assertFalse(self.material.exists())