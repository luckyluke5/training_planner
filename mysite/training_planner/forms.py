from django import forms
from django.db.models import Model
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.utils import ErrorList

from .models import Category, Range, Exercise, RangeUnit, Value, ValueQuery, ExerciseQuery, RangeQuery, ValueUnit


class SearchForm(forms.Form):
    complexity_minimum = forms.IntegerField(required=None)
    complexity_maximum = forms.IntegerField(required=None)
    intensity_minimum = forms.IntegerField(required=None)
    intensity_maximum = forms.IntegerField(required=None)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

        for category in Category.objects.all():
            self.fields[category.name] = forms.ModelMultipleChoiceField(queryset=category.categoryoption_set.all(),
                                                                        required=False)
        for requirement in RangeUnit.objects.all():
            self.fields[requirement.name] = forms.IntegerField(required=False)

        self.fields['number_exercises'] = forms.IntegerField(initial=1)

        self.fields['minimum_average_complexity'] = forms.IntegerField(required=False)
        self.fields['maximum_average_complexity'] = forms.IntegerField(required=False)
        self.fields['minimum_average_intensity'] = forms.IntegerField(required=False)
        self.fields['maximum_average_intensity'] = forms.IntegerField(required=False)

        # self.fields['strength_section'] = forms.BooleanField(required=False)
        # self.fields['']


class RangeForm(forms.ModelForm):
    class Meta:
        model = Range
        exclude = ['exercise','unit']


class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        exclude = ['exercise','unit']


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'categories']

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)

        self.range_formset = []

        # for range_query in self.instance.range_set.all():
        #     self.range_formset.append(
        #         RangeForm(data=data, instance=range_query, prefix="range_" + str(range_query.unit.pk)))

        self.value_formset = []
        # for value_query in self.instance.value_set.all():
        #     self.value_formset.append(
        #         ValueForm(data=data, instance=value_query, prefix="value_" + str(value_query.unit.pk)))

        for range_unit in RangeUnit.objects.all():
            range_form_instance, created = self.instance.range_set.get_or_create(unit__exact=range_unit,
                                                                                            defaults={
                                                                                                'unit': range_unit,
                                                                                                'exercise': self.instance})

            self.range_formset.append(
                RangeForm(data=data, instance=range_form_instance, prefix="range_" + str(range_unit.id),
                               label_suffix=" " + range_unit.name))

        for value_unit in ValueUnit.objects.all():
            value_form_instance, created = self.instance.value_set.get_or_create(unit__exact=value_unit,
                                                                                            defaults={
                                                                                                'unit': value_unit,
                                                                                                'exercise': self.instance})
            self.value_formset.append(
                ValueForm(data=data, instance=value_form_instance, prefix="value_" + str(value_unit.id),
                               label_suffix=" " + value_unit.name))

    def save(self, commit=True):
        for form in self.range_formset:

            if form.is_valid():

                form.save()

            else:
                raise forms.ValidationError("Range not valid")

        for form in self.value_formset:

            if form.is_valid():
                form.save()
            else:

                raise forms.ValidationError("Value not valid")

        return super().save(commit)


class RangeQueryForm(forms.ModelForm):
    class Meta:
        model = RangeQuery
        exclude = ['exercise_query', 'unit']


class ValueQueryForm(forms.ModelForm):
    class Meta:
        model = ValueQuery
        exclude = ['exercise_query', 'unit']


class ExerciseQueryForm(forms.ModelForm):
    class Meta:
        model = ExerciseQuery
        fields = ['number_of_exercises', 'category_queries']

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None, renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute, renderer)

        self.range_formset = []
        self.value_formset = []

        for range_unit in RangeUnit.objects.all():
            range_query_form_instance, created = self.instance.rangequery_set.get_or_create(unit__exact=range_unit,
                                                                                            defaults={
                                                                                                'unit': range_unit,
                                                                                                'exercise_query': self.instance})

            self.range_formset.append(
                RangeQueryForm(data=data, instance=range_query_form_instance, prefix="range_" + str(range_unit.id),
                               label_suffix=" " + range_unit.name))

        for value_unit in ValueUnit.objects.all():
            value_query_form_instance, created = self.instance.valuequery_set.get_or_create(unit__exact=value_unit,
                                                                                            defaults={
                                                                                                'unit': value_unit,
                                                                                                'exercise_query': self.instance})
            self.value_formset.append(
                ValueQueryForm(data=data, instance=value_query_form_instance, prefix="value_" + str(value_unit.id),
                               label_suffix=" " + value_unit.name))

    def save(self, commit=True):
        for form in self.range_formset:

            if form.is_valid():

                form.save()

            else:
                raise forms.ValidationError("Range not valid")

        for form in self.value_formset:

            if form.is_valid():
                form.save()
            else:

                raise forms.ValidationError("Value not valid")

        return super().save(commit)
