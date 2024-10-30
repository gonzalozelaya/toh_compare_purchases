{
    'name': 'Compare purchases / quotation',
    'summary': """
        Compara 2 o mas compras o cotizaciones en una vista intuitiva para poder elegir con mayor seguridad.
        Compare 2 or more purchases or quotation in an intuitive view to be able to choose with greater security.""",

    'description': """
        Para poder elegir bien al momento de checar proveedores es necesario poder visualizarlos de manera sencilla y clara, y asi elegir bien.
        In order to choose well when checking suppliers, it is necessary to be able to view them in a simple and clear way, and thus choose well.
    """,
    'version': '1.0',
    'category': 'Inventory/Purchase',
    'author': "Toh Soluciones Digitales",
    'website': 'https://tohsoluciones.com/',
    'depends': ['purchase','purchase_requisition'],
    'data': [
        'views/purchase_requisition_views.xml',
        'views/purchase_order_views.xml',
        'views/purchase_order_line_views.xml',
        'views/res_partner_views.xml',
        'security/ir.model.access.csv',
        'wizard/compare_wizard.xml',
        'wizard/confirm_wizard.xml',
        'wizard/survey_wizard.xml'
    ],
    'demo': [
       
    ],
    'assets': {
        'web.assets_backend': [
            'toh_compare_purchases/static/src/js/compare_template.js',
            'toh_compare_purchases/static/src/xml/compare_template.xml',
        ],
    },
    'price': '30.00',
    'currency': 'USD',
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
    'images': ["static/description/cover.png"]
}
