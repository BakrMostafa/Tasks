import hashlib
import hmac

import requests

from core.constants import VODAFONE_URL, VODAFONE_ACCOUNT_ID, VODAFONE_PASSWORD, VODAFONE_SENDER_NAME, \
    VODAFONE_SECRET_KEY
from api.models import WebServiceLog
from api.tools import get_headers, get_client_ip


def send_sms(request=None, phone="", msg=""):
    hmac_concatenated = str(f'AccountId={VODAFONE_ACCOUNT_ID}&')
    hmac_concatenated += str(f'Password={VODAFONE_PASSWORD}&')
    hmac_concatenated += str(f'SenderName={VODAFONE_SENDER_NAME}&')
    hmac_concatenated += str(f'ReceiverMSISDN={phone}&')
    hmac_concatenated += str(f'SMSText={msg}')
    hashed_hmac = hmac.new(VODAFONE_SECRET_KEY, hmac_concatenated.encode('utf-8'), hashlib.sha256).hexdigest()

    data = f"""<?xml version="1.0" encoding="UTF-8"?>
                <SubmitSMSRequest xmlns:="http://www.edafa.com/web2sms/sms/model/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.edafa.com/web2sms/sms/model/ SMSAPI.xsd " xsi:type="SubmitSMSRequest">
                    <AccountId>{VODAFONE_ACCOUNT_ID}</AccountId>
                    <Password>{VODAFONE_PASSWORD}</Password>
                    <SecureHash>{hashed_hmac.upper()}</SecureHash>
                    <SMSList>
                        <SenderName>{VODAFONE_SENDER_NAME}</SenderName>
                        <ReceiverMSISDN>{phone}</ReceiverMSISDN>
                        <SMSText>{msg}</SMSText>
                    </SMSList>
                </SubmitSMSRequest>"""

    response = requests.post(
        url=VODAFONE_URL,
        data=data.encode('utf-8'),
        headers={'content-type': 'application/xml'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=VODAFONE_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response
