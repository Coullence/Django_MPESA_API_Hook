from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment, STKPayment


def getAccessToken(request):
    consumer_key = 'GWN63gFpp6eGAroGw5qd0jMTVji5rMH9'
    consumer_secret = 'Ny4fkTh7RYIXQeC9'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254726634786,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254726634786,  # replace with your phone number to get stk push
        "CallBackURL": "https://young-refuge-80064.herokuapp.com/payments/api/v1/c2b/callback/",
        "AccountReference": "Henry",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://11fd346ae7ec.ngrok.io/payments/api/v1/c2b/confirmation/",
               "ValidationURL": "https://11fd346ae7ec.ngrok.io/payments/api/v1/c2b/validation/"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    
    print("hey its is here ******************************** ")
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    
    print (mpesa_payment)
    
    
    # Amount = mpesa_payment['Amount']
    # PhoneNumber = mpesa_payment['PhoneNumber']
    
    # json["items"][0]["links"]["self"] 
    
    # Amount = mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']['0']['Amount']['Value']
    
    # print ("The Amount".Amount)
    
    
#    {'Body': 
#        {'stkCallback': 
#            {'MerchantRequestID': '7458-11137033-1', 
#             'CheckoutRequestID': 'ws_CO_180620211648213536', 
#             'ResultCode': 0, 
#             'ResultDesc': 'The service request is processed successfully.', 
#             'CallbackMetadata': 
#                 {'Item': [
#                     {'Name': 'Amount', 'Value': 1.0}, 
#                     {'Name': 'MpesaReceiptNumber', 'Value': 'PFI0AO4WHS'}, 
#                     {'Name': 'Balance'}, 
#                     {'Name': 'TransactionDate', 'Value': 20210618164834}, 
#                     {'Name': 'PhoneNumber', 'Value': 254726634786}
#                     ]
#                  }
#                 }
#            }
#        }


    payment = STKPayment(
        amount= mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']['0']['Amount']['Value'],
        phone_number= mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']['0']['PhoneNumber']['Value'],
        transaction_code= mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item']['0']['MpesaReceiptNumber']['Value'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    
    print("hey its is here ******************************** ")
    

    return JsonResponse(dict(context))


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    print("called")
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))