import requests

from core import constants
from core.constants import EBS_USER, EBS_OTP_URL, EBS_CAR_INFO_URL, EBS_PASSWORD, EBS_CAR_HISTORY_URL
from api.models import WebServiceLog
from api.tools import get_client_ip, get_headers


def ebs_otp(request, otp=None, mob_num=None):
    data = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:rgi="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_cx_otp_pkg/" xmlns:otp="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_cx_otp_pkg/otp_send/">
                   <soapenv:Header>
                      <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                         <wsse:UsernameToken>
                            <wsse:Username>{EBS_USER}</wsse:Username>
                            <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{EBS_PASSWORD}</wsse:Password>
                         </wsse:UsernameToken>
                      </wsse:Security>
                   </soapenv:Header>
                   <soapenv:Body>
                      <otp:InputParameters>
                         <otp:P_OTP_CODE>{otp}</otp:P_OTP_CODE>
                         <otp:P_MOBILE_NO>{mob_num}</otp:P_MOBILE_NO>
                      </otp:InputParameters>
                   </soapenv:Body>
                </soapenv:Envelope>"""

    response = requests.post(
        url=EBS_OTP_URL,
        data=data.encode('utf-8'),
        headers={'content-type': 'text/xml'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=constants.EBS_OTP_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def ebs_car_info(request):
    data = f"""<soapenv:Envelope
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:rgi="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_info/"
                    xmlns:car="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_info/car_info/">
                    <soapenv:Header>
                      <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                         <wsse:UsernameToken>
                            <wsse:Username>{EBS_USER}</wsse:Username>
                            <wsse:Password
                             Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{EBS_PASSWORD}</wsse:Password>
                         </wsse:UsernameToken>
                      </wsse:Security>
                    </soapenv:Header>
                    <soapenv:Body>
                      <car:InputParameters>
                         <car:P_CHASSIS_NUM>{request.data['chassis_num']}</car:P_CHASSIS_NUM>
                         <car:P_ENGINE_NUM>{request.data['engine_num']}</car:P_ENGINE_NUM>
                      </car:InputParameters>
                    </soapenv:Body>
                </soapenv:Envelope>"""

    response = requests.post(url=EBS_CAR_INFO_URL, data=data.encode('utf-8'), headers={'content-type': 'text/xml'})

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=EBS_CAR_INFO_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def ebs_car_history(request, ebs_lot_number, ebs_serial_number):
    data = f"""<soapenv:Envelope
                    xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"
                    xmlns:rgi="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_history/"
                    xmlns:car="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_history/car_history/">
                    <soapenv:Header>
                      <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                         <wsse:UsernameToken>
                            <wsse:Username>{EBS_USER}</wsse:Username>
                            <wsse:Password
                             Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{EBS_PASSWORD}</wsse:Password>
                         </wsse:UsernameToken>
                      </wsse:Security>
                    </soapenv:Header>
                    <soapenv:Body>
                      <car:InputParameters>
                         <car:P_CHASSIS_NUM>{ebs_lot_number}</car:P_CHASSIS_NUM>
                         <car:P_ENGINE_NUM>{ebs_serial_number}</car:P_ENGINE_NUM>
                      </car:InputParameters>
                    </soapenv:Body>
                </soapenv:Envelope>"""

    response = requests.post(
        url=EBS_CAR_HISTORY_URL,
        data=data.encode('utf-8'),
        headers={'content-type': 'text/xml'}
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=EBS_CAR_HISTORY_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response


def ebs_car_km(request, ebs_instance_id):
    data = f"""<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:rgi="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_info/" xmlns:car="http://xmlns.oracle.com/apps/ar/soaprovider/plsql/rgi_car_info/car_info_km/">
               <soapenv:Header>
                  <wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">
                     <wsse:UsernameToken>
                        <wsse:Username>{EBS_USER}</wsse:Username>
                        <wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText">{EBS_PASSWORD}</wsse:Password>
                     </wsse:UsernameToken>
                  </wsse:Security>
               </soapenv:Header>
               <soapenv:Body>
                  <car:InputParameters>
                     <!--Optional:-->
                     <car:P_INSTANCE_ID>{ebs_instance_id}</car:P_INSTANCE_ID>
                  </car:InputParameters>
               </soapenv:Body>
            </soapenv:Envelope>"""

    response = requests.post(
        url=EBS_CAR_INFO_URL,
        data=data.encode('utf-8'),
        headers={
            'content-type': 'text/xml',
            'SOAPAction': 'CAR_INFO_KM'
        }
    )

    WebServiceLog(
        headers=get_headers(request),
        ip=get_client_ip(request),
        payload=data,
        method='POST',
        url=EBS_CAR_INFO_URL,
        status_code=response.status_code,
        status_msg=response.reason,
        response=response.text
    ).save()

    return response
