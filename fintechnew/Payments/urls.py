from django.urls import path
from . import views

app_name = 'Payments'

urlpatterns = [
    path('service-provider/<str:category_id>/', views.service_provider_page, name='provider'),
    path('provider/<str:service_id>/', views.buy_page_view, name="buy-now"),
    path('verify_smartcard/', views.verify_smartcard, name='verify_smartcard'),
    path('verify-meter/', views.verify_meter_number, name='electric-meter'),
    path('customer-confirm/', views.customer_comfirm_page, name="tv-customer"),
    path('change-plan/<str:service_id>/', views.change_tv_subcription_bouquet, name='tv-package'),
    path("renew-tv-subscription/", views.renew_tv_subscription_bouquet, name="tv-sub-renew"),
    path('subscription/payment/', views.handle_airtime_or_data_subscription, name='mobile-payment'),
    path('buy-electricity/', views.buy_electric_unit, name="buy-electricity"),
    path("transaction-success/<str:request_id>/", views.transaction_successful, name='success')
]



