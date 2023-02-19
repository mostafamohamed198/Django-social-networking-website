from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from .models import *
from django.http import JsonResponse
import json 
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def index(request):
    allposts = posts.objects.all().order_by('-timestamp')
    p = Paginator(posts.objects.all().order_by('-timestamp'), 4)
    page = request.GET.get('page')
    postss = p.get_page(page)
    user = request.user
    nums = "a" * postss.paginator.num_pages
    return render(request, "network/index.html",{"allposts": allposts, 'posts':postss, 'nums':nums, user: 'user'})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def newpost(request):
    if request.method == 'POST' and request.POST.get('textarea1'):
        if request.user.is_authenticated:
            post = request.POST['textarea1']
            user = request.user
            posts.objects.create(post = post, writer = user)
        else:
            return render(request, "network/login.html")

    return render (request, "network/newpost.html")


@csrf_exempt
def Users(request, name):
    allposts = posts.objects.all().order_by('-timestamp')
    p = Paginator(posts.objects.all().order_by('-timestamp'), 1)
    page = request.GET.get('page')
    postss = p.get_page(page)
    user = request.user
    nums = "a" * postss.paginator.num_pages
    x = User.objects.get(username=name)
    l = ''
    if follow.objects.filter(follower = request.user, following = x).exists():
        l = 'unfollow'
    else:
        l = 'follow'
    
    if request.method == 'PUT':
        print('we\'ve hit put')

        data = json.loads(request.body)

        if data.get('follow') is not None:
            print('in follow')

            # Note: [User Obj Itself]
            #   follower = request.user  (is: <User Obj>)
            #   following = x            (is: <User Obj>)

            followObj, createdBool = follow.objects.get_or_create(follower=request.user, following=x)

            print('followObj', followObj)
            print('created?', createdBool)
        
        print('past follow')
        if data.get('unfollow') is not None:
            follow.objects.filter(follower = request.user, following = x).delete()

        else:
            pass

    print('about to render')
    followers = follow.objects.filter(following = x)
    following = follow.objects.filter(follower = x)
    user_post = posts.objects.filter(writer = x)
    return render (request, "network/user.html",{"x":x, 'l':l, 'followers':followers , 'following':following , "user_posts":user_post, "allposts": allposts, 'posts':postss, 'nums':nums, user: 'user'})



@csrf_exempt
def like(request, post_id):
    liked__post = posts.objects.get(id = post_id)
    if request.method == 'PUT':
        print('we\'ve hit put')

        data = json.loads(request.body)

        if data.get('like') is not None:
            print('in like')

            # Note: [User Obj Itself]
            #   follower = request.user  (is: <User Obj>)
            #   following = x            (is: <User Obj>)

            liked__post.likers.add(request.user)
 

        elif data.get('notlike') is not None:
            print('not in like')
            liked__post.likers.remove(request.user)

        elif data.get('unlike') is not None:
            print('in like')

            # Note: [User Obj Itself]
            #   follower = request.user  (is: <User Obj>)
            #   following = x            (is: <User Obj>)

            liked__post.unlikers.add(request.user)
 

        elif data.get('notunlike') is not None:
            print('not in like')
            liked__post.unlikers.remove(request.user)
        
    print('about to render')


def edit(request, posttid):
    posttoedit = posts.objects.get(id = posttid)
    if request.method == 'POST' and request.POST.get('edit'):
        newedit = request.POST['edit']
        posttoedit.post = newedit
        posttoedit.save()
    return render(request, 'network/edit.html', {'posttoedit':posttoedit})

def following(request, user):
    xxy = User.objects.get(id= user).id
    xy = follow.objects.filter(follower = xxy)
    print(xy)

    return render(request, 'network/following.html', {'xy':xy})