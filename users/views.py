from django.shortcuts import render, redirect

from django.contrib import messages

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.



def registerView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            messages.success(request, "Registered succesfully. Let's login")
            return redirect('users:login')
        else:
            form = UserCreationForm(request.POST)
        

    else:
        form = UserCreationForm()


    context = {'form':form}
    return render(request, 'users/register.html', context)




def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login succesfully. Welcome " + user.username)

            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return redirect('blogs:blogpost_list')
        
        
        else:
            messages.error(request, 'Something is wrong. Please try again.')
            form = AuthenticationForm(request.POST)



    else:
        form = AuthenticationForm()

        if 'next' in request.GET:
            messages.warning(request, 'Please login again to do this operation.')


    context = {'form':form}
    return render(request, 'users/login.html', context)



def logoutView(request):

    user = request.user
    if not user.is_authenticated:
        messages.warning(request, 'Lan daha giriş yapmadın dümbük.')
    
    else:
        logout(request)
        messages.success(request, 'Logout succesfully. Good Bye :(')

    return redirect("blogs:blogpost_list")
