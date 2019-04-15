# Generated by Django 2.1.5 on 2019-04-15 02:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('votes', '0002_auto_20190412_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('votes', models.PositiveIntegerField(default=0)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('round', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='votes.Fixture')),
            ],
        ),
    ]