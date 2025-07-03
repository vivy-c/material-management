{
    'name': 'Material Supplier',
    'version': '14.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Manage material suppliers',
    'description': """
        Material Supplier Module
        ========================
        This module allows you to:
        * Register suppliers with codes, names, and contact information
        * Track supplier details including email, phone, and address
        * Manage supplier status (active/inactive)
        * View materials supplied by each supplier
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/supplier_views.xml',
        'views/supplier_menu.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}