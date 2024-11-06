from project.settings import DEBUG

if DEBUG:
    EBS_USER = 'RGI_CXINTG'
    EBS_PASSWORD = 'rgicx2020'
    EBS_OTP_URL = f"""http://172.16.170.153:7003/soa-infra/services/default/CX_PLSQL_RGI_CX_OTP_PKG/RGI_CX_OTP_PKG_Service"""
    EBS_CAR_INFO_URL = f"""http://172.16.170.153:7003/soa-infra/services/default/CX_PLSQL_RGI_CAR_INFO/RGI_CAR_INFO_Service"""
    EBS_CAR_HISTORY_URL = f"""http://172.16.170.153:7003/soa-infra/services/default/CX_PLSQL_RGI_CAR_HISTORY/RGI_CAR_HISTORY_Service"""

    VODAFONE_URL = f"""https://e3len.vodafone.com.eg/web2sms/sms/submit/"""
    VODAFONE_ACCOUNT_ID = '101009049'
    VODAFONE_PASSWORD = 'Vodafone.1'
    VODAFONE_SENDER_NAME = 'GB-Auto'
    VODAFONE_SECRET_KEY = b'888D4B0C4D6A467FA0046FC50A897BCB'

    RN_USER = 'cx.admin'
    RN_PASSWORD = 'AppsPro@2019'
    RN_BRAND = 'HYN'
    RN_BRAND_ID = 1
    RN_WORKSHOP_MECHANICAL_TYPE_ID = 3
    RN_BRAND_LOOKUP_NAME = 'Hyundai'
    RN_SHOWROOM_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/package.Showroom"""
    RN_BRANCH_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.Branch"""
    RN_OPERATION_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.Operation"""
    RN_APPOINTMENTS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/CO.Appointments"""
    RN_VEHICLE_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/package.Vehicle"""
    RN_QUERY_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/queryResults"""
    RN_MODEL_OPERATION_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.ModelOperation"""
    RN_MODEL_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.Model"""
    RN_CONTACTS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/contacts"""
    RN_OPERATION_CATEGORY_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.OperationCategory"""
    RN_EVENTS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/CO.events"""
    RN_APP_CANCEL_REASONS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.AppCancellationReas"""
    RN_INCIDENTS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/incidents"""
    RN_APPOINTMENT_PARTS_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.appointmentParts"""
    RN_APPOINTMENT_CONSUMBLE_URL = f"""https://gb-rightnow--tst1.custhelp.com/services/rest/connect/v1.3/Config.appointmentConsumble"""

    PAYMOB_API_KEY = f"""ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0luQnliMlpwYkdWZmNHc2lPakUwTXpRME9Td2lZMnhoYzNNaU9pSk5aWEpqYUdGdWRDSjkuQ0NINVJiWUtlbHRDblFMZW5xTnE1c1l3MHdsNjVpYWRMTWVxRk9oSUdzeG5LVmQybTFTSUt3cnJzN3FJU01sMzBiMUY0SG82RGZpdUNaVnhNYm5XakE="""
    PAYMOB_HMAC_KEY = b'AEBE8D5A687A6C3CD8FEBD7D42A023B4'
    PAYMOB_TOKENS_URL = f"""https://accept.paymob.com/api/auth/tokens"""
    PAYMOB_ORDERS_URL = f"""https://accept.paymob.com/api/ecommerce/orders"""
    PAYMOB_PAYMENT_KEYS_URL = f"""https://accept.paymob.com/api/acceptance/payment_keys"""

    CX_USER = 'cx.admin'
    CX_PASSWORD = 'AppsPro@2019'
    CX_CONTACTS_URL = f"""https://ccmf-test.fa.em3.oraclecloud.com/crmRestApi/resources/latest/contacts"""
    CX_SHOWROOM_URL = f"""https://ccmf-test.fa.em3.oraclecloud.com/crmRestApi/resources/latest/Showroom_c"""

    EXPO_URL = f"""https://exp.host/--/api/v2/push/send"""

    IT_EMAILS = [
        'developers@ghabbour.com',
        'bmostafa@ghabbour.com',
        'reem.hesham@ghabbour.com',
    ]

    RSA_EMAILS = [
                     'RSA@Ghabbour.com',
                 ] + IT_EMAILS
else:
    EBS_USER = 'RGI_CXINTG'
    EBS_PASSWORD = 'rgicx2020'
    EBS_OTP_URL = ""
    EBS_CAR_INFO_URL = f"""http://172.16.170.152:7003/soa-infra/services/default/PROD_PLSQL_RGI_CAR_INFO/RGI_CAR_INFO_Service"""
    EBS_CAR_HISTORY_URL = f"""http://172.16.170.152:7003/soa-infra/services/default/PROD_PLSQL_RGI_CAR_HISTORY/RGI_CAR_HISTORY_Service"""

    VODAFONE_URL = f"""https://e3len.vodafone.com.eg/web2sms/sms/submit/"""
    VODAFONE_ACCOUNT_ID = '101009049'
    VODAFONE_PASSWORD = 'Vodafone.1'
    VODAFONE_SENDER_NAME = 'GB-Auto'
    VODAFONE_SECRET_KEY = b'888D4B0C4D6A467FA0046FC50A897BCB'

    RN_USER = 'cx.admin'
    RN_PASSWORD = 'AppsPro@2019'
    RN_BRAND = 'HYN'
    RN_BRAND_ID = 1
    RN_WORKSHOP_MECHANICAL_TYPE_ID = 3
    RN_BRAND_LOOKUP_NAME = 'Hyundai'
    RN_SHOWROOM_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/package.Showroom"""
    RN_BRANCH_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.Branch"""
    RN_OPERATION_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.Operation"""
    RN_APPOINTMENTS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/CO.Appointments"""
    RN_VEHICLE_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/package.Vehicle"""
    RN_QUERY_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/queryResults"""
    RN_MODEL_OPERATION_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.ModelOperation"""
    RN_MODEL_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.Model"""
    RN_CONTACTS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/contacts"""
    RN_OPERATION_CATEGORY_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.OperationCategory"""
    RN_EVENTS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/CO.events"""
    RN_APP_CANCEL_REASONS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.AppCancellationReas"""
    RN_INCIDENTS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/incidents"""
    RN_APPOINTMENT_PARTS_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.appointmentParts"""
    RN_APPOINTMENT_CONSUMBLE_URL = f"""https://gb-rightnow.custhelp.com/services/rest/connect/v1.3/Config.appointmentConsumble"""

    PAYMOB_API_KEY = f"""ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SnVZVzFsSWpvaWFXNXBkR2xoYkNJc0luQnliMlpwYkdWZmNHc2lPakUwTXpRME9Td2lZMnhoYzNNaU9pSk5aWEpqYUdGdWRDSjkuQ0NINVJiWUtlbHRDblFMZW5xTnE1c1l3MHdsNjVpYWRMTWVxRk9oSUdzeG5LVmQybTFTSUt3cnJzN3FJU01sMzBiMUY0SG82RGZpdUNaVnhNYm5XakE="""
    PAYMOB_HMAC_KEY = b'AEBE8D5A687A6C3CD8FEBD7D42A023B4'
    PAYMOB_TOKENS_URL = f"""https://accept.paymob.com/api/auth/tokens"""
    PAYMOB_ORDERS_URL = f"""https://accept.paymob.com/api/ecommerce/orders"""
    PAYMOB_PAYMENT_KEYS_URL = f"""https://accept.paymob.com/api/acceptance/payment_keys"""

    CX_USER = 'cx.admin'
    CX_PASSWORD = 'AppsPro@2019'
    CX_CONTACTS_URL = f"""https://ccmf.fa.em3.oraclecloud.com/crmRestApi/resources/latest/contacts"""
    CX_SHOWROOM_URL = f"""https://ccmf.fa.em3.oraclecloud.com/crmRestApi/resources/latest/Showroom_c"""

    EXPO_URL = f"""https://exp.host/--/api/v2/push/send"""

    IT_EMAILS = [
        'developers@ghabbour.com',
        'ordermanagement@ghabbour.com',
    ]

    RSA_EMAILS = [
        'RSA@Ghabbour.com',
    ]
