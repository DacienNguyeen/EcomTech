import importlib, sys
names = [
    'apps.orders.services.cart_as_order',
    'apps.orders.api.v1.cart_serializers',
    'apps.orders.api.v1.cart_views',
    'apps.orders.api.v1.urls',
]
ok = True
for n in names:
    try:
        importlib.import_module(n)
        print('IMPORT OK', n)
    except Exception as e:
        print('IMPORT ERR', n, repr(e))
        ok = False
if not ok:
    sys.exit(1)
print('ALL IMPORTS OK')
