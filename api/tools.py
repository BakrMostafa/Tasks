import json
import re


def get_client_ip(request):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    except Exception as e:
        print(e)
        return ''


def no_bool_convert(pairs):
    return {k: str(v).casefold() if isinstance(v, bool) else v for k, v in pairs}


def get_headers(request=None):
    """
        Function:       get_headers(self, request)
        Description:    To get all the headers from request
    """
    try:
        regex = re.compile('^HTTP_')
        return json.dumps(dict((regex.sub('', header), value) for (header, value)
                               in request.META.items() if header.startswith('HTTP_')))
    except Exception as e:
        print(e)
        return ''
