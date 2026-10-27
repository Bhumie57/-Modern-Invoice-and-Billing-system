from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Invoice


class AddInvoiceTests(TestCase):
    def test_create_invoice_success(self):
        response = self.client.post(
            reverse('invoice_add'),
            {
                'customer_name': 'Test Customer',
                'invoice_number': 'INV-100',
                'amount': '150.50',
            },
            follow=True,
        )

        self.assertRedirects(
            response,
            reverse('invoice_list'),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.get()
        self.assertEqual(invoice.customer_name, 'Test Customer')
        self.assertEqual(invoice.invoice_number, 'INV-100')
        self.assertEqual(invoice.amount, Decimal('150.5000'))
        self.assertFalse(invoice.is_paid)
        self.assertContains(response, 'Invoice created successfully.')

    def test_invalid_amount_is_rejected(self):
        for invalid_amount in ('0', '-10'):
            with self.subTest(amount=invalid_amount):
                response = self.client.post(
                    reverse('invoice_add'),
                    {
                        'customer_name': 'Test Customer',
                        'invoice_number': 'INV-101',
                        'amount': invalid_amount,
                    },
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(Invoice.objects.count(), 0)
                self.assertContains(response, 'Amount must be greater than 0')
                self.assertContains(response, 'Please correct the errors below.')
