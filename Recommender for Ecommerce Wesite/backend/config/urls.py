from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('users.api.v1.urls')),
    path('api/v1/catalog/', include('catalog.api.v1.urls')),
    path('api/v1/cart/', include('cart.api.v1.urls')),
    path('api/v1/recs/', include('recommendations.api.v1.urls')),
]
