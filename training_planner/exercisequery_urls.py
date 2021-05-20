from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic

from . import views
from .forms import ExerciseQueryForm
from .models import ExerciseQuery

urlpatterns = [
    path('list/', views.ExerciseListView.as_view(),name="exercise_query_list"),
    path('create/',
         login_required(generic.CreateView.as_view(model=ExerciseQuery, fields=['name', 'description'])),
         name="exercise_query_create"),
    path('<slug:pk>/',
         generic.DetailView.as_view(model=ExerciseQuery),{'show_results':'not_show'},
         name="exercise_query_details"),

path('<slug:pk>/show_results=<str:show_results>',
         generic.DetailView.as_view(model=ExerciseQuery),
         name="exercise_query_details"),

    #path('<slug:pk>/results',
    #     generic.DetailView.as_view(model=ExerciseQuery),{'show_results':True},
    #     name="exercise_query_details_with_results"),

    path('<int:pk>/update',
         login_required(generic.UpdateView.as_view(model=ExerciseQuery, form_class=ExerciseQueryForm)),
         name="exercise_query_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view(model=ExerciseQuery)),
         name="exercise_query_delete"),
]
