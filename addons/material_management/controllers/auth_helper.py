import requests
import json

class OdooAPIClient:
    def __init__(self, base_url, database, username, password):
        self.base_url = base_url
        self.database = database
        self.session = requests.Session()
        self.login(username, password)
    
    def login(self, username, password):
        """Authenticate and get session cookies"""
        login_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'service': 'common',
                'method': 'login',
                'args': [self.database, username, password]
            },
            'id': 1
        }
        
        response = self.session.post(
            f'{self.base_url}/jsonrpc',
            data=json.dumps(login_data),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('result'):
                print("✅ Authentication successful")
                return True
        
        raise Exception("❌ Authentication failed")
    
    def call_api(self, endpoint, method='GET', data=None):
        """Make authenticated API calls"""
        api_data = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': data or {},
            'id': 1
        }
        
        response = self.session.post(
            f'{self.base_url}{endpoint}',
            data=json.dumps(api_data),
            headers={'Content-Type': 'application/json'}
        )
        
        return response.json()

# Usage Example:
client = OdooAPIClient(
    base_url='http://localhost:8069',
    database='your_database',
    username='admin',
    password='admin'
)

# Now you can make authenticated API calls
result = client.call_api('/api/materials')
print(result)