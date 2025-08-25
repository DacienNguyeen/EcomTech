from django.db import models
from django.conf import settings

class Interaction(models.Model):
    VIEW = 'view'; CART = 'cart'; PURCHASE = 'purchase'
    EVENT_CHOICES = [(VIEW,'view'), (CART,'cart'), (PURCHASE,'purchase')]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    product_id = models.CharField(max_length=255)
    event = models.CharField(max_length=16, choices=EVENT_CHOICES)
    weight = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['user','product_id','event','created_at'])]
