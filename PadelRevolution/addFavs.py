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
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)


class AddFavsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            key = self.request.get("id").strip()
            # key = self.request.get("id", "")

            contador = PlayerFav.query(ndb.AND(PlayerFav.playerkey == key, PlayerFav.list == user_name)).count()

            if contador == 0:
                players = Player.query(Player.usuario == user_name).order(Player.apellidos)
                favs = PlayerFav(playerkey=key, list=user_name)
                favs.put()

                players = Player.query()
                favs = PlayerFav.query(PlayerFav.list == user_name)

                favoritos = []

                for player in players:
                    for fav in favs:
                        if player.key.urlsafe() == fav.playerkey:
                            favoritos.append(player)

                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "id": key,
                    "favoritos": favoritos,
                    "favorito": "Jugador agregado a favoritos",
                }
                template = JINJA_ENVIRONMENT.get_template("showFavs.html")
                self.response.write(template.render(template_values));
            else:
                players = Player.query()
                favs = PlayerFav.query(PlayerFav.list == user_name)

                favoritos = []

                for player in players:
                    for fav in favs:
                        if player.key.urlsafe() == fav.playerkey:
                            favoritos.append(player)

                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "id": key,
                    "favoritos": favoritos,
                    "favorito": "El jugador ya esta en favoritos",
                }
                template = JINJA_ENVIRONMENT.get_template("showFavs.html")
                self.response.write(template.render(template_values));
        else:
            self.redirect("/")


    def post(self):

        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            key = self.request.get("id").strip()

            contador = PlayerFav.query(ndb.AND(PlayerFav.playerkey == key, PlayerFav.list == user_name)).count()

            if contador == 0:
                players = Player.query(Player.usuario == user_name).order(Player.apellidos)
                favs = PlayerFav(playerkey=key, list=user_name)


                players = Player.query()
                favs = PlayerFav.query(PlayerFav.list == user_name)

                favoritos = []

                for player in players:
                    for fav in favs:
                        if player.key.urlsafe() == fav.playerkey:
                            favoritos.append(player)


                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "id": key,
                    "favoritos": favoritos,
                }
                template = JINJA_ENVIRONMENT.get_template("showFavs.html")
                self.response.write(template.render(template_values));
            else:
                template_values = {
                    "user_name": user_name,
                    "access_link": access_link,
                    "id": key,
                    "favorito": "El jugador ya esta en favoritos",
                }
                template = JINJA_ENVIRONMENT.get_template("showFavs.html")
                self.response.write(template.render(template_values));
        else:
            self.redirect("/")