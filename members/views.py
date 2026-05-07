from django.views import View
from django.shortcuts import render, redirect
from .forms import MemberForm

# wellcome page

class Home (View):
    def get(self, request):
        form=MemberForm()
        return render(request, 'members/home.html', {'form': form})