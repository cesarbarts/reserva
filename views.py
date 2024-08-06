import json
import uuid
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import mercadopago
from django.contrib.auth.decorators import login_required
from feed.models import Variaveis
from feed.views import is_NOT_pro_required
from users.models import Influencer, Profile
from users.views_mixins import update_pro_status_required
from django.conf import settings

sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

def pagar(request):
    return render(request, 'pagar.html')

@csrf_exempt
def process_payment(request):
    if request.method == "POST":
        
        # description = request.POST.get('description')
        # payer_first_name = request.POST.get('payerFirstName')
        # payer_last_name = request.POST.get('payerLastName')
        # payer_email = request.POST.get('email')
        # identification_type = request.POST.get('identificationType')
        # identification_number = request.POST.get('identificationNumber')

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': str(uuid.uuid4())
        }

        
        
        payment_data = {
            "transaction_amount": 90,
            "description": "Acesso",
            "payment_method_id": "pix",
            "notification_url": "https://meuSiteAqui.com/ipn",
            "payer": {
                "email": "emaildetestes@gmailtesteeee.com",
                "first_name": "Cesar",
                "last_name": "Augusto",
                "identification": {
                    "type": "CPF",
                    "number": "98020002057" #cpfDeTestes
                },
               
            }
        }

        payment_response = sdk.payment().create(payment_data, request_options)
        payment = payment_response["response"]

        return JsonResponse(payment)

    return JsonResponse({'status': 'error', 'detail': 'Invalid request method'})


@csrf_exempt
def ipn(request):
    if request.method == 'POST':
        topic = request.GET.get('topic')
        resource_id = request.GET.get('id')
        
        if topic == 'payment':
            payment = sdk.payment().get(resource_id)
            payment_data = payment["response"]

            print(payment_data)
            
            
        elif topic == 'merchant_order':
            merchant_order = sdk.merchant_order().get(resource_id)
            merchant_order_data = merchant_order["response"]
            
            print(merchant_order_data)
            
        
        return HttpResponse(status=200)
    else:
        return JsonResponse({'status': 'error', 'detail': 'Invalid request method'}, status=400)
