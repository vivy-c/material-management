from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Supplier(models.Model):
    _name = 'material.supplier'
    _description = 'Material Supplier'
    _rec_name = 'name'
    
    name = fields.Char(
        string='Supplier Name',
        required=True,
        help='Name of the supplier'
    )
    
    code = fields.Char(
        string='Supplier Code',
        required=True,
        help='Unique code for the supplier'
    )
    
    email = fields.Char(
        string='Email',
        help='Supplier email address'
    )
    
    phone = fields.Char(
        string='Phone',
        help='Supplier phone number'
    )
    
    address = fields.Text(
        string='Address',
        help='Supplier address'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this supplier is active'
    )
    
    material_ids = fields.One2many(
        'material.management',
        'supplier_id',
        string='Materials',
        help='Materials supplied by this supplier'
    )
    
    material_count = fields.Integer(
        string='Material Count',
        compute='_compute_material_count',
        help='Number of materials from this supplier'
    )
    
    @api.depends('material_ids')
    def _compute_material_count(self):
        for supplier in self:
            supplier.material_count = len(supplier.material_ids)
    
    @api.constrains('code')
    def _check_code_format(self):
        for supplier in self:
            if supplier.code and not supplier.code.replace(' ', '').isalnum():
                raise ValidationError("Supplier code must contain only letters and numbers.")
    
    @api.model
    def create(self, vals):
        if 'code' in vals and vals['code']:
            vals['code'] = vals['code'].upper().strip()
        return super(Supplier, self).create(vals)
    
    def write(self, vals):
        if 'code' in vals and vals['code']:
            vals['code'] = vals['code'].upper().strip()
        return super(Supplier, self).write(vals)
    
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'Supplier code must be unique!'),
        ('unique_name', 'UNIQUE(name)', 'Supplier name must be unique!'),
    ]
    
    def action_view_materials(self):
        """Action to view materials for this supplier"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Materials from {self.name}',
            'res_model': 'material.management',
            'view_mode': 'tree,form',
            'domain': [('supplier_id', '=', self.id)],
            'context': {'default_supplier_id': self.id},
        }