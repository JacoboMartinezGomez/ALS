from google.appengine.ext import ndb


class PlayerFav(ndb.Model):
    playerkey = ndb.StringProperty(required=True)
    list = ndb.StringProperty(required=True)