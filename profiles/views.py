from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from .models import Profile
from files.views import addUserPhoto, getFile, uploadFile
from rest_framework import status
from readlists.models import List
from files.models import File

@csrf_exempt
def login(request):
    data = JSONParser().parse(request)
    user, created = User.objects.get_or_create(
        first_name=data['displayName'],
        email=data['email']
    )
    if (created):
        newList = List.objects.create(name = "Citește mai târziu", editable = False, user = data['uid'])
        newList.save()
        user.username = data['uid']
        user.save()
    profile, created = Profile.objects.get_or_create(
        token = data['uid'],
        user = user
    )
    if (created):
        profile.image = addUserPhoto(data['photoURL'], data['uid'])
        profile.save()
    response = {
        "imageUrl" : getFile(profile.image, "users/"),
        "image" : profile.image,
        "isStaff" : user.is_staff,
        "allowWriteComments" : profile.allowWriteComments,
        "allowChangeAvatar" : profile.allowChangeAvatar
    }
    return JsonResponse(response, status = status.HTTP_200_OK)

def getUserAuthorization(request, token):
    profile = Profile.objects.get(token = token)
    response = {
        "imageUrl" : getFile(profile.image, "users/"),
        "image" : profile.image,
        "isStaff" : profile.user.is_staff,
        "allowWriteComments" : profile.allowWriteComments,
        "allowChangeAvatar" : profile.allowChangeAvatar
    }
    return JsonResponse(response, status = status.HTTP_200_OK)

@csrf_exempt
def setUserImage(request, token):
    profile = Profile.objects.get(token = token)
    profile.image = uploadFile(request, token, "/users/", hidden = True)
    profile.save()
    return JsonResponse({}, status = status.HTTP_200_OK, safe=False)


def getAllUsers(request):
    response = []
    for profile in Profile.objects.order_by("-date"):
        response.append({
            "id" : profile.id,
            "username" : profile.user.first_name,
            "date" : profile.date,
            "imageUrl" : getFile(profile.image, "/users/"),
            "allowWriteComments" : profile.allowWriteComments,
            "allowChangeAvatar" : profile.allowChangeAvatar
        })
    return JsonResponse(response, status = status.HTTP_200_OK, safe=False)

@csrf_exempt
def updateUser(request):
    data = JSONParser().parse(request)
    profile = Profile.objects.get(id = data['id'])
    profile.allowWriteComments = data['allowWriteComments']
    profile.allowChangeAvatar = data['allowChangeAvatar']
    profile.save()
    return JsonResponse({}, status = status.HTTP_200_OK)

def setDefaultAvatar(request, id):
    profile = Profile.objects.get(id = id)
    profile.image = 16
    profile.save()
    return JsonResponse({}, status = status.HTTP_200_OK)

@csrf_exempt
def deleteUser(request, id):
    User.objects.get(id = Profile.objects.get(id = id).user.id).delete()
    return JsonResponse({}, status = status.HTTP_200_OK)