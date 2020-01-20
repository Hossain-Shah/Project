from django.shortcuts import render
from django.http.response import HttpResponse


def bview(request):
    if request.GET['hub.verify_token'] == 'a_secret_web_hook':
        return HttpResponse(request.GET['hub.challenge'])
    else :
        return HttpResponse('Invalid Token !')