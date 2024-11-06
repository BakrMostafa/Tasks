from django.contrib import admin


def admin_header_processor(request):
    site_header = getattr(admin.site, 'site_header')
    return {"site_header": site_header}
