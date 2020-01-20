from django.urls import path
from .views import HomePageView, CreatePostView, HomePage2View, HomePage3View, HomePage4View, HomePage1View, HomePage5View, CreatePost1View

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('doctors/', CreatePostView.as_view(), name='add_post'),
    path('doctors/', CreatePost1View.as_view(), name='add_post'),
    path('services.html/', HomePage2View.as_view(), name='add_post'),
    path('news.html/', HomePage3View.as_view(), name='add_post'),
    path('contact.html/', HomePage4View.as_view(), name='add_post'),
    path('doctors/doctors_diagnosis.html/', HomePage1View.as_view(), name='doctors_diagnosis'),
    path('doctors/doctors_todolist.html/', HomePage5View.as_view(), name='doctors_todolist'),
    path('doctors/todolist.html/', CreatePost1View.as_view(), name='todolist.html')
]

