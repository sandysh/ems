from django.http import request
import re
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json
from serializers.leaves_serializers import leavesSerializer
from django.http import JsonResponse, HttpResponse
from datetime import date, datetime

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


def make_serialized_pagination(request, query):
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
        "data": leavesSerializer(page_obj, many=True).data,
        "pagination": {
            "page": int(page),
            "limit": int(limit),
            "has_next": bool(page_obj.has_next()),
            "has_prev": bool(page_obj.has_previous()),
            "total": int(query.count())
        }
    }
    return data

def dateMaker(range):
    fromDate = None
    toDate = None
    if "to" in range:
        range = range.split(" to ")
        date_format = '%Y-%m-%d'
        fromDate = datetime.strptime(range[0], date_format)
        toDate = datetime.strptime(range[1], date_format)

    else:
        date_format = '%Y-%m-%d'
        fromDate = datetime.strptime(range, date_format)
    return [fromDate, toDate]