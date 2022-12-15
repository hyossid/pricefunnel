from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chart', views.line_chart, name='line_chart'),
    path('chartJSON', views.line_chart_json, name='line_chart_json')
]