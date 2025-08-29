from django.db import models


class CartItem(models.Model):
    """
    Session-based cart item (stored in session, not DB)
    This model is mainly for serializer validation
    """
    book_id = models.IntegerField()
    quantity = models.IntegerField(default=1)
    
    class Meta:
        # This is a virtual model for validation only
        managed = False
