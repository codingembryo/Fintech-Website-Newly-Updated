from django.shortcuts import render, redirect
import requests
from django.shortcuts import render
from .utils import get_vtpass_basic_auth
from django.http import HttpResponse



def verify_smartcard(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smartcard_number')
        service_id = 'dstv'
        verify_url = f'https://sandbox.vtpass.com/api/merchant-verify'

        headers = {
            'Authorization': get_vtpass_basic_auth(),
        }

        data = {
            'billersCode': smartcard_number,
            'serviceID': service_id,
        }

        response = requests.post(verify_url, headers=headers, data=data)

        if response.status_code == 200:
            api_response = response.json()
            # Process the API response and display relevant data to the user
            return render(request, 'verify_smartcard.html', {'api_response': api_response})
        else:
            error_message = "Error occurred while verifying smart card"
            return render(request, 'verify_smartcard.html', {'error_message': error_message})
        
    return render(request, 'verify_smartcard.html')




# views.py
def purchase_product(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smartcard_number')
        variation_code = request.POST.get('variation_code')
        amount = request.POST.get('amount')
        service_id = 'dstv'
        request_id = 'your_unique_request_id'  # Generate a unique request ID

        purchase_url = f'https://sandbox.vtpass.com/api/pay'

        headers = {
            'Authorization': get_vtpass_basic_auth(),
        }

        data = {
            'request_id': request_id,
            'serviceID': service_id,
            'billersCode': smartcard_number,
            'variation_code': variation_code,
            'amount': amount,
            'phone': 'customer_phone_number',
            'subscription_type': 'renew',  # or 'change' for bouquet change
            'quantity': 1,
        }

        response = requests.post(purchase_url, headers=headers, data=data)

        if response.status_code == 200:
            api_response = response.json()
            # Process the API response and display relevant data to the user
            return render(request, 'purchase_product.html', {'api_response': api_response})
        else:
            error_message = "Error occurred while purchasing product"
            return render(request, 'purchase_product.html', {'error_message': error_message})
        
    return HttpResponse("This is the purchase_product view.")


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

# def subscription_form(request):

#     bouquet_options = [

#         {"name": "DStv Padi", "value": "N2,500"},
#         {"name": "DStv Yanga", "value": "N3,500"},
#         {"name": "Dstv Confam", "value": "N6,200"},
#         {"name": "DStv Compact", "value": "N10,500"},
#         # Add more options as needed
#     ]
    
#     selected_amount = None

#     if request.method == "POST":
#         selected_bouquet = request.POST.get("bouquet")
#         for option in bouquet_options:

#             if option["name"] == selected_bouquet:

#                 selected_amount = option["value"]

#             else:
#                 return render(request, "home.html",)
#     else:
#         return render(request, "subscription_form.html", context)


#     context = {
#         "bouquet_options": bouquet_options,
#         "selected_amount": selected_amount
#     }

#     return render(request, "subscription_form.html", context)







