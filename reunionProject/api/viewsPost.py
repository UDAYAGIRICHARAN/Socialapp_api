
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import User_auth,User_followers,User_posts
#import jwt
import jwt
import datetime
from django.conf import settings
#jsonresponse
from django.http import JsonResponse
#import HttpResponse
from django.http import HttpResponse
import json



@csrf_exempt
def managePost(request):
    try:
        if request.method=='POST':
            token=request.headers.get('token')
            title=request.headers.get('title')
            description=request.headers.get('description')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])

            email=decoded['email']
            if User_auth.objects.filter(email=email).exists():
                createdTime=datetime.datetime.now()
                createdTime=createdTime.strftime("%d/%m/%Y %H:%M:%S")
                createdTime=str(createdTime)
                print(createdTime)
                post={'title':title,'description':description,'date':createdTime,'likes':[],'comments':[]}
                User_posts.objects.create(user_email=email,post=post)
                postId=User_posts.objects.get(user_email=email,post=post).id
                
                body={'postId':postId,'title':title,'description':description,'createdTime':createdTime}
                return JsonResponse({'message':'post added','body':body},status=200)
            else:
                return JsonResponse({'error':'user not found'},status=400)
        elif request.method=="GET":
            token=request.headers.get('token')
            postId=request.headers.get('postId')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            email=decoded['email']
            if User_posts.objects.filter(id=postId).exists():
                post=User_posts.objects.get(id=postId).post
                likesCount=len(post['likes'])
                commentsCount=len(post['comments'])
                return JsonResponse({'message':'post found','post':post,'likesCount':likesCount,'commentsCount':commentsCount},status=200)

        elif request.method=="DELETE":
            token=request.headers.get('token')
            postId=request.headers.get('postId')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            email=decoded['email']
            if User_posts.objects.filter(id=postId).exists():
                User_posts.objects.filter(id=postId).delete()
                return JsonResponse({'message':'post deleted'},status=200)
            else:
                return JsonResponse({'error':'post not found'},status=400)
        else:
            return JsonResponse({'error':'invalid method'},status=400)


    except Exception as e:
        error=str(e)
        return JsonResponse({'error':error},status=400)

@csrf_exempt
def allPosts(request):
    if request.method=="GET":
        token=request.headers.get('token')
        decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
        email=decoded['email']
        if User_posts.objects.filter(user_email=email).exists():
            posts=User_posts.objects.filter(user_email=email)
            postsList=[]
            for post in posts:
   
                postId=post.id
                title=post.post['title']
                description=post.post['description']
                createdTime=post.post['date']
                likesCount=post.post['likes']
                commentsCount=[]
                for comment in post.post['comments']:
                    commentsCount.append(comment['comment'])
                body={'postId':postId,'title':title,'description':description,'createdTime':createdTime,'likesCount':likesCount,'commentsCount':commentsCount}
                postsList.append(body)
            
            return JsonResponse({'message':'posts found','posts':postsList},status=200)
    else:
        return JsonResponse({'error':'invalid method'},status=400)

@csrf_exempt
def addLike(request):
    try:
        if request.method=="POST":
            token=request.headers.get('token')
            postId=request.headers.get('postId')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            email=decoded['email']
            if User_posts.objects.filter(id=postId).exists():
                post=User_posts.objects.get(id=postId).post
                likes=post['likes']
                if email in likes:
                    return JsonResponse({'error':'already liked'},status=400)
                else:
                    likes.append(email)
                post['likes']=likes
                User_posts.objects.filter(id=postId).update(post=post)
                return JsonResponse({'message':'like added'},status=200)
            else:
                return JsonResponse({'error':'post not found'},status=400)
        else:
            return JsonResponse({'error':'invalid method'},status=400)
    except Exception as e:
        return JsonResponse({'error':str(e)},status=400)

@csrf_exempt
def removeLike(request):
    try:
        if request.method=="POST":
            token=request.headers.get('token')
            postId=request.headers.get('postId')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            email=decoded['email']
            if User_posts.objects.filter(id=postId).exists():
                post=User_posts.objects.get(id=postId).post
                likes=post['likes']
                if email in likes:
                    likes.remove(email)
                else:
                    return JsonResponse({'error':'already unliked'},status=400)
                post['likes']=likes
                User_posts.objects.filter(id=postId).update(post=post)
                return JsonResponse({'message':'unlike added'},status=200)
            else:
                return JsonResponse({'error':'post not found'},status=400)
        else:   
            return JsonResponse({'error':'invalid method'},status=400)
    except Exception as e:
        error=str(e)
        return JsonResponse({'error':error},status=400)


@csrf_exempt
def addComment(request):
    try:
        if request.method=="POST": 
           token=request.headers.get('token')
           postId=request.headers.get('postId')
           comment=request.headers.get('comment')
           decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
           email=decoded['email']
           if User_posts.objects.filter(id=postId).exists():
               post=User_posts.objects.get(id=postId).post
               comments=post['comments']
               createdTime=datetime.datetime.now()
               createdTime=createdTime.strftime("%d/%m/%Y %H:%M:%S")
               createdTime=str(createdTime)
               comments.append({'user':email,'comment':comment,'createdTime':createdTime})
               comment_id=len(comments)-1
               post['comments']=comments
               User_posts.objects.filter(id=postId).update(post=post)
               return JsonResponse({'message':'comment added','commentId':comment_id},status=200)
           else:
               return JsonResponse({'error':'post not found'},status=400)
        else:
            return JsonResponse({'error':'invalid method'},status=400)
    except Exception as e:
        error=str(e)
        return JsonResponse({'error':error},status=400)