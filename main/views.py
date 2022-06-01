from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from datetime import *
from django.views.decorators.csrf import csrf_exempt

######## QUESTION MODEL FILTERING METHODS ########

def current_question():
    
    # Question들의 QuerySet을 불러온다.
    question_queryset = Question.objects.all()
    
    #현재 시각을 UTC 기준으로 선언한다.
    #DB에 있는 문제들의 업로드 날짜들은, UTC시각기준이다.
    rightnow = datetime.now(tz=timezone.utc)

    # 현재 문제와 다음 문제를 확정하기위한 Delta값
    question_current = None
    question_next = None
    question_next_countdown = None

    #Debugging
    # print("today is", rightnow)
    # print("")
    # print("today's tzinfo is ", rightnow.tzinfo)

    # upload_date와 오늘 현재 시각을 비교하여 data를 확정한다.
    for q in question_queryset:
        
        #now와의 시간차 계산
        delta_datetime = rightnow - q.upload_datetime

        #Debugging
        # print("0. question code is ", q)
        # print("1. upload_datetime is", q.upload_datetime)
        # print("2. upload_datetime's tzinfo is", q.upload_datetime.tzinfo)
        # print("3. delta_time is ", delta_datetime)
        # print("")

        #delta_datetime이 0이상이면, 지나간 문제다.
        #절댓값이 가장 낮은 값이 현재 업로드되어야하는 문제이다.

        if q.upload_datetime >= rightnow:
            if question_next == None:
                question_next = q
                question_next_countdown = -round(delta_datetime.total_seconds())

            else:
                if q.upload_datetime < question_next.upload_datetime:
                    question_next = q
                    question_next_countdown = -round(delta_datetime.total_seconds())
                else:
                    None

            #Debugging
        else:
            if question_current == None:
                question_current = q
            else:
                if q.upload_datetime > question_current.upload_datetime:
                    question_current = q
                else:
                    None

    if question_next == None:
        question_next_countdown = 0
        #다음문제 없을 때의 처리.

    #Debugging            
    # print("today's question is",question_current)
    # print("next question is ", question_next)
    # print("next question countdowns in seconds is ", -question_next_countdown, "seconds")
    # print(type(question_next_countdown))

    content = {
        'code' : question_current.code,
        'season' : question_current.season,
        'img' : question_current.img,
        'aswr' : question_current.aswr,
        'countdown' : question_next_countdown
    }

    return content

######## NOTICE MODEL FILTERING METHODS ########

def current_notice():
    notice_queryset = Notice.objects.all()
    current_notice = notice_queryset.first()

    #Debugging
    # print('notice_queryset is', notice_queryset)
    # print('Current notice is ', current_notice)

    if current_notice == None:
        return None
    
    else:
        content = {
            'notice' : current_notice.img
        }

        return content

######## 요청 응답처리 VIEWS ########

def index(request):
    content = current_question()

    if current_notice() != None:
        content.update(current_notice())

    #Debug Log
    # print("content is ",content)

    return render(request, 'main/index.html', content)
    # return render(request, 'main/timer_practice.html')



#### 답안 입력 POST 처리 VIEW ####
@csrf_exempt
def answer_post(request):
    answer_input = request.POST.get("answer_input")
    # answer_question_code = request.POST.get("question_code")

    if request.method =='POST':
        if answer_input==current_question()['aswr']:
            answer_response = 'Correct'

        else:
            answer_response = 'Wrong'
    
    if request.method =='GET':
        answer_response = 'Error'

    response_data = {
        'status' : 200,
        'debugging' : 'Success',
        'answer_response' : answer_response
    }

    # return HttpResponseRedirect(reverse('main:index'))
    return JsonResponse(response_data)
