from django.shortcuts import render
from django.http import HttpResponse
from random import choice, random
from .models import UserLocation, Ftuser

def TestCreate(request):
	lat = ( random() - 0.5) * 90
	lon = ( random() - 0.5) * 180
	user = choice(Ftuser.objects.all())
	qr_code = UserLocation(id=user,latitude=lat, longitude=lon)
	qr_code.save()
	return HttpResponse('success')

def TestRead(request):
	all_qr_code = UserLocation.objects.all()
	list = ''
	for qr_code in all_qr_code:
		list += f'{qr_code.qrcode}\tuser:{qr_code.id}' + \
			f'\tlatitude:{qr_code.latitude}' + \
			f'\tlongitude:{qr_code.longitude}' + \
			f'\tvalidity:{qr_code.isval}<br>'
	return HttpResponse(list)

def TestUpdate(request):
	all_qr_code = UserLocation.objects.all()
	if len(all_qr_code) == 0:
		return HttpResponse('table is empty')
	qr_code = choice(all_qr_code)
	qr_code.latitude = ( random() - 0.5) * 90
	qr_code.longitude = ( random() - 0.5) * 180
	qr_code.save()
	info = f'{qr_code.qrcode}\tuser:{qr_code.id}' + \
			f'\tlatitude:{qr_code.latitude}' + \
			f'\tlongitude:{qr_code.longitude}' + \
			f'\tvalidity:{qr_code.isval}\n'
	return HttpResponse(info)

def TestDelete(request):
	all_qr_code = UserLocation.objects.all()
	if len(all_qr_code) == 0:
		return HttpResponse('table is empty')
	qr_code = choice(all_qr_code)
	qr_code.delete()
	return HttpResponse('success')