from django.shortcuts import redirect,render
from django.http import HttpResponse as response
from django.core.exceptions import PermissionDenied
import re

def UsersMiddleware(get_response):

    def middleware(request):
        print(request.path)
        if re.match(request.path,'users') or re.match(request.path,'metrices'):
            if not request.user.is_superuser:
                raise PermissionDenied()
        response = get_response(request)
        return response
    return middleware