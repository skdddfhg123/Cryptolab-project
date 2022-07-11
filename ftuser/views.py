from doctest import Example
from locale 					import atoi
from django.shortcuts 			import render
from django.http 				import HttpResponse, Http404

from random 					import choice, random
from rest_framework.response	import Response
from rest_framework.views 		import APIView
from rest_framework 			import status, generics, mixins, permissions
from .models 					import UserLocation, Ftuser
from .serializers				import UserLocationSerializer
from drf_yasg.utils 			import swagger_auto_schema, status
from drf_yasg 					import openapi

QrCodeSchema = openapi.Schema(
	'qr-code',
	type=openapi.TYPE_OBJECT,
	properties={
		'id': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_INT32),
		'qrcode': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_UUID),
		'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
		'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_FLOAT),
		'isval': openapi.Schema(type=openapi.TYPE_BOOLEAN),
		'register_date': openapi.Schema(type=openapi.FORMAT_DATETIME),
		'userid': openapi.Schema(type=openapi.TYPE_STRING),
	}
)

class QrcodeApi(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
	queryset = UserLocation.objects.all()
	serializer_class = UserLocationSerializer

	@swagger_auto_schema(
		operation_id='Get All QR code',
		operation_summary='전체 QR code 가져오기',
		tags=['전체 QR code 가져오기'],
		responses={status.HTTP_200_OK: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'data': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=QrCodeSchema
				)
			}
		)}
	)
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	@swagger_auto_schema(
		operation_id='QR code 랜덤 생성',
		operation_summary='랜덤으로 QR code 하나 생성하기',
		tags=['랜덤으로 QR code 하나 생성하기'],
		responses={status.HTTP_200_OK: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'data': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=QrCodeSchema
				)
			}
		)}
	)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

# class QrcodeDetailApi(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
# 	queryset = UserLocation.objects.all()
# 	serializer_class = UserLocationSerializer

# 	def get(self, request, *args, **kwargs):
# 		return self.retrieve(request, *args, **kwargs)

# 	def put(self, request, *args, **kwargs):
# 		return self.update(request, *args, **kwargs)

# 	def delete(self, request, *args, **kwargs):
# 		return self.destroy(request, *args, **kwargs)

class LocationApi(APIView):
	@swagger_auto_schema(
		operation_id='Get all QR code',
		operation_summary='전체 QR code 가져오기',
		tags=['전체 QR code 가져오기'],
		responses={status.HTTP_200_OK: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'data': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=QrCodeSchema
				)
			}
		)}
	)
	def get(self, request, format=None):
		Qrcode = UserLocation.objects.all()
		serializer = UserLocationSerializer(Qrcode, many=True)
		return Response(serializer.data)

	@swagger_auto_schema(
		operation_id='Create QR code',
		operation_summary='랜덤으로 QR code 생성하기',
		tags=['랜덤으로 QR code 생성하기'],
		responses={
			status.HTTP_201_CREATED: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'data': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=QrCodeSchema
				)
			}
		),
			status.HTTP_409_CONFLICT: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'error': openapi.Schema(
					type=openapi.TYPE_STRING,
					example='DB is empty'
				)
			}
		)}
	)
	def post(self, request, format=None):
		lat = ( random() - 0.5) * 90
		lon = ( random() - 0.5) * 180
		user = choice(Ftuser.objects.all())
		if len(UserLocation.objects.all()) == 0:
			index = 1
		else:
			for users in UserLocation.objects.all():
				tmp = users.id
			index = atoi(tmp) + 1
		Qrcode = UserLocation(id=index, userid=user,latitude=lat, longitude=lon)
		Qrcode.save()
		serializer = UserLocationSerializer(Qrcode)
		return (Response(serializer.data, status=status.HTTP_201_CREATED))

	@swagger_auto_schema(
		operation_id='Delete All QR code',
		operation_summary='QR code 전체 삭제',
		tags=['QR code 전체 삭제'],
		responses={
			status.HTTP_204_NO_CONTENT: openapi.Schema(
			type=openapi.TYPE_OBJECT
		),
			status.HTTP_409_CONFLICT: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'error': openapi.Schema(
					type=openapi.TYPE_STRING,
					example='DB is empty'
				)
			}
		)}
	)
	def delete(self, request, format=None):
		Qrcode = UserLocation.objects.all()
		# serializer = UserLocationSerializer(Qrcode)
		if len(Qrcode) == 0:
			return (Response(status=status.HTTP_409_CONFLICT))
		Qrcode.delete()
		return HttpResponse(status=204)

class LocationDetail(APIView):
	def get_object(self, pk):
		try:
			return UserLocation.objects.get(pk=pk)
		except UserLocation.DoesNotExist:
			raise Http404

	# @swagger_auto_schema(
	# 	operation_id='Get QR code',
	# 	operation_summary='QR code 하나 가져오기',
	# 	tags=['QR code 하나 가져오기'],
	# 	responses={status.HTTP_200_OK: openapi.Schema(
	# 		type=openapi.TYPE_OBJECT,
	# 		properties={
	# 			'data': openapi.Schema(
	# 				type=openapi.TYPE_ARRAY,
	# 				items=QrCodeSchema
	# 			)
	# 		}
	# 	)}
	# )
	# def get(self, request, pk, format=None):
	# 	Qrcode = self.get_object(pk)
	# 	serializer = UserLocationSerializer(Qrcode, data=request.data)
	# 	print(serializer.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	@swagger_auto_schema(
		operation_id='Delete QR code',
		operation_summary='특정 QR code 삭제하기',
		tags=['특정 QR code 삭제하기'],
		responses={
			status.HTTP_204_NO_CONTENT: openapi.Schema(
			type=openapi.TYPE_OBJECT,
		),
			status.HTTP_409_CONFLICT: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'error': openapi.Schema(
					type=openapi.TYPE_STRING,
					example='DB is empty'
				)
			}
		)}
	)
	def delete(self, request, pk, format=None):
		Qrcode = self.get_object(pk)
		Qrcode.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	@swagger_auto_schema(
		operation_id='Get QR code',
		operation_summary='특정 QR code 랜덤으로 바꾸기',
		tags=['특정 QR code 랜덤으로 바꾸기'],
		responses={status.HTTP_200_OK: openapi.Schema(
			type=openapi.TYPE_OBJECT,
			properties={
				'data': openapi.Schema(
					type=openapi.TYPE_ARRAY,
					items=QrCodeSchema
				)
			}
		)}
	)
	def patch(self, request, pk, format=None):
		Qrcode = self.get_object(pk)
		Qrcode.latitude = ( random() - 0.5) * 90
		Qrcode.longitude = ( random() - 0.5) * 180
		Qrcode.save()
		serializer = UserLocationSerializer(Qrcode)
		return  Response(serializer.data, status=status.HTTP_200_OK)
