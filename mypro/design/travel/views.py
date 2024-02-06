from django.shortcuts import render
from travel.models import Place,Team
# Create your views here.
def home(request):
    p=Place.objects.all()
    e=Team.objects.all()
    return render(request,'home.html',{'o':p,'t':e})
