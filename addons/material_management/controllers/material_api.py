import json
import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

_logger = logging.getLogger(__name__)

class MaterialAPI(http.Controller):
    
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