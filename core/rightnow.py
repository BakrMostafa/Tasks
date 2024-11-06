import json

import requests

from core.constants import RN_SHOWROOM_URL, RN_USER, RN_PASSWORD, RN_BRANCH_URL, RN_OPERATION_URL, RN_APPOINTMENTS_URL, \
    RN_VEHICLE_URL, RN_QUERY_URL, RN_MODEL_OPERATION_URL, RN_MODEL_URL, RN_CONTACTS_URL, RN_OPERATION_CATEGORY_URL, \
    RN_EVENTS_URL, RN_INCIDENTS_URL, RN_APPOINTMENT_CONSUMBLE_URL, RN_APPOINTMENT_PARTS_URL
from api.models import WebServiceLog
from api.tools import get_client_ip, get_headers


def get_rn_showrooms(request, params=None):
    response = requests.get(
        url=RN_SHOWROOM_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_SHOWROOM_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_branches(request, params=None):
    response = requests.get(
        url=RN_BRANCH_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_BRANCH_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_operations(request, params=None):
    response = requests.get(
        url=RN_OPERATION_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_OPERATION_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_appointments(request, params=None):
    response = requests.get(
        url=RN_APPOINTMENTS_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_APPOINTMENTS_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_vehicle(request, params=None):
    response = requests.get(
        url=RN_VEHICLE_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_VEHICLE_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_query(request, params=None):
    response = requests.get(
        url=RN_QUERY_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_QUERY_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_model_operation(request, params=None):
    response = requests.get(
        url=RN_MODEL_OPERATION_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_MODEL_OPERATION_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_model(request, params=None):
    response = requests.get(
        url=RN_MODEL_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_MODEL_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_url(request, url=None, params=None):
    response = requests.get(
        url=url + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=url + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_contacts(request, params=None):
    response = requests.get(
        url=RN_CONTACTS_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_CONTACTS_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_contacts(request, payload=None):
    response = requests.post(
        url=RN_CONTACTS_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_CONTACTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_appointments(request, payload=None):
    response = requests.post(
        url=RN_APPOINTMENTS_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_APPOINTMENTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def get_rn_operation_category(request, params=None):
    response = requests.get(
        url=RN_OPERATION_CATEGORY_URL + params,
        auth=(RN_USER, RN_PASSWORD)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload='',
        method='GET',
        url=RN_OPERATION_CATEGORY_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_events(request, payload=None):
    response = requests.post(
        url=RN_EVENTS_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_EVENTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def patch_rn_appointments(request, params=None, payload=None):
    response = requests.patch(
        url=RN_APPOINTMENTS_URL + params,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='PATCH',
        url=RN_APPOINTMENTS_URL + params,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_incidents(request, payload=None):
    response = requests.post(
        url=RN_INCIDENTS_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_INCIDENTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_appointment_part(request, payload=None):
    response = requests.post(
        url=RN_APPOINTMENT_PARTS_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_APPOINTMENT_PARTS_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def post_rn_appointment_consumble(request, payload=None):
    response = requests.post(
        url=RN_APPOINTMENT_CONSUMBLE_URL,
        auth=(RN_USER, RN_PASSWORD),
        data=json.dumps(payload)
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=payload,
        method='POST',
        url=RN_APPOINTMENT_CONSUMBLE_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response
