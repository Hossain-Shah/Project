from django.conf.urls import include, url
from bot.views import BotView
urlpatterns = [
                  url(r'^tutorial01/?$', BotView.as_view())
               ]