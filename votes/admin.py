from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Teams)
admin.site.register(models.Fixture)

class SearchPlayerVotes(admin.ModelAdmin):
    search_fields = ['round__round', 'round__season']
    list_display =['round', 'voter' , 'three_votes','two_votes','one_vote']

admin.site.register(models.PlayerVotes,SearchPlayerVotes)
