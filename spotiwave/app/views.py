from django.shortcuts import render

# Create your views here.
def homepageview(request):
    return render(request, "home.html")