from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views import generic


from .models import ValueUnit

urlpatterns = [
    path('list/'
         , generic.ListView.as_view(model=ValueUnit),
         name="value_unit_list"),

    path('create/',
         login_required(generic.CreateView.as_view(model=ValueUnit, fields=['name', 'description'])),
         name="value_unit_create"),

    path('<slug:pk>/',
         generic.DetailView.as_view(model=ValueUnit),
         name="value_unit_details"),

    path('<int:pk>/update',
         login_required(generic.UpdateView.as_view(model=ValueUnit, fields=['name', 'description', 'category'])),
         name="value_unit_update"),

    path('<slug:pk>/delete',
         login_required(generic.DeleteView.as_view(model=ValueUnit,success_url=reverse_lazy('value_unit_list'))),
         name="value_unit_delete"),
]
