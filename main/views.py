from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from datetime import *

######## QUESTION MODEL FILTERING METHODS ########

def current_question():
    
    # Question들의 QuertSet을 불러온다.
    question_queryset = Question.objects.all()
    now = datetime.now()

    #Debugging
    print("today is", now)

    # upload_date와 오늘 현재 시각을 비교하여 data를 확정한다.
    for q in question_queryset:
        #Debugging
        print("upload_datetime is", q.upload_datetime)
        print("type is", type(q.upload_datetime))
        print(q.upload_datetime.tzinfo)
        # question_current = question_queryset.first()

        if q.upload_datetime.year == now.year and q.upload_datetime.month == now.month and q.upload_datetime.day==now.day:
            question_current = q

            #Debugging
            print("today's question is",question_current)

    content = {
        'code' : question_current.code,
        'season' : question_current.season,
        'img' : question_current.img,
        'aswr' : question_current.aswr
    }

    return content



######## 요청 응답처리 VIEWS ########

def index(request):
    content = current_question()

    #Debug Log
    print(content)

    return render(request, 'main/index.html', content)



#### 답안 입력 POST 처리 VIEW ####

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
