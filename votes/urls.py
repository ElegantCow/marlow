from django.urls import path, include
from . import views

app_name = 'votes'

urlpatterns = [
    path('', views.votes,name='votepage'),
    path('castvote/<int:pk>/', views.cast_vote, name="cast-vote"),
    path('weekly_results/', views.weekly_results, name='weekly'),
    path('yet_to_vote/', views.not_voted, name='yet_to_vote'),
    path('cumulative_results/', views.cumulative_results, name='total'),

]
