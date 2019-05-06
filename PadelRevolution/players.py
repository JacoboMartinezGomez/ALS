from google.appengine.ext import ndb


class Player(ndb.Model):
    usuario = ndb.StringProperty(required = True)
    nombre = ndb.StringProperty(required = True)
    apellidos = ndb.StringProperty(required = True)
    fechanacimiento = ndb.StringProperty(required=True)
    foto = ndb.StringProperty()
    telefono = ndb.StringProperty(required = True)
    equipo = ndb.StringProperty(required = True)