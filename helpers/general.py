from django.http import request
import re
from django.core.paginator import Paginator
from django.core.serializers import serialize
import json
from datetime import *
from pendulum import day

from serializers.leaves_serializers import LeavesSerializer
from django.http import JsonResponse, HttpResponse
from datetime import date, datetime

def is_ajax():
    requested_html = re.search(r'^text/html', request.META.get('HTTP_ACCEPT'))
    if not requested_html:
        return False
    else:
        return True

def serialize_data(queryset):
    serialized_page = serialize("json", queryset)
    serialized_page = [obj for obj in json.loads(serialized_page)]
    data_objects = []
    for index, obj in enumerate(serialized_page):
        data_objects.append(obj['fields'])
    data = {
        "data": data_objects
    }
    return data

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


def make_serialized_pagination(request, query, serializer):
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
        "data": serializer(page_obj, many=True).data,
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
        fromDate = range[0]
        toDate = range[1]

    else:
        date_format = '%Y-%m-%d'
        fromDate = range
    return [fromDate, toDate]


def date_splitter(date):
    data = {
        "year": 0,
        "month": 0,
        "day": 0,
    }
    splitted = date.split('-')
    data['year'] = int(splitted[0])
    data['month'] = int(splitted[1])
    data['day'] = int(splitted[2])
    return data

from datetime import datetime, timedelta
def date_list_from_date_range(start, end):
    start = date_splitter(start)
    end = date_splitter(end)
    days = []
    delta = end - start
    for i in range(delta.days + 1):
        days.append((start + timedelta(days=i)).strftime("%Y-%m-%d"))
    return days




def time_difference(time1, time2):
    if isinstance(time1,timedelta) and isinstance(time2,timedelta):
        diff = time1.total_seconds() - time2.total_seconds()
        if diff < timedelta(0).total_seconds(): 
            diff = timedelta(0).total_seconds()
        hours = diff // 3600
        minutes = (diff % 3600) // 60
        return timedelta(hours=hours,minutes=minutes)
    else:
        hours=time1.hour-time2.hour
        minutes=time1.minute-time2.minute
        return timedelta(hours=hours,minutes=minutes)
def time_sum(time1, time2):
    diff = time1.total_seconds() + time2.total_seconds()
    if diff < timedelta(0).total_seconds(): 
        diff = timedelta(0).total_seconds()
    hours = diff // 3600
    minutes = (diff % 3600) // 60
    return timedelta(hours=hours,minutes=minutes)


def parse_time(time_str:str):
    hour,minutes=map(int,time_str.split(':'))
    return time(hour=hour,minute=minutes)


def parse_duration(duration_str:str):
    hour,minutes=map(int,duration_str.split(':'))
    return timedelta(hours=hour,minutes=minutes)
    