from django import forms
from .models import Invoice

class InvoiceForm(forms.ModelForm):
    class Meta:
        model=Invoice
        fields=[
                'customer_name','invoice_number','amount','is_paid'
        
            ]
    def clean_amount(self):
        amount=self.cleaned_data.get(amount)
        if amount<=0:
            raise forms.ValidationError('Amount must be greater than 0')
        return amount

