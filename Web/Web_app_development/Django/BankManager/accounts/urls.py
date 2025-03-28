from django.urls import path
from . import views
from .views import HomePageView, CreatePostView
urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/', CreatePostView.as_view(), name='add_post'),
    path('', HomePageView.as_view(), name='home')
]
