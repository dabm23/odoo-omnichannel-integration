{
    'name': 'Integrador de Terminales Omnicanal',
    'version': '1.0',
    'category': 'Accounting',
    'summary': 'Registra ventas de terminales y genera asientos contables en España',
    'description': """
        Módulo diseñado para recibir transacciones de terminales físicos,
        gestionarlas en un estado de borrador y posteriormente integrarlas
        a la contabilidad de Odoo como asientos contables.
    """,
    # Dependemos de 'base' (el núcleo) y 'account' (porque tocaremos contabilidad luego)
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/terminal_transaction_views.xml',
        'reports/terminal_transaction_report.xml', # <-- NUESTRO REPORTE
    ],
    'installable': True,
    'application': True, # Esto hace que aparezca como una App principal en Odoo
    'license': 'LGPL-3',
}