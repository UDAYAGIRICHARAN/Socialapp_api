
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import User_auth,User_followers
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
def userAuthentification(request):
    try:

        if request.method == 'POST':
            email = request.headers.get('email')
            password = request.headers.get('password')
            print(email, password)
            if User_auth.objects.filter(email=email).exists():
                if User_auth.objects.get(email=email).password == password:
                    #jwt token
                    print('token')
                    token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, settings.SECRET_KEY, algorithm='HS256')
                    print(token)
                    token = token.decode('utf-8')
                 
                    response_data = {'token': token}
                    return JsonResponse(response_data, status=200)
                else:
                    return JsonResponse({'error': 'Invalid password'}, status=400)
            else:
                #create User_auth
                User_auth.objects.create(email=email, password=password)
                token = jwt.encode({'email': email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, settings.SECRET_KEY, algorithm='HS256')
                print(token)
                token = token.decode('utf-8')
                 
                response_data = {'token': token}
                return JsonResponse({'response_data': response_data}, status=200)
        else:
            return JsonResponse({'error': 'Invalid method'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
def userFollow(request):
    try:
        # Decode token and get email
        token = request.headers.get('token')
        follower_id = request.headers.get('followerId')
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        email = decoded['email']
        print(email, follower_id)

      

        # Check if follower exists
        if User_followers.objects.filter( user_email=email,  follower_email =follower_id).exists():
            return JsonResponse({'error': 'follower already exists'}, status=400)

        # Get User_auth instance for follower_id
        if User_auth.objects.filter(email=follower_id).exists():
            if User_auth.objects.filter(email=follower_id).exists():
                User_followers.objects.create( user_email=email,  follower_email =follower_id)
                return JsonResponse({'response_data': 'follower added'}, status=200)
            else:
                return JsonResponse({'response_data':'User doesnot exists'},status=400)
        else:
            return JsonResponse({'error': 'follower does not exist'}, status=400)

    except User_auth.DoesNotExist:
        return JsonResponse({'error': 'User_auth object does not exist'}, status=400)

    except Exception as e:
        error = str(e) 
        return JsonResponse({'error': error}, status=400)

@csrf_exempt
def userUnFollow(request):
    try:
        if request.method == 'POST':
            token = request.headers.get('token')
            follower_id = request.headers.get('followerId')
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            email = decoded['email']
            print(email, follower_id)

        

            # Check if follower exists
            if User_followers.objects.filter( user_email=email,  follower_email =follower_id).exists():
                User_followers.objects.filter( user_email=email,  follower_email =follower_id).delete()
                return JsonResponse({'response_data': 'follower deleted'}, status=200)
            else:
                return JsonResponse({'error': 'follower does not exist'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid method'}, status=400)

    except User_auth.DoesNotExist:
        return JsonResponse({'error': 'User_auth object does not exist'}, status=400)

    except Exception as e:
        error = str(e) 
        return JsonResponse({'error': error}, status=400)
@csrf_exempt
def getFollowers(request):
    try:
        if request.method == 'GET':
            token=request.headers.get('token')
            decoded=jwt.decode(token,settings.SECRET_KEY,algorithms=['HS256'])
            email=decoded['email']
            list_of_followers=      list(User_followers.objects.filter(user_email=email).values_list('follower_email',flat=True))
            return JsonResponse({'userName':email,
                'response_data':list_of_followers},status=200)
        else:
            return JsonResponse({'error':'Invalid method'},status=400)
    except Exception as e:
        error=str(e)
        return JsonResponse({'error':error},status=400)

