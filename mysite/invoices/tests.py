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


class InvoiceListAndDashboardTests(TestCase):
    def setUp(self):
        Invoice.objects.create(
            customer_name='Alice',
            invoice_number='INV-001',
            amount=Decimal('100.0000'),
            is_paid=True,
            email_id='alice@example.com',
        )
        Invoice.objects.create(
            customer_name='Alice',
            invoice_number='INV-002',
            amount=Decimal('50.0000'),
            is_paid=False,
            email_id='alice@example.com',
        )
        Invoice.objects.create(
            customer_name='Bob',
            invoice_number='INV-003',
            amount=Decimal('25.0000'),
            is_paid=False,
            email_id='bob@example.com',
        )

    def test_invoice_list_shows_model_fields(self):
        response = self.client.get(reverse('invoice_list'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'INV-001')
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'badge PAID')
        self.assertContains(response, 'badge UNPAID')
        self.assertContains(response, 'INV-002')
        self.assertNotContains(response, 'Due Date')
        self.assertNotContains(response, 'Shana')

    def test_dashboard_calculates_totals_from_database(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['total_invoices'], 3)
        self.assertEqual(response.context['total_customers'], 2)
        self.assertEqual(response.context['total_revenue'], Decimal('175.0000'))
        self.assertContains(response, 'INV-001')
        self.assertContains(response, 'INV-003')

    def test_customer_list_uses_invoice_records(self):
        response = self.client.get(reverse('cust_name'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Alice')
        self.assertContains(response, 'Bob')
        self.assertContains(response, 'INV-001')
        self.assertNotContains(response, 'Shana')
        self.assertNotContains(response, 'Aishwarya')
        self.assertNotContains(response, 'Nandni')
