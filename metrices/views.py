import json
from .models import Metrices
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from helpers.general import make_pagination
from django.views.decorators.http import require_http_methods

from helpers.general import is_ajax
from django_easy_validation import Validator
from metrices.rules.metrices_rules import MetricRules
from django.contrib.auth.decorators import login_required
from helpers.general import make_pagination

@require_http_methods('GET')
@login_required
def index(request):
    return render(request, 'metrices/index.html')


@require_http_methods('GET')
@login_required
def all(request):
    paginate = request.GET.get('paginate')
    searchText = request.GET.get('searchText')
    metrices = Metrices.objects.all().order_by('-id')
    if searchText is not None:
        metrices = metrices.filter(name__icontains=searchText)
    if paginate:
        data = make_pagination(request, metrices)
        return JsonResponse(data, safe=False)
    else:
        metrices = list(Metrices.objects.all().values())
        return JsonResponse(metrices, safe=False)


@require_http_methods('POST')
@login_required
def store(request):
    metrices = json.loads(request.body)
    #errors = Validator.validate(request, MetricRules.valid_rules, MetricRules.messages)
    # data = Validator.validated_data()
    # return JsonResponse(data, status=422, safe=False)
    # if Validator.failed():
    #     return JsonResponse(Validator.validation_error, status=422, safe=False)
    # if errors and is_ajax:
    #     return JsonResponse(errors, status=422, safe=False)
    inputs = {
        'name': metrices['name'],
        'score': metrices['score'],
        'is_active': metrices['is_active'],
    }
    metric = Metrices.objects.create(**inputs)
    return JsonResponse('success', safe=False)


@require_http_methods('DELETE')
@login_required
def destroy(request, metric_id):
    metric = Metrices.objects.filter(id=metric_id).delete()
    return JsonResponse('success', safe=False)


@require_http_methods('PUT')
@login_required
def update(request, metric_id):
    metrices = json.loads(request.body)
    errors = Validator.validate(request, {
        "name": "required|unique:rating_metrices|max:100|min:6",
        "score": "required|numeric"
    })
    if errors:
        return JsonResponse(errors, status=422, safe=False)

    if errors and is_ajax:
        return JsonResponse(errors, status=422, safe=False)

    inputs = {
        'name': metrices['name'],
        'score': metrices['score'],
        'is_active': metrices['is_active'],
    }
    metric = Metrices.objects.filter(id=metric_id).update(**inputs)
    return JsonResponse('success', safe=False)
