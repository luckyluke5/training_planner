from django.db import transaction
from django.db.models import Q
from django.forms import modelformset_factory, inlineformset_factory, ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
import django.views.generic as generic
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from .forms import SearchForm, ExerciseForm, ExerciseQueryForm

from .models import Exercise, Category, Value, RangeUnit, Range, ExerciseQuery, TrainingsQuery


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


# class ExerciseDetailView(generic.DetailView):
#     model = Exercise


# class MultipleFormsDemoView(generic.detail.SingleObjectMixin,
#                              generic.edit.FormMixin):
#
#     def get_context_data(self, **kwargs):
#         return super().get_context_data(**kwargs)
#
#     def form_valid(self, form):
#         return super().form_valid(form)
# class ExerciseUpdateView(generic.UpdateView):
#     form_class = ExerciseForm
#     model = Exercise


# class ExerciseUpdateView(generic.detail.SingleObjectMixin,
#                          generic.base.ContextMixin,
#                          generic.edit.ProcessFormView,
#                          generic.base.TemplateResponseMixin):
#     template_name = "training_planner/exercise_form.html"
#     model = Exercise
#
#     def setup(self, request, *args, **kwargs):
#
#         super().setup(request, *args, **kwargs)
#         self.object = self.get_object()
#         # self.exercise_form =
#         # self.range_form =
#         # self.value_form = ValueInlineFormSet(instance=self.object)
#
#     def get_context_data(self, **kwargs):
#         print('CONTEXT')
#
#         data = super().get_context_data(**kwargs)
#
#         self.exercise_form = ExerciseForm(instance=self.object)
#         self.range_form = RangeInlineFormSet(instance=self.object)
#         self.value_form = ValueInlineFormSet(instance=self.object)
#
#         data['form'] = self.exercise_form
#         data['range_formset'] = self.range_form
#         data['value_formset'] = self.value_form
#
#         return data
#
#     def post(self, request, *args, **kwargs):
#         print('POST')
#         # result =
#         # self.exercise_form()
#         self.exercise_form = ExerciseForm(request.POST, instance=self.object)
#         self.range_form = RangeInlineFormSet(request.POST, instance=self.object)
#         self.value_form = ValueInlineFormSet(request.POST, instance=self.object)
#
#         rederect = True
#
#         if self.exercise_form.is_valid():
#             try:
#                 self.exercise_form.save()
#             except Exception as err:
#                 self.exercise_form.add_error(None, err.__str__())
#                 rederect = False
#         else:
#             print('exercise form: error')
#
#             raise ValueError('exercise form: error')
#
#         if self.range_form.is_valid():
#             try:
#                 self.range_form.save()
#             except Exception as err:
#                 self.exercise_form.add_error(None, err.__str__())
#                 rederect = False
#
#         else:
#             print('Range Form: Error')
#             raise ValueError('Range Form: Error')
#
#         if self.value_form.is_valid():
#             try:
#                 self.value_form.save()
#             except Exception as err:
#                 self.exercise_form.add_error(None, err.__str__())
#                 rederect = False
#         else:
#             print('Value Form: Error')
#             raise ValueError('Value Form: Error')
#         if rederect:
#             return HttpResponseRedirect(self.object.get_absolute_url())
#         else:
#             return render(request, self.template_name, self.get_context_data())


# class ExerciseCreateView(generic.CreateView):
#     model = Exercise
#     fields = ['name', 'description']


# class ExerciseDeleteView(generic.DeleteView):
#     model = Exercise
#     success_url = reverse_lazy('exercise_list')
#
#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         data['query']=self.object.query_set()
#         return


# class SearchView(FormView):
#     template_name = 'training_planner/search_form.html'
#     form_class = SearchForm
#     success_url = reverse_lazy('exercise_list')


class ExerciseQueryDetailView(generic.DetailView):
    model = ExerciseQuery


class ExerciseQueryUpdateView(generic.UpdateView):
    form_class = ExerciseQueryForm
    model = ExerciseQuery

    #template_name = "training_planner/exercisequery_form.html"


class TrainingsQueryDetailView(generic.DetailView):
    model = TrainingsQuery


class TrainingsQueryUpdateView(generic.UpdateView):
    model = TrainingsQuery
