import os
import base64
import json
import secrets
import string
import requests
from django.utils import timezone
from .models import Category
from django.conf import settings



def generate_request_id():
    current_datetime = timezone.now()
    date_time_str = current_datetime.strftime("%Y%m%d%H%M%S")
    random_string = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
    # Combine date, time, and random string
    code = f"{date_time_str}{random_string}"
    return code

#utilities functions
def get_service_categories():
    try:
        headers={"api-key":settings.API_KEY, "public-key":settings.PUBLIC_KEY }
        response = requests.get(f"{settings.BASE_URL}api/service-categories", headers=headers)
        data = response.json()
        objects_to_create = [Category(**item) for item in data['content']]
        Category.objects.bulk_create(objects_to_create)
    except Exception as e: 
        return f"Request failed with status code {e}"
    
def get_variations_code(service_id):
    try:
        headers={"api-key":settings.API_KEY, "public-key":settings.PUBLIC_KEY }
        response = requests.get(f"{settings.BASE_URL}api/service-variations?serviceID={service_id}", headers=headers) 
        data=response.json()
        return data
    except Exception as e:
        return f"Request failed with status code {e}"
    
def get_vtpass_basic_auth():
    username = settings.VT_PASS_USERNAME  # Update with the actual setting name
    password = settings.VT_PASS_PASSWORD  # Update with the actual setting name
    auth_string = f"{username}:{password}"
    auth_bytes = auth_string.encode('utf-8')
    base64_auth = base64.b64encode(auth_bytes).decode('utf-8')
    return f"Basic {base64_auth}"

def verify_smartnumber(card_number, service_id):
    headers={}
    verify_url = f'{settings.BASE_URL}api/merchant-verify'
    try: 
        headers["api-key"]=settings.API_KEY
        headers["secret-key"]=settings.API_SECRET_KEY 
        payload= {
            'billersCode': card_number,
            'serviceID': service_id,
        }
        response = requests.post(verify_url, headers=headers, data=payload)
        print(response)
        api_result = response.json()
        return api_result
        
    except Exception as e:
        return f"Request failed with the following exception {e}"

def meter_number_verify(meter_number, meter_type, service_id):
    headers={}
    verify_url = f'{settings.BASE_URL}api/merchant-verify'
    try: 
        headers["api-key"]=settings.API_KEY
        headers["secret-key"]=settings.API_SECRET_KEY 
        payload= {
            'billersCode': meter_number,
            'serviceID': service_id,
            'type':meter_type
        }
        response = requests.post(verify_url, headers=headers, data=payload)
        api_result = response.json()
        return api_result
        
    except Exception as e:
        return f"Request failed with the following exception {e}"


def pay_for_tv_new_package_sub(input_data):
        purchase_url = f'https://sandbox.vtpass.com/api/pay'
        headers={}
        headers["api-key"]=settings.API_KEY
        headers["secret-key"]=settings.API_SECRET_KEY
        data = {
            'request_id': input_data['request_id'],
            'serviceID': input_data['service_id'],
            'billersCode': input_data['smartcard_number'],
            'variation_code': input_data['variation_code'],
            'amount': input_data['amount'],
            'phone': input_data['phone'],
            'subscription_type': 'change',  # or 'change' for bouquet change
            
        }
        response = requests.post(purchase_url, headers=headers, data=data)
        res = response.json()
        return res


def pay_for_tv_subscription_renew(input_data):
        purchase_url = f'https://sandbox.vtpass.com/api/pay'
        headers={}
        headers["api-key"]=settings.API_KEY
        headers["secret-key"]=settings.API_SECRET_KEY
        data = {
            'request_id': input_data['request_id'],
            'serviceID': input_data['service_id'],
            'billersCode': input_data['smartcard_number'],
            'amount': input_data['amount'], #renewal amount
            'phone': input_data['phone'],
            'subscription_type': 'renew',  # or 'change' for bouquet change
            
        }
        response = requests.post(purchase_url, headers=headers, data=data)
        res = response.json()
        return res

# def pay_internet_data_subscription(input):
#     api_url="https://sandbox.vtpass.com/api/pay"
#     try:  
#         headers={
#             "api-key":settings.API_KEY,
#             "secret-key":settings.API_SECRET_KEY
#         }
#         payload={
#             "request_id":input.get('req_id'),
#             "serviceID":input.get('service_id'),
#             "amount":input.get('amount'),
#             "billersCode":input.get('sub_phone'),
#             "variation_code":input.get('variation_code'),
#             "phone":input.get('phone_number') #login user phone
#         }
#         response = requests.post(api_url, data=payload, headers=headers)
#         result= response.json()
#         return result
#     except Exception as err:
#         return f"something when wrong with the following exception {err}"    

def pay_for_airtime_or_data_subscription(input:dict[str, any]):
    api_url='https://sandbox.vtpass.com/api/pay'
    payload={}
    try:  
        headers={
            "api-key":settings.API_KEY,
            "secret-key":settings.API_SECRET_KEY
        }
        if "data" in input.get('service_id'):
            payload["request_id"]=input.get('req_id'),
            payload["serviceID"]=input.get('service_id'),
            payload["amount"]=input.get('amount'),
            payload["billersCode"]=input.get('sub_phone'),
            payload["variation_code"]=input.get('variation_code'),
            payload["phone"]=input.get('phone_number') #login user phone      
        else:
            payload["request_id"]=input.get('req_id'),
            payload["serviceID"]=input.get('service_id'),
            payload["amount"]=input.get('amount'),
            payload["phone"]=input.get('sub_phone')
        print("payload: ", payload)
        response = requests.post(api_url, data=payload, headers=headers)
        result= response.json()
        return result
    except Exception as err:
        return f"something when wrong with the following exception {err}"
    
def transaction_status(request_id):
    api_url='https://sandbox.vtpass.com/api/requery'
    headers={
            "api-key":settings.API_KEY,
            "secret-key":settings.API_SECRET_KEY
        }
    data={"request_id": request_id}
    response = requests.post(api_url, data=data, headers=headers)
    res = response.json()
    return res

def buy_electricity_api_call(input_data):
        purchase_url = f'https://sandbox.vtpass.com/api/pay'
        headers={}
        headers["api-key"]=settings.API_KEY
        headers["secret-key"]=settings.API_SECRET_KEY
        data = {
            'request_id': input_data['request_id'],
            'serviceID': input_data['service_id'],
            'billersCode': input_data['meter_number'],
            'variation_code':input_data['meter_type'],  
            'amount': input_data['amount'], #renewal amount
            'phone': input_data['phone'],
                   
        }
        response = requests.post(purchase_url, headers=headers, data=data)
        res = response.json()
        return res
    

    


    
    


