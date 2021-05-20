import re
from io import StringIO

import pandas
from django import forms
from django.core.files import File
from django.db.models import Model
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.utils import ErrorList

from .models import Category, Range, Exercise, RangeUnit, Value, ValueQuery, ExerciseQuery, RangeQuery, ValueUnit, \
    CategoryOption


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
        exclude = ['exercise', 'unit']


class ValueForm(forms.ModelForm):
    class Meta:
        model = Value
        exclude = ['exercise', 'unit']


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
        fields = ['name','description','number_of_exercises', 'category_queries']

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


class CSVUploadForm(forms.Form):
    file = forms.FileField()




    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

    def is_valid(self):

        file = self.files['file']

        self.pandas_sheet = pandas.read_csv(file, sep=";")
        if "name" in self.pandas_sheet.columns:

            print("name ist da")
        else:
            self.add_error(None, "Die Spalte 'name' ist nicht da")


        if "description" in self.pandas_sheet.columns:
            print("description ist da")
        else:
            self.add_error(None, "Die Spalte 'description' ist nicht da")
            # return False

        values = [value.name for value in ValueUnit.objects.all()]
        ranges = [range.name for range in RangeUnit.objects.all()]
        categories = [range.name for range in Category.objects.all()]

        categories=[]

        category: Category
        for category in Category.objects.all():
            options = category.categoryoption_set.all()
            categories.append("^(" + "|".join([category.name+"_"+option.name for option in options]) + ")$");



        RANGES = "^(" + "|".join(ranges) + ")_(min|max)$"
        CATEGORIES = "^(" + "|".join(categories) + ")$"
        VALUES = "^(" + "|".join(values) + ")$"
        DESCRIPTION = "description"
        NAME = "name"




        for column in self.pandas_sheet.columns:


            # if re.search("^("+ "|".join(ranges) +")_(min|max)$",column):
            #     print(column +" ist eine Range ")
            #
            # if re.search("^("+ "|".join(categories) +")_.*$",column):
            #     print(column +" ist eine Categorie")
            #
            # if re.search("^("+ "|".join(values) +")$", column):
            #     print(column + " ist eine value")

            if re.search("("+"|".join([RANGES, CATEGORIES, VALUES, NAME, DESCRIPTION])+")+", column):
                pass
            else:
                self.add_error(None, "Es gibt keine Range, Value, Kategorie oder Kategorie Option mit dem Namen '"
                               +column+ "'. Fügen sie diese bitte unter setting hinzu")
                print(column)
                # return False

        print("Sucess")



        return super().is_valid()


    def delete_all_exercises(self):
        for exercise in Exercise.objects.all():
            exercise.delete()

    def save_all_exercises_from_csv(self):

        for exercise in self.pandas_sheet.iterrows():


            exercise=exercise[1]

            new_exercise: Exercise = Exercise.objects.create(name=exercise.get('name'),description=exercise.get('description'))

            for value in ValueUnit.objects.all():
                if pandas.notna(exercise.get(value.name)):

                    new_exercise.values.add(value,through_defaults={'value':exercise.get(value.name,pandas.NA)})


            #TODO nicht alle ranges werden angenommen

            #TODO Kategorien noch werden nicht importiert

            #todo Es sollen für jede Unit Value und Range zurerst die blanken verbindungen angelegt werden und dann
            # erst ggf. befüllt werden

            for range in RangeUnit.objects.all():

                dic={}
                if pandas.notna(exercise.get(range.name+"_min")):

                    dic['minimum']=exercise.get(range.name+"_min")

                    #Range(minimum=exercise.get(range.name+"_min",None),maximum=exercise.get(range.name+"_max",None))

                if pandas.notna(exercise.get(range.name + "_max")):
                    dic['maximum'] = exercise.get(range.name + "_max")

                new_exercise.ranges.add(range,through_defaults=dic)


            category_option: CategoryOption
            for category_option in CategoryOption.objects.all():

                if pandas.notna(exercise.get(category_option.category.name+"_"+category_option.name)):
                    if exercise.get(category_option.category.name+"_"+category_option.name):
                        new_exercise.categories.add(category_option)

            print(new_exercise.get_dictionary())

            print(exercise)




