from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.views import LoginView
from django.urls import path, include

# from .views import SearchView
from django.views import generic

from health_tracker.forms import ValueForm
from health_tracker.models import Date, Value, Rating
from health_tracker.views import ValueCreateView, RatingCreateView, ListViewWithUser


app_name = 'health_tracker'
urlpatterns = [
    path('value/create/',
         ValueCreateView.as_view(fields=['value','date']),
         name="value_create"),

    path('rating/create/',
        RatingCreateView.as_view(fields=['rating','date']),
         name="rating_create"),

    path('date/create/',
        generic.CreateView.as_view(model=Date,fields=['option','date']),
         name="date_create"),

    path('date/detail/<slug:pk>/',
        generic.DetailView.as_view(model=Date),
         name="date_detail"),

    path('value/detail/<slug:pk>/',
        generic.DetailView.as_view(model=Value),
         name="value_detail"),

    path('rating/detail/<slug:pk>/',
        generic.DetailView.as_view(model=Rating),
         name="rating_detail"),

    path('date/list/',
         generic.ListView.as_view(model=Date),
         name="date_list"),

    path('value/list/',
         ListViewWithUser.as_view(model=Value),
         name="value_list"),

    path('rating/list/',
         ListViewWithUser.as_view(model=Rating),
         name="rating_list"),


    path('', generic.TemplateView.as_view(template_name="health_tracker/base.html"),name="home"),


    #path('enterValue',,name="")
]
