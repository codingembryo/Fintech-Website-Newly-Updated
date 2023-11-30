from django.urls import path
from . import views

app_name = 'Payments'

urlpatterns = [
    path('service-provider/<str:category_id>/', views.service_provider_page, name='provider'),
    path('provider/<str:service_id>/', views.buy_page_view, name="buy-now"),
    path('verify_smartcard/', views.verify_smartcard, name='verify_smartcard'),
    path('customer-confirm/', views.customer_comfirm_page, name="tv-customer"),
    path('change-plan/<str:service_id>/', views.change_tv_subcription_bouquet, name='tv-package'),
    path('subscription_form/', views.subscription_form, name='subscription_form'),
]



