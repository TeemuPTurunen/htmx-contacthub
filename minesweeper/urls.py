from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    # path('open-cell/', views.open_cell, name='open_cell'),
    path('reset/', views.reset, name='reset'),
    path('cell-action/', views.cell_action, name='cell_action'),
    path('stream/', views.stream, name='stream'),
    
]
