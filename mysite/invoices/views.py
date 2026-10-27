from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import InvoiceForm
from .models import Invoice

#create a new record
def create_invoice(request):
    Invoice.objects.create(
        customer_name='Bhumika Gupta',
        invoice_number='I001',
        amount=15000,
        is_paid=False,
        date_created=4-8-2005,
        email_id='bhumi485@gmail.com'

    )
    return render(request,'invoice_list.html' ,{})


#fetch a recored
def show_unpaid_invoices(request):
    unpaid_invoices=Invoice.objects.filter(is_paid=False)
    data={
        'unpaid_invoices':unpaid_invoices
    }
    return render(request,'invoice_list.html',data)

def mark_as_paid(request):
    Invoice.objects.filter(invoice_name='INV-001').update(is_paid=False)
    all_invoices=Invoice.objects.filter(is_paid=False)
    data={
        'all_invoices':all_invoices
    }

    return render(request,'cust_name.html',data)

def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('invoice_list')
        messages.error(request, 'Please correct the errors below.')
    else:
        form = InvoiceForm()

    data = {
        'form': form
    }
    return render(request, 'add_invoice.html', data)







class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoices = Invoice.objects.all()
        total_amount = invoices.aggregate(total=Sum('amount'))['total']
        context['total_invoices'] = invoices.count()
        context['total_customers'] = invoices.values('customer_name').distinct().count()
        context['total_revenue'] = total_amount or 0
        context['recent_invoices'] = invoices.order_by('-date_created', '-id')[:5]
        return context

class InvoiceListView(TemplateView):
    template_name="invoice_list.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoices = Invoice.objects.all().order_by('-date_created', '-id')
        context['all_invoices'] = invoices
        context['unpaid_invoices'] = invoices.filter(is_paid=False)
        return context


def show_invoices(request):
    data = {
        'all_invoices': Invoice.objects.all().order_by('customer_name', '-id')
    }
    return render(request, "cust_name.html", data)




# Create your views here.
