from google.appengine.api import users
from players import Player
import os
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ["jinja2.ext.autoescape"],
    autoescape = True)


class PlayerShowallHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            players = Player.query(Player.usuario == user_name).order(Player.apellidos)

            template_values = {
                 "user_name": user_name,
                 "access_link": access_link,
                 "players": players,

            }
            template = JINJA_ENVIRONMENT.get_template("playerShowall.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")


