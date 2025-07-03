import json
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

class MaterialManagementAPI(http.Controller):
    
    @http.route('/api/materials', type='json', auth='user', methods=['GET'], csrf=False)
    def get_materials(self, **kwargs):
        """Get all materials with optional filtering"""
        try:
            domain = []
            
            # Add filters if provided
            if kwargs.get('type'):
                domain.append(('type', '=', kwargs['type']))
            if kwargs.get('supplier_id'):
                domain.append(('supplier_id', '=', int(kwargs['supplier_id'])))
            if kwargs.get('active') is not None:
                domain.append(('active', '=', kwargs['active']))
            
            materials = request.env['material.management'].search(domain)
            
            result = []
            for material in materials:
                result.append({
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id if material.supplier_id else None,
                    'supplier_name': material.supplier_id.name if material.supplier_id else None,
                    'active': material.active,
                })
            
            return {
                'success': True,
                'data': result,
                'count': len(result)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/api/materials/<int:material_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_material(self, material_id, **kwargs):
        """Get a specific material by ID"""
        try:
            material = request.env['material.management'].browse(material_id)
            
            if not material.exists():
                return {
                    'success': False,
                    'error': 'Material not found'
                }
            
            return {
                'success': True,
                'data': {
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id if material.supplier_id else None,
                    'supplier_name': material.supplier_id.name if material.supplier_id else None,
                    'active': material.active,
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/api/materials', type='json', auth='user', methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        """Create a new material"""
        try:
            required_fields = ['code', 'name', 'type', 'buy_price', 'supplier_id']
            
            # Validate required fields
            for field in required_fields:
                if field not in kwargs:
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }
            
            # Validate material type
            valid_types = ['fabric', 'jeans', 'cotton']
            if kwargs['type'] not in valid_types:
                return {
                    'success': False,
                    'error': f'Invalid material type. Must be one of: {valid_types}'
                }
            
            # Validate buy_price
            try:
                buy_price = float(kwargs['buy_price'])
                if buy_price < 100:
                    return {
                        'success': False,
                        'error': 'Buy price must be at least 100'
                    }
            except ValueError:
                return {
                    'success': False,
                    'error': 'Invalid buy_price format'
                }
            
            # Validate supplier exists
            supplier = request.env['material.supplier'].browse(int(kwargs['supplier_id']))
            if not supplier.exists():
                return {
                    'success': False,
                    'error': 'Supplier not found'
                }
            
            # Create material
            material_data = {
                'code': kwargs['code'],
                'name': kwargs['name'],
                'type': kwargs['type'],
                'buy_price': buy_price,
                'supplier_id': int(kwargs['supplier_id']),
                'active': kwargs.get('active', True)
            }
            
            material = request.env['material.management'].create(material_data)
            
            return {
                'success': True,
                'data': {
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name,
                    'active': material.active,
                },
                'message': 'Material created successfully'
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/api/materials/<int:material_id>', type='json', auth='user', methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        """Update an existing material"""
        try:
            material = request.env['material.management'].browse(material_id)
            
            if not material.exists():
                return {
                    'success': False,
                    'error': 'Material not found'
                }
            
            update_data = {}
            
            # Validate and prepare update data
            if 'code' in kwargs:
                update_data['code'] = kwargs['code']
            
            if 'name' in kwargs:
                update_data['name'] = kwargs['name']
            
            if 'type' in kwargs:
                valid_types = ['fabric', 'jeans', 'cotton']
                if kwargs['type'] not in valid_types:
                    return {
                        'success': False,
                        'error': f'Invalid material type. Must be one of: {valid_types}'
                    }
                update_data['type'] = kwargs['type']
            
            if 'buy_price' in kwargs:
                try:
                    buy_price = float(kwargs['buy_price'])
                    if buy_price < 100:
                        return {
                            'success': False,
                            'error': 'Buy price must be at least 100'
                        }
                    update_data['buy_price'] = buy_price
                except ValueError:
                    return {
                        'success': False,
                        'error': 'Invalid buy_price format'
                    }
            
            if 'supplier_id' in kwargs:
                supplier = request.env['material.supplier'].browse(int(kwargs['supplier_id']))
                if not supplier.exists():
                    return {
                        'success': False,
                        'error': 'Supplier not found'
                    }
                update_data['supplier_id'] = int(kwargs['supplier_id'])
            
            if 'active' in kwargs:
                update_data['active'] = kwargs['active']
            
            # Update material
            material.write(update_data)
            
            return {
                'success': True,
                'data': {
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'supplier_id': material.supplier_id.id,
                    'supplier_name': material.supplier_id.name,
                    'active': material.active,
                },
                'message': 'Material updated successfully'
            }
            
        except ValidationError as e:
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    @http.route('/api/materials/<int:material_id>', type='json', auth='user', methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        """Delete a material"""
        try:
            material = request.env['material.management'].browse(material_id)
            
            if not material.exists():
                return {
                    'success': False,
                    'error': 'Material not found'
                }
            
            material_name = material.name
            material.unlink()
            
            return {
                'success': True,
                'message': f'Material "{material_name}" deleted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }