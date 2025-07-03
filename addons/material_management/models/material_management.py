from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MaterialManagement(models.Model):
    _name = 'material.management'
    _description = 'Material Management'
    _rec_name = 'name'
    
    code = fields.Char(
        string='Material Code',
        required=True,
        help='Unique code for the material'
    )
    
    name = fields.Char(
        string='Material Name',
        required=True,
        help='Name of the material'
    )
    
    type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True, help='Type of material')
    
    buy_price = fields.Float(
        string='Buy Price',
        required=True,
        help='Purchase price of the material (must be >= 100)'
    )
    
    # Update the supplier_id field definition:
    supplier_id = fields.Many2one(
        'material.supplier',  # Changed from 'res.partner' to 'material.supplier'
        string='Supplier',
        required=True,
        help='Supplier of this material'
    )
    
    # Additional useful fields
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_material_code', 'UNIQUE(code)', 'Material code must be unique!'),
        ('check_buy_price', 'CHECK(buy_price >= 100)', 'Buy price must be at least 100!')
    ]
    
    # API Constraints (Python validation)
    @api.constrains('buy_price')
    def _check_buy_price(self):
        for record in self:
            if record.buy_price < 100:
                raise ValidationError(
                    f"Buy price must be at least 100. Current value: {record.buy_price}"
                )
    
    @api.constrains('code')
    def _check_code_format(self):
        for record in self:
            if not record.code or len(record.code.strip()) == 0:
                raise ValidationError("Material code cannot be empty!")
    
    # Optional: Override create method for additional validation
    @api.model
    def create(self, vals):
        # Ensure code is uppercase and trimmed
        if 'code' in vals:
            vals['code'] = vals['code'].strip().upper()
        return super(MaterialManagement, self).create(vals)
    
    # Optional: Override write method for additional validation
    def write(self, vals):
        # Ensure code is uppercase and trimmed
        if 'code' in vals:
            vals['code'] = vals['code'].strip().upper()
        return super(MaterialManagement, self).write(vals)
