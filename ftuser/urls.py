from django.urls 				import URLPattern, path, include

from rest_framework				import permissions
from rest_framework.urlpatterns import format_suffix_patterns
from drf_yasg.views 			import get_schema_view
from drf_yasg 					import openapi

from . 							import views

schema_view = get_schema_view(
	openapi.Info(
		title="Cryptolab-project",
		default_version='0.1',
		description="Cryptolab-project API 문서",
		terms_of_service="https://www.google.com/policies/terms/",
		contact=openapi.Contact(email="skdddfhg6@gmail.com"),
		license=openapi.License(name="mit"),
	),
	public=True,
	permission_classes=[permissions.AllowAny],
)


urlpatterns = [
	path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),	
	# # generics
	path('location/test/', views.QrcodeApi.as_view()),
	# path('location/test/<int:pk>/', views.QrcodeDetailApi.as_view()),
	# APIView
	path('location/', views.LocationApi.as_view()),
	path('location/<int:pk>/', views.LocationDetail.as_view()),
	# path('create/', views.TestCreate),
	# path('read/', views.TestRead),
	# path('update/', views.TestUpdate),
	# path('delete/', views.TestDelete),
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])