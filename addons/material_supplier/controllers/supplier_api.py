import json
from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError, AccessError

class SupplierAPI(http.Controller):
    
    @http.route('/api/suppliers', type='json', auth='public', csrf=False)
    def suppliers_api(self, **kwargs):
        """Handle all supplier operations based on operation parameter"""
        operation = kwargs.get('operation', 'list')
        
        if operation == 'list':
            return self._get_suppliers(**kwargs)
        elif operation == 'create':
            return self._create_supplier(**kwargs)
        else:
            return {
                'success': False,
                'error': f'Invalid operation: {operation}. Use "list" or "create"'
            }
    
    @http.route('/api/suppliers/<int:supplier_id>', type='json', auth='public', csrf=False)
    def supplier_by_id_api(self, supplier_id, **kwargs):
        """Handle supplier operations by ID"""
        operation = kwargs.get('operation', 'get')
        
        if operation == 'get':
            return self._get_supplier(supplier_id, **kwargs)
        elif operation == 'update':
            return self._update_supplier(supplier_id, **kwargs)
        elif operation == 'delete':
            return self._delete_supplier(supplier_id, **kwargs)
        else:
            return {
                'success': False,
                'error': f'Invalid operation: {operation}. Use "get", "update", or "delete"'
            }
    
    @http.route('/api/suppliers/<int:supplier_id>/materials', type='json', auth='public', csrf=False)
    def get_supplier_materials(self, supplier_id, **kwargs):
        """Get all materials for a specific supplier"""
        try:
            supplier = request.env['material.supplier'].browse(supplier_id)
            
            if not supplier.exists():
                return {
                    'success': False,
                    'error': 'Supplier not found'
                }
            
            materials = request.env['material.management'].search([('supplier_id', '=', supplier_id)])
            
            result = []
            for material in materials:
                result.append({
                    'id': material.id,
                    'code': material.code,
                    'name': material.name,
                    'type': material.type,
                    'buy_price': material.buy_price,
                    'active': material.active,
                })
            
            return {
                'success': True,
                'data': result,
                'count': len(result),
                'supplier': {
                    'id': supplier.id,
                    'name': supplier.name,
                    'code': supplier.code
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _get_suppliers(self, **kwargs):
        """Get all suppliers with optional filtering"""
        try:
            domain = []
            
            # Add filters if provided
            if kwargs.get('active') is not None:
                domain.append(('active', '=', kwargs['active']))
            if kwargs.get('name'):
                domain.append(('name', 'ilike', kwargs['name']))
            if kwargs.get('code'):
                domain.append(('code', 'ilike', kwargs['code']))
            
            suppliers = request.env['material.supplier'].search(domain)
            
            result = []
            for supplier in suppliers:
                result.append({
                    'id': supplier.id,
                    'code': supplier.code,
                    'name': supplier.name,
                    'email': supplier.email,
                    'phone': supplier.phone,
                    'address': supplier.address,
                    'active': supplier.active,
                    'material_count': supplier.material_count,
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
    
    def _get_supplier(self, supplier_id, **kwargs):
        """Get a specific supplier by ID"""
        try:
            supplier = request.env['material.supplier'].browse(supplier_id)
            
            if not supplier.exists():
                return {
                    'success': False,
                    'error': 'Supplier not found'
                }
            
            # Get materials for this supplier if requested
            include_materials = kwargs.get('include_materials', False)
            materials_data = []
            
            if include_materials:
                materials = request.env['material.management'].search([('supplier_id', '=', supplier_id)])
                for material in materials:
                    materials_data.append({
                        'id': material.id,
                        'code': material.code,
                        'name': material.name,
                        'type': material.type,
                        'buy_price': material.buy_price,
                        'active': material.active,
                    })
            
            return {
                'success': True,
                'data': {
                    'id': supplier.id,
                    'code': supplier.code,
                    'name': supplier.name,
                    'email': supplier.email,
                    'phone': supplier.phone,
                    'address': supplier.address,
                    'active': supplier.active,
                    'material_count': supplier.material_count,
                    'materials': materials_data if include_materials else None,
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def _create_supplier(self, **kwargs):
        """Create a new supplier"""
        try:
            required_fields = ['code', 'name']
            
            # Validate required fields
            for field in required_fields:
                if field not in kwargs:
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }
            
            # Create supplier
            supplier_data = {
                'code': kwargs['code'],
                'name': kwargs['name'],
                'email': kwargs.get('email', ''),
                'phone': kwargs.get('phone', ''),
                'address': kwargs.get('address', ''),
                'active': kwargs.get('active', True)
            }
            
            supplier = request.env['material.supplier'].create(supplier_data)
            
            return {
                'success': True,
                'data': {
                    'id': supplier.id,
                    'code': supplier.code,
                    'name': supplier.name,
                    'email': supplier.email,
                    'phone': supplier.phone,
                    'address': supplier.address,
                    'active': supplier.active,
                    'material_count': supplier.material_count,
                },
                'message': 'Supplier created successfully'
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
    
    def _update_supplier(self, supplier_id, **kwargs):
        """Update an existing supplier"""
        try:
            supplier = request.env['material.supplier'].browse(supplier_id)
            
            if not supplier.exists():
                return {
                    'success': False,
                    'error': 'Supplier not found'
                }
            
            update_data = {}
            
            # Prepare update data
            allowed_fields = ['code', 'name', 'email', 'phone', 'address', 'active']
            for field in allowed_fields:
                if field in kwargs:
                    update_data[field] = kwargs[field]
            
            # Update supplier
            supplier.write(update_data)
            
            return {
                'success': True,
                'data': {
                    'id': supplier.id,
                    'code': supplier.code,
                    'name': supplier.name,
                    'email': supplier.email,
                    'phone': supplier.phone,
                    'address': supplier.address,
                    'active': supplier.active,
                    'material_count': supplier.material_count,
                },
                'message': 'Supplier updated successfully'
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
    
    def _delete_supplier(self, supplier_id, **kwargs):
        """Delete a supplier"""
        try:
            supplier = request.env['material.supplier'].browse(supplier_id)
            
            if not supplier.exists():
                return {
                    'success': False,
                    'error': 'Supplier not found'
                }
            
            # Check if supplier has materials
            material_count = request.env['material.management'].search_count([('supplier_id', '=', supplier_id)])
            if material_count > 0:
                return {
                    'success': False,
                    'error': f'Cannot delete supplier. It has {material_count} associated materials.'
                }
            
            supplier_name = supplier.name
            supplier.unlink()
            
            return {
                'success': True,
                'message': f'Supplier "{supplier_name}" deleted successfully'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }