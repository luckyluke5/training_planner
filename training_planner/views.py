# Create your views here.


import numpy as np

import pandas as pd

import django.views.generic as generic
from django.http import HttpResponse
from django.urls import reverse_lazy

from .forms import SearchForm, ExerciseQueryForm, CSVUploadForm
from .models import Exercise, Category, RangeUnit, ExerciseQuery, TrainingsQuery


class ExerciseListView(generic.ListView):
    model = Exercise

    def get_queryset(self):
        # query = self.request.GET.get('intensity_maximum')

        search_form = SearchForm(self.request.GET)
        search_form.is_valid()
        cleaned_data = search_form.cleaned_data

        result = Exercise.objects.all()
        if cleaned_data['intensity_maximum']:
            result = result.filter(intensity__lte=cleaned_data['intensity_maximum'])

        if cleaned_data['intensity_minimum']:
            result = result.filter(intensity__gte=cleaned_data['intensity_minimum'])

        for category in Category.objects.all():
            if cleaned_data[category.name]:
                result = result.filter(categories__in=cleaned_data[category.name])

        for requirement in RangeUnit.objects.all():
            if cleaned_data[requirement.name]:
                required = requirement.required_set.filter(minimum_number__lte=cleaned_data[requirement.name]).filter(
                    maximum_number__gte=cleaned_data[requirement.name])
                result = result.filter(required__in=required)

        return result


def exportCSV(request):
    # Create the HttpResponse object with the appropriate CSV header.

    data_sheet = pd.DataFrame()

    for exercise in Exercise.objects.all():
        series = pd.Series(data=exercise.get_dictionary(), name=exercise.id)

        data_sheet = data_sheet.append(series)

    #print(data_sheet)

    # TODO Add Function to export csv File
    # for exercise in Exercise.object.all():
    #
    #
    #
    #
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="exercises.csv"'
    #
    # writer = csv.writer(response)
    # writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    # writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    #
    response.write(data_sheet.to_csv(index=False))

    return response


class CSVUploadFromView(generic.FormView):
    form_class = CSVUploadForm
    template_name = 'training_planner/csv_upload_form.html'
    success_url = reverse_lazy('training_planner:exercise_list')

    def form_valid(self, form):

        #if form.is_valid():
        form.delete_all_exercises()

        form.save_all_exercises_from_csv()



        return super().form_valid(form)




class ExerciseQueryDetailView(generic.DetailView):
    model = ExerciseQuery




class ExerciseQueryUpdateView(generic.UpdateView):
    form_class = ExerciseQueryForm
    model = ExerciseQuery

    # template_name = "training_planner/exercisequery_form.html"


class TrainingsQueryDetailView(generic.DetailView):
    model = TrainingsQuery


class TrainingsQueryUpdateView(generic.UpdateView):
    model = TrainingsQuery
