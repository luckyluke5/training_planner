#from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from health_tracker.models import Value, Rating


class CreateViewWithUser(LoginRequiredMixin,generic.CreateView):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ListViewWithUser(LoginRequiredMixin,generic.ListView):

    def get_queryset(self):



        return super().get_queryset().filter(user__exact=self.request.user)


class ValueCreateView(PermissionRequiredMixin,CreateViewWithUser):
    model = Value
    permission_required="health_tracker.add_value"



class RatingCreateView(PermissionRequiredMixin,CreateViewWithUser):
    model = Rating
    permission_required = "health_tracker.add_rating"