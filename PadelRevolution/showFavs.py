#!/usr/bin/env python
from google.appengine.api import users
from google.appengine.ext import ndb

from players import Player
from favs import PlayerFav

import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)

class ShowFavsHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

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
                    "favoritos": favoritos,
            }

            template = JINJA_ENVIRONMENT.get_template("showFavs.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")