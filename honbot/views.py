from django.shortcuts import render_to_response
from honbot import models


def home(request):
    return render_to_response('home.html')
