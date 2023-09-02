
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import random
import string
import json
from django.http import JsonResponse, HttpResponse
from datetime import datetime


# Create your views here.

def home(request):
     return render(request, 'home.html')



def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!!")
            return redirect('home')
        else:
            messages.error(request, "There was an error trying to login")
            return redirect('login')
    
    return render(request, 'login.html', {})
            


def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return render(request, 'logout.html')

def about(request):
    return render(request, 'about.html')

def security(request):
    return render(request, 'security.html')

def faq(request):
    return render(request, 'faq.html')

def support(request):
    return render(request, 'support.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have registered successfully...!!!")
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form':form})




def airtime(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        
        # Prepare the request data
        data = {
            "serviceID": "mtn",
            "amount": amount,
            "phone": phone_number
        }
        
        # Make the POST request to the VTpass API with API keys
        response = requests.post("https://api-service.vtpass.com/api/pay", json=data, headers={
            "api-key": "fc80349ce564c62d9be85521cc3b242c",
            "secret-key": "SK_5099bba9195a6a0fc596d0e8fa7a9e9b7e51051f285"
        })
        
        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            return JsonResponse(response_data)
        else:
            error_message = "An error occurred while processing the request."
            return render(request, "error_page.html", {"error_message": error_message})

    return render(request, "airtime.html")







# Define a function to get variation codes
def get_variation_codes():

    serviceID = "mtn-data"
    # Set the API endpoint
    api_url = "https://sandbox.vtpass.com/api/service-variations"
    # Send a GET request with serviceID as query parameter
    response = requests.get(api_url, params={"serviceID": serviceID})
    # Parse the response as JSON
    data = response.json()
    # Return the content field
    return data["content"]

# Define a function to purchase product
# def purchase_product(request_id, phone, variation_code):
# # Set your API key and secret key
#     api_key = "fc80349ce564c62d9be85521cc3b242c"
#     secret_key = "SK_952894cffaecd3191d6a580041776279f644e87db0a"

#     # Set the serviceID
#     serviceID = "mtn-data"
#     # Set the amount (will be ignored by API)
#     amount = 0
#     # Set the API endpoint
#     api_url = "https://sandbox.vtpass.com/api/pay"

#     # Set the data parameters based on user input and function arguments
#     data = {
#     "request_id": request_id,
#     "serviceID": serviceID,
#     "billersCode": phone,
#     "variation_code": variation_code,
#     "amount": amount,
#     "phone": phone
#     }

#     # Set the header parameters
#     headers = {
#     "api-key": api_key,
#     "secret-key": secret_key
#     }

#     # Send a POST request with data and header parameters
#     response = requests.post(api_url, data=data, headers=headers)

#      # Parse the response as JSON
#     data = response.json()

#     # Get the content field of the data or an empty dictionary if not found
#     content = data.get('content', {})

#     # Return the content as the output of the function
#     return content



# # Import requests library
# import requests

# # Define a function to query transaction status
# def query_transaction_status(request_id):
# # Set your API key and secret key
#     api_key = "fc80349ce564c62d9be85521cc3b242c"
#     secret_key = "SK_952894cffaecd3191d6a580041776279f644e87db0a"

#     # Set the API endpoint
#     api_url = "https://sandbox.vtpass.com/api/requery"

#     # Set the header parameters
#     headers = {
#     "api-key": api_key,
#     "secret-key": secret_key
#     }

#     # Set the data parameter with request_id
#     data = {"request_id": request_id}

#     # Send a POST request with data and header parameters
#     response = requests.post(api_url, data=data, headers=headers)

#     # Parse the response as JSON
#     data = response.json()

#     # Get the content field of the data or an empty dictionary if not found
#     content = data.get('content', {})

#     # Return the content as the output of the function
#     return content



def index(request):
    pass
#     # Get variation codes from API
#     variations = get_variation_codes()

#     # Initialize purchase result and transaction status as None
#     purchase_result = None
#     transaction_status = None

#     # Check if request method is POST
#     if request.method == "POST":
#         # Get user input from form fields
#         phone = request.POST["phone"]
#         print("request.POST:", request.POST)
#         variation_code = request.POST["variation_code"]

#         # Generate a random request_id
#         request_id = "".join(random.choices(string.ascii_letters + string.digits, k=16))

#         # Purchase product from API with user input and request_id
#         purchase_result = purchase_product(request_id, phone, variation_code)

#         # Check if purchase_result is a dictionary
#         if isinstance(purchase_result, dict):
#             # Check if purchase_result contains transactions field
#             if "transactions" in purchase_result:
#                 # Get the status of the transaction
#                 purchase_status = purchase_result["transactions"]["status"]
#             else:
#                 # Handle the case when purchase_result does not contain transactions field
#                 purchase_status = "Purchase failed: No transaction details found"
#         else:
#             # Handle the case when purchase_result is not a dictionary
#             purchase_status = f"Purchase failed: {purchase_result}"

#         # Query transaction status from API with request_id
#         transaction_status = query_transaction_status(request_id)

#         # Convert the transaction_status into a JSON string
#         transaction_status = json.dumps(transaction_status)

#         # Render HTML template with context variables
#         return render(request, "index.html", {
#             "variations": variations,
#             "purchase_status": purchase_status,
#             "transaction_status": transaction_status,
#             "phone": phone
#         })

#     # Add a default return statement outside the if block
#     return render(request, "index.html", {"variations": variations})


# Import requests library
import requests

# Define a function to query variation detail
def query_variation_detail(service, value):

    api_key = "ap_7fc5492227c0643709a95c8727286880"

    # Set the API endpoint
    api_url = "https://www.vtusub.com/api/variation"

    # Set the header parameter
    headers = {
    "Authorization": api_key
    }

    # Set the query parameters
    params = {
    "service": service,
    "value": value
    }

    # Send a GET request with header and query parameters
    response = requests.get(api_url, headers=headers, params=params)

    # Parse the response as JSON
    data = response.json()

    # Return the data as the output of the function
    return data


# import requests module
import requests
from .models import Category, Subcategory
from django.shortcuts import render

# define a function to get category
def get_category():
    response = requests.get("https://www.vtusub.com/api/category")
    # check if the request was successful
    if response.status_code == 200:
    # parse the JSON response
        data = response.json()
        # return the list of categories
        return data
    else:
        # return an error message
        return f"Request failed with status code {response.status_code}"

        # define a function to get subcategory given a category name
def get_subcategory(category):
        # send a GET request to the subcategory endpoint with the category parameter
    response = requests.get(f"https://www.vtusub.com/api/sub-category?category={category}")
        # check if the request was successful
    if response.status_code == 200:
        # parse the JSON response
        data = response.json()
        # return the list of subcategories
        return data
    else:
        # return an error message
        return f"Request failed with status code {response.status_code}"

#         # test the functions
# print(get_category())
# print(get_subcategory("mobile_vtu"))

def display_data(request):
# query all the categories and subcategories from the database
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    # pass the data to a template called data.html
    return render(request, "data.html", {"categories": categories, "subcategories": subcategories})


# import requests and os modules
import requests
import os

# import render function from django.shortcuts
from django.shortcuts import render

# get the base URL and API key from settings.py
BASE_URL = os.environ.get("BASE_URL")
API_KEY = os.environ.get("API_KEY")

# define a view function that takes a request object as an argument
def get_categories(request):
# send a GET request to the category endpoint with the API key as a header
    response = requests.get(BASE_URL + "/api/category", headers={"x-api-key": API_KEY})
    # check if the request was successful
    if response.status_code == 200:
    # parse the JSON response
        data = response.json()
    # pass the data to a template called categories.html
        return render(request, "categories.html", {"data": data})
    else:
    # return an error message
        return f"Request failed with status code {response.status_code}"


