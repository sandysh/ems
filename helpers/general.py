from django.http import request
import re
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json


def is_ajax():
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    if not requested_html:
        return False
    else:
        return True


def make_pagination(request, query):
    page = request.GET.get('page')
    limit = request.GET.get('limit', 25)
    paginator = Paginator(query, limit)
    page_obj = paginator.get_page(page)
    serialized_page = serialize("json", page_obj)
    serialized_page = [obj for obj in json.loads(serialized_page)]
    data_objects = []
    for index, obj in enumerate(serialized_page):
        obj['fields']['id'] = obj['pk']
        data_objects.append(obj['fields'])
    data = {
        "data": data_objects,
        "pagination": {
            "page": int(page),
            "limit": int(limit),
            "has_next": bool(page_obj.has_next()),
            "has_prev": bool(page_obj.has_previous()),
            "total": int(query.count())
        }
    }
    return data
