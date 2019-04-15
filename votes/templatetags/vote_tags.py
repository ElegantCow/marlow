from django import template
from django.utils import timezone
from datetime import timedelta
register = template.Library()

@register.filter
def is_current(game_time, now=timezone.now()):
    if game_time <= now <= game_time + timedelta(days=6):
        return 'Something'
    else:
        return None

@register.filter
def is_future(game_time, now=timezone.now()):
    if game_time >= now:
        return 'Something'
    else:
        return None
