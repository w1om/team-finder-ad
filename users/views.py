from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from team_finder.pagination import paginate_queryset

from .constants import (
    FILTER_FAVORITE_OWNERS,
    FILTER_MY_PROJECTS_INTERESTED,
    FILTER_MY_PROJECTS_PARTICIPANTS,
    FILTER_PARTICIPATING_OWNERS,
    USERS_PER_PAGE,
)
from .forms import CustomPasswordChangeForm, LoginForm, ProfileEditForm, RegisterForm
from .services import generate_default_avatar

User = get_user_model()


def register_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = RegisterForm(request.POST or None)

    if request.method != "POST" or not form.is_valid():
        return render(request, "users/register.html", {"form": form})

    user = form.save()
    generate_default_avatar(user)
    login(request, user)
    return redirect("projects:list")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("projects:list")

    form = LoginForm(request.POST or None)
    
    if request.method != "POST" or not form.is_valid():
        return render(request, "users/login.html", {"form": form})

    email = form.cleaned_data.get("email")
    password = form.cleaned_data.get("password")

    user = authenticate(request, username=email, password=password)

    if user is not None:
        login(request, user)
        return redirect("projects:list")
    else:
        form.add_error(None, "Неверный email или пароль")
        return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("users:login")


def participants_view(request):
    active_filter = request.GET.get("filter")
    queryset = User.objects.all()

    if active_filter and request.user.is_authenticated:
        if active_filter == FILTER_FAVORITE_OWNERS:
            queryset = User.objects.filter(owned_projects__in=request.user.favorites.all())
        elif active_filter == FILTER_PARTICIPATING_OWNERS:
            queryset = User.objects.filter(owned_projects__participants=request.user)
        elif active_filter == FILTER_MY_PROJECTS_INTERESTED:
            queryset = User.objects.filter(favorites__owner=request.user)
        elif active_filter == FILTER_MY_PROJECTS_PARTICIPANTS:
            queryset = User.objects.filter(participated_projects__owner=request.user)

    participants_list = queryset.distinct()
    participants = paginate_queryset(request, participants_list, USERS_PER_PAGE)

    context = {
        "participants": participants,
        "active_filter": active_filter
    }
    return render(request, "users/participants.html", context)


def user_details_view(request, pk):
    queryset = User.objects.prefetch_related(
        "owned_projects__owner",
        "participated_projects__owner"
    )
    user_instance = get_object_or_404(queryset, pk=pk)
    
    context = {"user": user_instance}
    return render(request, "users/user-details.html", context)


@login_required(login_url="users:login")
def edit_profile_view(request):
    form = ProfileEditForm(request.POST or None, request.FILES or None, instance=request.user)
    
    if request.method != "POST" or not form.is_valid():
        return render(request, "users/edit_profile.html", {"form": form})

    form.save()
    return redirect("users:user_details", pk=request.user.id)


@login_required(login_url="users:login")
def change_password_view(request):
    form = CustomPasswordChangeForm(user=request.user, data=request.POST or None)
    
    if request.method != "POST" or not form.is_valid():
        return render(request, "users/change_password.html", {"form": form})

    request.user.set_password(form.cleaned_data["new_password1"])
    request.user.save()

    update_session_auth_hash(request, request.user)
    return redirect("users:user_details", pk=request.user.pk)