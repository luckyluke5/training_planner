from django.urls import path
from django.views import generic

from . import views
from .models import TrainingsQuery

urlpatterns = [
    path('list/', generic.ListView.as_view(model=TrainingsQuery),name="trainings_query_list"),
    path('create/', generic.CreateView.as_view(model=TrainingsQuery,fields=['name','description']),name="trainings_query_create"),
    path('<slug:pk>/', generic.DetailView.as_view(model=TrainingsQuery),name="trainings_query_details"),

    path('<slug:pk>/update', generic.UpdateView.as_view(model=TrainingsQuery,fields=['name','description']),name="trainings_query_update"),
    #path('<slug:pk>/delete', views.ExerciseDeleteView.as_view(),name="exercise_delete"),
]