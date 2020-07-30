from django.urls import path
from chart.views import *

app_name = 'chart'

urlpatterns = [
    path('', ChartView.as_view(), name='index'),
]
