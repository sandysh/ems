from django.views import View
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from helpers.general import make_pagination
from django.contrib import messages
from project.models import Project, Status
from project.serializers import ProjectSerializer
from django.core.paginator import Paginator
import json
from logs.utils import log_action


class IndexView(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'project/index.html')


class AllProjectsView(LoginRequiredMixin, View):

    def get(self, request):
        paginate = request.GET.get('paginate')
        searchText = request.GET.get('searchText')
        projects = Project.objects.all().order_by('-id')
        if searchText is not None:
            projects = projects.filter(name__icontains=searchText)
        if paginate:
            limit = request.GET.get('limit', 25)
            page = request.GET.get('page')
            paginator = Paginator(projects, limit)
            page_obj = paginator.get_page(page)
            projects = ProjectSerializer(page_obj, many=True)
            data = {
                "data": projects.data,
                "pagination": {
                    "page": int(page),
                    "limit": int(limit),
                    "has_next": bool(page_obj.has_next()),
                    "has_prev": bool(page_obj.has_previous()),
                    "total": int(len(projects.data))
                }
            }
            return JsonResponse(data, safe=False)
        else:
            projects = ProjectSerializer(Project.objects.all(), many=True)
            return JsonResponse(projects.data, safe=False)


class ProjectCreateView(LoginRequiredMixin, View):

    def post(self, request):
        project = json.loads(request.body)
        if not project.get('name') or not project.get('description'):
            return JsonResponse({'error': 'Project name, description and status are required.'}, status=400)
        status = project.pop('status')
        project = Project.objects.create(**project)
        status = Status.objects.create(project=project, name=status)
        project.status = status
        project.save()

        # Log project creation
        log_action(
            action="Project Created",
            model="Project",
            action_by=request.user,
            action_to=None,
            old={},
            new={
                "project_id": project.id,
                "name": project.name,
                "description": project.description,
                "status": status.name
            }
        )
        return JsonResponse('success', safe=False)


class AddProjectStatusView(LoginRequiredMixin, View):

    def post(self, request, id):
        status = json.loads(request.body)
        if not status.get('name'):
            return JsonResponse({'error': 'Status name is required.'}, status=400)
        project_obj = Project.objects.get(id=id)
        status_obj = Status.objects.create(project=project_obj, name=status['name'])
        # Log status addition
        log_action(
            action="Project Status Added",
            model="Project",
            action_by=request.user,
            action_to=None,
            old={},
            new={
                "project_id": project_obj.id,
                "status_id": status_obj.id,
                "status_name": status_obj.name
            }
        )
        return JsonResponse('success', safe=False)


class UpdateProjectView(LoginRequiredMixin, View):

    def put(self, request, id):
        project = json.loads(request.body)
        if not project.get('name') or not project.get('description') or not project.get('status'):
            return JsonResponse({'error': 'Project name, description and status are required.'}, status=400)
        status = project.get('status').get('id') if isinstance(project.get('status'), dict) else project.get('status')
        data = {
            'name': project.get('name'),
            'description': project.get('description'),
            'status': Status.objects.get(id=status),
        }
        old_project = Project.objects.get(id=id)
        Project.objects.filter(id=id).update(**data)
        # Log project update
        log_action(
            action="Project Updated",
            model="Project",
            action_by=request.user,
            action_to=None,
            old={
                "project_id": old_project.id,
                "name": old_project.name,
                "description": old_project.description,
                "status": old_project.status.name if old_project.status else None
            },
            new={
                "project_id": id,
                "name": data['name'],
                "description": data['description'],
                "status": data['status'].name
            }
        )
        return JsonResponse('success', safe=False)


class ProjectRelatedStatusView(LoginRequiredMixin, View):

    def get(self, request, id):
        status = Status.objects.filter(project=id)
        data = [{'id': status.id, 'name': status.name} for status in status]
        data = json.dumps(data)
        return JsonResponse(data, safe=False)


class DeleteProjectView(LoginRequiredMixin, View):

    def delete(self, request, id):
        project = Project.objects.get(id=id)
        log_action(
            action="Project Deleted",
            model="Project",
            action_by=request.user,
            action_to=None,
            old={
                "project_id": project.id,
                "name": project.name,
                "description": project.description,
                "status": project.status.name if project.status else None
            },
            new={}
        )
        project.delete()
        return JsonResponse('success', safe=False)


class ProjectFetchView(LoginRequiredMixin, View):

    def get(self, request):
        projects = Project.objects.all()
        data = [{'id': project.id, 'name': project.name} for project in projects]
        return JsonResponse(data, safe=False)

