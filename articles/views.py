from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from .models import Article, Survey, Variant, Vote
from profiles.models import Profile
from files.models import File
from files.views import getFile
from readlists.views import addView

apiUrl = "http://infohub.pythonanywhere.com/api"


def formatDate(date):
    new_date = date.strftime("%d %B %Y, %H:%M").split()
    new_date[1] = new_date[1].capitalize()
    new_date = " ".join(new_date)
    return new_date


def getArticle(request, url):
    article = Article.objects.filter(url=url)
    if (not article.exists()):
        return JsonResponse("Nu am găsit acest articol", safe=False)
    article = article[0]
    article.views += 1
    article.save()
    response = {
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "subtitle": article.subtitle,
        "draft" : article.draft,
        "details" : {
            "date": formatDate(article.date),
            "hideViews": article.hideViews,
            "views": article.views,
        },
        "tags": article.tags.split(',' if article.tags.strip() else None),
        "coverImageDescription": article.coverImageDescription,
        "imageUrl": getFile(article.coverImage)
    }
    return JsonResponse(response, safe=False)

def getArticleToEdit(request, url):
    article = Article.objects.get_or_create(url=url)[0]
    response = {
        "id": article.id,
        "title": article.title,
        "text": article.text,
        "draft": article.draft,
        "framework" : article.framework,
        "subtitle": article.subtitle,
        "hideViews": article.hideViews,
        "tags": article.tags.split(',' if article.tags.strip() else None),
        "coverImage": article.coverImage,
        "imageUrl": getFile(article.coverImage),
        "coverImageDescription": article.coverImageDescription,
        "surveys" : getSurveysToEdit(article.url)
    }
    return JsonResponse(response, safe=False)


@csrf_exempt
def editArticle(request):
    data = JSONParser().parse(request)
    article = Article.objects.get(id=data['id'])
    if (article.title != data['title']):
        article.url = createUrl(data['title'].replace(' ', '-'))
    article.title = data['title']
    article.subtitle = data['subtitle']
    article.text = data['text']
    article.draft = data['draft']
    article.hideViews = data['hideViews']
    article.tags = ",".join(data['tags']).replace('#', '').lower()
    article.coverImage = data['coverImage']
    article.coverImageDescription = data["coverImageDescription"]
    article.framework = False
    for survey in Survey.objects.filter(article=article.url):
        for variant in Variant.objects.filter(survey=survey.id):
            variant.delete()
        survey.delete()
    for survey in data['surveys']:
        newSurvey = Survey.objects.create(
            article=article.url, question=survey['question'])
        newSurvey.save()
        for variant in survey['variants']:
            Variant.objects.create(survey=newSurvey.id, content=variant[0]).save()
    article.save()
    return JsonResponse(article.url, safe=False)

def createUrl(title, id=-1):
    articles = Article.objects.filter(url=title)
    if (len(articles)):
        for article in articles:
            if (article.id != id):
                title += '1'
                return createUrl(title)
    return title

@csrf_exempt
def getArticles(request, index):
    articles = []
    articles_total_raw = Article.objects.all().filter(draft=False).order_by("-date")
    articles_raw = Article.objects.all().filter(draft=False).order_by("-date")[7 * (index - 1): 7 * index]
    for article in articles_raw:
        articles.append({
            "url": article.url,
            "title": article.title,
            
            "text": article.text,
            "hideViews": article.hideViews,
            "details" : {
                "views": article.views,
                "date": formatDate(article.date),
            },
            "imageUrl": getFile(article.coverImage)
        })
    response = {
        "articles": articles,
        "noMoreArticles": (len(articles_total_raw) - 7 * (index - 1)) < 7
    }
    return JsonResponse(response, safe=False)

def getDrafts(request):
    articles = []
    for article in Article.objects.filter(draft=True):
        articles.append({
            "url": article.url,
            "title": article.title,
            "text": article.text,
            "imageUrl": getFile(article.coverImage)
        })
    return JsonResponse(articles, safe=False)

def getSlider(request):
    response = []
    articles = Article.objects.filter(draft=False).order_by("-date")
    for article in articles[: 5]:
        response.append({
            "url": article.url,
            "title": article.title,
            "imageUrl": getFile(article.coverImage)
        })
    return JsonResponse(response, safe=False)

def getRightSideArticles(request):
    response = []
    articles = Article.objects.filter(draft=False).order_by("-date")
    for article in articles[5 : 9]:
        response.append({
            "url": article.url,
            "title": article.title,
            "imageUrl": getFile(article.coverImage)
        })
    return JsonResponse(response, safe=False)

def getCategoryArticles(request, tag):
    response = []
    for article in Article.objects.filter(tags__contains=tag).filter(draft=False).order_by("-date")[: 5]:
        response.append({
            "url": article.url,
            "title": article.title,
            "imageUrl": getFile(article.coverImage)
        })
    return JsonResponse(response, safe=False)

def deleteArticle(request, id):
    article = Article.objects.get(id=id).delete()
    return JsonResponse("ok", safe=False)

@csrf_exempt
def search(request):
    def prepare(word):
        return word.lower().replace('ț', 't').replace('ș', 's').replace('î', 'i').replace('â', 'a').replace('ă', 'a')

    def prepareWordList(wordList):
        for i in ["și", "sau", "de", "care", "la", "a", "fi", "eu", "ea", "el", "dar", "tu"]:
            if i in wordList:
                wordList.remove(i)
        return wordList
    searchText = JSONParser().parse(request)['text']
    wordsList = prepareWordList(searchText.strip().split(' '))
    response = []
    articles = Article.objects.filter(draft=False).order_by("-date")
    if searchText[0] == "#":
        tag = searchText.replace('#', '')
        for article in articles:
            if tag in article.tags.split(","):
                response.append({
                    "url": article.url,
                    "title": article.title,
                    "text": article.text,
                    "imageUrl": getFile(article.coverImage)
                })
        return JsonResponse(response, safe=False)
    for article in articles:
        articleToAppend = {
            "url": article.url,
            "title": article.title,
            "text": article.text,
            "imageUrl": getFile(article.coverImage)
        }
        for word in wordsList:
            for wordOfTitle in prepareWordList(article.title.split(" ")):
                if prepare(word) in prepare(wordOfTitle) and articleToAppend not in response:
                    response.append(articleToAppend)
            for wordOfText in prepareWordList(article.text.split(' ')):
                if prepare(word) in prepare(wordOfText) and articleToAppend not in response:
                    response.append(articleToAppend)
    return JsonResponse(response, safe=False)

def getSurveysToEdit(article):
    response = []
    for survey in Survey.objects.filter(article=article):
        surveyRaw = {
            "id" : survey.id,
            "question" : survey.question,
            "variants" : [],
        }
        for variant in Variant.objects.filter(survey=survey.id):
            surveyRaw['variants'].append([variant.content])
        response.append(surveyRaw)
    return response

@csrf_exempt
def getSurvey(request):
    data = JSONParser().parse(request)
    surveysRaw = Survey.objects.filter(article=data['url'])
    surveys = []
    for survey in surveysRaw:
        survey_raw = ({
            "id": survey.id,
            "question": survey.question,
            "variants": [],
            "votes": 0
        })
        variants = Variant.objects.filter(survey=survey.id)
        for variant in variants:
            survey_raw['votes'] += Vote.objects.filter(variant=variant.id).count()
            variant = {
                "id": variant.id,
                "content": variant.content,
                "voted": bool(Vote.objects.filter(user=data.get('user'), variant=variant.id).count()),
                "votes": Vote.objects.filter(variant=variant.id).count()
            }
            survey_raw['variants'].append(variant)
        surveys.append(survey_raw)
    return JsonResponse(surveys, safe=False)

@csrf_exempt
def vote(request):
    data = JSONParser().parse(request)
    vote, created = Vote.objects.get_or_create(variant=data['id'], user=data['user'])
    vote.save() if created else vote.delete()
    return JsonResponse("ok", safe=False)
