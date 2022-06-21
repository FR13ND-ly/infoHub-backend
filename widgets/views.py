from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Widget
from files.views import getFile
from rest_framework import status

def getWidget(request, id):
    widget = Widget.objects.get(id = id)
    response = {
        "text" : widget.text,
        "link" : widget.link,
        "imageUrl" : getFile(widget.image),
        "author" : widget.author,
        "activated" : widget.activated
    }
    return JsonResponse(response, status=status.HTTP_200_OK)

def getWidgets(request):
    response = []
    for widget in Widget.objects.all():
        response.append({
        "text" : widget.text,
        "link" : widget.link,
        "imageUrl" : getFile(widget.image),
        "imageId" : widget.image,
        "author" : widget.author,
        "activated" : widget.activated
    })
    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def editWidget(request, id):
    data = JSONParser().parse(request)
    widget = Widget.objects.get(id = id)
    widget.text = data['text']
    widget.link = data['link']
    widget.image = data['imageId']
    widget.author = data['author']
    widget.activated = data['activated']
    widget.save()
    return JsonResponse({}, status=status.HTTP_200_OK)