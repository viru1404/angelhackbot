from django.conf.urls import include, url
from .views import bot
urlpatterns = [
                  url(r'^/?$', bot.as_view()) 
               ]