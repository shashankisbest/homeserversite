from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import User
from django.shortcuts import redirect
from .utils import get_system_status
from django.http import JsonResponse



def system_status(request):
    return JsonResponse(get_system_status())


    

def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('/')


    return render(request,"dashboard/page.html",{
    "var1forhtml" : "value1from this view",
    "username" : request.session['username'],
    "is_admin" : request.session['is_admin'],
    "system_status" : get_system_status(),
    })


