from django.urls import URLPattern, path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
	# generics
	path('location/test/', views.QrcodeApi.as_view()),
	path('location/test/<int:pk>/', views.QrcodeDetailApi.as_view()),
	# APIView
	path('location/', views.LocationApi.as_view()),
	path('location/<int:pk>/', views.LocationDetail.as_view()),
	# path('create/', views.TestCreate),
	# path('read/', views.TestRead),
	# path('update/', views.TestUpdate),
	# path('delete/', views.TestDelete),
]

urlpatterns = format_suffix_patterns(urlpatterns)