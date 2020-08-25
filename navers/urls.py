from django.urls import path
from . import views

urlpatterns = [
	path('', views.NaverView.as_view(), name='index'),
	path('<int:naver_id>/', views.NaverView.as_view(), name='view'),
	path('add-projeto/', views.addProjeto, name='addProjeto')
]