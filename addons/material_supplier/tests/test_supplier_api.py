import json
import time
from odoo.tests.common import HttpCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestSupplierAPI(HttpCase):
    
    def setUp(self):
        super().setUp()
        # Create test supplier with unique name
        timestamp = str(int(time.time()))
        self.supplier = self.env['material.supplier'].create({
            'code': f'TESTSUP{timestamp}',
            'name': f'Test Supplier {timestamp}',
            'email': f'test{timestamp}@supplier.com',
            'phone': '123456789'
        })
        
        # No authentication needed for public APIs
    
    def test_get_suppliers(self):
        """Test GET /api/suppliers"""
        response = self.url_open(
            '/api/suppliers',
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
    
    def test_create_supplier(self):
        """Test POST /api/suppliers"""
        timestamp = str(int(time.time()))
        supplier_data = {
            'operation': 'create',  # Added missing operation parameter
            'code': f'NEWSUP{timestamp}',
            'name': f'New Supplier {timestamp}',
            'email': f'new{timestamp}@supplier.com',
            'phone': '987654321'
        }
        
        response = self.url_open(
            '/api/suppliers',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': supplier_data,
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertTrue(result['result']['success'])
        self.assertEqual(result['result']['data']['code'], f'NEWSUP{timestamp}')
    
    def test_supplier_with_materials_deletion_prevention(self):
        """Test that suppliers with materials cannot be deleted"""
        # Create material for this supplier
        timestamp = str(int(time.time()))
        self.env['material.management'].create({
            'code': f'MATFORSUP{timestamp}',
            'name': f'Material for Supplier {timestamp}',
            'type': 'cotton',
            'buy_price': 150.0,
            'supplier_id': self.supplier.id
        })
        
        response = self.url_open(
            f'/api/suppliers/{self.supplier.id}',
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
        self.assertFalse(result['result']['success'])
        self.assertIn('materials', result['result']['error'].lower())