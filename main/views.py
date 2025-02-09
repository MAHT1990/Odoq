from ast import Try
from django.core.paginator import Paginator
from django.db.models import Case, When
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
    order = None #현재 filtering 및 ordering : 'like' , 'my'

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
            'onoff_weekend_question' : None,
        }

        #실제로 Query를 날리기 때문에 예외처리를 해준다.
        try:
            current_onoff_season = self.get_or_create_onoff_season()
            current_onoff_comment = self.get_or_create_onoff_comment()
            current_onoff_weekend_question = self.get_or_create_onoff_weekend_question()
            
        except:
            return content

        if current_onoff_season:
            content['onoff_season'] = current_onoff_season.on_off
            if current_onoff_season.off_img:
                content['season_off_img'] = current_onoff_season.off_img
        
        if current_onoff_comment:
            content['onoff_comment'] = current_onoff_comment.on_off

        if current_onoff_weekend_question:
            content['onoff_weekend_question'] = current_onoff_weekend_question.on_off
        
        return content
    
    def get_or_create_onoff_season(self):
        try:
            current_onoff_season = OnOff.objects.all().get(title__icontains="Season")
            if current_onoff_season:
                return current_onoff_season
        
        except:
            t_onoff_season = OnOff.objects.create(title="Season")
            return t_onoff_season
    
    def get_or_create_onoff_comment(self):
        try:
            current_onoff_comment = OnOff.objects.all().get(title__icontains="comment")
            if current_onoff_comment:
                return current_onoff_comment
        
        except:
            t_onoff_comment = OnOff.objects.create(title="comment")
            return t_onoff_comment
    
    def get_or_create_onoff_weekend_question(self):
        try:
            current_onoff_weekend_question = OnOff.objects.all().get(title__icontains="weekend")
            if current_onoff_weekend_question:
                return current_onoff_weekend_question
        
        except:
            t_onoff_weekend_question = OnOff.objects.create(title="weekend_question")
            return t_onoff_weekend_question



    ######## QUESTION MODEL FILTERING METHODS ########
    @classmethod
    def get_current_question(cls):
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

        #get_or_create_weekend_question().on_off가 True이면,
        #금요일, 토요일, 일요일 일 때의 countdown값을 달리준다.
        #금요일일 때는 하루 in 초 - 현재 시각 in 초 till 토
        #토요일일 때는 이틀 in 초 - 현재 시각 in 초 till 월
        #일요일일 때는 하루 in 초 - 현재 시각 in 초 till 월

        if not cls.get_or_create_onoff_weekend_question(cls).on_off:
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
            'login_form' : LoginForm(auto_id = False,)
        }

        return content

    ####### Comment 관련 #######
    def get_comments(self, **kwargs):

        comments = self.comments_filtering_ordering(Comment.objects.all(), **kwargs)
        
        if self.order != 'my' and self.order != 'like':
            self.order = 'latest'

        now = datetime.now()
        
        comments_today = comments.filter(
            created_at__year = now.year,
            created_at__month = now.month,
            created_at__day = now.day,
        )
        

        paginator = Paginator(comments, 5)
        pages = list()

        for page in paginator:
            pages.append(page)

        content = {
            'comments' : comments,
            'comments_today' : comments_today,
            'paginator' : paginator,
            'pages' : pages,
            'order' : self.order,
        }

        return content

    def comments_filtering_ordering(
        self, comments_queryset, queryset_filter=None, queryset_order=None):
        comments = comments_queryset
        
        '''인자가 들어오면 그 조건에 맞춰서 filtering and ordering'''

        if queryset_filter=="today" and queryset_order=="like_count":
            dates = comments.dates('created_at', 'day').reverse()
            
            result = []

            for date in dates:
                t_comments = comments.filter(created_at__date = date).order_by('-like_count', '-created_at')
                result += list(t_comments)
            
            result_pk = [comment.pk for comment in result]
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(result_pk)])
            comments = Comment.objects.filter(pk__in=result_pk).order_by(preserved)
            self.order = 'like'
        
        if queryset_filter=="my_comment":
            comments = Comment.objects.filter(user=self.request.user).order_by('-created_at')
            self.order = 'my'

        return comments


    def get_comment_form(self):
        # Comment 입력 form을 받아온다.
        form = CommentModelForm()
        content = {
            'comment_form' : form
        }
        return content
    
    def get_cocomment_form(self):
        form = CocommentModelForm(auto_id=False)
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
            # print(self.get_content(*args, **kwargs))
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
        response_data={
            'status' : 200,
            'debugging' : 'Success',
        }
        form = CommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            return JsonResponse(response_data)
    else:
        return redirect("main:index")

@login_required
def comment_blind(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        cocomment_id = request.POST.get("cocomment_id")

        if comment_id and not cocomment_id:
            try:
                trgt_comment = Comment.objects.get(id = comment_id)
            except:
                trgt_comment = None
                answer_response = "삭제되었거나 존재하지 않는 댓글입니다."

            if trgt_comment:
                if trgt_comment.blind == True:
                    trgt_comment.blind = False
                    answer_response = "블라인드 처리가 해제되었습니다."
                else:
                    trgt_comment.blind = True
                    answer_response = "블라인드 처리되었습니다."
                    if request.user.is_superuser:
                        trgt_comment.blind_text = "관리자에 의해 블라인드 처리되었습니다."
                    else:
                        trgt_comment.blind_text = "작성자에 의해 블라인드 처리되었습니다."
                
                trgt_comment.save()
        
        elif not comment_id and cocomment_id:
            try:
                trgt_cocomment = Cocomment.objects.get(id = cocomment_id)
            except:
                trgt_cocomment = None
                answer_response = "삭제되었거나 존재하지 않는 댓글입니다."
            
            if trgt_cocomment:
                if trgt_cocomment.blind == True:
                    trgt_cocomment.blind = False
                    answer_response = "블라인드 처리가 해제되었습니다."
                else:
                    trgt_cocomment.blind = True
                    answer_response = "블라인드 처리되었습니다."
                    if request.user.is_superuser:
                        trgt_cocomment.blind_text = "관리자에 의해 블라인드 처리되었습니다."
                    else:
                        trgt_cocomment.blind_text = "작성자에 의해 블라인드 처리되었습니다."
                trgt_cocomment.save()
    
        response_data = {
        'status' : 200,
        'debugging' : 'Success',
        'answer_response' : answer_response
        }

        return JsonResponse(response_data)
    else:
        return redirect("main : index")

@login_required
def comment_delete(request):
    if request.method == 'POST':
        comment_id = request.POST.get("comment_id")
        
        try:
            trgt_comment = Comment.objects.get(id = comment_id)
        except:
            trgt_comment = None
            answer_response = '삭제되었거나 존재하지않는 댓글입니다.'

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

    comment, cocomment = None, None

    if request.method == "POST":
        if request.POST.get('comment_id'):
            comment = Comment.objects.get(id=request.POST['comment_id'])
        elif request.POST.get('cocomment_id'):
            cocomment = Cocomment.objects.get(id=request.POST['cocomment_id'])

        if comment:
            form = CommentModelForm(request.POST, instance=comment)
        elif cocomment:
            form = CocommentModelForm(request.POST, instance=cocomment)
        else:
            return redirect("main:index")

        if form.is_valid():
            edit = form.save()
            return JsonResponse(response_data)
    else:
        return redirect("main:index")

## 대댓글 관련 view
@login_required
def cocomment_new(request):
    if request.method == 'POST':
        response_data={
            'status' : 200,
            'debugging' : 'Success',
        }
        form = CocommentModelForm(request.POST, request.FILES)
        if form.is_valid():
            cocomment = form.save(commit=False)
            cocomment.user = request.user
            cocomment.comment = Comment.objects.get(id = request.POST['comment_id'])
            cocomment.save()
            return JsonResponse(response_data)
        else:
            response_data['debugging'] = 'False'
            return render(request, 'accounts/user_profile_form.html', {
                    'form':form,
                })  
            # return JsonResponse(response_data)
    else:
        return redirect("main:index")

@login_required
def cocomment_blind(request):
    pass

@login_required
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
@login_required
def like(request, comment_id=None, cocomment_id=None):
    userprofile = request.user.userprofile

    response_data = {
        'status' : 200,
        'msg' : 'success',
        'comment_like_count' : None,
        'cocomment_like_count' : None,
    }

    if comment_id:
        liked_comment = Comment.objects.get(id=int(comment_id))
        
        if liked_comment not in userprofile.like_comments.all():
            liked_comment.like_count += 1
            liked_comment.save()

            userprofile.like_comments.add(liked_comment)
            userprofile.save()
        else:
            liked_comment.like_count -=1
            liked_comment.save()

            userprofile.like_comments.remove(liked_comment)
            userprofile.save()
        
        response_data['comment_like_count'] = liked_comment.like_count
    
    if cocomment_id:
        liked_cocomment = Cocomment.objects.get(id=int(cocomment_id))

        if liked_cocomment not in userprofile.like_cocomments.all():
            liked_cocomment.like_count +=1
            liked_cocomment.save()

            userprofile.like_cocomments.add(liked_cocomment)
            userprofile.save()
        else:
            liked_cocomment.like_count -=1
            liked_cocomment.save()

            userprofile.like_cocomments.remove(liked_cocomment)
            userprofile.save()

        response_data['cocomment_like_count'] = liked_cocomment.like_count

    return JsonResponse(response_data)