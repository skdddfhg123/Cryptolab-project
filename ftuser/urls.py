from django.urls import URLPattern, path, include
from . import views

urlpatterns = [
	path('create/', views.TestCreate),
	path('read/', views.TestRead),
	path('update/', views.TestUpdate),
	path('delete/', views.TestDelete),
]