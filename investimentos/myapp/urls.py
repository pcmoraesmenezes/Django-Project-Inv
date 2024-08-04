from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('data/', views.update_data, name='data_view'),
    path('inv/', views.view_inv, name='view_inv'),
    path('get_sheet/', views.get_sheet, name='get_sheet'),
    path('accounts/', include('django.contrib.auth.urls')),
]
