from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import MemberForm
from .models import Members

# wellcome page

def home (request):
    confirmation_message = ""
    if request.method== "post":
        form=MemberForm(request.POST)
        if form.is_valid():
            form.save()
            confirmation_message="new member added successfully"
            return render(request, 'members/home.html', {'confirmation_message': confirmation_message})
    else:
        form=MemberForm()
    return render(request, 'members/home.html', {'form': form, 'confirmation_message': confirmation_message})

def member_list(request):
    members=Members.objects.all()
    return render(request, 'members/member_list.html', {'members': members})