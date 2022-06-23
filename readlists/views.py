from django.shortcuts import render
from .models import List, ListItem, View
from likes.models import Like
from files.views import getFile
from articles.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from profiles.models import Profile
from rest_framework import status

@csrf_exempt
def getLightLists(request):
    data = JSONParser().parse(request)
    response = []
    for list in List.objects.filter(user=data.get('user')):
        response.append({
            "id" : list.id,
            "name": list.name,
            "public": list.public,
            "added": bool(ListItem.objects.filter(article=data['article'], List=list.pk))
        })
    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)

@csrf_exempt
def addToList(request):
    data = JSONParser().parse(request)
    nlist, created = ListItem.objects.get_or_create(
        List=data['List'],
        article=data['article']
    )
    if (created):
        nlist.save()
    else:
        nlist.delete()
    return JsonResponse({}, status=status.HTTP_200_OK)

@csrf_exempt
def getLists(request, token):
    response = []
    historicRaw = View.objects.filter(user=token).order_by('-date')
    history = {
        "id": 'istoric',
        "name": "Istoric",
        "lastPreview": "",
        "preview": [],
        "icon" : "history",
        "length": historicRaw.count()
    }
    for historic in historicRaw:
        if len(history['preview']) > 2:
            break
        article = Article.objects.filter(url=historic.article)
        if article.exists():
            article = article[0]
            history['preview'].append({
                "title": article.title,
                "url": article.url,
                "imageUrl": getFile(article.coverImage, "/medium/")
            })
            history['lastPreview'] = getFile(article.coverImage, "/medium/")
        else:
            historic.delete()
    response.append(history)
    likesRaw = Like.objects.filter(user=token).order_by('-date')
    likes = {
        "id": 'aprecieri',
        "name": "Apreciate",
        "lastPreview": "",
        "preview": [],
        "icon" : "favorite",
        "length": likesRaw.count()
    }
    for like in likesRaw:
        if len(likes['preview']) > 2:
            break
        article = Article.objects.filter(url=like.article)
        if article.exists():
            article = article[0]
            likes['preview'].append({
                "title": article.title,
                "url": article.url,
                "imageUrl": getFile(article.coverImage, "/medium/")
            })
            likes['lastPreview'] = getFile(article.coverImage, "/medium/")
        else:
            like.delete()
    response.append(likes)
    for list in List.objects.filter(user=token).order_by('date'):
        listItems = ListItem.objects.filter(List=list.id)
        responseList = {
            "id": list.id,
            "name": list.name,
            "lastPreview": "",
            "preview": [],
            "icon" : list.icon,
            "length": listItems.count()
        }
        for listItem in listItems:
            if len(responseList['preview']) > 2:
                break
            article = Article.objects.filter(url=listItem.article)
            if article.exists():
                article = article[0]
                responseList['preview'].append({
                    "title": article.title,
                    "url": article.url,
                    "imageUrl": getFile(article.coverImage, "/medium/")
                })
                responseList['lastPreview'] = getFile(article.coverImage)
            else:
                listItem.delete()
        response.append(responseList)
    return JsonResponse(response, status=status.HTTP_200_OK, safe=False)


@csrf_exempt
def getListInfo(request):
    data = JSONParser().parse(request)
    if not data.get('user'):
        return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
    user = Profile.objects.get(token=data.get('user'))
    response = {
        "name": '',
        "author": user.user.first_name,
        "public": False,
        "own": True,
        "length": 0,
        "editable" : True,
        "icon" : ''
    }
    if data['id'] == -1:
        response['length'] = View.objects.filter(user=data['user']).count()
        response['name'] = "Istoric"
        response['editable'] = False
    elif data['id'] == -2:
        response['length'] = Like.objects.filter(user=data['user']).count()
        response['name'] = "Aprecieri"
        response['editable'] = False
    else:
        list = List.objects.get(id=data['id'])
        if list.user != user.token and list.public:
            return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
        response['length'] = len(ListItem.objects.filter(List=data['id']))
        response['name'] = list.name
        response['public'] = not list.public
        response['own'] = list.user == user.token
        response['editable'] = list.editable
        response['icon'] = list.icon
        if (not response['own']):
            response['author'] = Profile.objects.get(
                token=list.user).user.first_name
    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def getListArticles(request):
    data = JSONParser().parse(request)
    index = data.get("index", 1)
    response = {
        "articles": [],
        "noMoreArticles": True,
    }
    if not data.get('user'):
        return JsonResponse({}, status=status.HTTP_401_UNAUTHORIZED)
    articles_raw = []
    if data['id'] == -1:
        articles_raw = View.objects.filter(user=data['user']).order_by("-date")
    elif data['id'] == -2:
        articles_raw = Like.objects.filter(user=data['user']).order_by("-date")
    else:
        articles_raw = ListItem.objects.filter(List=data['id']).order_by("-date")
    response["noMoreArticles"] = (len(articles_raw) - 30 * (index - 1)) < 30
    for article_raw in articles_raw[30 * (index - 1): 30 * index]:
        if (int(data['id']) > 0):
            if (not Article.objects.filter(url=article_raw.article)):
                article_raw.delete()
                continue
            article = Article.objects.get(url=article_raw.article)
        else:
            if (not Article.objects.filter(url=article_raw.article)):
                article_raw.delete()
                continue
            article = Article.objects.get(url=article_raw.article)
        response['articles'].append({
            "url": article.url,
            "title": article.title,
            "text": article.text,
            "imageUrl": getFile(article.coverImage, "/small/")
        })
    return JsonResponse(response, status=status.HTTP_200_OK)


@csrf_exempt
def addList(request):
    data = JSONParser().parse(request)
    List.objects.create(
        name=data['name'],
        user=data['user'],
        public=data['access']
    )
    return JsonResponse({}, status=status.HTTP_201_CREATED)


@csrf_exempt
def deleteList(request, id):
    List.objects.get(id=id).delete()
    for listItem in ListItem.objects.filter(List=id):
        listItem.delete()
    return JsonResponse("ok", safe=False)

@csrf_exempt
def editList(request, id):
    data = JSONParser().parse(request)
    readList = List.objects.get(id = id)
    readList.name = data['name']
    readList.public = not data['public']
    readList.icon = data['icon']
    readList.save()
    return JsonResponse({}, status=status.HTTP_200_OK)

@csrf_exempt
def addView(request):
    data = JSONParser().parse(request)
    if Article.objects.filter(url = data.get('article')).exists():
        newView = View.objects.create(article = data['article'], user = data.get('user'))
        newView.save()
    return JsonResponse({}, status=status.HTTP_201_CREATED)