from rest_framework.routers import SimpleRouter
from . import views

# Register all API Viewsets:
api = SimpleRouter()
api.register(r'elections', views.ElectionDay)
urlpatterns = api.urls
