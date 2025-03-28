from .views import bview
from django.conf.urls import url
urlpatterns = [
                url(r'^a_secret_web_hook/?$', bview)
            ]