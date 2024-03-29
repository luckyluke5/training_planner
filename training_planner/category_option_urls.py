from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views import generic


from .models import CategoryOption

urlpatterns = [
    # path('list/', views.ExerciseListView.as_view(),name="exercise_list"),
    path('create/',
         login_required(generic.CreateView.as_view(model=CategoryOption, fields=['name', 'description', 'category'])),
         name="category_option_create"),
    path('<slug:pk>/',
         generic.DetailView.as_view(model=CategoryOption),
         name="category_option_details"),

    path('<int:pk>/update',
         login_required(generic.UpdateView.as_view(model=CategoryOption, fields=['name', 'description', 'category'])),
         name="category_option_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view(model=CategoryOption)),
         name="category_option_delete"),
]
