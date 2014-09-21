
import webapp2
import jinja2
import urllib2
import os.path
import json

from urllib2 import Request, urlopen
from google.appengine.ext.webapp import template
from google.appengine.ext import ndb
from jinja2 import Template



class Main(ndb.Model):
  age = ndb.StringProperty()
  sex = ndb.StringProperty()
  part = ndb.StringProperty()
  sympt = ndb.StringProperty()
  docter = ndb.StringProperty()





headers = {
  'X-API-KEY': 'RIXjc9pnVHFNfwL/KJzohowzr10=',
  'X-CLIENT-ID': '90797d50-03ea-4825-8441-e561b74606fe'
}

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    autoescape=True,
    extensions=['jinja2.ext.autoescape'])


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render())

    def post(self):
        prt = self.request.get('part')
        smpt = self.request.get('sympt')
        special = Main.query(Main.part==prt, Main.sympt==smpt).get()

        url = 'https://api.practo.com/search/?city=bangalore&locality=whitefield&speciality={0}&filters=filters[qualification]'.format(special.docter)

        request = Request(url, headers=headers)
        response_body = urlopen(request).read()
        url = json.loads(response_body)
        params = {
            'v' : url
        }

        template = JINJA_ENVIRONMENT.get_template('result.html')
        self.response.write(template.render(params))



class DocterProfileHandler(webapp2.RequestHandler):
    def get(self):
        self.render_template('form.html')

    def post(self):
        part = self.request.get('part')
        sympt = self.request.get('sympt')
        doct = self.request.get('doct')

        data = Main(age="18-20",
                    sex="male",
                    part=part,
                    sympt=sympt,
                    docter=doct)
        data.put()
        self.render_template('form.html')

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
        self.response.out.write(template.render(path, params))


class ConfermHandler(webapp2.RequestHandler):
    def post(self,**kwargs):
        name = kwargs['name']
        params = {
            'v' : name
        }

        template = JINJA_ENVIRONMENT.get_template('endpage.html')
        self.response.write(template.render(params))




app = webapp2.WSGIApplication([
    webapp2.Route('/', handler=MainHandler),
    webapp2.Route('/profile', handler=DocterProfileHandler),
    webapp2.Route('/conferm/<name:.*>', handler=ConfermHandler)
], debug=True)
