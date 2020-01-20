from django.urls import path

from .views import HomePageView, CreatePostView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('Instagram/', CreatePostView.as_view(), name='add_post'),
]