from google.appengine.ext import ndb

class MyGpu(ndb.Model):
        name = ndb.StringProperty()
        manufacturer = ndb.StringProperty()
        date_issued = ndb.DateProperty()
        geometryShader = ndb.BooleanProperty()
        tesselationShader = ndb.BooleanProperty()
        shaderInt16 = ndb.BooleanProperty()
        sparseBinding = ndb.BooleanProperty()
        textureCompressionETC2 = ndb.BooleanProperty()
        vertexPipelineStoresAndAtomic = ndb.BooleanProperty()
