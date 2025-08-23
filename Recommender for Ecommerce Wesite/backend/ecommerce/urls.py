from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('admin/', admin.site.urls),
	path('products/', include('products.urls')),
	path('users/', include('users.urls')),
	path('recommendations/', include('recommendations.urls')),
	path('api/token/', __import__('rest_framework_simplejwt.views').rest_framework_simplejwt.views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
	path('api/token/refresh/', __import__('rest_framework_simplejwt.views').rest_framework_simplejwt.views.TokenRefreshView.as_view(), name='token_refresh'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
