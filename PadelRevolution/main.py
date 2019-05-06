#!/usr/bin/env python


from google.appengine.api import users
import webapp2
import os
import jinja2

from mainPage import MainPageHandler
from playerAdd import PlayerAddHandler
from playerShowall import PlayerShowallHandler
from playerEdit import PlayerEditHandler
from playerDelete import PlayerDeleteHandler
from addFavs import AddFavsHandler
from showFavs import ShowFavsHandler
from playerDeleteFav import PlayerDeleteFavHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainHandler(webapp2.RequestHandler):
    def get(self):
        user_name = "Inicia sesion"
        user = users.get_current_user()
        if user != None:
            self.redirect("/main")
            return
        else:
            access_link = users.create_login_url("/main")

        template_values = {
            "user_name": user_name,
            "access_link": access_link,
        }

        template = JINJA_ENVIRONMENT.get_template("index.html")
        self.response.write(template.render(template_values));


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ("/main", MainPageHandler),
    ("/playerAdd", PlayerAddHandler),
    ("/playerShowall",PlayerShowallHandler),
    ("/playerEdit",PlayerEditHandler),
    ("/playerDelete",PlayerDeleteHandler),
    ("/addFavs",AddFavsHandler),
    ("/showFavs",ShowFavsHandler),
    ("/playerDeleteFav",PlayerDeleteFavHandler),

], debug=True)