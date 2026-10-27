from django.db import models

# Create your models here.
class Invoice(models.Model):
    customer_name=models.CharField(max_length=200)
    invoice_number=models.CharField(max_length=50)
    amount=models.DecimalField(max_digits=10,decimal_places=4)
    date_created=models.DateField(auto_now=True)
    is_paid=models.BooleanField(default=False)
    email_id=models.CharField(max_length=50)

    def _str_(self):
        return self.invoice_number



