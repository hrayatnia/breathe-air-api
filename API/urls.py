from django.conf.urls import url, include
from .views import location_post, get_all_data
urlpatterns = [
    url(r'location', location_post),
    url(r'world', get_all_data)
]
