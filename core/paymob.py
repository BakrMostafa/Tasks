import json

import requests

from core.constants import PAYMOB_API_KEY, PAYMOB_TOKENS_URL, PAYMOB_ORDERS_URL, PAYMOB_PAYMENT_KEYS_URL
from api.models import WebServiceLog
from api.tools import get_client_ip, get_headers


def paymob_token(request):
    data = {
        "api_key": PAYMOB_API_KEY
    }

    data = json.dumps(data)

    response = requests.post(
        url=PAYMOB_TOKENS_URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=PAYMOB_TOKENS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    if response.status_code == 201:
        token = json.loads(response.text).get('token')
        return True, token
    else:
        return False


def paymob_order(request, token, amount, items):
    data = {
        "auth_token": token,
        "delivery_needed": "false",
        "amount_cents": amount,
        "items": items
    }

    data = json.dumps(data)

    response = requests.post(
        url=PAYMOB_ORDERS_URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=PAYMOB_ORDERS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    if response.status_code == 201:
        order_id = json.loads(response.text).get('id')
        return True, order_id
    else:
        return False


def paymob_payment_keys(request, token, amount, order_id):
    email = request.user.email
    first_name = request.user.first_name
    phone_number = request.user.username
    last_name = request.user.last_name

    data = {
        "auth_token": token,
        "amount_cents": amount,
        "expiration": 3600,
        "order_id": order_id,
        "currency": "EGP",
        "integration_id": 1632435,
        "billing_data": {
            "apartment": "NA",
            "email": email,
            "floor": "NA",
            "first_name": first_name,
            "street": "NA",
            "building": "NA",
            "phone_number": phone_number,
            "shipping_method": "NA",
            "postal_code": "NA",
            "city": "NA",
            "country": "NA",
            "last_name": last_name,
            "state": "NA"
        }
    }

    data = json.dumps(data)

    response = requests.post(
        url=PAYMOB_PAYMENT_KEYS_URL,
        data=data,
        headers={'Content-Type': 'application/json'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=PAYMOB_PAYMENT_KEYS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    if response.status_code == 201:
        payment_token = json.loads(response.text).get('token')
        return True, payment_token
    else:
        return False
