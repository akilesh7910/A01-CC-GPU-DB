import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from mygpu import MyGpu
from compare_func import Compare
from add_func import Edit


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'
        geometryShader = False
        tesselationShader = False
        shaderInt16 = False
        sparseBinding = False
        textureCompressionETC2 = False
        vertexPipelineStoresAndAtomic = False


        user = users.get_current_user()

        if user:
            url = users.create_logout_url(self.request.uri)
            myuser_key = ndb.Key("MyUser", user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                myuser = MyUser(id=user.user_id())
                myuser.put()


            if self.request.GET.get("search_func") == "Search":

                geometryShader = self.request.get("temp_geometryShader") == "on"
                tesselationShader = self.request.get("temp_tesselationShader") == "on"
                shaderInt16 = self.request.get("temp_shaderInt16") == "on"
                sparseBinding = self.request.get("temp_sparseBinding") == "on"
                textureCompressionETC2 = self.request.get("temp_textureCompressionETC2") == "on"
                vertexPipelineStoresAndAtomic = self.request.get("temp_vertexPipelineStoresAndAtomic") == "on"
                gpu_array = MyGpu.query()


                if geometryShader:
                    gpu_array = gpu_array.filter(MyGpu.geometryShader == True)

                if tesselationShader:
                    gpu_array = gpu_array.filter(MyGpu.tesselationShader == True)

                if shaderInt16:
                    gpu_array = gpu_array.filter(MyGpu.shaderInt16 == True)

                if sparseBinding:
                    gpu_array = gpu_array.filter(MyGpu.sparseBinding == True)

                if textureCompressionETC2:
                    gpu_array = gpu_array.filter(MyGpu.textureCompressionETC2 == True)

                if vertexPipelineStoresAndAtomic:
                    gpu_array = gpu_array.filter(MyGpu.vertexPipelineStoresAndAtomic == True)

                gpu_array_query = gpu_array.fetch()

            else:
                gpu_array_query = MyGpu.query().fetch()

        else:
            url = users.create_login_url(self.request.uri)
            gpu_array_query = None



        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
			'gpu_arr' :  gpu_array_query,
			'temp_geometryShader' : geometryShader,
			'temp_tesselationShader' : tesselationShader,
			'temp_shaderInt16' : shaderInt16,
			'temp_sparseBinding' : sparseBinding,
			'temp_textureCompressionETC2' : textureCompressionETC2,
			'temp_vertexPipelineStoresAndAtomic' : vertexPipelineStoresAndAtomic
		}

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ("/add_func",Edit),
    ("/compare_func",Compare)
], debug=True)
