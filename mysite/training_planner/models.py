# import datetime
import itertools
import random
import statistics

from django.db import models

# Create your models here.
from django.db.models import F, Q
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.name.__str__()


class CategoryOption(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)

    def __str__(self):
        return " <-- ".join([self.name.__str__(), self.category.__str__()])


class RangeUnit(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.name.__str__()


class Range(models.Model):
    unit = models.ForeignKey(RangeUnit, on_delete=models.CASCADE)
    minimum = models.PositiveIntegerField(blank=True, null=True)
    maximum = models.PositiveIntegerField(blank=True, null=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)

    def __str__(self):
        return "( " + " , ".join(
            [self.exercise.__str__(), self.minimum.__str__(), self.maximum.__str__(), self.unit.__str__()]) + " )"

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(minimum__lte=F('maximum')), name='Range_min_max'),
            models.UniqueConstraint(fields=['unit', 'exercise'], name='Range: unique_unit_exercise')
        ]


class RangeQuery(models.Model):
    unit = models.ForeignKey(RangeUnit, on_delete=models.CASCADE)
    value = models.PositiveIntegerField(blank=True, null=True)
    exercise_query = models.ForeignKey('ExerciseQuery', on_delete=models.CASCADE)

    def __str__(self):
        return "( " + " , ".join([self.exercise_query.__str__(), self.value.__str__(), self.unit.__str__()]) + " )"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['unit', 'exercise_query'], name='RangeQuery: unique_unit_exercise')
        ]

    # def filterSetWithThisQuery(self, query_set):
    #     return filter(lambda exercise: exercise.fitToRangeQuery(self), query_set)


class ValueUnit(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)

    def __str__(self):
        return self.name.__str__()


class Value(models.Model):
    unit = models.ForeignKey(ValueUnit, on_delete=models.CASCADE)
    value = models.IntegerField(blank=True, null=True)
    exercise = models.ForeignKey('Exercise', on_delete=models.CASCADE)

    def __str__(self):
        return "( " + " , ".join([self.exercise.__str__(), self.value.__str__(), self.unit.__str__()]) + " )"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['unit', 'exercise'], name='Value: unique_unit_exercise')
        ]


class ValueQuery(models.Model):
    unit = models.ForeignKey(ValueUnit, on_delete=models.CASCADE)
    minimum = models.PositiveIntegerField(blank=True, null=True)
    maximum = models.PositiveIntegerField(blank=True, null=True)

    exercise_query = models.ForeignKey('ExerciseQuery', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(minimum__lte=F('maximum')), name='ValueQuery_min_max'),
            models.UniqueConstraint(fields=['unit', 'exercise_query'], name='ValueQuery: unique_unit_exercise_query')
        ]

    def __str__(self):
        return "( " + " , ".join(
            [self.exercise_query.__str__(), self.minimum.__str__(), self.maximum.__str__(), self.unit.__str__()]) + " )"


class TrainingsValueQuery(models.Model):
    SUM = "SUM"
    MEAN = "MEAN"

    FUNCTIONS = [(SUM, 'Sum'), (MEAN, 'Mean')]

    unit = models.ForeignKey(ValueUnit, on_delete=models.CASCADE)
    minimum = models.PositiveIntegerField(blank=True, null=True)
    maximum = models.PositiveIntegerField(blank=True, null=True)

    function = models.TextField(choices=FUNCTIONS)
    trainings_query = models.ForeignKey('TrainingsQuery', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(minimum__lte=F('maximum')), name='TrainingsValueQuery_min_max'),
            models.UniqueConstraint(fields=['unit', 'function', 'trainings_query'],
                                    name='TrainingsValueQuery: unique_unit_exercise_query')
        ]

    def __str__(self):
        return "( " + " , ".join(
            [self.trainings_query.__str__(), self.minimum.__str__(), self.maximum.__str__(), self.function.__str__(),
             self.unit.__str__()]) + " )"

    # def filterSetWithThisQuery(self, query_set):
    #     return filter(lambda exercise: exercise.fitToValueQuery(self), query_set)
    def accept_exercise_sequence(self, sequence):
        values = []
        for exercise in sequence:
            try:
                values.append(exercise.value_set.get(unit__exact=self.unit).value)
            except Value.DoesNotExist:
                pass


        if values:
            if self.function == TrainingsValueQuery.MEAN:
                result = statistics.mean(values)

            if self.function == TrainingsValueQuery.SUM:
                result = sum(values)

            return self.minimum <= result and self.maximum >= result
        else:
            return True


class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)
    values = models.ManyToManyField(ValueUnit, through=Value, blank=True)
    ranges = models.ManyToManyField(RangeUnit, through=Range, blank=True)
    categories = models.ManyToManyField(CategoryOption, blank=True)

    def __str__(self):
        return self.name.__str__()

    def get_absolute_url(self):
        return reverse('exercise_details', args=[self.pk])

    def fitToCategories(self, categories):
        for category in Category.objects.all():
            category_options = self.categories.filter(category__exact=category)
            category_queries = categories.filter(category__exact=category)
            cat = False
            if category_queries:
                for category_option in category_options:
                    if category_option in category_queries:
                        cat = True
                        break

                if not cat:
                    return False

        return True

    def fitToRangeQuery(self, rangeQ: RangeQuery):

        if self.range_set.filter(unit__exact=rangeQ.unit).exists():
            range = self.range_set.get(unit__exact=rangeQ.unit)

            if rangeQ.value:
                if range.maximum and rangeQ.value > range.maximum:
                    return False
                if range.minimum and rangeQ.value < range.minimum:
                    return False

                return True


            else:
                return True
        else:
            return True

    def fitToValueQuery(self, valueQ: ValueQuery):
        if self.value_set.filter(unit__exact=valueQ.unit).exists():
            value=self.value_set.get(unit__exact=valueQ.unit)


            if value.value:
                if valueQ.minimum and valueQ.minimum>value.value:
                    return False
                if valueQ.maximum and valueQ.maximum<value.value:
                    return False

                return True

            else:
                return True

            # if valueQ.minimum and valueQ.maximum:
            #
            #     return self.value_set.filter(unit__exact=valueQ.unit, value__gte=valueQ.minimum,
            #                                  value__lte=valueQ.maximum).exists()
            #
            # elif valueQ.maximum:
            #     return self.value_set.filter(unit__exact=valueQ.unit, value__lte=valueQ.maximum).exists()
            #
            # elif valueQ.minimum:
            #     return self.value_set.filter(unit__exact=valueQ.unit, value__gte=valueQ.minimum).exists()
            #
            # else:
            #     raise ValueError("ValueQuery: Both are None")

        else:
            return True


class ExerciseQuery(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)
    value_queries = models.ManyToManyField(ValueUnit, through=ValueQuery, blank=True)
    range_queries = models.ManyToManyField(RangeUnit, through=RangeQuery, blank=True)
    category_queries = models.ManyToManyField(CategoryOption, blank=True)
    number_of_exercises = models.PositiveIntegerField(default=1)

    def get_absolute_url(self):
        return reverse('exercise_query_details', args=[self.pk])

    def query_set(self, result=Exercise.objects.all()):

        result = list(filter(lambda exercise: exercise.fitToCategories(self.category_queries.all()), result))

        for rangequery in self.rangequery_set.all():
            # result = rangequery.filterSetWithThisQuery(result)
            result = list(filter(lambda exercise: exercise.fitToRangeQuery(rangequery), result))



        for valuequery in self.valuequery_set.all():
            # result = valuequery.filterSetWithThisQuery(result)
            result = list(filter(lambda exercise: exercise.fitToValueQuery(valuequery), result))

        return result

    def __str__(self):
        return self.name.__str__()


class ExerciseQueryPlacement(models.Model):
    exercise_query = models.ForeignKey(ExerciseQuery, on_delete=models.CASCADE)
    placement = models.PositiveIntegerField()
    trainings_query = models.ForeignKey('TrainingsQuery', on_delete=models.CASCADE)

    def __str__(self):
        return "( " + " , ".join(
            [self.trainings_query.__str__(), self.placement.__str__(), self.exercise_query.__str__()]) + " )"


class TrainingsQuery(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, blank=True)
    generall_exercise_query = models.ForeignKey(ExerciseQuery, related_name='+', on_delete=models.CASCADE)
    exercise_queries = models.ManyToManyField(ExerciseQuery, related_name='+', through=ExerciseQueryPlacement,
                                              blank=True)

    value_queries = models.ManyToManyField(ValueUnit, related_name='+', through=TrainingsValueQuery, blank=True)

    def accept_exercise_sequence(self, sequence):
        value_query: TrainingsValueQuery
        for value_query in self.trainingsvaluequery_set.all():
            if not value_query.accept_exercise_sequence(sequence):
                return False

        return True

    def __str__(self):
        return self.name.__str__()

    def get_absolute_url(self):
        return reverse('trainings_query_details', args=[self.pk])

    def query_set(self):
        possible_exercises = [
            list(exerciseQueryPlacement.exercise_query.query_set(self.generall_exercise_query.query_set()))
            for exerciseQueryPlacement in self.exercisequeryplacement_set.order_by('placement')]

        choices = [random.choice(list) for list in possible_exercises]

        product = itertools.product(*possible_exercises)

        # print(product)
        data = []
        for sequence in product:
            data.append((self.accept_exercise_sequence(sequence), sequence))

        # print(self.accept_exercise_sequence(choices),choices)

        data = {'possible_choices': possible_exercises, 'choices': choices, 'data': data}
        return data
