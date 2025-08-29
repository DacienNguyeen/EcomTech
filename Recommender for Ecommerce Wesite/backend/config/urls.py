from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

def csrf_view(request):
    return JsonResponse({"ok": True})

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/v1/catalog/", include("apps.catalog.api.v1.urls")),
    path("api/v1/users/", include("apps.users.api.v1.urls")),
    path("api/v1/activities/", include("apps.activities.api.v1.urls")),
        # Cart URLs - disabled, using orders/cart/ instead
    # path("api/v1/cart/", include("apps.cart.api.v1.urls")),
    path("api/v1/orders/", include("apps.orders.api.v1.urls")),
    path("api/v1/payments/", include("apps.payments.api.v1.urls")),
    
    # CSRF endpoint
    path("api/csrf/", ensure_csrf_cookie(csrf_view), name="csrf"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
