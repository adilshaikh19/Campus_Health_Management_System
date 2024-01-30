from django.urls import path

from . import views
app_name = 'MedicalStore'

urlpatterns = [
    path('', views.index, name = "index"),
    path('search', views.search, name = "search"),
    path('buy/<int:medicine_id>/', views.buy_medicine, name='buy_medicine'),
    path('purchase_history/', views.purchase_history, name='purchase_history'),
]
