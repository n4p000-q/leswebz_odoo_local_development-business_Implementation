{
    'name': 'Thimo & Sons Guest House',
    'version': '19.0.1.0.0',
    'category': 'Hospitality',
    'summary': 'Guest house rooms, rates and bookings',
    'depends': ['base', 'contacts'],
    'data': [
        'data.xml',
        'security/ir.model.access.csv',
        'views/guest_views.xml',
        'views/room_type_views.xml',
        'views/room_views.xml',
        'views/rate_views.xml',
        'views/booking_views.xml',
        'views/menu_views.xml',
    ],
    'application': True,
    'installable': True,
}
