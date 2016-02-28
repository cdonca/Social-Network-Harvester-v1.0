
from AspiraUser.models import UserProfile
from django.contrib.auth.models import User
from .twUserUpdater import *
from .twFriendshipUpdater import *
from .twFollowersUpdater import *
from .twFavTweetUpdater import *

@twitterLogger.debug()
def harvestTwitter():
    #resetErrorsTwUser("_error_on_network_harvest")
    #resetErrorsTwUser("_error_on_update")
    try:
        all_profiles = UserProfile.objects.filter(twitterApp_parameters_error=False)
        clientList = getClientList(all_profiles)
        all_profiles = all_profiles.filter(twitterApp_parameters_error=False) # insures that his/her twitter app is valid
        clientQueue.maxsize = len(clientList)
        for client in clientList:
            clientQueue.put(client)

        threadList = []
        threadList += launchNetworkHarvestThreads(all_profiles)
        threadList += launchUpdaterTread()
        waitForThreadsToEnd(threadList)
    except:
        endAllThreads(threadList)
        raise

@twitterLogger.debug()
def launchUpdaterTread():
    allUserstoUpdate = orderQueryset(TWUser.objects.filter(_error_on_update=False), '_last_updated')
    updateThreads = []

    for user in allUserstoUpdate:
        updateQueue.put(user)

    threadNames = ['updater1']
    for threadName in threadNames:
        thread = TwUserUpdater(threadName)
        thread.start()
        updateThreads.append(thread)
    return updateThreads

def launchHarvesterThreads():
    pass


def launchNetworkHarvestThreads(profiles):
    twUsersToHarvest = []

    twUsers = profiles[0].twitterUsersToHarvest.filter(_error_on_network_harvest=False,protected=False)
    for profile in profiles[1:]:
        twUsers = twUsers | profile.twitterUsersToHarvest.filter(_error_on_network_harvest=False,protected=False)

    for twUser in orderQueryset(twUsers, '_last_friends_harvested'):
        friendsUpdateQueue.put(twUser)

    for twUser in orderQueryset(twUsers, '_last_followers_harvested'):
        followersUpdateQueue.put(twUser)

    for twUser in orderQueryset(twUsers, '_last_fav_tweet_harvested'):
        favoriteTweetUpdateQueue.put(twUser)


    threadList = []
    thread = TwFriendshipUpdater('friender1')
    thread.start()
    threadList.append(thread)
    thread = TwFollowersUpdater('follower1')
    thread.start()
    threadList.append(thread)
    thread = TwFavTweetUpdater('favtweeter1')
    thread.start()
    threadList.append(thread)
    return threadList

def waitForThreadsToEnd(threadList):
    while 1:
        if updateQueue.empty() and friendsUpdateQueue.empty() and \
        followersUpdateQueue.empty() and favoriteTweetUpdateQueue.empty():
            break
        if not exceptionQueue.empty():
#            exceptionQueueLock.acquire()
            (e, threadName) = exceptionQueue.get()
#            exceptionQueueLock.release()
            try:
                raise e
            except:
                twitterLogger.exception('An exception has been retrieved from a Thread. (%s)'%threadName)
                endAllThreads(threadList)
    endAllThreads(threadList)


#@twitterLogger.debug()
def getClientList(profiles):
    clientList = []
    for profile in profiles:
        client = createTwClient(profile)
        if client:
            clientList.append(client)
    return clientList

#@twitterLogger.debug()
def orderQueryset(queryset, dateTimeFieldName):
    isNull = dateTimeFieldName+"__isnull"
    lt = dateTimeFieldName+"__lt"
    ordered_elements = queryset.filter(**{isNull:True}) | \
                       queryset.filter(**{lt:today()}).order_by(dateTimeFieldName)
    return ordered_elements

#@twitterLogger.debug()
def createTwClient(profile):
    try:
        client = Client(
            name = "%s's App"%profile.user,
            ck = profile.twitterApp_consumerKey,
            cs = profile.twitterApp_consumer_secret,
            atk = profile.twitterApp_access_token_key,
            ats = profile.twitterApp_access_token_secret,
        )
        return client
    except tweepy.error.TweepError:
        profile.twitterApp_parameters_error = True
        profile.save()
        twitterLogger.exception('%s has got an invalid Twitter app'%profile.user)
        return None

@twitterLogger.debug()
def clearUpdatedTime():
    for twUser in TWUser.objects.filter(_last_updated__isnull=False):
        twUser._last_updated = None
        twUser.save()

@twitterLogger.debug(showArgs=True)
def resetErrorsTwUser(errorMarker):
    for twuser in TWUser.objects.filter(**{errorMarker:True}):
        setattr(twuser, errorMarker, False)
        twuser.save()

@twitterLogger.debug()
def endAllThreads(threadList):
    threadsExitFlag[0] = True
    for t in threadList:
        t.join()


class TwFollowerlistUpdater(CommonThread):

    def execute(self):
        pass

class TwFavoriteTweetUpdater(CommonThread):

    def execute(self):
        pass

class TwUserHarvester(CommonThread):

    def execute(self):
        pass

class TwHashtagHarvester(CommonThread):

    def execute(self):
        pass