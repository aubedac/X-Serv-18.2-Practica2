from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context, RequestContext
from models import shortedUrl
import urllib2
# Create your views here.

def homepage(request):
    if (request.method == "GET"):
        currentUrls = shortedUrl.objects.all()
        template = get_template("home.html")
        currentList = '<p> Current state: </p>'
        for url in currentUrls:
            currentList += '<li>' + url.original + " --->> "\
            '<a href=' + url.original + '> http://localhost:8000/' + str(url.id)  + '</a>'
    elif (request.method == "POST"):
        currentList = ""
        shorted = ""
        found = False
        template = get_template("emptyQS.html")
        requestUrl = urllib2.unquote(request.body.split("=",2)[2])
        try:
            parsedRequest = requestUrl.split("//")[1]
        except IndexError:
            parsedRequest = requestUrl

        parsedRequest = "https://" + parsedRequest
        if parsedRequest == "https://":
            template = get_template("emptyQS.html")
        else:
            shortedList = shortedUrl.objects.all()
            for url in shortedList:
                found = str(url.original) == str(parsedRequest)

            if found:
                currentList = ""
                template = get_template("found.html")
            else:
                database = shortedUrl(original=parsedRequest)
                database.save()
                n = database.id
                currentList = '<a href=' + parsedRequest + '> http://localhost:8000/'+ str(n) + '</a>'
                template = get_template("done.html")

    context = RequestContext(request, {"urls" : currentList})
    return HttpResponse(template.render(context))

def shorted(request, index):
    try:
        url = shortedUrl.objects.get(id=index)
        answer = url.original
    except:
        template = get_template('notFound.html')
        return HttpResponse(template.render())

    return HttpResponseRedirect(answer)

def notFound(request):
    template = get_template('notFound.html')
    return HttpResponse(template.render())
