#!/usr/bin/env python3
"""
Manual API Testing Script
Run this script to test your secure APIs
"""

import requests
import json
import time
from requests.sessions import Session

class OdooAPITester:
    def __init__(self, base_url='http://localhost:8069', database='db_test'):
        self.base_url = base_url
        self.database = database
        self.session = Session()
        self.authenticated = False
        self.timestamp = str(int(time.time()))  # Add timestamp for unique names
    
    def login(self, username='admin', password='admin'):
        """Login to Odoo and get session cookies"""
        print(f"🔐 Logging in as {username}...")
        
        login_url = f"{self.base_url}/web/session/authenticate"
        login_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'db': self.database,
                'login': username,
                'password': password
            },
            'id': 1
        }
        
        response = self.session.post(
            login_url,
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('result') and result['result'].get('uid'):
                print("✅ Login successful!")
                self.authenticated = True
                return True
        
        print("❌ Login failed!")
        return False
    
    def test_suppliers_api(self):
        """Test Suppliers API endpoints"""
        print("\n🏢 Testing Suppliers API...")
        
        # Test GET all suppliers
        print("\n1. Testing GET /api/suppliers")
        response = self.call_api_get('/api/suppliers')
        if response and response.get('success'):
            print(f"✅ Found {response.get('count', 0)} suppliers")
        else:
            print(f"❌ Error: {response.get('error') if response else 'No response'}")
        
        # Test CREATE supplier with unique code and name
        print("\n2. Testing POST /api/suppliers")
        new_supplier = {
            'code': f'TESTSUP{self.timestamp}',
            'name': f'API Test Supplier {self.timestamp}',
            'email': f'test{self.timestamp}@apisupplier.com',
            'phone': '123-456-7890'
        }
        
        response = self.call_api_post('/api/suppliers', new_supplier)
        if response and response.get('success'):
            supplier_id = response['data']['id']
            print(f"✅ Supplier created with ID: {supplier_id}")
            
            # Test UPDATE supplier
            print("\n3. Testing PUT /api/suppliers")
            update_data = {'name': f'Updated API Test Supplier {self.timestamp}'}
            response = self.call_api_put(f'/api/suppliers/{supplier_id}', update_data)
            if response and response.get('success'):
                print("✅ Supplier updated successfully")
            else:
                print(f"❌ Update failed: {response.get('error') if response else 'No response'}")
            
            # Test DELETE supplier
            print("\n4. Testing DELETE /api/suppliers")
            response = self.call_api_delete(f'/api/suppliers/{supplier_id}')
            if response and response.get('success'):
                print("✅ Supplier deleted successfully")
                return None  # Supplier deleted, can't use for materials
            else:
                print(f"❌ Delete failed: {response.get('error') if response else 'No response'}")
                return supplier_id  # Return ID if delete failed
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
                'code': f'MATSUP{self.timestamp}',
                'name': f'Material Test Supplier {self.timestamp}',
                'email': f'matsup{self.timestamp}@test.com'
            }
            
            supplier_response = self.call_api_post('/api/suppliers', test_supplier)
            if not supplier_response or not supplier_response.get('success'):
                print("❌ Failed to create test supplier for materials")
                return
            
            supplier_id = supplier_response['data']['id']
            print(f"✅ Test supplier created with ID: {supplier_id}")
        
        # Test GET all materials
        print("\n1. Testing GET /api/materials")
        response = self.call_api_get('/api/materials')
        if response and response.get('success'):
            print(f"✅ Found {response.get('count', 0)} materials")
        else:
            print(f"❌ Error: {response.get('error') if response else 'No response'}")
        
        # Test CREATE material with the test supplier
        print("\n2. Testing POST /api/materials")
        new_material = {
            'code': f'TESTMAT{self.timestamp}',
            'name': f'API Test Material {self.timestamp}',
            'type': 'cotton',
            'buy_price': 175.0,
            'supplier_id': supplier_id
        }
        
        response = self.call_api_post('/api/materials', new_material)
        if response and response.get('success'):
            material_id = response['data']['id']
            print(f"✅ Material created with ID: {material_id}")
            
            # Test UPDATE material
            print("\n3. Testing PUT /api/materials")
            update_data = {'name': f'Updated API Test Material {self.timestamp}'}
            response = self.call_api_put(f'/api/materials/{material_id}', update_data)
            if response and response.get('success'):
                print("✅ Material updated successfully")
            else:
                print(f"❌ Update failed: {response.get('error') if response else 'No response'}")
            
            # Test DELETE material
            print("\n4. Testing DELETE /api/materials")
            response = self.call_api_delete(f'/api/materials/{material_id}')
            if response and response.get('success'):
                print("✅ Material deleted successfully")
            else:
                print(f"❌ Delete failed: {response.get('error') if response else 'No response'}")
        else:
            print(f"❌ Create failed: {response.get('error') if response else 'No response'}")
    
    def test_authentication(self):
        """Test authentication requirements"""
        print("\n🔒 Testing Authentication...")
        
        # Test without authentication
        print("\n1. Testing API without authentication")
        temp_session = Session()
        response = temp_session.post(
            f'{self.base_url}/api/materials',
            data=json.dumps({
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {},
                'id': 1
            }),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code in [302, 403] or 'session' in response.text.lower():
            print("✅ Authentication is properly enforced")
        else:
            print("❌ Warning: API might be accessible without authentication")
    
    def call_api_get(self, endpoint):
        """Make GET API call"""
        return self._call_api(endpoint, {})
    
    def call_api_post(self, endpoint, data):
        """Make POST API call"""
        return self._call_api(endpoint, data)
    
    def call_api_put(self, endpoint, data):
        """Make PUT API call"""
        return self._call_api(endpoint, data)
    
    def call_api_delete(self, endpoint):
        """Make DELETE API call"""
        return self._call_api(endpoint, {})
    
    def _call_api(self, endpoint, data):
        """Make authenticated API call using JSON-RPC"""
        if not self.authenticated:
            print("❌ Not authenticated. Please login first.")
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
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('result')
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"Response: {response.text[:200]}...")
                return None
                
        except Exception as e:
            print(f"❌ Request failed: {str(e)}")
            return None

def main():
    print("🚀 Starting Odoo API Security Tests")
    print("=" * 50)
    
    # Initialize tester with db_test database
    tester = OdooAPITester(
        base_url='http://localhost:8069',
        database='db_test'
    )
    
    # Login with email
    if not tester.login('vivycahyani@gmail.com', 'admin'):
        print("❌ Cannot proceed without authentication")
        return
    
    # Run tests in order (suppliers first due to foreign key dependency)
    tester.test_authentication()
    remaining_supplier_id = tester.test_suppliers_api()
    tester.test_materials_api(remaining_supplier_id)
    
    print("\n" + "=" * 50)
    print("🎉 API Security Tests Completed!")

if __name__ == '__main__':
    main()