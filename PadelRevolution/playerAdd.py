
from google.appengine.api import users
from google.appengine.ext import ndb

from players import Player

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class PlayerAddHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "registrar": "Registrar Jugador",
                "registro": ""
            }
            template = JINJA_ENVIRONMENT.get_template("playerAdd.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")

    def post(self):
        name = self.request.get("nombre","")
        surname = self.request.get("apellidos", "")
        birthdate = self.request.get("fecha", "")
        picture = self.request.get("foto", "")
        phonenumber = self.request.get("telefono", "")
        team = self.request.get("equipo", "")

        user = users.get_current_user()
        player = Player(usuario=user.nickname(), nombre=name, apellidos=surname, fechanacimiento=birthdate, foto=picture
                        , telefono=phonenumber, equipo=team)
        print(player)
        player.put()

        user_name = user.nickname()
        access_link = users.create_logout_url("/")

        template_values = {
            "user_name": user_name,
            "access_link": access_link,
            "registrar": "Registrar Jugador",
            "registro": "Jugador registrado correctamente"
        }
        template=JINJA_ENVIRONMENT.get_template("playerAdd.html")
        self.response.write(template.render(template_values))


