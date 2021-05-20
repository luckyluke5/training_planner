from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views import generic


from .models import RangeUnit

urlpatterns = [
    path('list/',
         generic.ListView.as_view(model=RangeUnit),
         name="range_unit_list"),

    path('create/',
         login_required(generic.CreateView.as_view(model=RangeUnit, fields=['name', 'description'])),
         name="range_unit_create"),

    path('<slug:pk>/',
         generic.DetailView.as_view(model=RangeUnit),
         name="range_unit_details"),

    path('<int:pk>/update',
         login_required(generic.UpdateView.as_view(model=RangeUnit, fields=['name', 'description'])),
         name="range_unit_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view(model=RangeUnit,success_url=reverse_lazy('training_planner:range_unit_list'))),
         name="range_unit_delete"),
]
