from django.urls import path
from . import views

urlpatterns = [
	path('', views.ProjetoView.as_view(), name='index'),
	path('<int:projeto_id>/', views.ProjetoView.as_view(), name='view'),
]