from django.shortcuts import *
from django.contrib.auth.decorators import login_required
from SocialNetworkHarvester_v1p0.jsonResponses import *
from AspiraUser.models import getUserSelection, resetUserSelection
import re
from Youtube.models import *

from SocialNetworkHarvester_v1p0.settings import viewsLogger, DEBUG
log = lambda s: viewsLogger.log(s) if DEBUG else 0
pretty = lambda s: viewsLogger.pretty(s) if DEBUG else 0


plurial = lambda i: 's' if int(i)>1 else ''


validFormNames = [
        'YTAddChannel',
        'YTRemoveChannel',
        'YTAddPlaylist',
        'YTRemovePlaylist',
    ]


def formBase(request, formName):
    if not request.user.is_authenticated(): return jsonUnauthorizedError(request)
    if not formName in validFormNames: return jsonBadRequest(request, 'Specified form does not exists')
    try:
        return globals()[formName](request)
    except:
        viewsLogger.exception("ERROR OCCURED IN YOUTUBE AJAX WITH FORM NAME '%s'" % formName)
        return jsonUnknownError(request)


def YTAddChannel(request):
    if not 'channelURL' in request.POST and not 'Browse' in request.FILES : return jsonBadRequest(request, 'No channel url specified')
    channelUrls = request.POST.getlist('channelURL')
    if 'Browse' in request.FILES:
        channelUrls += readUrlsFromCSV(request)
    invalids = addChannels(request,channelUrls)

    numChannelAdded = len(channelUrls) - len(invalids)
    if not numChannelAdded:
        return jResponse({
            'status': 'exception',
            'errors': ['"%s" is an invalid channel URL'%url for url in invalids],
        })
    return jResponse({
        'status':'ok',
        'messages': ['%s channel%s have been added to your list (%i error%s)'%(numChannelAdded, plurial(numChannelAdded),
                                                                            len(invalids), plurial(len(invalids)))]
    })


def readUrlsFromCSV(request):
    return []

#@viewsLogger.debug(showArgs=True)
def addChannels(request,channelUrls):
    profile = request.user.userProfile
    invalids = []
    for url in channelUrls:
        newChannel = None
        match = re.match(r'https?://www.youtube.com/user/(?P<username>[\w\.-]+)/?.*',url)
        if match:
            newChannel,new = YTChannel.objects.get_or_create(userName=match.group('username'))
        else:
            match = re.match(r'https?://www.youtube.com/channel/(?P<channelId>[\w\.-]+)/?.*', url)
            if match:
                newChannel,new = YTChannel.objects.get_or_create(_ident=match.group('channelId'))
            else:
                invalids.append(url)
        if newChannel:
            profile.ytChannelsToHarvest.add(newChannel)
            profile.save()
    return invalids


def YTRemoveChannel(request):
    return HttpResponse("YTRemoveChannel")


@viewsLogger.debug(showArgs=True)
def YTAddPlaylist(request):
    if not 'playlistURL' in request.POST and not 'Browse' in request.FILES: return jsonBadRequest(request,
                                                                                                 'No playlist url specified')
    channelUrls = request.POST.getlist('channelURL')
    if 'Browse' in request.FILES:
        channelUrls += readUrlsFromCSV(request)
    invalids = addChannels(request, channelUrls)

    numChannelAdded = len(channelUrls) - len(invalids)
    if not numChannelAdded:
        return jResponse({
            'status': 'exception',
            'errors': ['"%s" is an invalid channel URL' % url for url in invalids],
        })
    return jResponse({
        'status': 'ok',
        'messages': ['%s channel%s have been added to your list (%i error%s)' % (numChannelAdded, plurial(numChannelAdded),
                                                                                 len(invalids), plurial(len(invalids)))]
    })


def YTRemovePlaylist(request):
    return HttpResponse('YTRemovePlaylist')