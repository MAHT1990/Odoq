from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *

# Create your views here.

def current_question():
    question_models = Question.objects.all().order_by("code")
    question_first = question_models.first()
    content = {
        'code' : question_first.code,
        'season' : question_first.season,
        'img' : question_first.img,
        'aswr' : question_first.aswr
    }

    return content

def index(request):
    content = current_question()

    return render(request, 'main/index.html', content)

def answer_post(request):
    answer_input = request.POST.get("answer_input")
    # answer_question_code = request.POST.get("question_code")

    if answer_input==current_question()['aswr']:
        answer_response = 'Correct'

    else:
        answer_response = 'Wrong'

    response_data = {
        'status' : 200,
        'debugging' : 'Success',
        'answer_response' : answer_response
    }

    # return HttpResponseRedirect(reverse('main:index'))
    return JsonResponse(response_data)
