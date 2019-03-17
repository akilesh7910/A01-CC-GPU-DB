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

class MainViewer(webapp2.RequestHandler):

    def get(self):
        self.response.headers["Content-Type"] = "text/html"

        gpu_array_query = MyGpu.query()
        if self.request.GET.get("search_func") == "Search":

            geometryShader = self.request.get("temp_geometryShader") == "on"
            tesselationShader = self.request.get("temp_tesselationShader") == "on"
            shaderInt16 = self.request.get("temp_shaderInt16") == "on"
            sparseBinding = self.request.get("temp_sparseBinding") == "on"
            textureCompressionETC2 = self.request.get("temp_textureCompressionETC2") == "on"
            vertexPipelineStoresAndAtomic = self.request.get("temp_vertexPipelineStoresAndAtomic") == "on"

            gpu_array_query = MyGpu.query(ndb.OR(MyGpu.geometryShader == geometryShader)).fetch()

        else:

            geometryShader = False
            tesselationShader = False
            shaderInt16 = False
            sparseBinding = False
            textureCompressionETC2 = False
            vertexPipelineStoresAndAtomic = False
            gpu_array_query = MyGpu.query().fetch()

        template_values = {

            'gpu_arr' :  gpu_array_query,
			'temp_geometryShader' : geometryShader,
			'temp_tesselationShader' : tesselationShader,
			'temp_shaderInt16' : shaderInt16,
			'temp_sparseBinding' : sparseBinding,
			'temp_textureCompressionETC2' : textureCompressionETC2,
			'temp_vertexPipelineStoresAndAtomic' : vertexPipelineStoresAndAtomic
		}

        template = JINJA_ENVIRONMENT.get_template("view_func.html")
        self.response.write(template.render(template_values))
