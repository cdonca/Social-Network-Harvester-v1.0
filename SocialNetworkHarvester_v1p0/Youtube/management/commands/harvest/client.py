
from .globals import *
from apiclient.discovery import build

class Client():

    def __init__(self, apiKey):
        self.apiKey = apiKey
        self.api = build("youtube", "v3", developerKey=apiKey)
        self.reset()
        self.testApi()

    def __str__(self):
        return 'Youtube API client (%s)'%(self.apiKey)

    def testApi(self):
        self.api.i18nLanguages().list(part='snippet').execute()

    def reset(self):
        self.call = None
        self.req = None
        self.response = None

    def list(self, callName, *args, **kwargs):
        self.reset()
        assert hasattr(self.api, callName), 'YT API has no %s method'%callName
        call = getattr(self.api, callName)
        assert callable(call), '%s is not a callable method'%callName
        self.call = call
        self.req = call().list(*args, **kwargs)
        try:
            self.response = self.req.execute()
            return self.response
        except errors.HttpError as e:
            if hasattr(e, 'resp') and e.resp.status in [500]:
                log("ERROR 500 RECEIVED FROM YOUTUBE API. RETRYING IN 1 SEC")
                time.sleep(1000)
                return self.list(callName,*args,**kwargs)

    def next(self):
        assert self.call, 'Must first call "list()" method'
        self.req = self.call().list_next(self.req, self.response)
        self.response = None
        if self.req:
            self.response = self.req.execute()
        return self.response


def getClient():
    client = None
    while not client:
        if not clientQueue.empty():
            client = clientQueue.get()
    #log('client found')
    return client

def returnClient(client):
    assert not clientQueue.full(),"Client Queue is already full. There is a Client that has been returned twice!"
    #log('client returned')
    clientQueue.put(client)



class ExitFlagRaised(Exception):
    pass