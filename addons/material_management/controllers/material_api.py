import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)

class MaterialAPI(http.Controller):
    
    @http.route('/api/docs', type='http', auth='public', methods=['GET'], csrf=False)
    def swagger_docs(self, **kwargs):
        """Swagger UI Documentation"""
        swagger_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Material Management API Documentation</title>
    <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui.css" />
    <style>
        html {
            box-sizing: border-box;
            overflow: -moz-scrollbars-vertical;
            overflow-y: scroll;
        }
        *, *:before, *:after {
            box-sizing: inherit;
        }
        body {
            margin:0;
            background: #fafafa;
        }
    </style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-bundle.js"></script>
    <script src="https://unpkg.com/swagger-ui-dist@3.25.0/swagger-ui-standalone-preset.js"></script>
    <script>
        window.onload = function() {
            const ui = SwaggerUIBundle({
                url: '/api/openapi.json',
                dom_id: '#swagger-ui',
                deepLinking: true,
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIStandalonePreset
                ],
                plugins: [
                    SwaggerUIBundle.plugins.DownloadUrl
                ],
                layout: "StandaloneLayout"
            });
        };
    </script>
</body>
</html>
        """
        return request.make_response(
            swagger_html,
            headers={'Content-Type': 'text/html'}
        )
    
    @http.route('/api/openapi.json', type='http', auth='public', methods=['GET'], csrf=False)
    def openapi_spec(self, **kwargs):
        """OpenAPI 3.0 Specification"""
        base_url = request.httprequest.host_url.rstrip('/')
        
        openapi_spec = {
            "openapi": "3.0.0",
            "info": {
                "title": "Material Management API",
                "description": "REST API for managing materials in Odoo",
                "version": "1.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "support@yourcompany.com"
                }
            },
            "servers": [
                {
                    "url": base_url,
                    "description": "Development server"
                }
            ],
            "security": [
                {
                    "sessionAuth": []
                }
            ],
            "paths": {
                "/api/materials": {
                    "get": {
                        "summary": "Get all materials",
                        "description": "Retrieve a list of materials with optional filtering",
                        "parameters": [
                            {
                                "name": "type",
                                "in": "query",
                                "description": "Filter by material type",
                                "required": False,
                                "schema": {
                                    "type": "string",
                                    "enum": ["fabric", "jeans", "cotton"]
                                }
                            },
                            {
                                "name": "active",
                                "in": "query",
                                "description": "Filter by active status",
                                "required": False,
                                "schema": {
                                    "type": "string",
                                    "enum": ["true", "false", "all"],
                                    "default": "true"
                                }
                            },
                            {
                                "name": "limit",
                                "in": "query",
                                "description": "Number of records to return",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "default": 100
                                }
                            },
                            {
                                "name": "offset",
                                "in": "query",
                                "description": "Number of records to skip",
                                "required": False,
                                "schema": {
                                    "type": "integer",
                                    "default": 0
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MaterialListResponse"
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "Bad request",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "post": {
                        "summary": "Create a new material",
                        "description": "Create a new material record",
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/MaterialCreate"
                                    }
                                }
                            }
                        },
                        "responses": {
                            "201": {
                                "description": "Material created successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MaterialResponse"
                                        }
                                    }
                                }
                            },
                            "400": {
                                "description": "Validation error",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ValidationErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "/api/materials/{id}": {
                    "get": {
                        "summary": "Get material by ID",
                        "description": "Retrieve a specific material by its ID",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "description": "Material ID",
                                "schema": {
                                    "type": "integer"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Successful response",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MaterialResponse"
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Material not found",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/ErrorResponse"
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "put": {
                        "summary": "Update material",
                        "description": "Update an existing material",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "description": "Material ID",
                                "schema": {
                                    "type": "integer"
                                }
                            }
                        ],
                        "requestBody": {
                            "required": True,
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/MaterialUpdate"
                                    }
                                }
                            }
                        },
                        "responses": {
                            "200": {
                                "description": "Material updated successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/MaterialResponse"
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Material not found"
                            },
                            "400": {
                                "description": "Validation error"
                            }
                        }
                    },
                    "delete": {
                        "summary": "Delete material",
                        "description": "Delete a material by ID",
                        "parameters": [
                            {
                                "name": "id",
                                "in": "path",
                                "required": True,
                                "description": "Material ID",
                                "schema": {
                                    "type": "integer"
                                }
                            }
                        ],
                        "responses": {
                            "200": {
                                "description": "Material deleted successfully",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/DeleteResponse"
                                        }
                                    }
                                }
                            },
                            "404": {
                                "description": "Material not found"
                            }
                        }
                    }
                }
            },
            "components": {
                "securitySchemes": {
                    "sessionAuth": {
                        "type": "apiKey",
                        "in": "cookie",
                        "name": "session_id",
                        "description": "Odoo session cookie"
                    }
                },
                "schemas": {
                    "Material": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer", "description": "Material ID"},
                            "code": {"type": "string", "description": "Material code"},
                            "name": {"type": "string", "description": "Material name"},
                            "type": {
                                "type": "string",
                                "enum": ["fabric", "jeans", "cotton"],
                                "description": "Material type"
                            },
                            "buy_price": {
                                "type": "number",
                                "minimum": 100,
                                "description": "Buy price (minimum 100)"
                            },
                            "supplier_id": {"type": "integer", "description": "Supplier ID"},
                            "supplier_name": {"type": "string", "description": "Supplier name"},
                            "active": {"type": "boolean", "description": "Active status"},
                            "create_date": {"type": "string", "format": "date-time"},
                            "write_date": {"type": "string", "format": "date-time"}
                        }
                    },
                    "MaterialCreate": {
                        "type": "object",
                        "required": ["code", "name", "type", "buy_price", "supplier_id"],
                        "properties": {
                            "code": {"type": "string", "description": "Material code"},
                            "name": {"type": "string", "description": "Material name"},
                            "type": {
                                "type": "string",
                                "enum": ["fabric", "jeans", "cotton"]
                            },
                            "buy_price": {
                                "type": "number",
                                "minimum": 100
                            },
                            "supplier_id": {"type": "integer"},
                            "active": {"type": "boolean", "default": True}
                        }
                    },
                    "MaterialUpdate": {
                        "type": "object",
                        "properties": {
                            "code": {"type": "string"},
                            "name": {"type": "string"},
                            "type": {
                                "type": "string",
                                "enum": ["fabric", "jeans", "cotton"]
                            },
                            "buy_price": {
                                "type": "number",
                                "minimum": 100
                            },
                            "supplier_id": {"type": "integer"},
                            "active": {"type": "boolean"}
                        }
                    },
                    "MaterialResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "message": {"type": "string"},
                            "data": {"$ref": "#/components/schemas/Material"}
                        }
                    },
                    "MaterialListResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "data": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/Material"}
                            },
                            "total_count": {"type": "integer"},
                            "limit": {"type": "integer"},
                            "offset": {"type": "integer"}
                        }
                    },
                    "DeleteResponse": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "example": "success"},
                            "message": {"type": "string"},
                            "deleted_data": {"$ref": "#/components/schemas/Material"}
                        }
                    },
                    "ErrorResponse": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"},
                            "status": {"type": "string", "example": "error"}
                        }
                    },
                    "ValidationErrorResponse": {
                        "type": "object",
                        "properties": {
                            "error": {"type": "string"},
                            "details": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "status": {"type": "string", "example": "error"}
                        }
                    }
                }
            }
        }
        
        return request.make_response(
            json.dumps(openapi_spec, indent=2),
            headers={'Content-Type': 'application/json'}
        )
    
    def _get_material_data(self, material):
        """Helper method to format material data for API response"""
        return {
            'id': material.id,
            'code': material.code,
            'name': material.name,
            'type': material.type,
            'buy_price': material.buy_price,
            'supplier_id': material.supplier_id.id if material.supplier_id else None,
            'supplier_name': material.supplier_id.name if material.supplier_id else None,
            'active': material.active,
            'create_date': material.create_date.isoformat() if material.create_date else None,
            'write_date': material.write_date.isoformat() if material.write_date else None,
        }
    
    def _validate_material_data(self, data):
        """Validate material data before create/update"""
        errors = []
        
        # Required fields validation
        required_fields = ['code', 'name', 'type', 'buy_price', 'supplier_id']
        for field in required_fields:
            if field not in data or not data[field]:
                errors.append(f"Field '{field}' is required")
        
        # Type validation
        if 'type' in data and data['type'] not in ['fabric', 'jeans', 'cotton']:
            errors.append("Type must be one of: fabric, jeans, cotton")
        
        # Price validation
        if 'buy_price' in data:
            try:
                price = float(data['buy_price'])
                if price < 100:
                    errors.append("Buy price must be at least 100")
            except (ValueError, TypeError):
                errors.append("Buy price must be a valid number")
        
        # Supplier validation
        if 'supplier_id' in data:
            try:
                supplier_id = int(data['supplier_id'])
                supplier = request.env['res.partner'].sudo().browse(supplier_id)
                if not supplier.exists():
                    errors.append(f"Supplier with ID {supplier_id} does not exist")
                elif not supplier.is_company or supplier.supplier_rank <= 0:
                    errors.append(f"Partner {supplier_id} is not a valid supplier")
            except (ValueError, TypeError):
                errors.append("Supplier ID must be a valid integer")
        
        return errors
    
    @http.route('/api/materials', type='http', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        """GET /api/materials - Get all materials with optional type filter"""
        try:
            domain = []
            
            # Add type filter if provided
            material_type = kwargs.get('type')
            if material_type:
                if material_type not in ['fabric', 'jeans', 'cotton']:
                    return request.make_response(
                        json.dumps({
                            'error': 'Invalid type. Must be one of: fabric, jeans, cotton',
                            'status': 'error'
                        }),
                        status=400,
                        headers={'Content-Type': 'application/json'}
                    )
                domain.append(('type', '=', material_type))
            
            # Add active filter (default to active materials only)
            active_filter = kwargs.get('active', 'true').lower()
            if active_filter == 'true':
                domain.append(('active', '=', True))
            elif active_filter == 'false':
                domain.append(('active', '=', False))
            # If 'all', don't add active filter
            
            # Pagination
            limit = int(kwargs.get('limit', 100))
            offset = int(kwargs.get('offset', 0))
            
            materials = request.env['material.management'].sudo().search(
                domain, limit=limit, offset=offset, order='create_date desc'
            )
            
            total_count = request.env['material.management'].sudo().search_count(domain)
            
            result = {
                'status': 'success',
                'data': [self._get_material_data(material) for material in materials],
                'total_count': total_count,
                'limit': limit,
                'offset': offset
            }
            
            return request.make_response(
                json.dumps(result),
                status=200,
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error(f"Error getting materials: {str(e)}")
            return request.make_response(
                json.dumps({
                    'error': 'Internal server error',
                    'status': 'error'
                }),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    
    @http.route('/api/materials', type='http', auth='user', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        """POST /api/materials - Create a new material"""
        try:
            # Parse JSON data
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Validate data
            errors = self._validate_material_data(data)
            if errors:
                return request.make_response(
                    json.dumps({
                        'error': 'Validation failed',
                        'details': errors,
                        'status': 'error'
                    }),
                    status=400,
                    headers={'Content-Type': 'application/json'}
                )
            
            # Create material
            material = request.env['material.management'].sudo().create({
                'code': data['code'],
                'name': data['name'],
                'type': data['type'],
                'buy_price': float(data['buy_price']),
                'supplier_id': int(data['supplier_id']),
                'active': data.get('active', True)
            })
            
            result = {
                'status': 'success',
                'message': 'Material created successfully',
                'data': self._get_material_data(material)
            }
            
            return request.make_response(
                json.dumps(result),
                status=201,
                headers={'Content-Type': 'application/json'}
            )
            
        except ValidationError as e:
            return request.make_response(
                json.dumps({
                    'error': 'Validation error',
                    'details': str(e),
                    'status': 'error'
                }),
                status=400,
                headers={'Content-Type': 'application/json'}
            )
        except json.JSONDecodeError:
            return request.make_response(
                json.dumps({
                    'error': 'Invalid JSON data',
                    'status': 'error'
                }),
                status=400,
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            _logger.error(f"Error creating material: {str(e)}")
            return request.make_response(
                json.dumps({
                    'error': 'Internal server error',
                    'status': 'error'
                }),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='user', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        """PUT /api/materials/<id> - Update an existing material"""
        try:
            # Find material
            material = request.env['material.management'].sudo().browse(material_id)
            if not material.exists():
                return request.make_response(
                    json.dumps({
                        'error': f'Material with ID {material_id} not found',
                        'status': 'error'
                    }),
                    status=404,
                    headers={'Content-Type': 'application/json'}
                )
            
            # Parse JSON data
            data = json.loads(request.httprequest.data.decode('utf-8'))
            
            # Validate data (only validate provided fields)
            errors = []
            if 'type' in data and data['type'] not in ['fabric', 'jeans', 'cotton']:
                errors.append("Type must be one of: fabric, jeans, cotton")
            
            if 'buy_price' in data:
                try:
                    price = float(data['buy_price'])
                    if price < 100:
                        errors.append("Buy price must be at least 100")
                except (ValueError, TypeError):
                    errors.append("Buy price must be a valid number")
            
            if 'supplier_id' in data:
                try:
                    supplier_id = int(data['supplier_id'])
                    supplier = request.env['res.partner'].sudo().browse(supplier_id)
                    if not supplier.exists():
                        errors.append(f"Supplier with ID {supplier_id} does not exist")
                    elif not supplier.is_company or supplier.supplier_rank <= 0:
                        errors.append(f"Partner {supplier_id} is not a valid supplier")
                except (ValueError, TypeError):
                    errors.append("Supplier ID must be a valid integer")
            
            if errors:
                return request.make_response(
                    json.dumps({
                        'error': 'Validation failed',
                        'details': errors,
                        'status': 'error'
                    }),
                    status=400,
                    headers={'Content-Type': 'application/json'}
                )
            
            # Update material
            update_vals = {}
            for field in ['code', 'name', 'type', 'active']:
                if field in data:
                    update_vals[field] = data[field]
            
            if 'buy_price' in data:
                update_vals['buy_price'] = float(data['buy_price'])
            
            if 'supplier_id' in data:
                update_vals['supplier_id'] = int(data['supplier_id'])
            
            material.write(update_vals)
            
            result = {
                'status': 'success',
                'message': 'Material updated successfully',
                'data': self._get_material_data(material)
            }
            
            return request.make_response(
                json.dumps(result),
                status=200,
                headers={'Content-Type': 'application/json'}
            )
            
        except ValidationError as e:
            return request.make_response(
                json.dumps({
                    'error': 'Validation error',
                    'details': str(e),
                    'status': 'error'
                }),
                status=400,
                headers={'Content-Type': 'application/json'}
            )
        except json.JSONDecodeError:
            return request.make_response(
                json.dumps({
                    'error': 'Invalid JSON data',
                    'status': 'error'
                }),
                status=400,
                headers={'Content-Type': 'application/json'}
            )
        except Exception as e:
            _logger.error(f"Error updating material: {str(e)}")
            return request.make_response(
                json.dumps({
                    'error': 'Internal server error',
                    'status': 'error'
                }),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        """DELETE /api/materials/<id> - Delete a material"""
        try:
            # Find material
            material = request.env['material.management'].sudo().browse(material_id)
            if not material.exists():
                return request.make_response(
                    json.dumps({
                        'error': f'Material with ID {material_id} not found',
                        'status': 'error'
                    }),
                    status=404,
                    headers={'Content-Type': 'application/json'}
                )
            
            # Store material data before deletion
            material_data = self._get_material_data(material)
            
            # Delete material
            material.unlink()
            
            result = {
                'status': 'success',
                'message': 'Material deleted successfully',
                'deleted_data': material_data
            }
            
            return request.make_response(
                json.dumps(result),
                status=200,
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error(f"Error deleting material: {str(e)}")
            return request.make_response(
                json.dumps({
                    'error': 'Internal server error',
                    'status': 'error'
                }),
                status=500,
                headers={'Content-Type': 'application/json'}
            )
    
    @http.route('/api/materials/<int:material_id>', type='http', auth='user', methods=['GET'], csrf=False)
    def get_material_by_id(self, material_id, **kwargs):
        """GET /api/materials/<id> - Get a specific material by ID"""
        try:
            material = request.env['material.management'].sudo().browse(material_id)
            if not material.exists():
                return request.make_response(
                    json.dumps({
                        'error': f'Material with ID {material_id} not found',
                        'status': 'error'
                    }),
                    status=404,
                    headers={'Content-Type': 'application/json'}
                )
            
            result = {
                'status': 'success',
                'data': self._get_material_data(material)
            }
            
            return request.make_response(
                json.dumps(result),
                status=200,
                headers={'Content-Type': 'application/json'}
            )
            
        except Exception as e:
            _logger.error(f"Error getting material: {str(e)}")
            return request.make_response(
                json.dumps({
                    'error': 'Internal server error',
                    'status': 'error'
                }),
                status=500,
                headers={'Content-Type': 'application/json'}
            )