from google.appengine.api import users
from google.appengine.ext import ndb
from players import Player

import os
import webapp2
import jinja2
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class PlayerEditHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            try:
                id = self.request.GET['id']
            except:
                id = None

            if id == None:
                self.redirect("/main")
                return

            else:
                player = ndb.Key(urlsafe=self.request.GET['id']).get()
                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "player": player,
                }

                template = JINJA_ENVIRONMENT.get_template("playerEdit.html")
                self.response.write(template.render(template_values));

        else:
            self.redirect("/")

    def post(self):

        user = users.get_current_user()

        if user != None:

            player = ndb.Key(urlsafe=self.request.get("id")).get()

            player.nombre = self.request.get("nombre").strip()
            player.apellidos = self.request.get("apellidos").strip()
            player.fechanacimiento = self.request.get("fecha").strip()
            player.foto = self.request.get("foto").strip()
            player.telefono = self.request.get("telefono").strip()
            player.equipo = self.request.get("equipo").strip()
            player.usuario = user.nickname()

            #Guardar datos en BD
            player.put()

            #Prueba

            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            players = Player.query(Player.usuario == user_name).order(Player.apellidos)

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "players": players,
                "registro": "Jugador editado correctamente",
            }

            template = JINJA_ENVIRONMENT.get_template("playerShowall.html")
            self.response.write(template.render(template_values))

            #time.sleep(15)
            #self.redirect("/playerShowall")
        else:
            self.redirect("/")
