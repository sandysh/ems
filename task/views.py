from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from helpers.general import make_pagination
from django.contrib import messages
from project.models import Project, Status, Task
from rest_framework.views import APIView
from django.core.paginator import Paginator
from django.db.models import Q
import json
from task.serializers import TaskSerializer


# Create your views here.
class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'task/index.html')


class TaskView(APIView):

    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return JsonResponse(serializer.data, safe=False)


class AllTaskView(LoginRequiredMixin, View):

    def get(self, request):
        paginate = request.GET.get('paginate')
        searchText = request.GET.get('searchText')
        tasks = Task.objects.all().order_by('-id')
        if searchText is not None:
            tasks = tasks.filter(Q(title__icontains=searchText) | Q(project__name__icontains=searchText))
        if paginate:
            limit = request.GET.get('limit', 25)
            page = request.GET.get('page')
            paginator = Paginator(tasks, limit)
            page_obj = paginator.get_page(page)
            tasks = TaskSerializer(page_obj, many=True)
            data = {
                "data": tasks.data,
                "pagination": {
                    "page": int(page),
                    "limit": int(limit),
                    "has_next": bool(page_obj.has_next()),
                    "has_prev": bool(page_obj.has_previous()),
                    "total": int(len(tasks.data))
                }
            }
            return JsonResponse(data, safe=False)
        else:
            tasks = TaskSerializer(Task.objects.all(), many=True)
            return JsonResponse(tasks.data, safe=False)


class TaskCreateView(LoginRequiredMixin, View):

    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        project = request.POST.get('project')
        status = request.POST.get('status')
        assign_to = request.POST.get('assign_to')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        attachments = request.FILES.getlist('attachments')
        if not title or not start_time or not end_time or not project or not status or not assign_to:
            return JsonResponse({'error': 'except description and attachments all fields are required.'}, status=400)
        project = Project.objects.get(pk=project)
        assign_to = User.objects.get(pk=assign_to)
        status = Status.objects.get(pk=status)
        owner = request.user
        instance = Task.objects.create(title=title, description=description, project=project, status=status,
                                       start_time=start_time, end_time=end_time, assigned_to=assign_to, owner=owner)
        for f in attachments:
            instance.attachments.append(default_storage.save(f.name, f))
        instance.save()
        return JsonResponse('success', safe=False)


class DeleteTaskView(LoginRequiredMixin, View):

    def delete(self, request, id):
        task = Task.objects.get(id=id)
        task.delete()
        return JsonResponse('success', safe=False)


class TaskUpdateView(LoginRequiredMixin, View):

    def post(self, request, id):
        title = request.POST.get('title')
        description = request.POST.get('description')
        project = request.POST.get('project')
        status = request.POST.get('status')
        assign_to = request.POST.get('assign_to')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        attachments = request.FILES.getlist('attachments')
        print(title, description, project, status, assign_to, start_time, end_time, attachments, id)
        if not title or not start_time or not end_time or not project or not status or not assign_to:
            return JsonResponse({'error': 'except description and attachments all fields are required.'}, status=400)
        project = Project.objects.get(pk=project)
        assign_to = User.objects.get(pk=assign_to)
        status = Status.objects.get(pk=status)
        import re
        pattern = r"\d{2}/(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)/\d{4}"
        task_dict = {
            "title": title,
            "description": description,
            "project": project,
            "status": status,
            "start_time": start_time,
            "end_time": end_time,
            "assigned_to": assign_to
        }
        if re.match(pattern, start_time):
            task_dict.pop('start_time')
        if re.match(pattern, end_time):
            task_dict.pop('end_time')
        Task.objects.filter(id=id).update(**task_dict)
        if attachments:
            task = Task.objects.get(id=id)
            task.attachments.clear()
            for f in attachments:
                task.attachments.append(default_storage.save(f.name, f))
            task.save()
        return JsonResponse('success', safe=False)
