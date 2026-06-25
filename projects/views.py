from http import HTTPStatus

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.pagination import paginate_queryset

from .constants import PROJECTS_PER_PAGE
from .forms import ProjectForm
from .models import Project, ProjectStatus


def project_list_view(request):
    all_projects = Project.objects.select_related("owner").prefetch_related("participants").all()
    projects = paginate_queryset(request, all_projects, PROJECTS_PER_PAGE)
    
    context = {"projects": projects}
    return render(request, "projects/project_list.html", context)


def project_details_view(request, pk):
    project = get_object_or_404(
        Project.objects.select_related("owner").prefetch_related("participants"), pk=pk
    )
    return render(request, "projects/project-details.html", {"project": project})


@login_required(login_url="users:login")
def create_project_view(request):
    form = ProjectForm(request.POST or None)
    
    if request.method != "POST" or not form.is_valid():
        return render(request, "projects/create-project.html", {"form": form, "is_edit": False})

    project = form.save(commit=False)
    project.owner = request.user
    project.save()
    project.participants.add(request.user)
    return redirect("projects:details", pk=project.id)


@login_required(login_url="users:login")
def edit_project_view(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return redirect("projects:details", pk=project.id)

    form = ProjectForm(request.POST or None, instance=project)
    
    if request.method != "POST" or not form.is_valid():
        return render(request, "projects/create-project.html", {"form": form, "is_edit": True})

    form.save()
    return redirect("projects:details", pk=project.id)


@login_required(login_url="users:login")
def toggle_favorite_view(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid method"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = get_object_or_404(Project, pk=pk)

    if request.user.favorites.filter(pk=project.pk).exists():
        request.user.favorites.remove(project)
        favorited = False
    else:
        request.user.favorites.add(project)
        favorited = True

    return JsonResponse({"status": "ok", "favorited": favorited})


@login_required(login_url="users:login")
def favorite_projects_view(request):
    projects = request.user.favorites.select_related("owner").prefetch_related("participants").all()
    return render(request, "projects/favorite_projects.html", {"projects": projects})


@login_required(login_url="users:login")
def participate_view(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Метод не разрешен"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = get_object_or_404(Project, pk=pk)

    if project.owner == request.user:
        return JsonResponse({"error": "Доступ запрещен"}, status=HTTPStatus.FORBIDDEN)

    if project.status != ProjectStatus.OPEN:
        return JsonResponse({"error": "Проект закрыт"}, status=HTTPStatus.BAD_REQUEST)

    if request.user in project.participants.all():
        project.participants.remove(request.user)
        participates = False
    else:
        project.participants.add(request.user)
        participates = True

    return JsonResponse({"status": "ok", "participant": participates})


@login_required(login_url="users:login")
def complete_project_view(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "Метод не разрешен"}, status=HTTPStatus.METHOD_NOT_ALLOWED)

    project = get_object_or_404(Project, pk=pk)

    if project.owner != request.user:
        return JsonResponse({"error": "Доступ запрещен"}, status=HTTPStatus.FORBIDDEN)

    project.status = ProjectStatus.CLOSED
    project.save(update_fields=["status"])

    return JsonResponse({"status": "ok"})