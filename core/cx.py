import json

import requests

from core.constants import CX_SHOWROOM_URL, CX_USER, CX_PASSWORD, CX_CONTACTS_URL, CX_TESTDRIVE_URL
from api.models import WebServiceLog
from api.tools import get_client_ip, get_headers


def get_cx_showrooms(request=None, params=None):
    response = requests.get(
        url=CX_SHOWROOM_URL + params,
        auth=(CX_USER, CX_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=CX_SHOWROOM_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_cx_contacts(request=None, params=None):
    response = requests.get(
        url=CX_CONTACTS_URL + params,
        auth=(CX_USER, CX_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=CX_CONTACTS_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_cx_test_drives(request=None, params=None):
    response = requests.get(
        url=CX_TESTDRIVE_URL + params,
        auth=(CX_USER, CX_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=CX_TESTDRIVE_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def patch_cx_testdrive(request, params=None, payload=None):
    response = requests.patch(
        url=CX_TESTDRIVE_URL + params,
        auth=(CX_USER, CX_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='PATCH',
        url=CX_TESTDRIVE_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_cx_contacts(request, payload=None):
    response = requests.post(
        url=CX_CONTACTS_URL,
        auth=(CX_USER, CX_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=CX_CONTACTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response
