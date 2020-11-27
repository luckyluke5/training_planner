from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic

from .models import Category

urlpatterns = [
    # path('list/', views.ExerciseListView.as_view(),name="exercise_list"),
    path('create/',
         login_required(generic.CreateView.as_view(model=Category, fields=['name', 'description'])),
         name="category_create"),

    path('<slug:pk>/',
         generic.DetailView.as_view(model=Category),
         name="category_details"),

    path('<int:pk>/update',
         login_required(generic.UpdateView.as_view(model=Category, fields=['name', 'description'])),
         name="category_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view(model=Category)),
         name="category_delete"),
]
