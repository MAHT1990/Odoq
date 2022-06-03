from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import *
from datetime import *
from django.views.decorators.csrf import csrf_exempt

######## QUESTION MODEL FILTERING METHODS ########

def current_question():
    #요일 처리
    seoul_timezone = timezone(timedelta(hours=9))
    rightnow_kor = datetime.now(tz=seoul_timezone)
    rightnow_weekday_kor = rightnow_kor.weekday()

    #현재 시각을 UTC 기준으로 선언한다. (DB는 UTC 기준)
    rightnow_utc = datetime.now(tz=timezone.utc)
    
    # Question들의 QuerySet을 불러온다.
    question_queryset = Question.objects.all()

    # 현재 문제와 다음 문제를 확정하기위한 Delta값
    question_current = None
    question_next = None
    question_next_countdown = None

    
    # upload_date와 오늘 현재 시각을 비교하여 data를 확정한다.
    for q in question_queryset:
        
        #now와의 시간차 계산
        delta_datetime = rightnow_utc - q.upload_datetime

        #delta_datetime이 0이상이면, 지나간 문제다.
        #절댓값이 가장 낮은 값이 현재 업로드되어야하는 문제이다.

        if q.upload_datetime >= rightnow_utc:
            if question_next == None:
                question_next = q
                question_next_countdown = -round(delta_datetime.total_seconds())

            else:
                if q.upload_datetime < question_next.upload_datetime:
                    question_next = q
                    question_next_countdown = -round(delta_datetime.total_seconds())
                else:
                    None

        else:
            if question_current == None:
                question_current = q
            else:
                if q.upload_datetime > question_current.upload_datetime:
                    question_current = q
                else:
                    None

    #다음문제 없을 때의 처리.
    if question_next == None:
        question_next_countdown = 0

    #금요일, 토요일, 일요일 일 때의 countdown값을 달리준다.
    #금요일일 때는 하루 in 초 - 현재 시각 in 초 till 토
    #토요일일 때는 이틀 in 초 - 현재 시각 in 초 till 월
    #일요일일 때는 하루 in 초 - 현재 시각 in 초 till 월

    if rightnow_weekday_kor == 4 or rightnow_weekday_kor == 5 or rightnow_weekday_kor == 6: #금요일일 때,
        t_hour = rightnow_kor.hour
        t_min = rightnow_kor.minute
        t_sec = rightnow_kor.second

        t_day_in_seconds = 86400
        t_now_in_seconds = 3600 * t_hour + 60 * t_min + t_sec

        if rightnow_weekday_kor == 4: #금요일
            #24시간을 초로 환산해서 현재시각을 초로 환산한 값을 빼준다.
            delta_datetime = t_day_in_seconds - t_now_in_seconds 
    
        elif rightnow_weekday_kor == 5: #토요일
            delta_datetime = t_day_in_seconds * 2 - t_now_in_seconds
        
        elif rightnow_weekday_kor == 6: #일요일
            delta_datetime = t_day_in_seconds - t_now_in_seconds 

        question_next_countdown = delta_datetime

    
    #Debugging            
    # print("today's question is",question_current)
    # print("next question is ", question_next)
    # print("next question countdowns in seconds is ", -question_next_countdown, "seconds")
    # print(type(question_next_countdown))

    content = {
        'weekday' : rightnow_weekday_kor,
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
        content = {'notice' : current_notice.img}
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
