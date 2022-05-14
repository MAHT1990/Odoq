from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *

# Create your views here.

def index(request):
    question_models = Question.objects.all().order_by("code")
    question_first = question_models.first()
    content = {
        'code' : question_first.code,
        'season' : question_first.season,
        'img' : question_first.img,
        'aswr' : question_first.aswr
    }
    return render(request, 'main/index.html', content)
