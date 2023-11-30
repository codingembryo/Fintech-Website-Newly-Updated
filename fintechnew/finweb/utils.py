import os
import base64
import requests
from .models import Category
from django.conf import settings


#utilities function
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
        if service_id == "dstv":
            headers['Authorization']=get_vtpass_basic_auth(),
        else:
            headers["api-key"]=settings.API_KEY
            headers["secret-key"]=settings.API_SECRET_KEY 
        payload= {
            'billersCode': card_number,
            'serviceID': service_id,
        }
        response = requests.post(verify_url, headers=headers, data=payload)
        api_result = response.json()
        return api_result
        
    except Exception as e:
        return f"Request failed with the following exception {e}"


    

    


    
    


