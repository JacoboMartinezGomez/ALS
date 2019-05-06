#!/usr/bin/python
from google.appengine.api import users
import webapp2
import jinja2
import os

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)


class MainPageHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user != None:
            user_name = user.nickname()
            access_link = users.create_logout_url("/")

            template_values = {
                "user_name": user_name,
                "access_link": access_link,
                }

            template = JINJA_ENVIRONMENT.get_template("mainPage.html")
            self.response.write(template.render(template_values));
        else:
            self.redirect("/")