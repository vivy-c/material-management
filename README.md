# Material Management System

A comprehensive Odoo-based ERP system for managing materials and suppliers, designed specifically for manufacturing and textile businesses.

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
python3 test_api_manual.py
```

This script will:
- Test authentication
- Perform CRUD operations on suppliers
- Perform CRUD operations on materials
- Validate API security

### Test Coverage
- Authentication enforcement
- Data validation
- CRUD operations
- Error handling
- Relationship integrity

## 🔧 Configuration

### Database Configuration
Edit `config/odoo.conf` to modify:
- Database connection settings
- Security parameters
- Performance tuning

### Docker Configuration
Modify `docker-compose.yml` for:
- Port mappings
- Volume mounts
- Environment variables

## 🚀 Development

### Adding New Features
1. Create new models in `models/` directory
2. Add views in `views/` directory
3. Update `__manifest__.py` with dependencies
4. Add security rules in `security/`

### Custom API Endpoints
Extend `controllers/material_api.py` or create new controller files.
