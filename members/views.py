from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .forms import MemberForm,LoginForm
from .models import Members

# wellcome page

def home(request):

    confirmation_message = ""

    if request.method == "POST":
        form = MemberForm(request.POST)

        if form.is_valid():
            form.save()
            confirmation_message = "New member added successfully"
            form = MemberForm()  # reset only AFTER success
        else:
            confirmation_message = "Form is not valid"
    else:
        form = MemberForm()

    return render(request, 'members/home.html', {
        'form': form,
        'confirmation_message': confirmation_message
    })
def login_view(request):
    
    error_message =None
    if request.method=="POST":
        form=LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user=authenticate(request,username=email,password=password) 
            print(user)
            if user is not None:
               return redirect('profile')
            else:
                error_message="Invalid email or member id"
    form = LoginForm()         
    return render(request,'members/login.html', {'form': form,'error_message': error_message})

def member_list(request):
    members=Members.objects.all()
    return render(request, 'members/member_list.html', {'members': members})