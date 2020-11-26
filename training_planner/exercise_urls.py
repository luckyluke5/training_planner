from django.urls import path, reverse_lazy
from django.views import generic

from . import views
from .forms import ExerciseForm
from .models import Exercise

urlpatterns = [
    path('list/', views.ExerciseListView.as_view(), name="exercise_list"),
    path('create/', generic.CreateView.as_view(model=Exercise, fields=['name', 'description']), name="exercise_create"),

    path('<slug:pk>/', generic.DetailView.as_view(model=Exercise), name="exercise_details"),

    path('<slug:pk>/update', generic.UpdateView.as_view(model=Exercise, form_class=ExerciseForm),
         name="exercise_update"),
    path('<slug:pk>/delete', generic.DeleteView.as_view(model=Exercise, success_url=reverse_lazy('exercise_list')),
         name="exercise_delete"),
]
