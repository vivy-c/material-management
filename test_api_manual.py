#!/usr/bin/env python3
"""
Manual API Testing Script
Run this script to test your APIs with authentication
"""

import requests
import json
import time
from requests.sessions import Session

class OdooAPITester:
    def __init__(self, base_url='http://localhost:8069', database='db_test', username='vivycahyani@gmail.com', password='admin'):
        self.base_url = base_url
        self.database = database
        self.username = username
        self.password = password
        self.session = Session()
        self.timestamp = str(int(time.time()))
        self.authenticated = False
        
    def authenticate(self):
        """Authenticate with Odoo using web session"""
        auth_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': self.database,
                'login': self.username,
                'password': self.password
            },
            'id': 1
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}/web/session/authenticate',
                data=json.dumps(auth_data),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('result') and result['result'].get('uid'):
                    self.authenticated = True
                    print("✅ Authentication successful")
                    return True
                else:
                    print(f"❌ Authentication failed: {result.get('error', 'Unknown error')}")
                    return False
            else:
                print(f"❌ Authentication request failed with status {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Authentication error: {str(e)}")
            return False
    
    def test_suppliers_api(self):
        """Test Suppliers API endpoints"""
        print("\n🏢 Testing Suppliers API...")
        
        # Test GET all suppliers
        print("\n1. Testing GET /api/suppliers")
        response = self.call_api('/api/suppliers', {'operation': 'list'})
        if response and response.get('success'):
            print(f"✅ Found {response.get('count', 0)} suppliers")
        else:
            print(f"❌ Error: {response.get('error') if response else 'No response'}")
        
        # Test CREATE supplier with unique code and name
        print("\n2. Testing POST /api/suppliers")
        new_supplier = {
            'operation': 'create',
            'code': f'TESTSUP{self.timestamp}',
            'name': f'API Test Supplier {self.timestamp}',
            'email': f'test{self.timestamp}@apisupplier.com',
            'phone': '123-456-7890'
        }
        
        response = self.call_api('/api/suppliers', new_supplier)
        if response and response.get('success'):
            supplier_id = response['data']['id']
            print(f"✅ Supplier created with ID: {supplier_id}")
            return supplier_id
        else:
            print(f"❌ Create failed: {response.get('error') if response else 'No response'}")
            return None
    
    def test_materials_api(self, supplier_id=None):
        """Test Materials API endpoints"""
        print("\n📦 Testing Materials API...")
        
        # Create a supplier if none provided
        if not supplier_id:
            print("\n0. Creating test supplier for material tests")
            test_supplier = {
                'operation': 'create',
                'code': f'MATSUP{self.timestamp}',
                'name': f'Material Test Supplier {self.timestamp}',
                'email': f'matsup{self.timestamp}@test.com'
            }
            
            supplier_response = self.call_api('/api/suppliers', test_supplier)
            if not supplier_response or not supplier_response.get('success'):
                print("❌ Failed to create test supplier for materials")
                print(f"Supplier response: {supplier_response}")
                return
            
            supplier_id = supplier_response['data']['id']
            print(f"✅ Test supplier created with ID: {supplier_id}")
        
        # Test GET all materials
        print("\n1. Testing GET /api/materials")
        response = self.call_api('/api/materials', {'operation': 'list'})
        if response and response.get('success'):
            print(f"✅ Found {response.get('count', 0)} materials")
        else:
            print(f"❌ Error: {response.get('error') if response else 'No response'}")
        
        # Test CREATE material with the test supplier
        print("\n2. Testing POST /api/materials")
        new_material = {
            'operation': 'create',
            'code': f'TESTMAT{self.timestamp}',
            'name': f'API Test Material {self.timestamp}',
            'type': 'cotton',
            'buy_price': 175.0,
            'supplier_id': supplier_id
        }
        
        response = self.call_api('/api/materials', new_material)
        print(f"Debug - Material creation response: {response}")
        
        if response and response.get('success'):
            material_id = response['data']['id']
            print(f"✅ Material created with ID: {material_id}")
            
            # Test UPDATE material
            print("\n3. Testing PUT /api/materials")
            update_data = {
                'operation': 'update',
                'name': f'Updated API Test Material {self.timestamp}'
            }
            response = self.call_api(f'/api/materials/{material_id}', update_data)
            if response and response.get('success'):
                print("✅ Material updated successfully")
            else:
                print(f"❌ Update failed: {response.get('error') if response else 'No response'}")
            
            # Test DELETE material
            print("\n4. Testing DELETE /api/materials")
            delete_data = {'operation': 'delete'}
            response = self.call_api(f'/api/materials/{material_id}', delete_data)
            if response and response.get('success'):
                print("✅ Material deleted successfully")
            else:
                print(f"❌ Delete failed: {response.get('error') if response else 'No response'}")
        else:
            print(f"❌ Create failed: {response.get('error') if response else 'No response'}")
    
    def test_public_access(self):
        """Test that APIs are accessible after authentication"""
        temp_session = Session()
        response = temp_session.post(
            f'{self.base_url}/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {'operation': 'list'},
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('result', {}).get('success'):
                print("✅ API is accessible")
                return True
        
        print("❌ API access failed - authentication required")
        return False
    
    def call_api(self, endpoint, data):
        """Make API call using JSON-RPC with authentication"""
        if not self.authenticated:
            print("❌ Not authenticated. Please authenticate first.")
            return None
            
        api_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': data,
            'id': 1
        }
        
        try:
            response = self.session.post(
                f'{self.base_url}{endpoint}',
                data=json.dumps(api_data),
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result')
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return None

def main():
    print("🚀 Starting Odoo Authenticated API Tests")
    print("=" * 50)
    
    # Initialize tester with authentication credentials
    tester = OdooAPITester(
        base_url='http://localhost:8069',
        database='db_test',
        username='vivycahyani@gmail.com',
        password='admin'
    )
    
    # Authenticate first
    if not tester.authenticate():
        print("❌ Authentication failed. Cannot proceed with tests.")
        return
    
    # Test API accessibility
    tester.test_public_access()
    
    # Test Suppliers API
    supplier_id = tester.test_suppliers_api()
    
    # Test Materials API
    tester.test_materials_api(supplier_id)
    
    print("\n" + "=" * 50)
    print("🎉 Authenticated API Tests Completed!")

if __name__ == '__main__':
    main()