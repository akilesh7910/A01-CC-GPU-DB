import webapp2
import jinja2
from google.appengine.ext import ndb
import os

from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Compare(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Contents-Type"] = "text/html"

        selected_processor_name = self.request.GET.get("selected_processor")
        current_processor_name = self.request.GET.get("current_processor")

        if selected_processor_name != None and current_processor_name !=None:

            selected_processor_key = ndb.Key("MyGpu", selected_processor_name)
            selected_processor = selected_processor_key.get()

            current_processor_key = ndb.Key("MyGpu", current_processor_name)
            current_processor = current_processor_key.get()

            gpu_array_query = MyGpu.query(ndb.OR(MyGpu.name == selected_processor_name,
                                     MyGpu.name == current_processor_name)).fetch()

        else:
               
            gpu_array_query = MyGpu.query().fetch()

        template_values= {
            "gpu_arr": gpu_array_query
        }

        if self.request.get("cancel"):
            self.redirect("/")

        template = JINJA_ENVIRONMENT.get_template("compare_func.html")
        self.response.write(template.render(template_values))
