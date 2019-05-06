#!/usr/bin/python
from google.appengine.api import users
from google.appengine.ext import ndb
from players import Player
from favs import PlayerFav

import os
import webapp2
import jinja2
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class PlayerDeleteHandler(webapp2.RequestHandler):
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
                player = ndb.Key(urlsafe=id).get()
                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "delete": "delete",
                    "player": player,
                }

                template = JINJA_ENVIRONMENT.get_template("playerDelete.html")
                self.response.write(template.render(template_values));

        else:
            self.redirect("/")

    def post(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")
            players = ndb.Key(urlsafe=self.request.get("id")).get()
            players.key.delete()

            contador = PlayerFav.query(PlayerFav.playerkey == self.request.get("id")).count()
            if contador > 0:
                access_token = self.request.get("id")
                gprofiles = PlayerFav.query(PlayerFav.playerkey == access_token)
                for g in gprofiles:
                    g.key.delete()

            players = Player.query(Player.usuario == user_name).order(Player.apellidos)
            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                "registro": "Jugador eliminado correctamente",
                "players": players,
            }

            template = JINJA_ENVIRONMENT.get_template("playerShowall.html")
            self.response.write(template.render(template_values));


            #time.sleep(5)
            #self.redirect("/playerShowall")
        else:
            self.redirect("/")
