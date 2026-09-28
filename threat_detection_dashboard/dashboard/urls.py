from django.urls import path
from . import views

urlpatterns = [
    path("save-threat/", views.save_threat, name="save_threat"),
    path("stats/", views.threat_stats, name="threat_stats"),
    path("dashboard/", views.dashboard, name="dashboard"),
]