from django.shortcuts import render, get_object_or_404
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from finweb.utils import get_vtpass_basic_auth, get_variations_code, verify_smartnumber
from finweb.models import Category, NetworkService





@login_required
def service_provider_page(request, category_id):
    service_providers=NetworkService.objects.filter(category__identifier=category_id)
    context={
        'providers':service_providers,
        'category':Category.objects.get(identifier=category_id)
    }
    return render(request, "payments/airtime.html", context)

@login_required
def buy_page_view(request, service_id):
    provider=get_object_or_404(NetworkService, service_id=service_id)
    context={'provider':provider }
    if "data" in service_id:
        variations=get_variations_code(service_id)
        data_plans=variations['content']['varations']
        context['data_plans']=data_plans
    else:
        print("no")
    
    return render(request, "payments/payment.html", context)

@login_required
def verify_smartcard(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smart_number')
        service_id = request.POST.get('serviceid')
        request.session['global_service_id']=service_id
        customer=verify_smartnumber(smartcard_number, service_id)
        customer_obj=customer['content']
        request.session['customer']=customer_obj
        return redirect("Payments:tv-customer") 
    g_service_id=request.session.get('global_service_id')    
    return redirect("Payments:buy-now", service_id=g_service_id)

@login_required
def customer_comfirm_page(request):
    customer=request.session.get('customer')
    context={
        "customer":customer,
        "service_id":request.session.get('global_service_id')
    }
    return render(request, "payments/customer-confirm.html", context)


@login_required
def change_tv_subcription_bouquet(request, service_id):
    variations=get_variations_code(service_id)
    available_plan=variations['content']['varations']
    print(available_plan)
    context={
        "package_plans":available_plan,
        "service_id":service_id
    }
    return render(request, "payments/change_plan.html", context)


@login_required
def renew_tv_subscription_bouquet(request):
    pass

# def purchase_product(request):
#     if request.method == 'POST':
#         smartcard_number = request.POST.get('smartcard_number')
#         variation_code = request.POST.get('variation_code')
#         amount = request.POST.get('amount')
#         service_id = 'dstv'
#         request_id = 'your_unique_request_id'  # Generate a unique request ID

#         purchase_url = f'https://sandbox.vtpass.com/api/pay'

#         headers = {
#             'Authorization': get_vtpass_basic_auth(),
#         }

#         data = {
#             'request_id': request_id,
#             'serviceID': service_id,
#             'billersCode': smartcard_number,
#             'variation_code': variation_code,
#             'amount': amount,
#             'phone': 'customer_phone_number',
#             'subscription_type': 'renew',  # or 'change' for bouquet change
#             'quantity': 1,
#         }

#         response = requests.post(purchase_url, headers=headers, data=data)

#         if response.status_code == 200:
#             api_response = response.json()
#             # Process the API response and display relevant data to the user
#             return render(request, 'purchase_product.html', {'api_response': api_response})
#         else:
#             error_message = "Error occurred while purchasing product"
#             return render(request, 'purchase_product.html', {'error_message': error_message})
        
#     return HttpResponse("This is the purchase_product view.")


def subscription_form(request):

    bouquet_options = [

        {"name": "DStv Padi", "value": "N2,500"},
        {"name": "DStv Yanga", "value": "N3,500"},
        {"name": "Dstv Confam", "value": "N6,200"},
        {"name": "DStv Compact", "value": "N10,500"},
        # Add more options as needed
    ]
    
    context = {

        "bouquet_options": bouquet_options,
    }
    
    if request.method == "POST":
        selected_bouquet = request.POST.get("bouquet")
        for option in bouquet_options:
            if option["name"] == selected_bouquet:
                context["selected_amount"] = option["value"]
                break

    return render(request, "subscription_form.html", context)









