from django.conf.urls import url, include
from .views import location_post
urlpatterns = [
    url(r'location', location_post)
]
