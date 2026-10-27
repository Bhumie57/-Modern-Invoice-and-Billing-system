"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from invoices import views
from django.contrib.auth import views as auth_views
from accounts import views as account_views




#path('address/', view_function,name='nickname')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('cust_name/',views.show_invoices,name='cust_name'),
    path('all/',views.InvoiceListView.as_view(),name='invoice_list'),
    
   
    path('home/',views.HomePageView.as_view(),name='home'),
    path('invoice_add/' ,views.add_invoice,name='invoice_add'),
    path('login/',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('signup/',account_views.signup,name='signup'),
         
]
