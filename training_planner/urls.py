from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import path, include

# from .views import SearchView
from django.views import generic

from training_planner import views

app_name = 'training_planner'
urlpatterns = [
    path('exercise/', include('training_planner.exercise_urls')),
    path('category/', include('training_planner.category_urls')),
    path('category_option/', include('training_planner.category_option_urls')),
    path('value_unit/', include('training_planner.value_unit_urls')),
    path('range_unit/', include('training_planner.range_unit_urls')),
    path('exercise_query/', include('training_planner.exercisequery_urls')),
    path('trainings_query/', include('training_planner.trainingsquery_urls')),

    path('', generic.TemplateView.as_view(template_name="training_planner/home.html"), name="home"),
    path('settings', generic.TemplateView.as_view(template_name="training_planner/settings.html"), name="settings"),
    path('csv_export', views.exportCSV, name="csv_export"),
    path('csv_import', views.CSVUploadFromView.as_view(), name="csv_import")
    #    path('search/', SearchView.as_view()),
]
