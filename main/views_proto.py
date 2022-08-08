from ast import Try
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from datetime import *
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .models import *
from .forms import CommentModelForm, CocommentModelForm

from accounts.forms import OdoqCreationForm, LoginForm

def all_comments(request, page):
    comment_list = Comment.objects.all()
    paginator = Paginator(comment_list, 5)
    comments = paginator.get_page(page)
    return render(request, "main/comments_pagination.html", {"comments" : comments})