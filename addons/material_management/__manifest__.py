{
    'name': 'Material Management',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Manage materials for sale',
    'description': """
        Material Management Module
        =========================
        This module allows you to:
        * Register materials with codes, names, and types
        * Set buy prices with minimum validation
        * Link materials to suppliers
        * Filter materials by type
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_management_views.xml',
        'views/material_management_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}