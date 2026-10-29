
from django.conf import settings
from django.db import models


class Invoice(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='invoices',
        null=True,
        blank=True,
    )
    customer_name = models.CharField(max_length=200)
    invoice_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=4)
    date_created = models.DateField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    email_id = models.CharField(max_length=50)

    def __str__(self):
        return self.invoice_number



