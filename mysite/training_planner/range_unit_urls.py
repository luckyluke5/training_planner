from django.urls import path
from django.views import generic


from .models import RangeUnit

urlpatterns = [
    # path('list/', views.ExerciseListView.as_view(),name="exercise_list"),
    path('create/', generic.CreateView.as_view(model=RangeUnit, fields=['name', 'description']),
         name="range_unit_create"),
    path('<slug:pk>/', generic.DetailView.as_view(model=RangeUnit), name="range_unit_details"),

    path('<int:pk>/update',
         generic.UpdateView.as_view(model=RangeUnit, fields=['name', 'description', 'category']),
         name="range_unit_update"),

    path('<slug:pk>/delete', generic.DeleteView.as_view(model=RangeUnit), name="range_unit_delete"),
]
