from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from django.http import HttpRequest

def servus (request):
	return HttpResponse("servus, schön dass es dich gibt!")

def jetzt (request):
	eben = datetime.now()
	return HttpResponse(f"aktuelle Uhrzeit: {eben:%Hh %Mm %Ss}")

def setcookie(request):
	response = HttpResponse("hier wurde ein Keks gesetzt")
	response["Content-Type"] = "text/plain"
	response.set_cookie("keks", ":-)")
	response.set_cookie("vergammelterkeks", ":-(")
	return response