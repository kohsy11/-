from django.shortcuts import render, redirect
from .models import Community, Comments, Option, Leggings
import datetime
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .utils import upload_and_save

# Create your views here.

def login(request):
    if request.method == 'POST':
        found_user = auth.authenticate(
            username = request.POST['username'],
            password = request.POST['password']
        )
        if found_user is None:
            error = 'Incorrect ID or Password'
            return render(request, 'common/login.html', {'error': error})
            
        auth.login(request, found_user, backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect('option')
    return render(request, 'common/login.html')

def start(request):
    return render(request, 'common/start.html')

def registration(request):
    if request.method == 'POST':
        found_user = User.objects.filter(username = request.POST['username'])
        if len(found_user) > 0:
            error = '이미 존재하는 아이디입니다'
            return render(request, 'common/registration.html', {'error' : error})
        
        new_user = User.objects.create_user(
            username = request.POST['username'],
            password = request.POST['password']
        )
        auth.login(request, new_user, backend = 'django.contrib.auth.backends.ModelBackend')
        return redirect('index')
    return render(request, 'common/registration.html')

def index(request):
    options = list(Option.objects.filter(user_id=request.user.pk))
    latest_option = options[len(options)-1]
    option_1 = latest_option.option1
    option_2 = latest_option.option2
    my_dict_1 = {"hipup":"#볼륨 있는 엉덩이", "bigsize":"#사이즈 업!", "shortheight":"#작은 키가 고민인", "yzone":"#와이존 완벽커버"}
    my_dict_2 = {"red":"#분홍색", "blue":"#하늘색", "gray":"#회색", "black":"#검정색", "yellow":"#노란색"}
    sorted_leggings = Leggings.objects.filter(feature=option_1,color=option_2)
    return render(request, 'index.html',{"sorted_leggings" : sorted_leggings, "option_1" : my_dict_1[option_1], "option_2" : my_dict_2[option_2]})

def option(request):
    if request.method == 'POST':
        Option.objects.create(
            option1 = request.POST['option1'],
            option2 = request.POST['option2'],
            user = request.user,
        )
        return redirect('index')
    return render(request, 'common/option.html')

# def logout(request):
#     auth.logout(request)
#     return redirect('index')

def search_option(request):
    return(render, "index.html")

@login_required(login_url = '/common/registration')
def com_new(request):
    if request.method == 'POST':
        file_to_upload = request.FILES.get('img')
        new_post = Community.objects.create(
            title = request.POST['title'],
            content = request.POST['content'],
            author = request.user,
            img = upload_and_save(request, file_to_upload)
        )
        return redirect('com_detail', new_post.pk)
    return render(request, 'com_new.html')

def mypage(request, mykey):
    mystyles = Option.objects.filter(user = request.user)
    posts = Community.objects.filter(author = request.user)
    if request.method == 'POST':
        Option.objects.filter(user = request.user).update(
            option1 = request.POST['option1'],
            option2 = request.POST['option2'],
        )
        return redirect('mypage')
    return render(request, 'mypage.html', {'mystyles' : mystyles , 'posts':posts} )

def com_list(request):
    posts = Community.objects.all()
    return render(request, 'com_list.html', { 'posts' : posts })

def com_detail(request, key):
    post = Community.objects.get(pk = key)
    if request.method == "POST":
        Comments.objects.create(
            post = post,
            comment = request.POST['comment'],
            author = request.user
        )
        return redirect('com_detail', key)
    return render(request, 'com_detail.html', {'post' : post})

def search_option(request):
    if request.method == 'POST':
        Option.objects.create(
            option1 = request.POST['option1'],
            option2 = request.POST['option2'],
            user = request.user,
        )
        return redirect('search_result')
    return render(request, 'search_option.html')

def search_result(request):
    options = list(Option.objects.filter(user_id=request.user.pk))
    latest_option = options[len(options)-1]
    option_1 = latest_option.option1
    option_2 = latest_option.option2
    my_dict_1 = {"hipup":"#볼륨 있는 엉덩이", "bigsize":"#사이즈 업!", "shortheight":"#작은 키가 고민인", "yzone":"#와이존 완벽커버"}
    my_dict_2 = {"red":"#분홍색", "blue":"#하늘색", "gray":"#회색", "black":"#검정색", "yellow":"#노란색"}
    sorted_leggings = Leggings.objects.filter(feature=option_1,color=option_2)
    return render(request, 'search_result.html',{"sorted_leggings" : sorted_leggings, "option_1" : my_dict_1[option_1], "option_2" : my_dict_2[option_2]})

