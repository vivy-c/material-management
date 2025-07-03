# Material Management System

## 🚀 Features

### Material Management
- **Material Registration**: Unique codes, names, and categorization
- **Material Types**: Support for Fabric, Jeans, and Cotton
- **Price Management**: Buy price tracking with validation (minimum 100.0)
- **Supplier Integration**: Link materials to suppliers
- **REST API**: Full CRUD operations via JSON API

### Supplier Management
- **Supplier Registration**: Codes, names, and contact information
- **Contact Details**: Email, phone, and address tracking
- **Status Management**: Active/inactive supplier status
- **Material Tracking**: View all materials from each supplier

## 🏗️ Architecture

### Technology Stack
- **Platform**: Odoo 14.0
- **Database**: PostgreSQL 13
- **Containerization**: Docker & Docker Compose
- **API**: JSON-RPC based REST API

### Project Structure
```
material-management/
├── addons/
│   ├── material_management/     # Core material management module
│   └── material_supplier/       # Supplier management module
├── config/
│   └── odoo.conf               # Odoo configuration
├── docker-compose.yml          # Docker services definition
├── test_api_manual.py          # API testing script
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd material-management
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the application**
   - Web Interface: http://localhost:8069
   - Database: localhost:1234
   - Default credentials: admin/admin

4. **Install modules**
   - Navigate to Apps in Odoo
   - Install "Material Management" and "Material Supplier" modules

## 📚 API Documentation

### Authentication
All API endpoints require user authentication. Login via `/web/session/authenticate` first.

### Materials API

#### Get All Materials
```http
GET /api/materials
```

**Query Parameters:**
- `type`: Filter by material type (fabric, jeans, cotton)
- `supplier_id`: Filter by supplier ID
- `active`: Filter by active status

#### Get Material by ID
```http
GET /api/materials/{id}
```

#### Create Material
```http
POST /api/materials
```

**Request Body:**
```json
{
  "code": "MAT001",
  "name": "Premium Cotton",
  "type": "cotton",
  "buy_price": 150.0,
  "supplier_id": 1
}
```

#### Update Material
```http
PUT /api/materials/{id}
```

#### Delete Material
```http
DELETE /api/materials/{id}
```

### Suppliers API

#### Get All Suppliers
```http
GET /api/suppliers
```

#### Create Supplier
```http
POST /api/suppliers
```

**Request Body:**
```json
{
  "code": "SUP001",
  "name": "Textile Supplier Co.",
  "email": "contact@supplier.com",
  "phone": "+1-234-567-8900"
}
```

## 🧪 Testing

### Manual API Testing
Use the included testing script:

```bash
# Copy the updated script
docker cp test_api_manual.py $(docker-compose ps -q web):/tmp/test_api_manual.py

# Run the authenticated test
docker-compose exec web python3 /tmp/test_api_manual.py
```

This script will:
- Test authentication
- Perform CRUD operations on suppliers
- Perform CRUD operations on materials
- Validate API security

#### Sample Test Output
```
$ docker-compose exec web python3 /tmp/test_api_manual.py
WARN[0000] /Users/vivycahyani/Kerja/material-management/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
🚀 Starting Odoo Authenticated API Tests
==================================================
✅ Authentication successful
✅ API is accessible

🏢 Testing Suppliers API...

1. Testing GET /api/suppliers
✅ Found 4 suppliers

2. Testing POST /api/suppliers
✅ Supplier created with ID: 24

📦 Testing Materials API...

1. Testing GET /api/materials
✅ Found 0 materials

2. Testing POST /api/materials
Debug - Material creation response: {'success': True, 'data': {'id': 22, 'code': 'TESTMAT1751552042', 'name': 'API Test Material 1751552042', 'type': 'cotton', 'buy_price': 175.0, 'supplier_id': 24, 'supplier_name': 'API Test Supplier 1751552042', 'active': True}, 'message': 'Material created successfully'}
✅ Material created with ID: 22

3. Testing PUT /api/materials
✅ Material updated successfully

4. Testing DELETE /api/materials
✅ Material deleted successfully

==================================================
🎉 Authenticated API Tests Completed!
```

        
