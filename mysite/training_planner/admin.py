from django.contrib import admin

# Register your models here.
from .models import Exercise,ExerciseQuery, Category, Range, RangeUnit, CategoryOption, ValueUnit, Value,RangeQuery, ValueQuery,ExerciseQueryPlacement,TrainingsQuery,TrainingsValueQuery

admin.site.register(Exercise)
admin.site.register(CategoryOption)
admin.site.register(Category)
admin.site.register(Range)
admin.site.register(RangeUnit)
admin.site.register(Value)
admin.site.register(ValueUnit)

admin.site.register(RangeQuery)

admin.site.register(ValueQuery)

admin.site.register(ExerciseQuery)
admin.site.register(ExerciseQueryPlacement)
admin.site.register(TrainingsQuery)
admin.site.register(TrainingsValueQuery)

