from django.shortcuts import render
from .models import List, ListItem, View
from likes.models import Like
from files.views import getFile
from articles.models import Article
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from profiles.models import Profile

@csrf_exempt
def getLightLists(request):
    data = JSONParser().parse(request)
    response = []
    for ulist in List.objects.filter(user=data['user']):
        response.append({
            "id" : ulist.id,
            "name": ulist.name,
            "public": ulist.public,
            "added": bool(ListItem.objects.filter(article=data['article'], List=ulist.pk))
        })
    return JsonResponse(response, safe=False)

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
    return JsonResponse("ok", safe=False)

@csrf_exempt
def getLists(request, token):
    response = []
    historic_raw = View.objects.filter(user=token).order_by('-date')
    history = {
        "id": 'istoric',
        "name": "Istoric",
        "lastPreview": "",
        "preview": [],
        "icon" : "history",
        "length": historic_raw.count()
    }
    if len(historic_raw):
        for historic in historic_raw[0: 3]:
            if (not len(Article.objects.filter(url=historic.article))):
                Article.objects.filter(url=historic.article).delete()
            article = Article.objects.filter(url=historic.article)[0]
            history['preview'].append({
                "title": article.title,
                "url": article.url,
                "imageUrl": getFile(article.coverImage)
            })
            history['lastPreview'] = getFile(article.coverImage)
    response.append(history)
    likes_raw = Like.objects.filter(user=token).order_by('-date')
    likes = {
        "id": 'aprecieri',
        "name": "Apreciate",
        "lastPreview": "",
        "preview": [],
        "icon" : "favorite",
        "length": likes_raw.count()
    }
    if len(likes_raw):
        for like in likes_raw[0: 3]:
            article = Article.objects.filter(url=like.article)[0]
            likes['preview'].append({
                "title": article.title,
                "url": article.url,
                "imageUrl": getFile(article.coverImage)
            })
            likes['lastPreview'] = getFile(article.coverImage)
    response.append(likes)
    for tlist in List.objects.filter(user=token).order_by('date'):
        rlist_raw = ListItem.objects.filter(List=tlist.id)
        rlist = {
            "id": tlist.id,
            "name": tlist.name,
            "lastPreview": "",
            "preview": [],
            "icon" : tlist.icon,
            "length": rlist_raw.count()
        }
        if len(rlist_raw):
            for listItem in rlist_raw[0: 3]:
                article = Article.objects.get(url=listItem.article)
                rlist['preview'].append({
                    "title": article.title,
                    "url": article.url,
                    "imageUrl": getFile(article.coverImage)
                })
                rlist['lastPreview'] = getFile(article.coverImage)
        response.append(rlist)
    return JsonResponse(response, safe=False)


@csrf_exempt
def getListInfo(request):
    data = JSONParser().parse(request)
    if not data.get('user'):
        return JsonResponse({}, safe=False)
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
    articles_raw = []
    if data['id'] == -1:
        response['length'] = len(View.objects.filter(user=data['user']))
        response['name'] = "Istoric"
        response['editable'] = False
    elif data['id'] == -2:
        response['length'] = len(Like.objects.filter(user=data['user']))
        response['name'] = "Aprecieri"
        response['editable'] = False
    else:
        nList = List.objects.get(id=data['id'])
        response['length'] = len(ListItem.objects.filter(List=data['id']))
        response['name'] = nList.name
        response['public'] = not nList.public
        response['own'] = nList.user == user.token
        response['editable'] = nList.editable
        response['icon'] = nList.icon
        if (not response['own']):
            response['author'] = Profile.objects.get(
                token=nList.user).user.username
    return JsonResponse(response, safe=False)


@csrf_exempt
def getListArticles(request, index=1):
    data = JSONParser().parse(request)
    response = {
        "articles": [],
        "noMoreArticles": True,
    }
    if not data.get('user'):
        return JsonResponse(response, safe=False)
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
            "imageUrl": getFile(article.coverImage)
        })
    return JsonResponse(response, safe=False)


@csrf_exempt
def addList(request):
    data = JSONParser().parse(request)
    List.objects.create(
        name=data['name'],
        user=data['user'],
        public=data['access']
    )
    return JsonResponse("ok", safe=False)


@csrf_exempt
def deleteList(request, id):
    List.objects.get(id=id).delete()
    for listItem in ListItem.objects.filter(List=id):
        listItem.delete()
    return JsonResponse("ok", safe=False)


@csrf_exempt
def changePublicList(request):
    data = JSONParser().parse(request)
    nList = List.objects.get(id=data['id'])
    nList.public = data['publicity']
    nList.save()
    return JsonResponse("ok", safe=False)

@csrf_exempt
def editList(request, id):
    data = JSONParser().parse(request)
    readList = List.objects.get(id = id)
    readList.name = data['name']
    readList.public = not data['public']
    readList.icon = data['icon']
    readList.save()
    return JsonResponse("ok", safe=False)


@csrf_exempt
def changeTitleList(request):
    data = JSONParser().parse(request)
    nList = List.objects.get(id=data['id'])
    nList.name = data['name']
    nList.save()
    return JsonResponse("ok", safe=False)

@csrf_exempt
def addView(request):
    data = JSONParser().parse(request)
    newView = View.objects.create(article = data['article'], user = data.get('user'))
    newView.save()
    return JsonResponse("ok", safe=False)