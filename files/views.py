from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
import os
from .models import File
from django.core.files import File as fileReader
import urllib.request
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from PIL import Image
import PIL
from rest_framework import status


apiUrl = "http://localhost:8000"

def getFiles(request, index):
    files = File.objects.filter(hidden=False).order_by('-date')
    response = {
        "files": [],
        "noMoreFiles": (len(files) - 16 * (index - 1)) < 16
    }
    for file in files[16 * (index - 1): 16 * index]:
        response["files"].append({
            "id": file.id,
            "name": file.file.name,
            "imageUrl": apiUrl + file.file.url
        })
    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)

def removeFile(request, id):
    file = File.objects.get(id=id)
    if os.path.exists(os.getcwd().replace("\\", "/") + "/media/" + str(file.file)):
        os.remove(os.getcwd().replace("\\", "/") + "/media/" + str(file.file))
    file.delete()
    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def addFile(request):
    file = File.objects.create(file=request.FILES['file'])
    file.save()
    compressImage(file.id)
    return JsonResponse(file.id, status=status.HTTP_200_OK, safe=False)


def uploadFile(request, name=False, path="", hidden=False):
    tmpFile = request.FILES['file']
    filename = name if name else tmpFile.name
    extension = os.path.splitext(tmpFile.name)[-1]
    filePath = default_storage.save(settings.MEDIA_ROOT + path + filename + extension, ContentFile(tmpFile.read()))
    file = File.objects.create(file = filePath)
    file.hidden = hidden
    file.save()
    compressImage(file.id, path)
    return file.id

def addUserPhoto(imageUrl, usertoken):
    image = File.objects.create()
    result = urllib.request.urlretrieve(imageUrl + "?.jpg", settings.MEDIA_ROOT + '/users/' + usertoken + ".jpg")
    image.file = settings.MEDIA_ROOT + '/users/' + usertoken + ".jpg"
    image.hidden = True
    image.save()
    compressImage(image.id, "/users")
    return image.id

def getFile(id, path=""):
    if File.objects.filter(id = id).exists():
        return apiUrl + "/media/" + path + os.path.basename(File.objects.get(id = id).file.name)
    else:
        return ""

def compressImage(id, path=""):
    image = settings.MEDIA_ROOT + path + '/' + os.path.basename(File.objects.get(id = id).file.name)
    im = Image.open(image)
    im.save(image, optimize=True, quality = 40)