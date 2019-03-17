import webapp2
import jinja2
from google.appengine.ext import ndb
import os

from datetime import datetime
from mygpu import MyGpu

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Edit(webapp2.RedirectHandler):

    def get(self):

        self.response.headers["Content-Type"] = "text/html"
        button_action = "Add Function"

        selected_name = self.request.GET.get("gpu_name")

        if selected_name == None:
            selected_name = ""
            selected_gpu = MyGpu(name="",
                                 manufacturer="",
                                 date_issued=None,
                                 geometryShader=False,
                                 tesselationShader=False,
                                 shaderInt16=False,
                                 sparseBinding=False,
                                 textureCompressionETC2=False,
                                 vertexPipelineStoresAndAtomic=False)

        else:
            button_action = "Update Function"
            selected_gpu_key = ndb.Key("MyGpu",selected_name)
            selected_gpu = selected_gpu_key.get()

        template_values = {
            "selected_gpu" : selected_gpu,
            "button_action" : button_action,
            "gpu_name" : selected_name
        }

        template = JINJA_ENVIRONMENT.get_template("add_func.html")
        self.response.write(template.render(template_values))

    def post(self):

        self.response.headers["Contents-Type"] = "text/html"

        if self.request.get("add_function") == "Add Function":

            name = self.request.get("name")

            if self.request.get("date_issued") == "" or name == "":
                self.redirect("/add_func")
                return

            gpu_array_query = MyGpu.query(MyGpu.name == name).fetch()

            if len(gpu_array_query) > 0:

                self.redirect("/add_func")
                return

            manufacturer = self.request.get("manufacturer")
            date_issued = datetime.strptime(self.request.get("date_issued"), "%Y-%m-%d")
            geometryShader = self.request.get("temp_geometryShader") == "on"
            tesselationShader = self.request.get("temp_tesselationShader") == "on"
            shaderInt16 = self.request.get("temp_shaderInt16") == "on"
            sparseBinding = self.request.get("temp_sparseBinding") == "on"
            textureCompressionETC2 = self.request.get("temp_textureCompressionETC2") == "on"
            vertexPipelineStoresAndAtomic = self.request.get("temp_vertexPipelineStoresAndAtomic") == "on"

            new_processor =  MyGpu(id = name,
                                   name=name,
                                   manufacturer=manufacturer,
                                   date_issued=date_issued,
                                   geometryShader=geometryShader,
                                   tesselationShader=tesselationShader,
                                   shaderInt16=shaderInt16,
                                   sparseBinding=sparseBinding,
                                   textureCompressionETC2=textureCompressionETC2,
                                   vertexPipelineStoresAndAtomic=vertexPipelineStoresAndAtomic)

            new_processor.put()
            self.redirect("/")

        elif self.request.get("add_function") == "Update Function":

            selected_name = self.request.get("gpu_name")
            selected_gpu_key = ndb.Key("MyGpu", selected_name)
            selected_gpu = selected_gpu_key.get()

            name = self.request.get("name")
            manufacturer = self.request.get("manufacturer")
            date_issued = datetime.strptime(self.request.get("date_issued"), "%Y-%m-%d")
            geometryShader = self.request.get("temp_geometryShader") == "on"
            tesselationShader = self.request.get("temp_tesselationShader") == "on"
            shaderInt16 = self.request.get("temp_shaderInt16") == "on"
            sparseBinding = self.request.get("temp_sparseBinding") == "on"
            textureCompressionETC2 = self.request.get("temp_textureCompressionETC2") == "on"
            vertexPipelineStoresAndAtomic = self.request.get("temp_vertexPipelineStoresAndAtomic") == "on"

            selected_gpu.name = name
            selected_gpu.manufacturer = manufacturer
            selected_gpu.date_issued = date_issued
            selected_gpu.geometryShader = geometryShader
            selected_gpu.tesselationShader = tesselationShader
            selected_gpu.shaderInt16 = shaderInt16
            selected_gpu.sparseBinding = sparseBinding
            selected_gpu.textureCompressionETC2 = textureCompressionETC2
            selected_gpu.vertexPipelineStoresAndAtomic = vertexPipelineStoresAndAtomic

            selected_gpu.put()
            self.redirect("/")

        if self.request.get("cancel"):

            self.redirect("/")
