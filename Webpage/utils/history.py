import datetime

from blog.models import blogPost
from web.models import infoPage
from jollen.models import nachricht_historie

'''
delete history older than one Month and if there are more than 7 from Models

Models:     blogPost -> blogPostHistory
            infoPage -> infoPageHistory
'''
def deleteOlderHistory():
    for alleBlogPosts in blogPost.objects.all():
        for hist in alleBlogPosts.history.all().order_by('-id'):
            if alleBlogPosts.history.all().count() > 7:
                break
            if (hist.date < datetime.now()- datetime.timedelta(days=30)):
                hist.delete()

    for allinfoPage in infoPage.objects.all():
        for hist in allinfoPage.history.all().order_by('-id'):
            if allinfoPage.history.all().count() > 7:
                break
            if (hist.date < datetime.now()- datetime.timedelta(days=30)):
                hist.delete()
    
    for Nachricht in nachricht_historie.objects.all().order_by('-id'):
        if nachricht_historie.objects.all().count() > 7:
            break
        if (Nachricht.date < datetime.now()- datetime.timedelta(days=120)):
            Nachricht.delete()

