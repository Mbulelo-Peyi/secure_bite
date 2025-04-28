from django.conf import settings

def clear_cookie(response, name, path="/",domain=None):
    response.set_cookie(
        name,
        max_age=0,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        path=path,
        domain=domain,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
    )