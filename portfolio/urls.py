from django.shortcuts import redirect
from django.urls import path
from . import views
from .views import (
    ProjectDetailView,
    ProjectListView,
)

app_name = "portfolio"

urlpatterns = [
    path('', lambda request: redirect('portfolio:about')),
    path('about/', views.about, name='about'),
    path("projects/", ProjectListView.as_view(), name="projects_list",),
    path("projects/<slug:slug>/", ProjectDetailView.as_view(), name="project_detail",),
    path("resume/", views.resume, name="resume"),
]
