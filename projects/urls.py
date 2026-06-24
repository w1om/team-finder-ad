from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.project_list_view, name="list"),
    path("projects/list/", views.project_list_view, name="list_alias"),
    path("projects/create-project/", views.create_project_view, name="create"),
    path("favorites/", views.favorite_projects_view, name="favorites"),
    path("projects/<int:pk>/", views.project_details_view, name="details"),
    path("projects/<int:pk>/edit/", views.edit_project_view, name="edit"),
    path("projects/favorites/", views.favorite_projects_view, name="favorites"),
    path("projects/<int:pk>/toggle-favorite/", views.toggle_favorite_view, name="toggle_favorite"),
    path("projects/<int:pk>/toggle-participate/", views.participate_view, name="participate"),
    path("projects/<int:pk>/complete/", views.complete_project_view, name="complete"),
]
