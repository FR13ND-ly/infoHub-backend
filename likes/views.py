import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Like
from rest_framework import status

@csrf_exempt
def getLikes(request):
    data = JSONParser().parse(request)
    response = {
        "likes": Like.objects.filter(article=data['article']).count(),
        "liked": "favorite" if Like.objects.filter(article=data['article'], user=data.get('user')) else "favorite_border"
    }
    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def addLike(request):
    data = JSONParser().parse(request)
    like, created = Like.objects.get_or_create(article=data['article'], user=data['user'])
    if (created):
        like.save()
    else:
        like.delete()
    return JsonResponse({}, status=status.HTTP_200_OK)