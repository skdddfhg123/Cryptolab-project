from locale import atoi
from django.shortcuts import render
from django.http import HttpResponse, Http404

from random import choice, random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, generics, mixins
from .models import UserLocation, Ftuser
from .serializers import UserLocationSerializer

class QrcodeApi(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
	queryset = UserLocation.objects.all()
	serializer_class = UserLocationSerializer

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class QrcodeDetailApi(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
	queryset = UserLocation.objects.all()
	serializer_class = UserLocationSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

class LocationApi(APIView):
	def get(self, request, format=None):
		Qrcode = UserLocation.objects.all()
		serializer = UserLocationSerializer(Qrcode, many=True)
		return Response(serializer.data)
	
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

	def delete(self, request, format=None):
		Qrcode = UserLocation.objects.all()
		serializer = UserLocationSerializer(Qrcode)
		if len(Qrcode) == 0:
			return (Response(serializer.data, status=status.HTTP_409_CONFLICT))
		Qrcode.delete()
		return HttpResponse(status=204)


class LocationDetail(APIView):
	def get_object(self, pk):
		try:
			return UserLocation.objects.get(pk=pk)
		except UserLocation.DoesNotExist:
			raise Http404

	# def get(self, request, pk, format=None):
	# 	Qrcode = self.get_object(pk)
	# 	serializer = UserLocationSerializer(Qrcode, data=request.data)
	# 	if serializer.is_valid():
	# 		serializer.save()
	# 		return Response(serializer.data)
	# 	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, pk, format=None):
		Qrcode = self.get_object(pk)
		Qrcode.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

	def patch(self, request, pk, format=None):
		Qrcode = self.get_object(pk)
		Qrcode.latitude = ( random() - 0.5) * 90
		Qrcode.longitude = ( random() - 0.5) * 180
		Qrcode.save()
		sserializer = UserLocationSerializer(Qrcode)
		return  Response(status=status.HTTP_200_OK)

# def TestCreate(request):
# 	lat = ( random() - 0.5) * 90
# 	lon = ( random() - 0.5) * 180
# 	user = choice(Ftuser.objects.all())
# 	qr_code = UserLocation(id=user,latitude=lat, longitude=lon)
# 	qr_code.save()
# 	return HttpResponse('success')

# def TestRead(request):
# 	all_qr_code = UserLocation.objects.all()
# 	list = ''
# 	for qr_code in all_qr_code:
# 		list += f'{qr_code.qrcode}\tuser:{qr_code.id}' + \
# 			f'\tlatitude:{qr_code.latitude}' + \
# 			f'\tlongitude:{qr_code.longitude}' + \
# 			f'\tvalidity:{qr_code.isval}<br>'
# 	return HttpResponse(list)

# def TestUpdate(request):
# 	all_qr_code = UserLocation.objects.all()
# 	if len(all_qr_code) == 0:
# 		return HttpResponse('table is empty')
# 	qr_code = choice(all_qr_code)
# 	qr_code.latitude = ( random() - 0.5) * 90
# 	qr_code.longitude = ( random() - 0.5) * 180
# 	qr_code.save()
# 	info = f'{qr_code.qrcode}\tuser:{qr_code.id}' + \
# 			f'\tlatitude:{qr_code.latitude}' + \
# 			f'\tlongitude:{qr_code.longitude}' + \
# 			f'\tvalidity:{qr_code.isval}\n'
# 	return HttpResponse(info)

# def TestDelete(request):
# 	all_qr_code = UserLocation.objects.all()
# 	if len(all_qr_code) == 0:
# 		return HttpResponse('table is empty')
# 	qr_code = choice(all_qr_code)
# 	qr_code.delete()
# 	return HttpResponse('success')