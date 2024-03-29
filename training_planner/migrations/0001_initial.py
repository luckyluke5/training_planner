# Generated by Django 3.1.2 on 2020-11-17 13:57

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='CategoryOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.category')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('categories', models.ManyToManyField(blank=True, to='training_planner.CategoryOption')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_exercises', models.PositiveIntegerField(default=1)),
                ('category_queries', models.ManyToManyField(blank=True, to='training_planner.CategoryOption')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseQueryPlacement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placement', models.PositiveIntegerField()),
                ('exercise_query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.exercisequery')),
            ],
        ),
        migrations.CreateModel(
            name='RangeUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='ValueUnit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
            ],
        ),
        migrations.CreateModel(
            name='ValueQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum', models.PositiveIntegerField()),
                ('maximum', models.PositiveIntegerField(blank=True, null=True)),
                ('exercise_query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.exercisequery')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.valueunit')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.exercise')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.valueunit')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingsQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('exercise_queries', models.ManyToManyField(blank=True, related_name='_trainingsquery_exercise_queries_+', through='training_planner.ExerciseQueryPlacement', to='training_planner.ExerciseQuery')),
                ('generall_exercise_query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='training_planner.exercisequery')),
            ],
        ),
        migrations.CreateModel(
            name='RangeQuery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField()),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.exercisequery')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.rangeunit')),
            ],
        ),
        migrations.CreateModel(
            name='Range',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minimum', models.PositiveIntegerField()),
                ('maximum', models.PositiveIntegerField(blank=True, null=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.exercise')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.rangeunit')),
            ],
        ),
        migrations.AddField(
            model_name='exercisequeryplacement',
            name='trainings_query',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training_planner.trainingsquery'),
        ),
        migrations.AddField(
            model_name='exercisequery',
            name='range_queries',
            field=models.ManyToManyField(blank=True, through='training_planner.RangeQuery', to='training_planner.RangeUnit'),
        ),
        migrations.AddField(
            model_name='exercisequery',
            name='value_queries',
            field=models.ManyToManyField(blank=True, through='training_planner.ValueQuery', to='training_planner.ValueUnit'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='ranges',
            field=models.ManyToManyField(blank=True, through='training_planner.Range', to='training_planner.RangeUnit'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='values',
            field=models.ManyToManyField(blank=True, through='training_planner.Value', to='training_planner.ValueUnit'),
        ),
        migrations.AddConstraint(
            model_name='range',
            constraint=models.CheckConstraint(check=models.Q(minimum__lte=django.db.models.expressions.F('maximum')), name='min_max'),
        ),
        migrations.AddConstraint(
            model_name='range',
            constraint=models.UniqueConstraint(fields=('unit', 'exercise'), name='unique_unit_exercise'),
        ),
    ]
