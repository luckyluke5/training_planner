from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic

from . import views
from .models import TrainingsQuery

urlpatterns = [
    path('list/',
         generic.ListView.as_view(model=TrainingsQuery),
         name="trainings_query_list"),

    path('create/',
         login_required(generic.CreateView.as_view(model=TrainingsQuery, fields=['name', 'description'])),
         name="trainings_query_create"),

    path('<slug:pk>/',
         generic.DetailView.as_view(model=TrainingsQuery),
         name="trainings_query_details"),

    path('<slug:pk>/update',
         login_required(generic.UpdateView.as_view(model=TrainingsQuery, fields=['name', 'description'])),
         name="trainings_query_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view()),
         name="trainings_query_delete"),
]
