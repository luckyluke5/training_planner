from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic

from .forms import ExerciseQueryForm
from .models import ExerciseQuery

urlpatterns = [
    # path('list/', views.ExerciseListView.as_view(),name="exercise_list"),
    path('create/', generic.CreateView.as_view(model=ExerciseQuery, fields=['name', 'description']),
         name="exercise_query_create"),
    path('<slug:pk>/', generic.DetailView.as_view(model=ExerciseQuery), name="exercise_query_details"),

    path('<int:pk>/update', login_required(generic.UpdateView.as_view(model=ExerciseQuery, form_class=ExerciseQueryForm)),
         name="exercise_query_update"),

    path('<slug:pk>/delete', generic.DeleteView.as_view(model=ExerciseQuery), name="exercise_delete"),
]
