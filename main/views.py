from ast import Try
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import *
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import CommentModelForm, CocommentModelForm

from accounts.forms import OdoqCreationForm, LoginForm

class IndexView:

    get_current_question_bool = True
    get_current_notice_bool = True
    get_login_form_bool = True
    get_comment_form_bool = True
    get_comments_bool = True
    get_cocomment_form_bool = True
    request = None

    ####### CONSTRUCTOR #######
    def __init__(self, **initkwargs):
        for key, value in initkwargs.items():
            setattr(self, key, value)
    
    ######## OnOff MODEL FILTERING METHODS ########
    def current_OnOff(self):
        content = {
            'onoff_season' : None,
            'season_off_img' : None,
            'onoff_comment' : None,
        }

        #실제로 Query를 날리기 때문에 예외처리를 해준다.
        try:
            current_onoff_season = OnOff.objects.all().get(title__icontains="Season")
            current_onoff_comment = OnOff.objects.all().get(title__icontains="comment")
        except:
            return content

        if current_onoff_season:
            content['onoff_season'] = current_onoff_season.on_off
            if current_onoff_season.off_img:
                content['season_off_img'] = current_onoff_season.off_img
        
        if current_onoff_comment:
            content['onoff_comment'] = current_onoff_comment.on_off
        
        return content

    ######## QUESTION MODEL FILTERING METHODS ########
    @classmethod
    def get_current_question(self):
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

        if rightnow_weekday_kor == 4 or rightnow_weekday_kor == 5 or rightnow_weekday_kor == 6: #금,토,일요일일 때,
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
            'pk' : question_current.pk,
            'code' : question_current.code,
            'season' : question_current.season,
            'img' : question_current.img,
            'aswr' : question_current.aswr,
            'countdown' : question_next_countdown,
        }

        return content

    ######## NOTICE MODEL FILTERING METHODS ########
    def get_current_notice(self):
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


    ####### Authentication 관련 #######
    def get_creation_form(self):
        content = {
            'creation_form' : OdoqCreationForm()
        }

        return content

    def get_login_form(self):
        content = {
            'login_form' : LoginForm()
        }

        return content

    ####### Comment 관련 #######
    def get_comments(self, **kwargs):

        comments = self.comments_filtering_ordering(Comment.objects.all(), **kwargs)
        
        paginator = Paginator(comments, 5)

        pages = list()
        for page in paginator:
            pages.append(page)

        content = {
            'comments' : comments,
            'paginator' : paginator,
            'pages' : pages,
        }

        return content

    def comments_filtering_ordering(
        self, comments_queryset, queryset_filter=None, queryset_order=None):
        comments = comments_queryset
        
        if queryset_filter=="today":
            now = datetime.now()
            comments = comments_queryset.filter(
                created_at__year = now.year,
                created_at__month = now.month,
                created_at__day = now.day,
            )

        if queryset_order=="like_count":
            comments = comments.order_by('-like_count')

        return comments


    def get_comment_form(self):
        # Comment 입력 form을 받아온다.
        form = CommentModelForm()
        content = {
            'comment_form' : form
        }
        return content
    
    def get_cocomment_form(self):
        form = CocommentModelForm()
        content = {
            'cocomment_form' : form
        }
        return content

    ###### content : Response에 넣어줄 <Dictionary : content> ######
    def get_content(self, *args, **kwargs):
        
        #1. get_current_question()으로 <Dict : get_current_question()>을 받는다.
        #2. current_OnOff()으로 <Dict : current_OnOff()>을 추가한다.
        #3. current_notice()으로 <Dict : current_notice()>을 추가한다.
        
        content = dict()
        content.update(self.current_OnOff())
        

        if self.get_current_question_bool:
            content.update(self.get_current_question())
        
        if self.get_current_notice() != None:
            content.update(self.get_current_notice())

        if self. get_login_form_bool:
            content.update(self.get_login_form())

        if self.get_comments_bool:
            content.update(self.get_comments(**kwargs))

        if self.get_comment_form_bool:
            content.update(self.get_comment_form())
        
        if self.get_cocomment_form_bool:
            content.update(self.get_cocomment_form())
        
        #Debug Log
        # debug_title = 'get_content'
        # len_debug_title = len(debug_title)
        # print('=' * len_debug_title,'\n',debug_title,'\n','=' * len_debug_title)
        # print("content is ",content)
        # for key, value in content.items():
        #     print(key, '----', value ,'\n')

        return content

    ###### as_view 정의 ######
    @classmethod
    def as_view(cls, **initkwargs):

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            self.request = request
            return render(request, 'main/index.html', self.get_content(*args, **kwargs))

        return view

######## 요청 응답처리 VIEWS ########

index = ensure_csrf_cookie(IndexView.as_view())


#### 답안 입력 POST 처리 VIEW ####
def answer_post(request):
    answer_input = request.POST.get("answer_input")
    # answer_question_code = request.POST.get("question_code")

    if request.method =='POST':
        if answer_input== IndexView.get_current_question()['aswr']:
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

#### SMS 알림 처리 번호 등록 VIEW ####
def sms_new(request):
    if request.method == 'POST':
        phone_number_input = request.POST.get("phone_number_input")

        phoneNumber_queryset = PhoneNumber.objects.all()
        
        #Debugging
        # print(phoneNumber_queryset)
        # print(type(phoneNumber_queryset))
        if len(phone_number_input)==11 and phone_number_input[0:3] == '010':
            if phoneNumber_queryset.filter(phone_number=phone_number_input):
                answer_response = '이미 등록된 번호입니다.'

            else:
                new_phone_number = PhoneNumber(phone_number = phone_number_input)
                new_phone_number.save()
                
                answer_response = '등록완료'


        else:
            #Debugging
            # print(phone_number_input)
            # print(type(phone_number_input))
            # print(phone_number_input[0:3])
            answer_response = '잘못된 형식입니다.'

    response_data = {
    'status' : 200,
    'debugging' : 'Success',
    'answer_response' : answer_response
    }
    
    return JsonResponse(response_data)

#### SMS 알림 처리 번호 삭제 VIEW ####
def sms_delete(request):
    if request.method == 'POST':
        phone_number_input = request.POST.get("phone_number_input")

        phoneNumber_queryset = PhoneNumber.objects.all()
        
        #Debugging
        # print(phoneNumber_queryset)
        # print(type(phoneNumber_queryset))
        if len(phone_number_input)==11 and phone_number_input[0:3] == '010':
            if phoneNumber_queryset.filter(phone_number=phone_number_input):
                trgt_phone_number = phoneNumber_queryset.filter(phone_number=phone_number_input)
                trgt_phone_number.delete()
                answer_response = '삭제되었습니다.'

            else:                
                answer_response = '등록되지않은 번호입니다.'


        else:
            #Debugging
            # print(phone_number_input)
            # print(type(phone_number_input))
            # print(phone_number_input[0:3])
            answer_response = '잘못된 형식입니다.'

    response_data = {
    'status' : 200,
    'debugging' : 'Success',
    'answer_response' : answer_response
    }
    
    return JsonResponse(response_data)

#### comment 처리관련 VIEWS ####
@login_required
def comment_new(request):
    if request.method == 'POST':
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return redirect("main:index")
    else:
        return redirect("main:index")

@login_required
def comment_delete(request):
    if request.method == 'POST':
        comment_id = request.POST.get("comment_id")
        
        trgt_comment = Comment.objects.get(id = comment_id)

        if trgt_comment:
            trgt_comment.delete()
            answer_response = '삭제되었습니다.'
    
    response_data = {
    'status' : 200,
    'debugging' : 'Success',
    'answer_response' : answer_response
    }

    return JsonResponse(response_data)

@login_required
def comment_edit(request):
    response_data = {
    'status' : 200,
    'debugging' : 'Success',
    }

    if request.method == "POST":
        print(request.POST)
        try:
            comment = Comment.objects.get(id=request.POST['comment_id'])
        except Comment.DoesNotExist:
            comment = None

        if comment:
            form = CommentModelForm(request.POST, instance=comment)
            
            if form.is_valid():
                comment_edit = form.save()
                return JsonResponse(response_data)
        else:
            return redirect("main:index")

    else:
        return redirect("main:index")

## 대댓글 관련 view
@login_required
def cocomment_new(request):
    if request.method == 'POST':
        form = CocommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            cocomment = form.save(commit=False)
            cocomment.user = User.objects.get(username = request.POST['user'])
            cocomment.comment = Comment.objects.get(id = request.POST['comment_id'])
            cocomment.save()
            return redirect("main:index")
    else:
        return redirect("main:index")

def cocomment_delete(request):
    if request.method == 'POST':
        cocomment_id = request.POST.get("cocomment_id")
        trgt_cocomment = Cocomment.objects.get(id = cocomment_id)

        if trgt_cocomment:
            trgt_cocomment.delete()
            answer_response = '삭제되었습니다.'
    
    response_data = {
    'status' : 200,
    'debugging' : 'Success',
    'answer_response' : answer_response
    }

    return JsonResponse(response_data)

@login_required
def cocomment_edit(request):
    pass


## 댓글 및 대댓글 좋아요
def like(request, zero_xor_one, comment_id=None, cocomment_id=None):
    userprofile = request.user.userprofile

    response_data = {
        'status' : 200,
        'msg' : 'success',
        'comment_like_count' : None,
        'cocomment_like_count' : None,
    }

    if comment_id:
        liked_comment = Comment.objects.get(id=int(comment_id))
        
        if zero_xor_one == 0:
            liked_comment.like_count += 1
            liked_comment.save()

            userprofile.like_comments.add(liked_comment)
            userprofile.save()
        
        elif zero_xor_one == 1:
            liked_comment.like_count -=1
            liked_comment.save()

            userprofile.like_comments.remove(liked_comment)
            userprofile.save()
        
        response_data['comment_like_count'] = liked_comment.like_count
    
    if cocomment_id:
        liked_cocomment = Cocomment.objects.get(id=int(cocomment_id))

        if zero_xor_one == 0:
            liked_cocomment.like_count +=1
            liked_cocomment.save()

            userprofile.like_cocomments.add(liked_cocomment)
            userprofile.save()

        elif zero_xor_one == 1:
            liked_cocomment.like_count -=1
            liked_cocomment.save()

            userprofile.like_cocomments.remove(liked_cocomment)
            userprofile.save()

        response_data['cocomment_like_count'] = liked_cocomment.like_count

    return JsonResponse(response_data)