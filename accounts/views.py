from django.shortcuts import render
from django.http import HttpResponse
from accounts.models import User
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
# Create your views here.

def logout(request):
    request.session.flush()
    return redirect('/')



def login_page(request):

    if request.method == "GET":
        return render(request, 'accounts/login.html')

    username = request.POST['username']
    password = request.POST['password']

    try:
        user = User.objects.get(username=username)

        if check_password(password, user.password):
            # return render(request, 'accounts/login.html', {'message': 'Login successful'})  #^ this was for testing

            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['is_admin'] = user.is_admin

            return redirect('dashboard/')  #^ redirect to home page after successful login

    except User.DoesNotExist:
        pass


    return render(request, 'accounts/login.html', {'message': 'Invalid username or password'})
