from django.shortcuts import render, get_object_or_404
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from finweb import utils 
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
        variations=utils.get_variations_code(service_id)
        data_plans=variations['content']['varations']
        context['data_plans']=data_plans
    return render(request, "payments/payment.html", context)

def handle_airtime_or_data_subscription(request):
    if request.method == "POST":
        phone=request.POST.get('phone_number')
        amount=request.POST.get('amount')
        service_id=request.POST.get('serviceid')
        sub_plan=request.POST.get('plan_choice') #variation_code
        req_id=utils.generate_request_id()
        incoming_payload={
            "req_id":req_id,
            "service_id":service_id,
            "amount":amount,
            "sub_phone":phone,
            "variation_code":sub_plan,
            "phone_number":int('08011111111')
        }
        request.session['sev_id']=service_id
        output_result=utils.pay_for_airtime_or_data_subscription(incoming_payload)
        print(output_result)
        request.session['reqID']=output_result['requestId']
        return redirect("Payments:success", request_id=req_id)
    get_service_id=request.session.pop('sev_id')
    return redirect("Payments:buy-now", service_id=get_service_id)


def transaction_successful(request, request_id):
    get_transaction_status=utils.transaction_status(request_id)
    print(get_transaction_status)
    context={}
    transaction=get_transaction_status['content']['transactions']
    context['status_data']=transaction
    if transaction['type'] == "Electricity Bill":
        context['token']=get_transaction_status['purchased_code']
        context['unit']=get_transaction_status['units']

    return render(request, "payments/success.html", context)

@login_required
def verify_smartcard(request):
    if request.method == 'POST':
        smartcard_number = request.POST.get('smart_number')
        service_id = request.POST.get('serviceid')
        request.session['global_service_id']=service_id
        customer=utils.verify_smartnumber(smartcard_number, service_id)
        print('customer', customer)
        customer_obj=customer['content']
        request.session['customer']=customer_obj
        return redirect("Payments:tv-customer") 
    g_service_id=request.session.get('global_service_id')    
    return redirect("Payments:buy-now", service_id=g_service_id)

@login_required
def verify_meter_number(request):
    if request.method == 'POST':
        meter_number = request.POST.get('meter_number')
        meter_type = request.POST.get('meter_type_choice')
        service_id = request.POST.get('serviceid')
        request.session['global_service_id']=service_id
        request.session['meter_type']=meter_type
        customer=utils.meter_number_verify(meter_number,  meter_type, service_id)
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
    variations=utils.get_variations_code(service_id)
    available_plan=variations['content']['varations']
    context={
        "package_plans":available_plan,
        "service_id":service_id
    }
    if request.method == "POST":
        variation_code = request.POST.get('variation_code')
        card_num = request.POST.get('card_number')
        phone = request.POST.get('phone')
        amount= request.POST.get('amount')
        sev_id=request.POST.get('serviceid')
        req_id=utils.generate_request_id()
        incoming_payload={
            "request_id":req_id,
            "service_id":sev_id,
            "amount":amount,
            "phone":phone,
            "variation_code":variation_code,
            "smartcard_number": card_num
        }
        result=utils.pay_for_tv_new_package_sub(incoming_payload)
        print(result)
        request.session['request_id']=result['requestId']
        if result['response_description'] == "TRANSACTION SUCCESSFUL":
            return redirect("Payments:success", request_id=req_id)
    return render(request, "payments/change_plan.html", context)


@login_required
def renew_tv_subscription_bouquet(request):
    customer=request.session.get('customer')
    context={
        "customer":customer,
        "service_id":request.session.get('global_service_id')

    }
    # handle post req
    if request.method == 'POST':
        card_num = request.POST.get('smartcard_number')
        phone = request.POST.get('phone')
        amount= request.POST.get('amount')
        sev_id=request.POST.get('service_id')
        req_id=utils.generate_request_id()
        incoming_payload={
            "request_id":req_id,
            "service_id":sev_id,
            "amount":amount,
            "phone":phone,
            "smartcard_number": card_num
        }
        result=utils.pay_for_tv_subscription_renew(incoming_payload)
        print(result)
        request.session['request_id']=result['requestId']
        if result['response_description'] == "TRANSACTION SUCCESSFUL":
            return redirect("Payments:success", request_id=req_id)
    return render(request, "payments/renews.html", context)


@login_required
def buy_electric_unit(request): 
    context={
        "service_id":request.session.get('global_service_id'),      
    }
    # handle post req
    if request.method == 'POST':
        card_num = request.POST.get('meter_number')
        phone = request.POST.get('phone')
        amount= request.POST.get('amount')
        sev_id=request.POST.get('service_id')
        req_id=utils.generate_request_id()
        incoming_payload={
            "request_id":req_id,
            "service_id":sev_id,
            "amount":amount,
            "phone":phone,
            "meter_number": card_num,
            "meter_type":request.session.get('meter_type')
        }
        result=utils.buy_electricity_api_call(incoming_payload)
        request.session['request_id']=result['requestId']
        if result['response_description'] == "TRANSACTION SUCCESSFUL":
            return redirect("Payments:success", request_id=req_id)
    return render(request, "payments/buy_electricity.html", context)











