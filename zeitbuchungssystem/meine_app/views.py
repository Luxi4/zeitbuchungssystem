from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

'''
from django.http import HttpResponse
from datetime import datetime

#test
def servus (request):
	return HttpResponse("servus, schön dass es dich gibt!")

def jetzt (request):
	eben = datetime.now()
	return HttpResponse(f"aktuelle Uhrzeit: {eben:%Hh %Mm %Ss}")
'''

def register(request, template_name='meine_app/register.html', next_page_name=None):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if next_page_name is None:
                next_page = '/'
            else:
                next_page = reverse(next_page_name)
            return HttpResponseRedirect(next_page)
    else:
        form = UserCreationForm()
    return render(request, template_name, {'form': form})