import os, traceback
os.environ.setdefault('DJANGO_SETTINGS_MODULE','config.settings.base')
try:
    import django
    django.setup()
    import importlib
    m = importlib.import_module('apps.cart.api.v1.views')
    print('Imported module:', m.__file__)
    print('Functions available:', [name for name in dir(m) if name.startswith('get_') or name.endswith('_cart') or name in ('add_to_cart','update_cart_item')])
except Exception:
    traceback.print_exc()
