import pytz
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Like

@csrf_exempt
def getLikes(request):
    data = JSONParser().parse(request)
    response = {
        "likes": Like.objects.filter(article=data['url']).count(),
        "liked": "favorite" if Like.objects.filter(article=data['url'], user=data['token']) else "favorite_border"
    }
    return JsonResponse(response, safe=False)


@csrf_exempt
def addLike(request):
    data = JSONParser().parse(request)
    like, created = Like.objects.get_or_create(article=data['url'], user=data['token'])
    if (created):
        like.save()
    else:
        like.delete()
    return JsonResponse("ok", safe=False)