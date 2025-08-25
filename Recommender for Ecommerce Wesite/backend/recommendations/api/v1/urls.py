from django.urls import path
from . import views

urlpatterns = [
  path('home/', views.home_recs, name='home-recs'),
  path('user/<int:user_id>/', views.user_recs, name='user-recs'),
  path('similar/<int:product_id>/', views.similar_items, name='similar-items'),
]
