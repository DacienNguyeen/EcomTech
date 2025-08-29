import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.users.jwt import issue_tokens
from apps.users.models import Customer

# Test JWT creation
c = Customer(CustomerID=1, Email='test@test.com')
try:
    tokens = issue_tokens(c)
    print(f'✅ JWT test successful: access token length = {len(tokens["access"])}')
    print(f'   Refresh token length = {len(tokens["refresh"])}')
    print(f'   JWT utilities working correctly')
except Exception as e:
    print(f'❌ JWT test failed: {e}')
